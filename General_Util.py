def print_junction_tree_structure(junction_tree):
    print("Junction Tree nodes (cliques):", junction_tree.nodes())
    print("Junction Tree edges:", junction_tree.edges())


# print potentials for (normal) junction tree using the method get_factors()
def print_all_potentials(junction_tree):
    for clique in junction_tree.nodes:
        print(f"\n Potential for  {clique}:\n")
        print(junction_tree.get_factors(clique))


def print_all_cpds(bayesian_network):
    for cpd in bayesian_network.get_cpds():
        print(f"CPD for {cpd.variable}:")
        print(cpd)
        print("\n")


# function to check if a clique contains some/all variables in Q
def is_in_clique(multiple_cliques_involved, Q, clique, reducibleQ):
    # multiple_cliques_involved is a set of cliques that contains altogether the variables in Q
    i = 0
    for variable in Q:
        if variable in clique:
            i += 1
            if len(reducibleQ) > 0 and variable in reducibleQ:
                reducibleQ.discard(variable)

    if i == len(Q):
        return True
    else:
        if i > 0:
            multiple_cliques_involved.append(clique)


def apply_evidence_to_all_potentials(custom_junction_tree, evidences):
    for clique in custom_junction_tree.nodes:
        _dict = {}
        print(f"apply evidence on clique : {clique}")
        projecting_dict_on_clique(clique, _dict, evidences)
        print(_dict)
        print(_dict.items())
        custom_junction_tree.apply_evidence_to_potentials(clique, _dict.items())
        print(_dict)
        _dict.clear()
    for potential in custom_junction_tree.separators:
        _dict = {}
        projecting_dict_on_clique(custom_junction_tree.separators[potential].variables, _dict, evidences)
        custom_junction_tree.apply_evidence_to_separator(_dict.items(), potential)
        _dict.clear()


# function to project all the evidences on a specific clique
def projecting_dict_on_clique(clique, _dict, evidences):
    for variable in clique:
        if variable in evidences:
            evidence = evidences[variable]
            _dict[variable] = evidence


def create_assignment_dict(bayesian_network):
    cpds = bayesian_network.get_cpds()
    assignment_dict = {}
    for cpd in cpds:
        for variable in cpd.variables:
            if variable in assignment_dict:
                continue
            else:
                assignment_dict[variable] = cpd.state_names[variable]

    return assignment_dict


# Manage the state names of the potentials for an error found in the library when using method to_junction_tree()
def update_state_names(assignment_dict, potential):
    relevant_assignment = {var: states for var, states in assignment_dict.items() if var in potential.variables}
    print(relevant_assignment)
    for var, states in relevant_assignment.items():
        potential.state_names[var] = states
        potential.name_to_no[var] = ({states[i]: i for i in range(len(states))})


def update_junction_tree_state_names(bayesian_network, junction_tree):
    assignment_dict = create_assignment_dict(bayesian_network)
    print(assignment_dict)
    for factor in junction_tree.get_factors():
        update_state_names(assignment_dict, factor)


def print_all_states_to_no(junction_tree):
    for potential in junction_tree.get_factors():
        print(f"mapping  is :\n {potential.name_to_no}\n\n\n")
