import os
from flask import Flask, render_template, jsonify, request

# Importe suas funções de algoritmo (ajuste os caminhos se necessário)
# from src.algorithms.prim import prim_mst
# from src.algorithms.bellman_ford import bellman_ford
# from src.algorithms.floyd_warshall import floyd_warshall
# from src.dot_parser import parse_dot

app = Flask(__name__)

# --- Constantes de Pastas (Caminhos Absolutos) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_DIR = os.path.join(BASE_DIR, 'graphs')
DIGRAPH_DIR = os.path.join(BASE_DIR, 'digraphs')

def get_available_graphs():
    """Lê os diretórios e retorna os arquivos .dot ou .gv"""
    graphs = []
    digraphs = []
    
    # --- NOSSO DEBUG ---
    print("--- INICIANDO get_available_graphs ---")
    print(f"BASE_DIR absoluto: {BASE_DIR}")
    print(f"Buscando em GRAPH_DIR: {GRAPH_DIR}")
    # --- FIM DO DEBUG ---

    # Tenta ler a pasta de grafos não direcionados
    try:
        graphs = [f for f in os.listdir(GRAPH_DIR) if f.endswith('.dot') or f.endswith('.gv')]
        # --- NOSSO DEBUG ---
        print(f"Arquivos encontrados em graphs: {graphs}")
        # --- FIM DO DEBUG ---
    except FileNotFoundError:
        print(f"Aviso: Diretório '{GRAPH_DIR}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler GRAPH_DIR: {e}") # Adicionado para pegar outros erros

    # --- NOSSO DEBUG ---
    print(f"Buscando em DIGRAPH_DIR: {DIGRAPH_DIR}")
    # --- FIM DO DEBUG ---

    # Tenta ler a pasta de grafos direcionados
    try:
        digraphs = [f for f in os.listdir(DIGRAPH_DIR) if f.endswith('.dot') or f.endswith('.gv')]
        # --- NOSSO DEBUG ---
        print(f"Arquivos encontrados em digraphs: {digraphs}")
        # --- FIM DO DEBUG ---
    except FileNotFoundError:
        print(f"Aviso: Diretório '{DIGRAPH_DIR}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler DIGRAPH_DIR: {e}") # Adicionado para pegar outros erros

    print("--- FIM get_available_graphs ---")
    return {"graphs": graphs, "digraphs": digraphs}

# --- Rota 1: Servir a Página Principal ---
@app.route('/')
def index():
    """Renderiza o arquivo index.html da pasta 'templates'."""
    return render_template('index.html')

# --- Rota 2: A API para listar os arquivos ---
@app.route('/api/get-graphs')
def api_get_graphs():
    """Fornece a lista de arquivos em formato JSON."""
    files = get_available_graphs()
    return jsonify(files)

# --- Rota 3: Receber o formulário e rodar o algoritmo ---
@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    """Executa o algoritmo selecionado."""
    try:
        # 1. Coletar dados do formulário
        algo = request.form.get('algorithm')
        graph_type = request.form.get('graph_type')
        filename = request.form.get('graph_file')

        if not all([algo, graph_type, filename]):
            return "Erro: Faltando parâmetros no formulário.", 400

        # 2. Determinar o caminho do arquivo
        base_dir = DIGRAPH_DIR if graph_type == 'directed' else GRAPH_DIR
        filepath = os.path.join(base_dir, filename)

        if not os.path.exists(filepath):
            return f"Erro: Arquivo não encontrado: {filepath}", 404

        # 3. (COMENTADO) Chamar seu código Python
        #    Esta parte é onde você integra seu trabalho.
        # -----------------------------------------------------------
        # graph = parse_dot(filepath)
        # result = None
        # if algo == 'prim':
        #     # O algoritmo de Prim precisa de um vértice inicial.
        #     # Você precisará de mais um campo no formulário para isso!
        #     start_vertex = request.form.get('start_vertex', 'a') # 'a' como padrão
        #     result = prim_mst(graph, start_vertex)
        # elif algo == 'bellman_ford':
        #     start_vertex = request.form.get('start_vertex', 'a') # 'a' como padrão
        #     result = bellman_ford(graph, start_vertex)
        # elif algo == 'floyd_warshall':
        #     result = floyd_warshall(graph)
        # -----------------------------------------------------------

        # 4. (SIMULAÇÃO) Apenas para demonstração
        result_message = f"Executando {algo} em {filepath}..."
        print(result_message)
        
        # 5. Renderizar a página de resultados
        # Você pode passar o 'result' real para o template
        return render_template('results.html', 
                               title=f"Resultado de {algo}", 
                               result_data=result_message)

    except Exception as e:
        return f"Ocorreu um erro interno: {e}", 500


if __name__ == '__main__':
    app.run(debug=True) # debug=True recarrega o servidor a cada mudança