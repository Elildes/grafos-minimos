/**
 * Contém toda a lógica de manipulação do formulário
 */

// Importa a função de responsabilidade única do api.js
import { fetchAvailableGraphs } from './api.js';

// --- Variáveis Globais ---
let availableGraphs = {
    graphs: [],
    digraphs: []
};

// --- Referências aos elementos do DOM ---
const algorithmRadios = document.querySelectorAll('input[name="algorithm"]');
const graphTypeRadios = document.querySelectorAll('input[name="graph_type"]');
const typeSelectionDiv = document.getElementById('graph-type-selection');
const fileSelectionDiv = document.getElementById('graph-file-selection');
const fileContainer = document.getElementById('graph-file-container');
const startVertexDiv = document.getElementById('start-vertex-selection');
const startVertexInput = document.getElementById('start-vertex-input');
const submitButton = document.getElementById('submit-button');
const algorithmForm = document.getElementById('algorithm-form');

// --- Definições das Funções de Lógica ---

function handleAlgorithmChange(event) {
    const selectedAlgorithm = event.target.value;
    
    // Reseta as etapas seguintes
    resetStep(2);
    resetStep(3);
    resetStep(4);

    if (selectedAlgorithm === 'prim') {
        // Pula direto para a Etapa 3, forçando "Não Direcionado"
        typeSelectionDiv.style.display = 'none';
        document.getElementById('graph_type_undirected').checked = true;

        // Popula os arquivos da pasta 'graphs' (usa a var global availableGraphs)
        populateGraphFiles('graphs');
        fileSelectionDiv.style.display = 'block';

        // MOSTRA a Etapa 4 (Vértice Inicial)
        startVertexDiv.style.display = 'block';

    } else if (selectedAlgorithm === 'bellman_ford') {
        // Mostra a Etapa 2
        typeSelectionDiv.style.display = 'block';
        
        // MOSTRA a Etapa 4 (Vértice Inicial)
        startVertexDiv.style.display = 'block';

    } else if (selectedAlgorithm === 'floyd_warshall') {
        // Mostra a Etapa 2
        typeSelectionDiv.style.display = 'block';
        
        // OCULTA a Etapa 4 (Vértice Inicial)
        startVertexDiv.style.display = 'none';
    }
}

function handleGraphTypeChange(event) {
    const selectedType = event.target.value; // 'directed' or 'undirected'
    resetStep(3);

    const folder = (selectedType === 'directed') ? 'digraphs' : 'graphs';
    populateGraphFiles(folder);
    fileSelectionDiv.style.display = 'block';
}

/**
 * Popula a lista de seleção de arquivos (Etapa 3)
 */
function populateGraphFiles(folder) {
    const files = availableGraphs[folder]; // Lê da var global
    fileContainer.innerHTML = ''; // Limpa a lista anterior
    
    if (!files || files.length === 0) {
        fileContainer.innerHTML = '<p class="text-danger">Nenhum grafo disponível! Favor criar o grafo</p>';
        submitButton.disabled = true;
    } else {
        const selectList = document.createElement('select');
        selectList.id = 'graph-file-list';
        selectList.name = 'graph_file';
        selectList.className = 'form-select';
        
        const defaultOption = document.createElement('option');
        defaultOption.value = "";
        defaultOption.text = "Selecione um arquivo...";
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectList.appendChild(defaultOption);

        files.forEach(file => {
            const option = document.createElement('option');
            option.value = file;
            option.text = file;
            selectList.appendChild(option);
        });

        selectList.addEventListener('change', () => {
            submitButton.disabled = (selectList.value === "");
        });

        fileContainer.appendChild(selectList);
    }
}

/**
 * Reseta uma etapa do formulário
 */
function resetStep(step) {
    submitButton.disabled = true;

    if (step === 2) {
        typeSelectionDiv.style.display = 'none';
        graphTypeRadios.forEach(radio => radio.checked = false);
    }
    if (step === 3) {
        fileSelectionDiv.style.display = 'none';
        fileContainer.innerHTML = '';
    }
    if (step === 4) { // Reseta a nova etapa
        startVertexDiv.style.display = 'none';
        startVertexInput.value = '';
    }
}


/**
 * Intercepta o envio do formulário, envia os dados como JSON via fetch
 * e exibe a página de resultados.
 */
async function handleFormSubmit(event) {
    // 1. Impede o envio padrão do formulário
    event.preventDefault(); 
    
    // Desabilita o botão para evitar cliques duplos
    submitButton.disabled = true;
    submitButton.textContent = 'Executando...';

    // 2. Coleta os dados do formulário manualmente (Método mais robusto)
    
    // Pega os valores dos campos que sempre existem
    const algorithm = document.querySelector('input[name="algorithm"]:checked').value;
    const startVertex = document.getElementById('start-vertex-input').value;
    
    // Pega os valores dos campos que podem estar ocultos ou dinâmicos
    const graphFileSelect = document.getElementById('graph-file-list');
    const graphTypeRadio = document.querySelector('input[name="graph_type"]:checked');

    // 3. Converte os dados para um objeto JSON
    const data = {
        algorithm: algorithm,
        start_vertex: startVertex,
        // Usa o valor do <select> se ele existir, senão envia null
        graph_file: graphFileSelect ? graphFileSelect.value : null,
        // Usa o valor do radio button se ele estiver checado, senão envia null
        // (Nota: para o Prim, nós o marcamos via JS, então ele será pego aqui)
        graph_type: graphTypeRadio ? graphTypeRadio.value : null
    };

    // Adiciona um log de depuração para vermos o que está sendo enviado
    console.log("Enviando JSON para o servidor:", JSON.stringify(data, null, 2));

    try {
        // 4. Envia os dados como JSON usando fetch
        const response = await fetch(algorithmForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // 5. Pega a resposta. O servidor enviará a página HTML de resultados
        const resultHtml = await response.text();

        // 6. Substitui o conteúdo da página atual pela página de resultados
        document.body.innerHTML = resultHtml;
        
    } catch (error) {
        console.error('Erro ao submeter o formulário:', error);
        alert('Ocorreu um erro ao processar sua solicitação. Verifique o console.');
        submitButton.disabled = false;
        submitButton.textContent = 'Executar Algoritmo';
    }
}


// --- Ponto de Entrada (Main) ---

/**
 * Função principal de inicialização.
 */
async function main() {
    // 1. Adiciona os "ouvintes" de eventos nos botões de rádio
    algorithmRadios.forEach(radio => radio.addEventListener('change', handleAlgorithmChange));
    graphTypeRadios.forEach(radio => radio.addEventListener('change', handleGraphTypeChange));
    
    // 2. ADICIONA O OUVINTE DE SUBMISSÃO DO FORMULÁRIO
    algorithmForm.addEventListener('submit', handleFormSubmit);

    // 3. Busca os dados da API e preenche a var global
    availableGraphs = await fetchAvailableGraphs();
    console.log("Grafos carregados:", availableGraphs);
    
    // 4. (Opcional) Re-popula caso o usuário tenha voltado
    const selectedTypeRadio = document.querySelector('input[name="graph_type"]:checked');
    if (selectedTypeRadio) {
        handleGraphTypeChange({ target: selectedTypeRadio });
    }
}

// Inicia o script quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', main);