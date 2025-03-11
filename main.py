import Plot
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

    default_couple = {"Data/cancer.bif": [{"Q": {"Cancer": "True"}, "E": {"Xray": "positive"}},
                                          {"Q": {"Cancer": "False"}, "E": {"Pollution": "low"}},
                                          {"Q": {"Pollution": "high"}, "E": {"Cancer": "False"}},
                                          {"Q": {"Smoker": "False"}, "E": {"Dyspnoea": "True"}}
                                          ],
                      "Data/asia.bif": [{"Q": {"either": "Yes"}, "E": {"xray": "Yes", "dysp": "No"}},
                                        {"Q": {"lung": "Yes", "bronc": "Yes", "xray": "Yes"},
                                         "E": {"tub": "Yes", "asia": "No"}},
                                        {"Q": {"smoke": "No"}, "E": {"either": "No", "asia": "Yes"}},
                                        {"Q": {"asia": "Yes"}, "E": {"xray": "Yes", "dysp": "No", "tub": "Yes"}}
                                        ],
                      "Data/urn.bif": [{"Q": {"draw": "blue"}, "E": {"lie": "yes"}},
                                       {"Q": {"actual_action": "red", "group_action": "rb"}, "E": {"draw": "red"}},
                                       {"Q": {"lie": "no"}, "E": {"draw": "red", "actual_action": "blue"}},
                                       {"Q": {"personal_action": "blue"}, "E": {"lie": "yes"}}
                                       ]
                      }
    show_default_results = InputHandler.is_printing_result()

    if show_default_results:

        for file in files:

            iterations = 20
            brute_force_results = []
            jta_results = []
            formattedQs = []
            formattedEs = []

            for j in range(iterations):

                temp_brute_force_results = []
                temp_jta_results = []

                for i in range(len(default_couple[file])):

                    if file in loaded_models:
                        bayesian_network = loaded_models[file][0].copy()
                        junction_tree = loaded_models[file][1].copy()

                    else:

                        bayesian_network = Bayesian_Network_Util.load_bayesian_network(file)
                        Bayesian_Network_Util.apply_smoothing_to_bn(bayesian_network)
                        junction_tree = Bayesian_Network_Util.transform_to_junction_tree(bayesian_network)
                        loaded_models[file] = (bayesian_network.copy(), junction_tree.copy())

                    provide_evidence = True
                    evidences = default_couple[file][i]["E"]
                    Q = default_couple[file][i]["Q"]
                    (evidences, Q, formattedQ, formattedEvidences, formattedQ_brute_force,
                     formattedEvidences_brute_force, stringU) = InputHandler.load_variables_from_input(provide_evidence,
                                                                                                       bayesian_network,
                                                                                                       Q,
                                                                                                       evidences)
                    formattedQs.append(formattedQ)
                    formattedEs.append(formattedEvidences)

                    brute_force_value = CondtionalQuery.calculate_and_print_brute_force_result(bayesian_network, Q,
                                                                                               evidences,
                                                                                               provide_evidence,
                                                                                               formattedQ_brute_force,
                                                                                               formattedEvidences_brute_force,
                                                                                               stringU)
                    temp_brute_force_results.append(brute_force_value)
                    jt = CustomJunctionTree(junction_tree, bayesian_network)
                    jt.print_junction_tree_structure()
                    #jt.print_all_potentials()
                    General_Util.apply_evidence_to_all_potentials(jt, evidences)
                    #jt.print_all_potentials()

                    print('Starting JTA...\n')
                    root, keysQ, evidences_key = list(jt.nodes)[0], tuple(Q.keys()), tuple(evidences.keys())
                    cliques_containingQ = message_passing(keysQ, jt, root)
                    cliques_paths, separator_paths = General_Util.connect_cliques(jt, cliques_containingQ)
                    print(cliques_paths, separator_paths)

                    if cliques_paths and separator_paths:
                        cliques_containingQ = cliques_paths
                        print("found path between cliques")
                        print(f"path is : {cliques_paths}, separators path is : {separator_paths}")

                    print("JTA finished\n")
                    jt.normalize_all_potentials()

                    jta_value = JTA.print_result_for_jta(provide_evidence, cliques_containingQ, Q, keysQ, evidences_key,
                                                         jt,
                                                         formattedQ_brute_force,
                                                         formattedQ, formattedEvidences, separator_paths)
                    temp_jta_results.append(jta_value)

                if not brute_force_results:
                    brute_force_results = temp_brute_force_results
                    jta_results = temp_jta_results
                else:
                    brute_force_results = [x + y for x, y in zip(brute_force_results, temp_brute_force_results)]
                    jta_results = [x + y for x, y in zip(jta_results, temp_jta_results)]

            brute_force_results = [x / iterations for x in brute_force_results]
            jta_results = [x / iterations for x in jta_results]
            Plot.save_values_to_text(brute_force_results, jta_results, file, iterations, formattedQs, formattedEs)
            Plot.plot_differences(brute_force_results, jta_results, file, iterations)
    else:

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
                                                                                                   bayesian_network, Q,
                                                                                                   evidences)

                # 3.1 Calculate conditional probability using brute force
                CondtionalQuery.calculate_and_print_brute_force_result(bayesian_network, Q, evidences, provide_evidence,
                                                                       formattedQ_brute_force,
                                                                       formattedEvidences_brute_force, stringU)

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
                #check for a path between clique
                cliques_paths, separator_paths = General_Util.connect_cliques(jt, cliques_containingQ)
                print(cliques_paths, separator_paths)

                if cliques_paths and separator_paths:
                    cliques_containingQ = cliques_paths
                    print("found path between cliques")
                    print(f"path is : {cliques_paths}, separators path is : {separator_paths}")

                print("JTA finished\n")


                # normalize all potentials to get actual distributions
                jt.normalize_all_potentials()


                # 4.3 calculate the conditional probability
                JTA.print_result_for_jta(provide_evidence, cliques_containingQ, Q, keysQ, evidences_key, jt,
                                         formattedQ_brute_force,
                                         formattedQ, formattedEvidences,separator_paths)

                # 5 Possible new request:
                choice = InputHandler.process_new_request()
                if choice == 0:
                    exit()
                elif choice == 1:
                    continue
                elif choice == 2:
                    break
