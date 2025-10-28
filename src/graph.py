"""
Usa uma lista de adjacência (implementada com dicionários) para armazenar os vértices e arestas
"""
class Graph:
    def __init__(self, directed=False):
        """
        Inicializa o grafo.
        
        self.adj_list armazena o grafo no formato:
        {
            'vertice_origem': {'vertice_destino_1': peso, 'vertice_destino_2': peso, ...},
            ...
        }
        
        :param directed: Define se o grafo é direcionado (True) ou não (False).
        """
        self.adj_list = {}
        self.directed = directed

    def add_vertex(self, vertex_label):
        """
        Adiciona um vértice ao grafo se ele ainda não existir.
        
        :param vertex_label: O rótulo (nome) do vértice (ex: 'a').
        """
        if vertex_label not in self.adj_list:
            self.adj_list[vertex_label] = {}
            # print(f"[Graph] Vértice adicionado: {vertex_label}") # Debug

    def add_edge(self, u, v, weight=1.0):
        """
        Adiciona uma aresta entre os vértices 'u' e 'v' com um peso.
        
        Se o grafo não for direcionado, a aresta reversa (v, u) também é
        adicionada com o mesmo peso.
        
        :param u: Vértice de origem.
        :param v: Vértice de destino.
        :param weight: Peso da aresta (float). Padrão é 1.0.
        """
        # Garante que ambos os vértices existam na lista de adjacência
        self.add_vertex(u)
        self.add_vertex(v)

        # Adiciona a aresta de u para v
        self.adj_list[u][v] = float(weight)
        # print(f"[Graph] Aresta adicionada: {u} -> {v} (peso {weight})") # Debug

        # Se o grafo não for direcionado, adiciona a aresta de volta
        if not self.directed:
            self.adj_list[v][u] = float(weight)
            # print(f"[Graph] Aresta adicionada: {v} -> {u} (peso {weight})") # Debug

    def get_vertices(self):
        """
        Retorna uma lista de todos os vértices no grafo.
        
        :return: list
        """
        return list(self.adj_list.keys())

    def get_neighbors(self, vertex_label):
        """
        Retorna um dicionário dos vizinhos e pesos para um dado vértice.
        
        :param vertex_label: O rótulo do vértice.
        :return: dict no formato {vizinho: peso, ...}
                 Retorna um dicionário vazio se o vértice não existir.
        """
        return self.adj_list.get(vertex_label, {})

    def __str__(self):
        """Retorna uma representação em string do grafo (lista de adjacência)."""
        output = ""
        for u, neighbors in self.adj_list.items():
            output += f"{u} -> {neighbors}\n"
        return output