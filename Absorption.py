import numpy as np
def absorption(junction_tree, absorbed_clique, absorber_clique, separator):
    absorbed_potential = junction_tree.get_factors(absorbed_clique)
    absorber_potential = junction_tree.get_factors(absorber_clique)

    current_separator =separator


    shared_vars = list(separator.variables)

    marginalized_vars = list(set(absorbed_potential.variables) - set(shared_vars))
    message=absorbed_potential.marginalize(variables=marginalized_vars, inplace=False)

    # 4. Aggiorna il potenziale della cricca assorbente
    absorber_potential.product(message,inplace=True)
    absorber_potential.divide(current_separator,inplace=True)

    # 5. Aggirna il valore del separatore con il messaggio
    separator.values = message.values  # Aggiorna direttamente i valori del separatore

    # 6. Aggiorna il junction tree con i fattori aggiornati
    junction_tree.add_factors(absorber_potential)  # Sostituisce il potenziale dell'assorbitore

def message_passing(junction_tree, junction_tree_root, evidences, separator_tables,leaves):

    def propagatemessage(current_clique, parent_clique=None):

        potential = junction_tree.get_factors(current_clique)
        dict={}
        # Applica evidenze, se presenti
        for variable in current_clique:
            if variable in evidences:
                evidence = evidences[variable]
                dict[variable]=evidence
        apply_evidence(potential, list(dict.items()))

        # Trova i vicini escludendo il genitore
        neighbors = [neighbor for neighbor in junction_tree.neighbors(current_clique) if neighbor != parent_clique]
        if not neighbors:  # Se non ci sono vicini escluso il genitore, è una foglia
            return
        else:
            # Propaga ai vicini
            for neighbor in neighbors:
                separator =separator_tables[tuple(sorted(set(current_clique).union(set(neighbor))))]
                absorption(junction_tree, current_clique, neighbor, separator)
                propagatemessage(neighbor, current_clique)


    def collectmessages(leaves):
        visited_edges = set()
        def propagatebackwards(clique,parent_clique=None):
            if clique==junction_tree_root:
                return

            neighbors = [neighbor for neighbor in junction_tree.neighbors(clique) if neighbor != parent_clique]

            for neighbor in neighbors:
                edge =tuple(sorted(set(clique).union(set(neighbor))))
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    separator = separator_tables[edge]
                    absorption(junction_tree,clique ,neighbor , separator)
                    propagatebackwards(neighbor,clique)
        for leaf in leaves:
            propagatebackwards(leaf)

    collectmessages(leaves)
    propagatemessage(junction_tree_root)


def apply_evidence(potential, evidence):
    print('sto applicando la evidenza')
    print(potential)
    new_potential=potential.reduce(evidence, inplace=False)
    potential=new_potential
    print(potential)



