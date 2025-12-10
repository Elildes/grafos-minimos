def dsatur(graph):
    """
    Executa o algoritmo DSATUR para coloração de grafos.

    Assume que o grafo segue a API:
    - graph.get_vertices()
    - graph.get_neighbors(v)

    Retorna uma estrutura padronizada semelhante ao Floyd-Warshall.
    """

    vertices = graph.get_vertices()
    if not vertices:
        return {
            'success': False,
            'algorithm': 'DSATUR',
            'error': 'O grafo está vazio.'
        }

    # Conjunto de vértices não coloridos
    U = set(vertices)

    # Estruturas
    color = {v: 0 for v in vertices}              # cor 0 = não colorido
    saturation = {v: 0 for v in vertices}         # grau de saturação
    degree = {v: len(graph.get_neighbors(v)) for v in vertices}

    order_colored = []                             # ordem de coloração
    saturation_history = {v: [] for v in vertices} # evolução da saturação

    # Função auxiliar: escolher vértice com maior saturação (empate → maior grau)
    def choose_vertex():
        best = None
        best_sat = -1
        best_deg = -1

        for v in U:
            sat = saturation[v]
            deg = degree[v]

            if sat > best_sat or (sat == best_sat and deg > best_deg):
                best_sat = sat
                best_deg = deg
                best = v

        return best

    # Loop principal do DSATUR
    while U:
        u = choose_vertex()

        # Determinar as cores usadas pelos vizinhos
        used_colors = set()
        for neigh in graph.get_neighbors(u):
            if color[neigh] != 0:
                used_colors.add(color[neigh])

        # Menor cor disponível
        c = 1
        while c in used_colors:
            c += 1

        color[u] = c
        U.remove(u)
        order_colored.append(u)

        # Atualizar saturação dos vizinhos NÃO COLORIDOS
        for neigh in graph.get_neighbors(u):
            if neigh in U:
                # Só aumenta se a cor é NOVA para o vizinho
                neigh_used = {color[k] for k in graph.get_neighbors(neigh) if color[k] != 0}
                if c not in neigh_used:
                    saturation[neigh] += 1

                saturation_history[neigh].append(saturation[neigh])

    # Número de cores usadas
    color_count = len(set(color.values()) - {0})

    return {
        'success': True,
        'algorithm': 'DSATUR',
        'message': 'Coloração realizada com sucesso.',
        'results': {
            'colors': color,
            'color_count': color_count,
            'order': order_colored,
            'saturation_history': saturation_history
        }
    }
