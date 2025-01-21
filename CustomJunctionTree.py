import numpy as np
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.models import JunctionTree


class CustomJunctionTree(JunctionTree):

    def __init__(self, junction_tree, bayesian_network):
        super().__init__()
        self.__dict__.update(junction_tree.__dict__)
        self.potentials = {}
        self.assign_potentials()

        # a dict that contains discreteFactors for each separator
        self.separators = self.create_separators(bayesian_network)

    def add_potential(self, clique, potential):
        self.potentials[clique] = potential

    def assign_potentials(self):
        for node in self.nodes():
            potential = self.get_factors(node)
            self.add_potential(node, potential)

    def get_potential(self, clique):
        return self.potentials.get(clique, None)

    # these two functions are used to apply evidence(list of variable,realization correlated to this clique)
    # to the potentials and to the separators, evidences must be a list
    def apply_evidence_to_potentials(self, clique, evidence):
        if clique in self.potentials:
            print(self.potentials[clique].state_names)
            self.potentials[clique].reduce(evidence, inplace=True)

    def apply_evidence_to_separator(self, evidence, edge):
        self.separators[edge].reduce(evidence, inplace=True)

    def create_separators(self, bayesian_network):
        separator_potentials = {}

        for edge in self.edges:
            clique1, clique2 = edge
            union = tuple(sorted(set(clique1).union(set(clique2))))
            separator = list(set(clique1).intersection(set(clique2)))
            if not separator:
                continue
            cardinalities_separator = [bayesian_network.get_cardinality(var) for var in separator]
            state_names_separator = {
                var: bayesian_network.get_cpds(var).state_names[var] for var in separator
            }
            values_separator = [1] * int(np.prod(cardinalities_separator))
            separator_factor = DiscreteFactor(
                variables=separator,
                cardinality=cardinalities_separator,
                values=values_separator,
                state_names=state_names_separator
            )

            separator_potentials[union] = separator_factor

        return separator_potentials

    def normalize_all_potentials(self):
        for potential in self.potentials:
            self.potentials[potential].normalize(inplace=True)
        for potential in self.separators:
            self.separators[potential].normalize(inplace=True)

    # several print methods
    def print_all_vars_and_state_names(self):
        for potential in self.potentials:
            print(f"Potential for clique {potential} :\n {self.potentials[potential].variables}")
            print(f"Potential for clique {potential} :\n {self.potentials[potential].state_names}")

    def print_all_states_to_no(self):
        for potential in self.potentials:
            print(f"mapping for  {potential} is :\n {self.potentials[potential].name_to_no}")

    def print_all_potentials(self, _str=None):
        print("printing all nodes' potentials \n")
        for potential in self.potentials:
            if not _str:
                print(f"Potential for clique {potential} :\n {self.potentials[potential]}\n")
            else:
                print(f"{_str} for clique {potential} :\n {self.potentials[potential]._str(phi_or_p=_str)}")
        print("printing all separator potentials")
        for potential in self.separators:
            if not _str:
                print(f"Potential for separator identified with {potential} :\n {self.separators[potential]}")
            else:
                print(f"{_str} for separator identified with {potential} :\n {self.separators[potential]._str(phi_or_p=_str)}")

    def print_all_probability(self):
        self.print_all_potentials('probability')
