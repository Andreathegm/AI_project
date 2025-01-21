def calculate_conditional_probability(cliques_containingQ, Q, evidences_key, custom_junction_tree):
    factors_to_multiply = []
    factor = None
    if isinstance(cliques_containingQ, list):
        for clique in cliques_containingQ:
            potential = custom_junction_tree.get_potential(clique)
            marginalized_vars = set(potential.variables)-(set(potential.variables).intersection(set(Q))-set(evidences_key))
            print(f" Marginalized var for clique= {clique} are : {marginalized_vars}")
            if not len(marginalized_vars) == 0:
                factors_to_multiply.append(potential.marginalize(variables=list(marginalized_vars), inplace=False))
                print("value appended")
            else:
                factors_to_multiply.append(potential)
    else:
        marginalized_vars = set(cliques_containingQ)-(set(cliques_containingQ).intersection(set(Q))-set(evidences_key))
        print(marginalized_vars)
        potential = custom_junction_tree.get_potential(cliques_containingQ)
        print(f" variables for {cliques_containingQ} are {potential.variables}")
        if not len(marginalized_vars) == 0:
            factor = potential.marginalize(variables=list(marginalized_vars), inplace=False)
            print("marginalized")
        else:
            print("not marginalized")
            factor = potential

    if isinstance(cliques_containingQ, list):
        print("Multiplying factors to get conjunctive factor")
        factor = factors_to_multiply[0].copy()
        print(len(factors_to_multiply))
        for i in range(1, len(factors_to_multiply)):
            print("i'm in the loop")
            factor = factor.product(factors_to_multiply[i], inplace=False)

    return factor


def conditional_probability_bruteforce(bayesian_network, Q, evidences):
    variables = set(bayesian_network.nodes())

    query_variables = set(Q.keys())
    evidence_variables = set(evidences.keys())
    observed_variables = query_variables.union(evidence_variables)

    hidden_variables = variables - observed_variables

    joint_factor = None
    for cpd in bayesian_network.get_cpds():
        if joint_factor is None:
            joint_factor = cpd.to_factor()
        else:
            joint_factor = joint_factor.product(cpd, inplace=False)

    pu_full = joint_factor.copy()
    pu_reduced = joint_factor.copy()

    marginalized_out_1 = hidden_variables
    pu_reduced.marginalize(variables=list(marginalized_out_1), inplace=True)

    marginalized_out_2 = variables - evidence_variables
    pu_full.marginalize(variables=marginalized_out_2, inplace=True)

    pu_reduced.divide(pu_full, inplace=True)

    return pu_reduced
