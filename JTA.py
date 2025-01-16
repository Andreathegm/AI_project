import General_Util


def absorption(junction_tree, absorbed_clique, absorber_clique, separator):
    print(f"Absorbed clique:{absorbed_clique},Absorber clique:{absorber_clique}")
    absorbed_potential = junction_tree.get_potential(absorbed_clique)#TODO prima era .get_factors
    print(absorbed_potential)
    absorber_potential = junction_tree.get_potential(absorber_clique)
    print(absorber_potential)

    current_separator = separator
    shared_vars = list(separator.variables)
    marginalized_vars = list(set(absorbed_potential.variables) - set(shared_vars))
    message = absorbed_potential.marginalize(variables=marginalized_vars, inplace=False)

    absorber_potential.product(message, inplace=True)
    absorber_potential.divide(current_separator, inplace=True)

    separator.values = message.values

    junction_tree.add_factors(absorber_potential)


def message_passing(Q, custom_junction_tree, custom_junction_tree_root, evidences, leaves):
    single_clique = None
    multiple_cliques_involved = []   # set of cliques that contains altogether the variables in Q
    reducableQ = set(Q)

    def propagatemessage(current_clique, parent_clique=None):
        nonlocal single_clique
        nonlocal multiple_cliques_involved
        nonlocal reducableQ

        if General_Util.is_in_clique(multiple_cliques_involved, Q, current_clique, reducableQ) and single_clique is None:
                single_clique = current_clique

        potential = custom_junction_tree.get_factors(current_clique)
        dict = {}

        # partitioning the real dict of the evidences-->projecting on the variables of the clique
        for variable in current_clique:
            if variable in evidences:
                evidence = evidences[variable]
                dict[variable] = evidence
        custom_junction_tree.apply_evidence_to_potentials(current_clique, dict.items())

        neighbors = [neighbor for neighbor in custom_junction_tree.neighbors(current_clique) if neighbor != parent_clique]
        if not neighbors:
            return
        else:
            for neighbor in neighbors:
                edge = tuple(sorted(set(current_clique).union(set(neighbor))))
                separator = custom_junction_tree.separators[edge]
                dict.clear()
                for variable in separator.variables:
                    if variable in evidences:
                        evidence = evidences[variable]
                        dict[variable] = evidence
                custom_junction_tree.apply_evidence_to_separator(dict.items(), edge)
                absorption(custom_junction_tree, current_clique, neighbor, separator)
                propagatemessage(neighbor, current_clique)

    def collectmessages(leaves):

        visited_edges = set()

        def propagatebackwards(clique, parent_clique=None):
            if clique == custom_junction_tree_root:
                return

            neighbors = [neighbor for neighbor in custom_junction_tree.neighbors(clique) if neighbor != parent_clique]

            for neighbor in neighbors:
                edge = tuple(sorted(set(clique).union(set(neighbor))))
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    separator = custom_junction_tree.separators[edge]
                    absorption(custom_junction_tree, clique, neighbor, separator)
                    propagatebackwards(neighbor, clique)
        for leaf in leaves:
            propagatebackwards(leaf)

    collectmessages(leaves)
    propagatemessage(custom_junction_tree_root)
    if single_clique is None:
        print(f"Q is in cliques:")
        for address in multiple_cliques_involved:
            print(address)
        return multiple_cliques_involved
    else:
        print(f"Q is in clique {single_clique} ")
        return single_clique


