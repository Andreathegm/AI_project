from pgmpy.readwrite import BIFReader
import numpy as np
import General_Util


def load_bayesian_network(file_path):
    print("Loading Bayesian Network...")
    reader = BIFReader(file_path)
    bayesian_network = reader.get_model()
    print("Bayesian Network loaded successfully!\n")
    return bayesian_network


def transform_to_junction_tree(bayesian_network):
    print("Transforming Bayesian Network to Junction Tree...")
    jt = bayesian_network.to_junction_tree()
    print("Junction Tree built successfully!\n")
    print("Updating junction tree state names...")
    General_Util.update_junction_tree_state_names(bayesian_network, jt)
    print("Updated junction tree state names\n")
    return jt


def print_network_structure(network):
    print("Nodes:", network.nodes())
    print("Edges:", network.edges())


def print_all_cpds(bayesian_network):
    print("----PRINTING CPDS FOR ALL VARIABLES IN THE BAYESIAN NETWORK----\n")
    for cpd in bayesian_network.get_cpds():
        print(f"CPD for {cpd.variable}:\n{cpd}\n")
    print("\n")


def apply_smoothing(cpd, epsilon=1e-6):
    values = np.array(cpd.values)

    values = values + epsilon

    values /= values.sum(axis=0)

    cpd.values = values


def apply_smoothing_to_bn(bayesian_network, epsilon=1e-6):
    print("Applying smoothing to Bayesian Network...")
    for cpd in bayesian_network.get_cpds():
        apply_smoothing(cpd, epsilon)
    print("Smoothing applied successfully!\n\n")
