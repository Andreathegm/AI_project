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

    # 1 Choose file to load
    loaded_models = {}
    files = ["Data/cancer.bif", "Data/asia.bif", "Data/urn.bif"]

    while True:

        bif_file = InputHandler.choose_file(files)

        while True:

            if bif_file in loaded_models:
                print(f"Using already existing Model from '{bif_file}'")
                bayesian_network = loaded_models[bif_file][0].copy()
                junction_tree = loaded_models[bif_file][1].copy()
            else:
                # 2 Load Bayesian network
                bayesian_network = Bayesian_Network_Util.load_bayesian_network(bif_file)

                # 2.1  Bayesian network smoothing (print before and after to see the effect)
                Bayesian_Network_Util.print_all_cpds(bayesian_network)
                Bayesian_Network_Util.apply_smoothing_to_bn(bayesian_network)
                Bayesian_Network_Util.print_all_cpds(bayesian_network)

                # 2.2 Transform Bayesian network to junction tree
                junction_tree = Bayesian_Network_Util.transform_to_junction_tree(bayesian_network)

                # 2.3  Save the loaded models with copies to ensure immutability
                loaded_models[bif_file] = (bayesian_network.copy(), junction_tree.copy())

            # 3 Manage user input
            provide_evidence = InputHandler.provide_evidence()
            evidences = {}
            Q = {}

            # 3.1 load variables from input
            (evidences, Q, formattedQ, formattedEvidences, formattedQ_brute_force,
             formattedEvidences_brute_force, stringU) = InputHandler.load_variables_from_input(provide_evidence,
                                                                                               bayesian_network, Q, evidences)

            # 3.1 Calculate conditional probability using brute force
            CondtionalQuery.calculate_and_print_brute_force_result(bayesian_network, Q, evidences, provide_evidence,
                                                                    formattedQ_brute_force,formattedEvidences_brute_force, stringU)

            # 4 custom junction tree building
            jt = CustomJunctionTree(junction_tree, bayesian_network)

            # print information about junction tree
            jt.print_junction_tree_structure()
            jt.print_all_potentials()

            # 4.1  apply evidence to all potentials (including the separators) and print them
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

            # 5 Possible new request:
            choice = InputHandler.process_new_request()
            if choice == 0:
                exit()
            elif choice == 1:
                continue
            elif choice == 2:
                break




