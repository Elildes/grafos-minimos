# app.py

import os
import sys
import json
from flask import Flask, render_template, jsonify, request

# --- Configuração de Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Importe suas funções de algoritmo
# ----------------------------------------------------
from src.algorithms.prim import prim_mst
from src.algorithms.bellman_ford import bellman_ford 
from src.algorithms.floyd_warshall import floyd_warshall
from src.dot_parser import parse_dot

app = Flask(__name__)

# --- Constantes de Pastas ---
GRAPH_DIR = os.path.join(BASE_DIR, 'graphs')
DIGRAPH_DIR = os.path.join(BASE_DIR, 'digraphs')


def get_available_graphs():
    """Lê os diretórios e retorna os arquivos .dot ou .gv"""
    graphs = []
    digraphs = []
    
    # Tenta ler a pasta de grafos não direcionados
    try:
        graphs = [f for f in os.listdir(GRAPH_DIR) if f.endswith('.dot') or f.endswith('.gv')]
    except FileNotFoundError:
        print(f"Aviso: Diretório '{GRAPH_DIR}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler GRAPH_DIR: {e}")

    # Tenta ler a pasta de grafos direcionados
    try:
        digraphs = [f for f in os.listdir(DIGRAPH_DIR) if f.endswith('.dot') or f.endswith('.gv')]
    except FileNotFoundError:
        print(f"Aviso: Diretório '{DIGRAPH_DIR}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler DIGRAPH_DIR: {e}")
        
    return graphs, digraphs


@app.route('/')
def index():
    """Renderiza a página inicial (seleção de algoritmo)."""
    return render_template('index.html')


@app.route('/api/get-graphs', methods=['GET'])
def api_get_graphs():
    """API endpoint para o JavaScript buscar os arquivos de grafo."""
    graphs, digraphs = get_available_graphs()
    return jsonify({
        'graphs': graphs,
        'digraphs': digraphs
    })

@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    try:
        # 1. Obter dados do JSON enviado pelo JavaScript
        data = request.get_json()
        
        # 2. Ler os dados do dicionário 'data'
        filename = data.get('graph_file')
        algo = data.get('algorithm')
        graph_type = data.get('graph_type')
        start_vertex = data.get('start_vertex') # Pode ser string vazia
        
        # Limpa o vértice inicial se for uma string vazia
        if not start_vertex:
            start_vertex = None

        if not filename or not algo:
            return render_template('results.html', success=False, error="Nome do arquivo ou algoritmo faltando."), 400

        # 3. Encontrar o caminho do arquivo e carregar o grafo
        if graph_type == 'directed':
            filepath = os.path.join(DIGRAPH_DIR, filename)
        else:
            filepath = os.path.join(GRAPH_DIR, filename)

        if not os.path.exists(filepath):
            return render_template('results.html', success=False, error=f"Arquivo não encontrado: {filename}"), 404

        graph = parse_dot(filepath)

        # --- 4. Executar o algoritmo selecionado ---
        
        if algo == 'prim':
            if not start_vertex:
                return render_template('results.html', success=False, algorithm='Prim', error="Vértice inicial não fornecido para o Prim.")
            
            # Chama o algoritmo
            context = prim_mst(graph, start_vertex)
            
            # Adiciona informações extras ao contexto para o template
            context['algorithm'] = 'Prim'
            context['filename'] = filename
            context['start_vertex'] = start_vertex
            return render_template('results.html', **context)
        
        elif algo == 'bellman_ford':
            if not start_vertex:
                return render_template('results.html', success=False, algorithm='Bellman-Ford', error="Vértice inicial não fornecido para o Bellman-Ford.")
            
            # Chama o algoritmo
            context = bellman_ford(graph, start_vertex)
            
            # Adiciona informações extras ao contexto
            context['filename'] = filename
            # (bellman_ford já adiciona 'algorithm' e 'start_vertex' ao context)
            return render_template('results.html', **context)
        
        elif algo == 'floyd_warshall':

            # Chama o algoritmo
            context = floyd_warshall(graph)

            print(context)

            # Adiciona informações extras ao contexto
            context['filename'] = filename
            context['algorithm'] = 'Floyd-Warshall'

            return render_template('results.html', **context)
        else:
             return render_template('results.html', success=False, error=f"Erro: Algoritmo '{algo}' desconhecido."), 400
        # -----------------------------------------------------------

    except FileNotFoundError:
        return render_template('results.html', success=False, error=f"Erro: O arquivo .dot não foi encontrado."), 404
    except ValueError as ve:
        # Erros de parsing do dot_parser ou outros erros de valor
        return render_template('results.html', success=False, error=f"Erro de Valor (ex: parsing): {ve}"), 400
    except Exception as e:
        print(f"Ocorreu um erro interno: {e}")
        # Pega a linha do erro para debug
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] # type: ignore
        error_details = f"Erro interno: {e} (em {fname}, linha {exc_tb.tb_lineno})" # type: ignore
        return render_template('results.html', success=False, error=error_details), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)