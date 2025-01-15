import General_Util
import Network_Util
from CustomJunctionTree import CustomJunctionTree
from JTA import message_passing

if __name__ == "__main__":
    bif_file = "Data/cancer.bif"
    bayesian_network = Network_Util.load_bayesian_network(bif_file)

    print("Building Custom Junction Tree")
    junction_tree = Network_Util.transform_to_junction_tree(bayesian_network)
    jt = CustomJunctionTree(junction_tree, bayesian_network)
    print("Custom Junction Tree built successfully!")
    General_Util.print_junction_tree_structure(jt)

    print('Starting JTA\n')
    evidences = {'Cancer': 'True'}
    root = list(jt.nodes)[0]
    print(f"the root is:{root}")
    leaves = General_Util.get_leaves(jt, root)
    print(f"leaves are:{leaves}")
    message_passing(jt, root, evidences, leaves)
    jt.print_all_potentials()
