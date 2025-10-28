"""
Ler e interpretar arquivos DOT e criar objetos graph a partir deles.
"""
import re
from .graph import Graph  # Import relativo do mesmo pacote 'src'

# Expressões Regulares (Regex) para interpretar o formato DOT

# 1. Regex para 'graph' ou 'digraph' (ignora case)
#    Captura 'di' se for 'digraph'
GRAPH_TYPE_RE = re.compile(r'^\s*(di)?graph', re.IGNORECASE)

# 2. Regex para arestas, com ou sem peso
#    Captura: Grupo 1 (u), Grupo 2 (op), Grupo 3 (v), Grupo 4 (peso)
#    Exemplos:
#    a -- b;
#    a -> b [weight=5];
#    a -> b [weight=5.5];
EDGE_RE = re.compile(
    r'^\s*(\w+)\s*(--|->)\s*(\w+)'  # Grupo 1 (u), 2 (op), 3 (v)
    # Grupo 4 (peso) opcional, permite inteiros ou floats
    r'\s*(?:\[.*?weight\s*=\s*(\d+(?:\.\d+)?)\])?' 
    r'\s*;?\s*$'  # Final da linha, ponto e vírgula opcional
)

# 3. Regex para vértices sozinhos (Ex: a;)
VERTEX_RE = re.compile(r'^\s*(\w+)\s*;?\s*$')


def parse_dot(filepath):
    """
    Lê um arquivo .dot e o converte em um objeto Graph.
    
    :param filepath: O caminho completo para o arquivo .dot (ex: '/.../graphs/graph01.dot')
    :return: Um objeto da classe Graph.
    """
    g = None
    is_directed = None

    try:
        # print(f"[Parser] Abrindo arquivo: {filepath}") # Debug
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()

                # Ignora linhas vazias ou comentários
                if not line or line.startswith('#') or line.startswith('//'):
                    continue

                # Ignora a linha de fechamento '}'
                if line.startswith('}'):
                    continue

                # --- 1. Determina o tipo de grafo (deve ser a primeira linha) ---
                if g is None:
                    match = GRAPH_TYPE_RE.search(line)
                    if match:
                        # se o grupo 1 ('di') existir, é direcionado
                        is_directed = (match.group(1) is not None)
                        g = Graph(directed=is_directed)
                        # print(f"[Parser] Grafo iniciado. Direcionado: {is_directed}") # Debug
                        continue
                    else:
                        # Se a primeira linha não for 'graph' ou 'digraph'
                        raise ValueError(f"Arquivo DOT inválido: 'graph' ou 'digraph' não encontrado na primeira linha. Linha: '{line}'")

                # --- 2. Tenta dar match em uma aresta ---
                edge_match = EDGE_RE.match(line)
                if edge_match:
                    u, op, v, weight_str = edge_match.groups()
                    
                    # Validação de tipo de aresta vs tipo de grafo
                    if is_directed and op == '--':
                        raise ValueError(f"Erro de sintaxe (linha {line_number}): Aresta '--' (não direcionada) usada em um 'digraph'.")
                    if not is_directed and op == '->':
                        raise ValueError(f"Erro de sintaxe (linha {line_number}): Aresta '->' (direcionada) usada em um 'graph'.")

                    # Define o peso (padrão 1.0 se não especificado)
                    weight = float(weight_str) if weight_str else 1.0
                    
                    g.add_edge(u, v, weight)
                    continue

                # --- 3. Tenta dar match em um vértice sozinho (Ex: a;) ---
                vertex_match = VERTEX_RE.match(line)
                if vertex_match:
                    u = vertex_match.group(1)
                    g.add_vertex(u) # Garante que o vértice exista
                    continue

                # Se não deu match em nada, pode ser um atributo do grafo, etc.
                # Para este projeto, vamos apenas registrar e ignorar.
                # print(f"[Parser] Linha ignorada (não é aresta nem vértice): {line}")

    except FileNotFoundError:
        print(f"Erro [Parser]: Arquivo não encontrado: {filepath}")
        raise # Re-levanta a exceção para o app.py tratar
    except Exception as e:
        print(f"Erro [Parser] ao processar o arquivo DOT: {e}")
        raise

    if g is None:
        raise ValueError("Não foi possível criar o grafo. O arquivo está vazio ou em formato inválido.")

    # print(f"[Parser] Grafo finalizado:\n{g}") # Debug
    return g