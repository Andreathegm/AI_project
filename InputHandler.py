def select_variable(nodes):
    print(nodes)
    print(f"Choose a variable to apply  evidences on from the following list:")
    for i, node in enumerate(nodes):
        print(f"{i + 1}. {node}")

    while True:
        try:
            selected = int(input("Enter the number of the variable: "))
            if 1 <= selected <= len(nodes):
                return nodes[selected - 1]
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def select_state_of_a_variable(bayesian_network, node):
    print(f"Choose a state of the variable {node} to apply evidence on from the following list:")
    states = bayesian_network.get_cpds(node).state_names[node]
    for i, state in enumerate(states):
        print(f"{i + 1}. {state}")

    while True:
        try:
            selected = int(input("Enter the number of the state: "))
            if 1 <= selected <= len(states):
                return states[selected - 1]
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def select_subset_of_universe(nodes_already_choosen, nodes):
    print(f"Choose a subset of the universe  from the following list:")
    for i, node in enumerate(nodes):
        if node not in nodes_already_choosen:
            print(f"{i + 1}. {node}")

    while True:
        try:
            selected = int(input("Enter the number of the variable: "))
            if 1 <= selected <= len(nodes):
                return nodes[selected - 1]
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def request_conditional_probability(bayesian_network):
    print("Select a variable or a cluster of variables to apply evidence on:")
    nodes = list(bayesian_network.nodes())
    evidences = {}
    while True:
        variable = select_variable(nodes)
        nodes.remove(variable)
        state = select_state_of_a_variable(bayesian_network, variable)
        evidences[variable] = state
        print("Do you want to select another variable? (y/n)")
        if input() == 'n':
            break
    return evidences

