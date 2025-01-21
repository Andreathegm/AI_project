def select_variable(nodes, string):
    print(nodes)
    print(string)
    for i, node in enumerate(nodes):
        print(f"{i + 1}. {node}")
    return validating_input(nodes, "Enter the number of the variable: ")


def select_state_of_a_variable(bayesian_network, node):
    print(f"Choose a state of the variable {node} to apply evidence on from the following list:")
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
        print("Do you want to select another variable? (y/n)")
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
