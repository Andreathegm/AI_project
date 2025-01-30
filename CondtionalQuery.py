def calculate_conditional_probability(cliques_containingQ, Q, evidences_key, custom_junction_tree, separator_paths):
    factors_to_multiply = []
    factor = None
    if isinstance(cliques_containingQ, list):
        for clique in cliques_containingQ:
            '''
            potential = custom_junction_tree.get_potential(clique)
            marginalized_vars = set(potential.variables)-(set(potential.variables).intersection(set(Q)))-set(evidences_key)
            print(f" Marginalized var for clique= {clique} are : {marginalized_vars}")
            if not len(marginalized_vars) == 0:
                factors_to_multiply.append(potential.marginalize(variables=list(marginalized_vars), inplace=False))
                print("value appended")
            else:
                factors_to_multiply.append(potential)'''
            factors_to_multiply.append(custom_junction_tree.get_potential(clique))
    else:
        marginalized_vars = set(cliques_containingQ)-(set(cliques_containingQ).intersection(set(Q)))-set(evidences_key)
        potential = custom_junction_tree.get_potential(cliques_containingQ)
        if not len(marginalized_vars) == 0:
            factor = potential.marginalize(variables=list(marginalized_vars), inplace=False)
        else:
            factor = potential

    if isinstance(cliques_containingQ, list):
        factor = factors_to_multiply[0].copy()
        print(len(factors_to_multiply))
        for i in range(1, len(factors_to_multiply)):
            factor = factor.product(factors_to_multiply[i], inplace=False)
        print(f"Factor after multiplication is :\n {factor}")
        for separator in separator_paths:
            factor.divide(separator, inplace=True)
        marginalized_vars = set(factor.variables) - set(Q) - set(evidences_key)
        print(f"Marginalized vars are : {marginalized_vars}")
        factor = factor.marginalize(variables=list(marginalized_vars), inplace=False)


    return factor


def conditional_probability_bruteforce(provide_evidence, bayesian_network, Q, evidences):
    joint_factor = None
    for cpd in bayesian_network.get_cpds():
        if joint_factor is None:
            joint_factor = cpd.to_factor()
        else:
            joint_factor = joint_factor.product(cpd, inplace=False)

    if provide_evidence:
        variables = set(bayesian_network.nodes())
        query_variables = set(Q.keys())
        evidence_variables = set(evidences.keys())
        observed_variables = query_variables.union(evidence_variables)
        hidden_variables = variables - observed_variables

        pu_full = joint_factor.copy()
        pu_reduced = joint_factor.copy()

        # Calculate nominator P(Q, E)
        marginalized_out_1 = hidden_variables
        pu_reduced.marginalize(variables=list(marginalized_out_1), inplace=True)

        # Calculate denominator P(E)
        marginalized_out_2 = variables - evidence_variables
        pu_full.marginalize(variables=marginalized_out_2, inplace=True)

        # Calculate P(Q|E) = P(Q, E) / P(E)
        pu_reduced.divide(pu_full, inplace=True)
        return pu_reduced

    else:
        return joint_factor


def calculate_and_print_brute_force_result(bayesian_network, Q, evidences, provide_evidence, formattedQ_brute_force,
                                                        formattedEvidences_brute_force, stringU):
    print("----PRINTING RESULT USING BRUTE FORCE----\n")
    if provide_evidence:
        factor = conditional_probability_bruteforce(provide_evidence, bayesian_network, Q, evidences)
        print(f"P({formattedQ_brute_force}|{formattedEvidences_brute_force}):\n"
              f"{factor}\n")
        factor.reduce(Q.items() | evidences.items(), inplace=True)
        return factor.values
    else:
        print(f"{stringU}\n{conditional_probability_bruteforce(provide_evidence,bayesian_network, Q, evidences)}\n")
