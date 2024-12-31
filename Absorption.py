from pgmpy.factors.discrete import DiscreteFactor
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

def message_passing(junction_tree, junction_tree_root, evidences, separator_tables):
    def forward_pass(current_clique, parent_clique=None, leaves=None):
        # Inizializza leaves solo se non è già stato passato come argomento
        if leaves is None:
            leaves = []

        # Recupera il potenziale della cricca
        potential = junction_tree.get_factors(current_clique)

        # Applica evidenze, se presenti
        for variable in current_clique:
            if variable in evidences:
                evidence = evidences[variable]
                apply_evidence(potential, {variable: evidence})

        # Trova i vicini escludendo il genitore
        neighbors = [neighbor for neighbor in junction_tree.neighbors(current_clique) if neighbor != parent_clique]
        if not neighbors:  # Se non ci sono vicini escluso il genitore, è una foglia
            leaves.append(current_clique)
        else:
            # Propaga ai vicini
            for neighbor in neighbors:
                separator =separator_tables[tuple(sorted(set(current_clique).union(set(neighbor))))]
                absorption(junction_tree, current_clique, neighbor, separator)
                forward_pass(neighbor, current_clique, leaves)

        return leaves

    def backward_pass(leaves):

        visited_edges = set()  # Per evitare di processare lo stesso arco più volte

        def propagate(clique, parent_clique=None):

            # Recupera i vicini escluso il nodo da cui proviene il messaggio
            neighbors = [neighbor for neighbor in junction_tree.neighbors(clique) if neighbor != parent_clique]
            if clique==junction_tree_root:
                return

            for neighbor in neighbors:
                print(neighbor)
                edge =tuple(sorted(set(clique).union(set(neighbor))))
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    separator = separator_tables[edge]
                    absorption(junction_tree,clique ,neighbor , separator)
                propagate(neighbor,clique)


        # Avvia la propagazione per ogni foglia
        for leaf in leaves:
            propagate(leaf)


    leaves = forward_pass(junction_tree_root)
    backward_pass(leaves)


def apply_evidence(potential, evidence):
    factor_shape = potential.values.shape

    # Itera su tutte le combinazioni di valori degli stati del potenziale
    for index in range(potential.values.size):
        # Converte l'indice lineare in un indice multidimensionale
        state_combination = np.unravel_index(index, factor_shape)

        # Verifica se la combinazione soddisfa l'evidenza
        valid = True
        for var, assignment in evidence.items():
            var_index = potential.variables.index(var)  # Trova l'indice della variabile
            state_no = potential.get_state_no(var, assignment)  # Ottieni lo stato corrispondente
            if state_combination[var_index] != state_no:
                valid = False
                break

        # Se non è valido, imposta il valore a 0
        if not valid:
            potential.values.flat[index] = 0


