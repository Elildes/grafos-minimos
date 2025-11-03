import math
import sys

def floyd_warshall(graph):
    """
    Executa o algoritmo de Floyd-Warshall para encontrar os caminhos mínimos
    entre todos os pares de vértices em um grafo ponderado (direcionado ou não).

    Detecta ciclos de custo negativo e reconstrói os caminhos mínimos.

    Assume que a API do objeto 'graph' é:
    - graph.get_vertices(): Retorna uma lista/set de todos os vértices.
    - graph.get_neighbors(v): Retorna um dict {vizinho: peso, ...}

    :param graph: Objeto grafo (esperado de graph.py).
    :return: Um dicionário contendo as distâncias mínimas, caminhos e status.
    """

    # --- 1. Validação e Inicialização ---

    vertices = graph.get_vertices()
    if not vertices:
        return {
            'success': False,
            'algorithm': 'Floyd-Warshall',
            'error': 'O grafo está vazio.'
        }

    # Lista ordenada para indexação estável
    vertices = list(vertices)
    n = len(vertices)

    # Criação das matrizes de distância e predecessor
    dist = {u: {v: math.inf for v in vertices} for u in vertices}
    next_vertex = {u: {v: None for v in vertices} for u in vertices}

    # Inicializa as distâncias com os pesos das arestas
    for u in vertices:
        dist[u][u] = 0
        for v, weight in graph.get_neighbors(u).items():
            dist[u][v] = weight
            next_vertex[u][v] = v

    # --- 2. Algoritmo Principal (Dinâmica de Programação) ---
    # Itera sobre todos os vértices intermediários
    for k in vertices:
        for i in vertices:
            for j in vertices:
                # Evita operações desnecessárias
                if dist[i][k] == math.inf or dist[k][j] == math.inf:
                    continue

                new_dist = dist[i][k] + dist[k][j]
                if new_dist < dist[i][j]:
                    dist[i][j] = new_dist
                    next_vertex[i][j] = next_vertex[i][k]

    # --- 3. Detecção de Ciclos Negativos ---
    # Um ciclo negativo existe se dist[v][v] < 0 para algum vértice v
    negative_cycles = []
    for v in vertices:
        if dist[v][v] < 0:
            negative_cycles.append(v)

    if negative_cycles:
        return {
            'success': False,
            'algorithm': 'Floyd-Warshall',
            'negative_cycle': True,
            'error': f'Ciclo(s) de custo negativo detectado(s) envolvendo: {negative_cycles}'
        }

    # --- 4. Reconstrução dos Caminhos ---
    def reconstruct_path(u, v):
        """Reconstrói o caminho mínimo de u até v usando a matriz next_vertex."""
        if next_vertex[u][v] is None:
            return None
        path = [u]
        while u != v:
            u = next_vertex[u][v]
            if u is None:
                return None
            path.append(u)
        return path

    paths = {}
    for i in vertices:
        paths[i] = {}
        for j in vertices:
            if dist[i][j] != math.inf:
                paths[i][j] = reconstruct_path(i, j)
            else:
                paths[i][j] = None

    # --- 5. Preparação e Retorno dos Resultados ---
    display_dist = {
        i: {j: (dist[i][j] if dist[i][j] != math.inf else 'Infinito') for j in vertices}
        for i in vertices
    }

    return {
        'success': True,
        'algorithm': 'Floyd-Warshall',
        'message': 'Caminhos mínimos entre todos os pares encontrados com sucesso.',
        'negative_cycle': False,
        'results': {
            'vertices': vertices,
            'distances': display_dist,
            'paths': paths
        }
    }

