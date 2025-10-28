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

Depois clicar no link que aparecerá no terminal ou digitar no navehagor [http://127.0.0.1:8080](http://127.0.0.1:8080).  

**Obs.:** o comando `./devserver.sh` é usado somente em modo `desenvolvedor`, não use ele no modo de `produção`.  

## Estrutura do projeto


```
|
|-- /digraphs           # Armazena os grafos direcionados
|   |-- digraph01.dot
|  
|-- /graphs             # Armazena os grafos não direcionados
|    |-- graph01.dot
|  
|-- /src
|   |-- init.py  
|   |-- graph.py        # Módulo para representação do grafo  
|   |-- dot_parser.py   # Módulo para ler e interpretar arquivos DOT  
|   |  
|   |-- /algorithms  
|       |-- init.py  
|       |-- prim.py             # Implementação do Algoritmo de Prim  
|       |-- bellman_ford.py     # Implementação do Algoritmo de Bellman-Ford  
|       |-- floyd_warshall.py   # Implementação do Algoritmo de Floyd-Warshall  
|       |-- heap.py             # Implementação da estrutura de heap binário  
|
|-- /static             # Pasta padrão do Flask para arquivos estáticos
|   |-- /css
|       |-- styles.css  # Estilos css
|
|-- /templates  
|   |-- index.html                # Pagina inicial
|   |-- templates/results.html    # Mostra resultados do servidor
|
|-- app.py              # Servidor API da aplicação
|-- devserver.sh        # Script para executar a aplicação
|-- README.md           # Descrição do projeto e instruções de uso  
|-- requirements.txt    # Lista de dependências do projeto  
```
