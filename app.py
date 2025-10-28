import os
import sys
import json
from flask import Flask, render_template, jsonify, request

# --- Configuração de Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Importe suas funções de algoritmo
from src.algorithms.prim import prim_mst
# from src.algorithms.bellman_ford import bellman_ford # Mantenha comentado se não implementado
# from src.algorithms.floyd_warshall import floyd_warshall # Mantenha comentado se não implementado
from src.dot_parser import parse_dot

app = Flask(__name__)

# --- Constantes de Pastas ---
GRAPH_DIR = os.path.join(BASE_DIR, 'graphs')
DIGRAPH_DIR = os.path.join(BASE_DIR, 'digraphs')

def get_available_graphs():
    """Lê os diretórios e retorna os arquivos .dot ou .gv"""
    graphs = []
    digraphs = []
    
    print("--- INICIANDO get_available_graphs ---")
    
    # Tenta ler a pasta de grafos não direcionados
    try:
        print(f"Buscando em GRAPH_DIR: {GRAPH_DIR}")
        graphs = [f for f in os.listdir(GRAPH_DIR) if f.endswith('.dot') or f.endswith('.gv')]
        print(f"Arquivos encontrados em graphs: {graphs}")
    except FileNotFoundError:
        print(f"Aviso: Diretório '{GRAPH_DIR}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler GRAPH_DIR: {e}")

    # Tenta ler a pasta de grafos direcionados
    try:
        print(f"Buscando em DIGRAPH_DIR: {DIGRAPH_DIR}")
        digraphs = [f for f in os.listdir(DIGRAPH_DIR) if f.endswith('.dot') or f.endswith('.gv')]
        print(f"Arquivos encontrados em digraphs: {digraphs}")
    except FileNotFoundError:
        print(f"Aviso: Diretório '{DIGRAPH_DIR}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler DIGRAPH_DIR: {e}")

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
        # Vértice inicial é necessário para Prim e Bellman-Ford
        start_vertex = request.form.get('start_vertex')

        if not all([algo, graph_type, filename]):
            return render_template('results.html', title="Erro", result_data="Erro: Faltando parâmetros no formulário (algoritmo, tipo ou nome de arquivo)."), 400

        # 2. Determinar o caminho do arquivo
        base_dir = DIGRAPH_DIR if graph_type == 'directed' else GRAPH_DIR
        filepath = os.path.join(base_dir, filename) # type: ignore

        if not os.path.exists(filepath):
            return render_template('results.html', title="Erro", result_data=f"Erro: Arquivo não encontrado: {filepath}"), 404

        # 3. Chamar o código Python
        # -----------------------------------------------------------
        graph = parse_dot(filepath)
        result = None
        title = f"Resultado de {algo}"

        if algo == 'prim':
            # Validação do vértice inicial
            if not start_vertex:
                return render_template('results.html', title="Erro", result_data="Erro: O Algoritmo de Prim requer um vértice inicial."), 400
            
            # O vértice inicial é passado para a função
            result = prim_mst(graph, start_vertex)
            title = f"Algoritmo de Prim (início: {start_vertex})"
        
        elif algo == 'bellman_ford':
            # (Implementação futura)
            # if not start_vertex:
            #     return render_template('results.html', title="Erro", result_data="Erro: O Algoritmo de Bellman-Ford requer um vértice inicial."), 400
            # result = bellman_ford(graph, start_vertex)
            # title = f"Algoritmo de Bellman-Ford (início: {start_vertex})"
            result = f"Algoritmo {algo} ainda não implementado." # Placeholder
        
        elif algo == 'floyd_warshall':
            # (Implementação futura)
            # result = floyd_warshall(graph)
            # title = "Algoritmo de Floyd-Warshall"
            result = f"Algoritmo {algo} ainda não implementado." # Placeholder
        
        else:
             return render_template('results.html', title="Erro", result_data=f"Erro: Algoritmo '{algo}' desconhecido."), 400
        # -----------------------------------------------------------

        # 4. Formatar e Renderizar a página de resultados
        
        # Converte resultados complexos (como dicts/listas) para JSON formatado
        if isinstance(result, (dict, list)):
            result_data = json.dumps(result, indent=4, ensure_ascii=False)
        else:
            result_data = str(result) # Para mensagens de erro simples

        return render_template('results.html', 
                               title=title, 
                               result_data=result_data,
                               result_dict=result if isinstance(result, dict) else None) # Passa o dict original

    except Exception as e:
        print(f"Ocorreu um erro interno: {e}")
        return render_template('results.html', title="Erro Interno", result_data=f"Ocorreu um erro interno no servidor: {e}"), 500


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 8080)))