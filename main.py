import General_Util
import Bayesian_Network_Util
from CustomJunctionTree import CustomJunctionTree
from JTA import message_passing
import InputHandler
import CondtionalQuery

if __name__ == "__main__":
    bif_file = "Data/asia.bif"
    bayesian_network = Bayesian_Network_Util.load_bayesian_network(bif_file)
    print("Bayesian Network loaded successfully!")
    provide_evidence = InputHandler.provide_evidence()

    evidences = {}
    Q = {}
    formattedQ = None
    formattedEvidences = None
    formattedQ_brute_force = None
    formattedEvidences_brute_force = None
    stringU = None

    if provide_evidence:
        evidences, Q = InputHandler.request_conditional_probability(bayesian_network)
        print(f"Evidences: {evidences} , Q: {Q}")
        formattedQ = ', '.join(f"{key} = {value}" for key, value in Q.items())
        formattedEvidences = ', '.join(f"{key} = {value}" for key, value in evidences.items())
        formattedQ_brute_force = ', '.join(f"{key} " for key in Q)
        formattedEvidences_brute_force = ', '.join(f"{key} " for key in evidences)

    else:
        stringU = "P(U) : "

    if provide_evidence:
        print(f"P({formattedQ_brute_force}|{formattedEvidences_brute_force})\n"
              f"{CondtionalQuery.conditional_probability_bruteforce(bayesian_network, Q, evidences)}")
    else:
        print(f"{stringU}\n{CondtionalQuery.conditional_probability_bruteforce(bayesian_network, Q, evidences)}")

    print("Building Junction Tree\n")
    junction_tree = Bayesian_Network_Util.transform_to_junction_tree(bayesian_network)
    print("\n\nUpdating junction tree state names")
    General_Util.update_junction_tree_state_names(bayesian_network, junction_tree)
    print("\n\nUpdated junction tree state names\n")
    for factor in junction_tree.get_factors():
        print(f"Potential variables: {factor.variables} \n Potential names: {factor.state_names}")

    General_Util.print_all_states_to_no(junction_tree)

    print("Building Custom Junction Tree")
    jt = CustomJunctionTree(junction_tree, bayesian_network)
    print("Custom Junction Tree built successfully!")

    # print information about junction tree
    General_Util.print_junction_tree_structure(jt)
    jt.print_all_potentials()
    jt.print_all_vars_and_state_names()

    # apply evidence to all potentials (including the separators)
    General_Util.apply_evidence_to_all_potentials(jt, evidences)
    jt.print_all_potentials()

    # start JTA
    print('Starting JTA...\n')
    root = list(jt.nodes)[0]
    print(f"the root is:{root}")
    keysQ = tuple(Q.keys())
    evideces_key = tuple(evidences.keys())

    # returns all the necessary cliques to calculate the conditional probability
    cliques_containingQ = message_passing(keysQ, jt, root)

    # normalize all potentials to get actual distributions
    jt.normalize_all_potentials()
    print("All potentials normalized\n\n")

    # print all necessary potentials to calculate the conditional probability
    print("Printing all potentials to calculate the conditional probability")
    if not isinstance(cliques_containingQ, list):
        print(cliques_containingQ)
        print(jt.potentials[cliques_containingQ])
    else:
        for clique in cliques_containingQ:
            print(clique)
            print(jt.potentials[clique])

    # calculate the conditional probability
    if provide_evidence:
        probability = CondtionalQuery.calculate_conditional_probability(cliques_containingQ, keysQ, evideces_key, jt)
        print(f" Distribution requested :  P({formattedQ_brute_force} | {formattedEvidences}) :\n{probability._str(phi_or_p='probabilty')}")
        probability.reduce(Q.items(), inplace=True)
        value = probability.values
        print(f" Probability of requested realization of Q  :  P({formattedQ} | {formattedEvidences}) : {value}")
    else:
        # print the distribution of the variable U across all network
        jt.print_all_probability()

