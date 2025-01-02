from pgmpy.factors.discrete import DiscreteFactor
import numpy as np
from LoadBayesianNetwork import load_bayesian_network
from LoadBayesianNetwork import print_network_structure
from Absorption import message_passing

def print_junction_tree_structure(junction_tree):
    print("Nodi del Junction Tree (cliques):", junction_tree.nodes())
    print("Archi del Junction Tree:", junction_tree.edges())


def printallpotentials():
    for clique in jt.nodes:
        print(f"\nPotenziale del clique {clique}:")
        print(jt.get_factors(clique))


def printallcpds():
    for cpd in bayesian_network.get_cpds():
        print(f"CPD for {cpd.variable}:")
        print(cpd)
        print("\n")

def create_separator(junction_tree, bayesian_network):
    separator_factors = {}

    # Itera su tutti gli archi del junction tree
    for edge in junction_tree.edges:
        clique1, clique2 = edge

        # Trova l'unione delle variabili delle due cricche (questa sarà la chiave)
        union = tuple(sorted(set(clique1).union(set(clique2))))  # Usa un tupla ordinata come chiave

        # Trova l'intersezione tra le variabili delle due cricche (questo è il separatore)
        separator = list(set(clique1).intersection(set(clique2)))

        # Se il separatore non ha variabili, continua
        if not separator:
            continue

        # Determina le cardinalità e gli state names delle variabili del separatore
        cardinalities_separator = [bayesian_network.get_cardinality(var) for var in separator]
        state_names_separator = {
            var: bayesian_network.get_cpds(var).state_names[var] for var in separator
        }

        # Inizializza il separatore con valori uniformi
        values_separator = [1] * int(np.prod(cardinalities_separator))  # Tutti i valori inizialmente 1

        # Crea il fattore del separatore
        separator_factor = DiscreteFactor(
            variables=separator,
            cardinality=cardinalities_separator,
            values=values_separator,
            state_names=state_names_separator
        )

        # Associa il separatore all'unione delle variabili
        separator_factors[union] = separator_factor

    return separator_factors
def printAllseparator(separators):
    for edge, table in separator_tables.items():
        print(f"Separator for edge {edge}:\n{table}\n")
def get_leaves(junction_tree, root):
    visited = set()

    def dfs(node, parent=None):
        visited.add(node)
        neighbors = [neighbor for neighbor in junction_tree.neighbors(node) if neighbor != parent]

        if len(neighbors) == 0:
            return node

        leaves =[]
        for neighbor in neighbors:
            if neighbor not in visited:
                leaves.append(dfs(neighbor, node))

        return leaves

    return dfs(root)
if __name__ == "__main__":
    bif_file = "Data/cancer.bif"
    bayesian_network = load_bayesian_network(bif_file)
    print_network_structure(bayesian_network)

    jt=bayesian_network.to_junction_tree()
    print("Junction Tree costruito con successo!")
    print_junction_tree_structure(jt)

    #apply_evidence(jt.get_factors(('Cancer', 'Xray')),{'Cancer':'True'})
    separator_tables = create_separator(jt, bayesian_network)
    print('Starting JTA\n')
    evidences={'Cancer':'False'}
    root=list(jt.nodes)[0]
    print(root)
    leaves=get_leaves(jt,root)
    print(leaves)
    message_passing(jt,root,evidences,separator_tables,leaves)
    #for edge, table in separator_tables.items():
     #   print(f"Separator for edge {edge}:\n{table}\n")

    #print("Available edges in separator_tables:", list(separator_tables.keys()))
    #absorption(jt, ('Cancer', 'Smoker', 'Pollution'),('Cancer', 'Xray'),separator_tables[(('Cancer', 'Smoker', 'Pollution'), ('Cancer', 'Xray'))])
    printallpotentials()
    printAllseparator(separator_tables)


