from pgmpy.readwrite import BIFReader
from pgmpy.models import JunctionTree

def load_bayesian_network(file_path):
    reader = BIFReader(file_path)
    bayesian_network = reader.get_model()
    return bayesian_network

def print_network_structure(network):
    print("Nodi:", network.nodes())
    print("Archi:", network.edges())

if __name__ == "__main__":

    bif_file = "Data/cancer.bif"
    bayesian_network = load_bayesian_network(bif_file)
    print("Rete Bayesiana caricata con successo!")
    print_network_structure(bayesian_network)
