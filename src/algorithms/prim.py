import heapq
import sys

def prim_mst(graph, start_vertex):
    """
    Executa o algoritmo de Prim para encontrar a Árvore Geradora Mínima (MST)
    de um grafo não direcionado, ponderado e conectado.

    Assume que a API do objeto 'graph' é:
    - graph.get_vertices(): Retorna uma lista/set de todos os vértices.
    - graph.get_neighbors(v): Retorna um dict {vizinho: peso, ...}

    :param graph: Objeto grafo (esperado de graph.py).
    :param start_vertex: O vértice para iniciar a construção da MST.
    :return: Um dicionário contendo a MST, o custo total e um status.
    """

    # --- 1. Validação e Inicialização ---
    
    # Verifica se o grafo tem vértices
    all_vertices = graph.get_vertices()
    if not all_vertices:
        return {
            'success': False,
            'error': 'O grafo está vazio.'
        }

    # Verifica se o vértice inicial existe
    if start_vertex not in all_vertices:
        return {
            'success': False,
            'error': f'O vértice inicial "{start_vertex}" não foi encontrado no grafo.'
        }

    mst_edges = []      # Lista para armazenar as arestas (u, v, peso) da MST
    total_cost = 0      # Custo total da MST
    visited = set()     # Conjunto de vértices já incluídos na MST
    
    # Fila de prioridade (min-heap) para armazenar as arestas candidatas
    # Formato: (peso, vértice_origem, vértice_destino)
    min_heap = []

    # --- 2. Lógica Principal do Algoritmo ---

    try:
        # Adiciona o vértice inicial ao conjunto de visitados
        visited.add(start_vertex)

        # Adiciona todas as arestas do vértice inicial à fila de prioridade
        # (Assumindo que get_neighbors retorna um dict {vizinho: peso})
        for neighbor, weight in graph.get_neighbors(start_vertex).items():
            heapq.heappush(min_heap, (weight, start_vertex, neighbor))

        # Loop principal: continua enquanto houver arestas na fila
        while min_heap:
            # Pega a aresta com o menor peso da fila
            weight, u, v = heapq.heappop(min_heap)

            # Se o vértice de destino (v) já foi visitado, pula (evita ciclos)
            if v in visited:
                continue

            # Processa o novo vértice
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_cost += weight

            # Adiciona as arestas do novo vértice (v) à fila
            for neighbor, new_weight in graph.get_neighbors(v).items():
                # Só adiciona se o vizinho ainda não foi visitado
                if neighbor not in visited:
                    heapq.heappush(min_heap, (new_weight, v, neighbor))

        # --- 3. Verificação de Conectividade e Retorno ---

        # Verifica se todos os vértices foram visitados.
        # Se não, o grafo não é conectado.
        is_connected = (len(visited) == len(all_vertices))
        
        if not is_connected:
            return {
                'success': True,
                'status': 'Grafo não conectado',
                'message': f'MST encontrada apenas para o componente conectado de "{start_vertex}".',
                'mst_edges': mst_edges,
                'total_cost': total_cost
            }

        return {
            'success': True,
            'status': 'Conectado',
            'message': 'Árvore Geradora Mínima encontrada com sucesso.',
            'mst_edges': mst_edges,
            'total_cost': total_cost
        }

    except Exception as e:
        # Captura erros inesperados (ex: se get_neighbors não for um dict)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        return {
            'success': False,
            'error': f'Erro interno durante a execução do Prim: {e} (linha {exc_tb.tb_lineno})' # type: ignore
        }