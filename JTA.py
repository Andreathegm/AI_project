import CondtionalQuery
import General_Util


def absorption(junction_tree, absorbed_clique, absorber_clique, separator, edge):
    absorbed_potential = junction_tree.get_potential(absorbed_clique)
    absorber_potential = junction_tree.get_potential(absorber_clique)

    current_separator = separator
    shared_vars = list(separator.variables)
    marginalized_vars = list(set(absorbed_potential.variables) - set(shared_vars))
    message = absorbed_potential.marginalize(variables=marginalized_vars, inplace=False)

    absorber_potential.product(message, inplace=True)
    absorber_potential.divide(current_separator, inplace=True)

    update_separator(junction_tree, edge, message)


def message_passing(Q, custom_junction_tree, custom_junction_tree_root):
    single_clique = None
    multiple_cliques_involved = []   # set of cliques that contains altogether the variables in Q
    reducableQ = set(Q)

    def propagate_message(current_clique, parent_clique=None):
        nonlocal single_clique
        nonlocal multiple_cliques_involved
        nonlocal reducableQ

        if General_Util.is_in_clique(multiple_cliques_involved, Q, current_clique, reducableQ) and single_clique is None:
            single_clique = current_clique

        neighbors = [neighbor for neighbor in custom_junction_tree.neighbors(current_clique) if neighbor != parent_clique]
        if not neighbors:
            return
        else:
            for neighbor in neighbors:
                edge = tuple(sorted(set(current_clique).union(set(neighbor))))
                separator = custom_junction_tree.separators[edge]
                absorption(custom_junction_tree, current_clique, neighbor, separator, edge)
                propagate_message(neighbor, current_clique)

    def collect_messages(root):

        visited_edges = set()

        def propagate_upwards(clique, parent_clique=None):

            neighbors = [
                neighbor for neighbor in custom_junction_tree.neighbors(clique)
                if neighbor != parent_clique
            ]
            if not neighbors:
                return

            for neighbor in neighbors:
                edge = tuple(sorted(set(clique).union(set(neighbor))))

                if edge not in visited_edges:
                    visited_edges.add(edge)

                    propagate_upwards(neighbor, clique)

                    separator = custom_junction_tree.separators[edge]

                    absorption(custom_junction_tree, neighbor, clique, separator, edge)

        propagate_upwards(root)

    collect_messages(custom_junction_tree_root)
    propagate_message(custom_junction_tree_root)

    if single_clique is None:
        print(f"Q is in cliques:")
        for address in multiple_cliques_involved:
            print(address)
        print("\n")
        return multiple_cliques_involved
    else:
        print(f"Q is in clique : {single_clique}\n ")
        return single_clique


def update_separator(junction_tree, edge, new_separator):
    junction_tree.separators[edge] = new_separator


def print_result_for_jta(provide_evidence, cliques_containingQ, Q, keysQ, evideces_key, jt, formattedQ_brute_force,
                         formattedQ, formattedEvidences):
    if provide_evidence:
        probability = CondtionalQuery.calculate_conditional_probability(cliques_containingQ, keysQ, evideces_key, jt)
        print(f"DISTRIBUTION REQUESTED :  P({formattedQ_brute_force} | {formattedEvidences}) :\n{probability._str(phi_or_p='probabilty')}\n")
        probability.reduce(Q.items(), inplace=True)
        value = probability.values
        print(f"Probability of requested realization of Q  :  P({formattedQ} | {formattedEvidences}) : {value}")
    else:
        # print the distribution of the variable U across all network
        jt.print_all_probability()