# Flask Web App Starter

A Flask starter template as per [these docs](https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application).

## Getting Started

Previews should run automatically when starting a workspace.

## Clonar o repositório

```bash
git clone https://github.com/Elildes/grafos-minimos.git
cd grafos-minimos
```


## Criar um ambiente virtual

```bash
python -m venv venv
```

## Ativar o ambiente virtual (Windows)

```bash
venv\Scripts\activate
```

## Ativar o ambiente virtual (Linux/macOS)

```bash
source venv/bin/activate
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar a aplicação web (Linux)

```bash
./devserver.sh
```

## Estrutura do projeto


```
| 
|-- main.py             # Ponto de entrada do programa  
|-- README.md           # Descrição do projeto e instruções de uso  
|-- devserver.sh        # Script para executar a aplicação
|-- requirements.txt    # Lista de dependências do projeto  
|  
|-- /src 
|   |-- index.html 
|   |-- init.py  
|   |-- graph.py        # Módulo para representação do grafo  
|   |-- dot_parser.py   # Módulo para ler e interpretar arquivos DOT  
|   |  
|   |-- /algorithms  
|   |-- init.py  
|   |-- prim.py             # Implementação do Algoritmo de Prim  
|   |-- bellman_ford.py     # Implementação do Algoritmo de Bellman-Ford  
|   |-- floyd_warshall.py   # Implementação do Algoritmo de Floyd-Warshall  
|   |-- heap.py             # Implementação da estrutura de heap binário  
|
|-- /tests  
|   |-- test_graph.py  
|   |-- test_prim.py  
|   |-- test_bellman_ford.py  
|   |-- test_floyd_warshall.py  
|  
|-- /examples  
    |-- grafo_nao_direcionado.dot
    |-- grafo_direcionado.dot
```
