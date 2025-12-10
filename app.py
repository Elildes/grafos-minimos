import os
import sys
import json
from flask import Flask, render_template, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Funções necessárias
# ----------------------------------------------------
from src.algorithms.dsatur_algorithm import dsatur
from src.dot_parser import parse_dot

app = Flask(__name__)

# Diretórios com grafos (pode manter apenas 1 se quiser)
GRAPH_DIR = os.path.join(BASE_DIR, 'graphs')


def get_available_graphs():
    """Lista arquivos .dot ou .gv disponíveis."""
    try:
        return [
            f for f in os.listdir(GRAPH_DIR)
            if f.endswith('.dot') or f.endswith('.gv')
        ]
    except Exception:
        return []


@app.route('/')
def index():
    """Página inicial."""
    return render_template('index.html')


@app.route('/api/get-graphs', methods=['GET'])
def api_get_graphs():
    """Fornece a lista de grafos para o frontend."""
    graphs = get_available_graphs()
    return jsonify({'graphs': graphs})


@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    try:
        data = request.form

        filename = data.get('graph_file')
        if not filename:
            return render_template(
                'results.html',
                success=False,
                error="Arquivo de grafo não informado."
            ), 400

        # Caminho completo
        filepath = os.path.join(GRAPH_DIR, filename)

        if not os.path.exists(filepath):
            return render_template(
                'results.html',
                success=False,
                error=f"Arquivo não encontrado: {filename}"
            ), 404

        # Parseia o arquivo DOT/Graphviz
        graph = parse_dot(filepath)

        # Executa DSATUR
        context = dsatur(graph)
        context['algorithm'] = 'DSATUR'
        context['filename'] = filename

        return render_template('results.html', **context)

    except Exception as e:
        print(f"Erro interno: {e}")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_details = f"Erro interno: {e} (em {fname}, linha {exc_tb.tb_lineno})"
        return render_template('results.html', success=False, error=error_details), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
