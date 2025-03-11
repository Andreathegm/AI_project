from collections import deque


# print potentials for (normal) junction tree using the method get_factors()
def print_all_potentials(junction_tree):
    for clique in junction_tree.nodes:
        print(f"\n Potential for  {clique}:\n")
        print(junction_tree.get_factors(clique))


# function to check if a clique contains some/all variables in Q
def is_in_clique(multiple_cliques_involved, Q, clique, reducibleQ):
    # multiple_cliques_involved is a set of cliques that contains altogether the variables in Q
    i = 0
    for variable in Q:
        if variable in clique:
            if len(reducibleQ) > 0 and variable in reducibleQ:
                i += 1
                reducibleQ.discard(variable)

    if i == len(Q):
        return True

    if i > 0:
        multiple_cliques_involved.append(clique)


def apply_evidence_to_all_potentials(custom_junction_tree, evidences):
    print("Applying evidence on all potentials and separators...\n")
    for clique in custom_junction_tree.nodes:
        _dict = {}
        print(f"apply evidence on clique : {clique}")
        projecting_dict_on_clique(clique, _dict, evidences)
        custom_junction_tree.apply_evidence_to_potentials(clique, _dict.items())
        _dict.clear()
    for potential in custom_junction_tree.separators:
        _dict = {}
        projecting_dict_on_clique(custom_junction_tree.separators[potential].variables, _dict, evidences)
        custom_junction_tree.apply_evidence_to_separator(_dict.items(), potential)
        _dict.clear()
    print("\nEvidence applied successfully!\n")


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
    for var, states in relevant_assignment.items():
        potential.state_names[var] = states
        potential.name_to_no[var] = ({states[i]: i for i in range(len(states))})


def update_junction_tree_state_names(bayesian_network, junction_tree):
    assignment_dict = create_assignment_dict(bayesian_network)
    for factor in junction_tree.get_factors():
        update_state_names(assignment_dict, factor)


def print_all_states_to_no(junction_tree):
    for potential in junction_tree.get_factors():
        print(f"mapping  is :\n {potential.name_to_no}\n\n\n")


def connect_cliques(junction_tree, cliques_containing_Q):
    # Input validation
    if not isinstance(cliques_containing_Q, list):
        return None, None

    # Remove duplicates while preserving order
    seen = set()
    unique_cliques = [c for c in cliques_containing_Q if not (c in seen or seen.add(c))]

    if not unique_cliques:
        return [], []

    # Initialize with first clique
    result_cliques = [unique_cliques[0]]
    connected = {unique_cliques[0]}
    separators = []

    def find_connection_path(start, targets):
        visited = set()
        queue = deque([(start, [], [])])

        while queue:
            current, path, seps = queue.popleft()
            if current in targets:
                return path + [current], seps
            if current in visited:
                continue
            visited.add(current)

            for neighbor in junction_tree.neighbors(current):
                # Get separator between current and neighbor
                edge = tuple(sorted(set(current).union(set(neighbor))))
                sep = junction_tree.separators.get(edge, None)

                new_path = path + [current]
                new_seps = seps + [sep] if sep is not None else seps
                queue.append((neighbor, new_path, new_seps))

        return None, None

    # Connect remaining cliques
    for clique in unique_cliques[1:]:
        if clique in connected:
            continue

        # Find path to connected component
        path, path_seps = find_connection_path(clique, connected)
        print(f"path is : {path}, separators path is : {path_seps}")
        if not path:
            continue  # Shouldn't happen in valid junction tree

        # Add new cliques (excluding last one which is already connected)
        for c in path[:-1]:
            if c not in connected:
                result_cliques.append(c)
                connected.add(c)

        # Add new separators
        for sep in path_seps:
            if all(id(sep) != id(existing_sep) for existing_sep in separators):
                separators.append(sep)

    return result_cliques, separators
