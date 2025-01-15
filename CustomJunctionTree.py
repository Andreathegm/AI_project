import numpy as np
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.models import JunctionTree


class CustomJunctionTree(JunctionTree):

    def __init__(self, junction_tree, bayesian_network):
        super().__init__()
        self.__dict__.update(junction_tree.__dict__)
        self.potentials = {}
        self.assign_potentials()
        self.separators = self.create_separators(bayesian_network) # a dict that contains discreteFactors for each separator

    def add_potential(self, clique, potential):
        self.potentials[clique] = potential

    def assign_potentials(self):
        for node in self.nodes():
            potential = self.get_factors(node)
            self.add_potential(node, potential)

    def get_potential(self, clique):
        print("Collect a potential")
        return self.potentials.get(clique, None)

    def apply_evidence_to_potentials(self, clique, evidence):
        if clique in self.potentials:
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
##TODO cosa fa np.prod
            values_separator = [1] * int(np.prod(cardinalities_separator))
            separator_factor = DiscreteFactor(
                variables=separator,
                cardinality=cardinalities_separator,
                values=values_separator,
                state_names=state_names_separator
            )

            separator_potentials[union] = separator_factor

        return separator_potentials

    def print_all_potentials(self):
        print("printing all nodes' potentials ")
        for potential in self.potentials:
            print(self.potentials[potential])
        print("printing all separator potentials")
        for potential in self.separators:
            print(self.separators[potential])
