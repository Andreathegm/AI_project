from pgmpy.factors.discrete import DiscreteFactor
import numpy as np


class CustomJunctionTree:

    def __init__(self, junction_tree, bayesian_network):
        self.junction_tree = junction_tree
        self.potentials = {}
        self.assign_potentials()
        self.separators = self.create_separator(bayesian_network)

    def add_potential(self, clique, potential):
        self.potentials[clique] = potential

    def assign_potentials(self):
        for potential in self.junction_tree.get_factors():
            self.add_potential(tuple(potential.variables), potential)

    def get_factors(self, clique):

        return self.potentials.get(clique, None)

    def apply_evidence(self, clique, evidence):
        if clique in self.potentials:
            factor = self.potentials[clique]
            reduced_factor = factor.reduce(evidence, inplace=False)
            self.potentials[clique] = reduced_factor

    def create_separator(self, bayesian_network):
        separator_factors = {}

        for edge in self.junction_tree.edges:
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

            separator_factors[union] = separator_factor

        return separator_factors
