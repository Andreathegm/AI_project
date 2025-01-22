def select_variable(nodes, string):
    print("----ALL AVAILABLE VARIABLES IN THE MODEL----\n")
    print(f"----> {','.join(map(str, nodes))}\n")
    print(string)
    for i, node in enumerate(nodes):
        print(f"{i + 1}. {node}")
    return validating_input(nodes, "Enter the number of the variable: ")


def select_state_of_a_variable(bayesian_network, node):
    print(f"\nChoose a state of the variable {node} to apply evidence on from the following list:")
    states = bayesian_network.get_cpds(node).state_names[node]
    for i, state in enumerate(states):
        print(f"{i + 1}. {state}")
    return validating_input(states, "Enter the number of the state: ")


def request_conditional_probability(bayesian_network):
    stringEvidences = "Choose a variable to apply  evidences on from the following list:"
    stringQ = "Choose Q from the following list:"
    not_chosen_nodes = list(bayesian_network.nodes())
    evidences = {}
    Q = {}
    evidences = apply_evidence(bayesian_network, not_chosen_nodes, evidences,stringEvidences)
    Q = apply_evidence(bayesian_network, not_chosen_nodes, Q, stringQ)
    return evidences, Q


def validating_input(nodes, _string):
    while True:
        try:
            selected = int(input(_string))
            if 1 <= selected <= len(nodes):
                return nodes[selected - 1]
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def apply_evidence(bayesian_network, not_chosen_nodes, evidences, string):
    while True:
        variable = select_variable(not_chosen_nodes, string)
        not_chosen_nodes.remove(variable)
        state = select_state_of_a_variable(bayesian_network, variable)
        evidences[variable] = state
        print("\nDo you want to select another variable? (y/n)")
        if input() == 'n':
            break

    return evidences


def provide_evidence():
    while True:
        try:
            print("Do you want to provide evidence? (y/n)")
            _input = input()
            if _input == 'y':
                return True
            elif _input == 'n':
                return False
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def choose_file(files):
    print("Choose a file from the following list:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    file = validating_input(files, "Enter the number of the file: ")
    print(f"\nFile {file} has been chosen.\n")
    return file


def load_variables_from_input(provide_evidence, bayesian_network, Q, evidences):
    formattedQ = formattedEvidences = formattedQ_brute_force = formattedEvidences_brute_force = None
    stringU = None

    if provide_evidence:
        evidences, Q = request_conditional_probability(bayesian_network)
        print(f"\nEvidences: {evidences}, Q: {Q}\n\n")
        formattedQ = ', '.join(f"{key} = {value}" for key, value in Q.items())
        formattedEvidences = ', '.join(f"{key} = {value}" for key, value in evidences.items())
        formattedQ_brute_force = ', '.join(f"{key} " for key in Q)
        formattedEvidences_brute_force = ', '.join(f"{key} " for key in evidences)
    else:
        stringU = "P(U) : "

    return evidences, Q, formattedQ, formattedEvidences, formattedQ_brute_force, formattedEvidences_brute_force, stringU

