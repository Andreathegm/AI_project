import os
os.environ["NUMEXPR_MAX_THREADS"] = "16"
import General_Util
import Bayesian_Network_Util
import JTA
from CustomJunctionTree import CustomJunctionTree
from JTA import message_passing
import InputHandler
import CondtionalQuery

if __name__ == "__main__":

    # 1 Load Bayesian Network from file chosen by user
    files = ["Data/cancer.bif", "Data/asia.bif", "Data/urn.bif"]
    bif_file = InputHandler.choose_file(files)
    bayesian_network = Bayesian_Network_Util.load_bayesian_network(bif_file)

    # 2 Manage user input
    provide_evidence = InputHandler.provide_evidence()
    evidences = {}
    Q = {}

    # 2.1 load variables from input
    (evidences, Q, formattedQ, formattedEvidences, formattedQ_brute_force,
     formattedEvidences_brute_force, stringU) = InputHandler.load_variables_from_input(provide_evidence,
                                                                                       bayesian_network, Q, evidences)
    # 3 Bayesian network smoothing
    Bayesian_Network_Util.print_all_cpds(bayesian_network)
    Bayesian_Network_Util.apply_smoothing_to_bn(bayesian_network)
    Bayesian_Network_Util.print_all_cpds(bayesian_network)

    # 3.1 Calculate conditional probability using brute force
    CondtionalQuery.calculate_and_print_brute_force_result(bayesian_network, Q, evidences, provide_evidence,
                                                            formattedQ_brute_force,formattedEvidences_brute_force, stringU)

    # 4 junction tree building
    junction_tree = Bayesian_Network_Util.transform_to_junction_tree(bayesian_network)
    jt = CustomJunctionTree(junction_tree, bayesian_network)

    # print information about junction tree
    jt.print_junction_tree_structure()
    jt.print_all_potentials()

    # 4.1  apply evidence to all potentials (including the separators) and print them(to see the effect of the evidence)
    General_Util.apply_evidence_to_all_potentials(jt, evidences)
    jt.print_all_potentials()

    # 4.2  JTA
    print('Starting JTA...\n')
    root, keysQ, evidences_key = list(jt.nodes)[0], tuple(Q.keys()), tuple(evidences.keys())
    # returns all the necessary cliques to calculate the conditional probability
    cliques_containingQ = message_passing(keysQ, jt, root)
    print("JTA finished\n")

    # normalize all potentials to get actual distributions
    jt.normalize_all_potentials()

    # 4.3 calculate the conditional probability
    JTA.print_result_for_jta(provide_evidence, cliques_containingQ, Q, keysQ, evidences_key, jt, formattedQ_brute_force,
                             formattedQ, formattedEvidences)


