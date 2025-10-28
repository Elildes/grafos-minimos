/**
 * Busca a lista de grafos disponíveis no servidor.
 * @returns {Promise<Object>} Uma promessa que resolve para o objeto { graphs: [], digraphs: [] }.
 */
export async function fetchAvailableGraphs() {
    try {
        const response = await fetch('/api/get-graphs');
        if (!response.ok) {
            throw new Error(`Erro de rede: ${response.statusText}`);
        }
        const data = await response.json();
        
        // --- NOSSO DEBUG ---
        console.log("DADOS EXATOS RECEBIDOS DA API:", JSON.stringify(data));
        // --- FIM DO DEBUG ---
        
        return data;

    } catch (error) {
        console.error('Erro ao buscar lista de grafos:', error);
        // Retorna um objeto vazio em caso de falha para a UI não quebrar
        return { graphs: [], digraphs: [] };
    }
}