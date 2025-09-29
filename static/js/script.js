// Gerencia a interatividade da interface, captura os inputs e comunica-se com o backend.

// Alterna a visualização entre as abas de "Texto" e "Arquivo".
function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    document.querySelectorAll('.tab-button').forEach(button => button.classList.remove('active'));
    event.currentTarget.classList.add('active');
}

// Mostra o nome do arquivo selecionado na interface.
document.getElementById('file-input').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Nenhum arquivo selecionado';
    document.getElementById('file-name').textContent = fileName;
});

// Evento principal: acionado ao clicar no botão "Analisar Email".
document.getElementById('analyze-btn').addEventListener('click', async function() {
    const emailText = document.getElementById('email-text').value;
    const fileInput = document.getElementById('file-input');
    let content = '';

    // Determina se o input é texto direto ou um arquivo da outra aba.
    if (document.getElementById('text-tab').classList.contains('active')) {
        content = emailText;
    } else {
        if (fileInput.files.length === 0) {
            showError('Por favor, selecione um arquivo');
            return;
        }
        const file = fileInput.files[0];
        if (file.type === 'text/plain') {
            content = await readTextFile(file);
        } else {
            content = `Arquivo: ${file.name} - Processamento de PDF não implementado`;
        }
    }

    if (!content.trim()) {
        showError('Por favor, insira o conteúdo do email');
        return;
    }
    
    analyzeEmail(content);
});

// Envia o conteúdo para o backend via API fetch e exibe o resultado.
async function analyzeEmail(content) {
    showLoading();
    hideError();
    hideResults();
    
    try {
        // Ponto de comunicação com o servidor Flask.
        const response = await fetch('/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: content })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro desconhecido na análise');
        }
        
        showResults(data);
        
    } catch (error) {
        showError(error.message);
    }
}

// --- Funções Auxiliares para Manipular a Interface (UI) ---

function showResults(data) {
    hideLoading();
    const resultsDiv = document.getElementById('results');
    const classificationSpan = document.getElementById('classification');
    const responseDiv = document.getElementById('suggested-response');
    
    classificationSpan.textContent = data.classification;
    classificationSpan.className = `classification-badge ${data.classification.toLowerCase()}`;
    responseDiv.textContent = data.response;
    
    resultsDiv.classList.remove('hidden');
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showError(message) {
    hideLoading();
    const errorDiv = document.getElementById('error');
    document.getElementById('error-message').textContent = message;
    errorDiv.classList.remove('hidden');
    console.error('Erro na aplicação:', message);
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

// Utilitário para ler o conteúdo de um arquivo .txt usando a API FileReader.
function readTextFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = e => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

// Copia o texto da resposta para a área de transferência do usuário.
document.getElementById('copy-btn').addEventListener('click', function() {
    const responseText = document.getElementById('suggested-response').textContent;
    navigator.clipboard.writeText(responseText).then(() => {
        const button = this;
        const originalContent = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copiado!';
        setTimeout(() => {
            button.innerHTML = originalContent;
        }, 2000);
    });
});

// Limpa a interface para uma nova análise.
document.getElementById('new-analysis').addEventListener('click', function() {
    document.getElementById('email-text').value = '';
    document.getElementById('file-input').value = '';
    document.getElementById('file-name').textContent = '';
    hideResults();
    hideError();
});