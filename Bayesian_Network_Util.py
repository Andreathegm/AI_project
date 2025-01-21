from pgmpy.readwrite import BIFReader


def load_bayesian_network(file_path):
    reader = BIFReader(file_path)
    bayesian_network = reader.get_model()
    return bayesian_network


def transform_to_junction_tree(bayesian_network):
    return bayesian_network.to_junction_tree()


def print_network_structure(network):
    print("Nodes:", network.nodes())
    print("Edges:", network.edges())
