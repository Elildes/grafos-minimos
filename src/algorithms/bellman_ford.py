import math
import sys

def bellman_ford(graph, start_vertex):
    """
    Executa o algoritmo de Bellman-Ford para encontrar os caminhos mínimos
    a partir de um vértice de origem em um grafo ponderado.

    Detecta ciclos de custo negativo acessíveis a partir da origem.

    Assume que a API do objeto 'graph' é:
    - graph.get_vertices(): Retorna uma lista/set de todos os vértices.
    - graph.get_neighbors(v): Retorna um dict {vizinho: peso, ...}

    :param graph: Objeto grafo (esperado de graph.py).
    :param start_vertex: O vértice de origem.
    :return: Um dicionário contendo os caminhos, custos e status.
    """

    # --- 1. Validação e Inicialização ---

    # O algoritmo executará em grafos não direcionados.
    # Se um grafo não direcionado tiver uma aresta de peso negativo,
    # isso criará um ciclo negativo (ex: a <-> b), que será
    # detectado corretamente pela Etapa 4.

    vertices = graph.get_vertices()
    if not vertices:
        return {
            'success': False, 
            'algorithm': 'Bellman-Ford',
            'error': 'O grafo está vazio.'
        }

    if start_vertex not in vertices:
        return {
            'success': False, 
            'algorithm': 'Bellman-Ford',
            'error': f'O vértice inicial "{start_vertex}" não foi encontrado no grafo.'
        }

    # Coleta todas as arestas do grafo no formato (u, v, peso)
    edges = []
    for u in vertices:
        for v, weight in graph.get_neighbors(u).items():
            edges.append((u, v, weight))

    # --- 2. Inicialização (INITIALIZE-SINGLE-SOURCE) ---
    distances = {v: math.inf for v in vertices}
    predecessors = {v: None for v in vertices}
    
    distances[start_vertex] = 0
    
    num_vertices = len(vertices)

    # --- 3. Relaxamento (V-1 iterações) ---
    
    # Itera |V| - 1 vezes
    for _ in range(num_vertices - 1):
        # Itera sobre todas as arestas do grafo
        for u, v, weight in edges:
            # Etapa de Relaxamento (RELAX)
            if distances[u] != math.inf and distances[v] > distances[u] + weight:
                distances[v] = distances[u] + weight
                predecessors[v] = u

    # --- 4. Detecção de Ciclo Negativo ---
    
    # Itera uma |V|-ésima vez
    for u, v, weight in edges:
        # Se ainda for possível relaxar uma aresta, há um ciclo negativo
        if distances[u] != math.inf and distances[v] > distances[u] + weight:
            return {
                'success': False, # Falha, pois os caminhos mínimos não são bem definidos
                'algorithm': 'Bellman-Ford',
                'negative_cycle': True,
                'error': 'Ciclo de custo negativo detectado. Os caminhos mínimos não podem ser calculados.'
            }

    # --- 5. Preparação dos Resultados ---
    
    # Se não houver ciclo negativo, formata a saída
    
    display_distances = {v: (d if d != math.inf else 'Infinito') for v, d in distances.items()}
    
    paths = {}
    for vertex in vertices:
        if distances[vertex] == math.inf:
            paths[vertex] = None
            continue

        path = []
        curr = vertex
        while curr is not None:
            path.append(curr)
            if curr == start_vertex:
                break
            curr = predecessors.get(curr)
        
        if path and path[-1] == start_vertex:
            paths[vertex] = path[::-1] # Inverte para [start, ..., end]
        else:
            if vertex == start_vertex:
                paths[vertex] = [start_vertex]
            else:
                paths[vertex] = None # Inacessível

    return {
        'success': True,
        'algorithm': 'Bellman-Ford',
        'start_vertex': start_vertex,
        'negative_cycle': False,
        'message': 'Caminhos mínimos encontrados com sucesso.',
        'results': {
            'distances': display_distances,
            'paths': paths
        }
    }