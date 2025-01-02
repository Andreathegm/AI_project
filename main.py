import CustomJunctionTree
from Build_Junction_tree import print_junction_tree_structure, get_leaves
from LoadBayesianNetwork import load_bayesian_network
from LoadBayesianNetwork import print_network_structure
from Absorption import message_passing
if __name__ == "__main__":
    bif_file = "Data/cancer.bif"
    bayesian_network = load_bayesian_network(bif_file)
    print_network_structure(bayesian_network)

    junction_tree = bayesian_network.to_junction_tree()
    jt = CustomJunctionTree(junction_tree,bayesian_network)
    print("Junction Tree costruito con successo!")
    #print_junction_tree_structure(jt)


    print('Starting JTA\n')
    evidences = {'Cancer': 'False'}
    root = list(jt.nodes)[0]
    print(root)
    leaves=get_leaves(jt, root)
    print(leaves)
    message_passing(jt, root, evidences,separator_tables,leaves)