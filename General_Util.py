def print_junction_tree_structure(junction_tree):
    print("Junction Tree nodes (cliques):", junction_tree.nodes())
    print("Junction Tree edges:", junction_tree.edges())


def print_all_potentials(junction_tree):
    for clique in junction_tree.nodes:
        print(f"\nPotenziale del clique {clique}:")
        print(junction_tree.get_factors(clique))
#TODO verify later that everything is cohesive


def print_all_cpds(bayesian_network):
    for cpd in bayesian_network.get_cpds():
        print(f"CPD for {cpd.variable}:")
        print(cpd)
        print("\n")


def get_leaves(junction_tree, root):
    visited = set()

    def dfs(node, parent=None):
        visited.add(node)
        neighbors = [neighbor for neighbor in junction_tree.neighbors(node) if neighbor != parent]

        if len(neighbors) == 0:
            return node

        leaves = []
        for neighbor in neighbors:
            if neighbor not in visited:
                leaves.append(dfs(neighbor, node))

        return leaves

    return dfs(root)


def is_in_clique(multiple_cliques_involved, Q, clique, reduceableQ):
    # multiple_cliques_involved is a set of cliques that contains altogether the variables in Q
    i = 0
    for variable in Q:
        if variable in clique:
            i += i
            if len(reduceableQ) > 0 and variable in reduceableQ:
                reduceableQ.discard(variable)
    if i == len(Q):
        return True
    else:
        if len(reduceableQ) > 0:
            multiple_cliques_involved.add(clique)

