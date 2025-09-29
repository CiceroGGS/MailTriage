function openTab(tabName) {
    // Esconder todas as tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostrar tab selecionada
    document.getElementById(tabName).classList.add('active');
    
    // Atualizar botões das tabs
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}
console.log('Script carregado - iniciando aplicação');

document.getElementById('file-input').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Nenhum arquivo selecionado';
    document.getElementById('file-name').textContent = fileName;
});

document.getElementById('analyze-btn').addEventListener('click', async function() {
    const emailText = document.getElementById('email-text').value;
    const fileInput = document.getElementById('file-input');
    
    let content = '';
    
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
            content = `Arquivo: ${file.name} - Processamento de PDF será implementado`;
        }
    }
    
    if (!content.trim()) {
        showError('Por favor, insira o conteúdo do email');
        return;
    }
    
    analyzeEmail(content);
});

async function analyzeEmail(content) {
    showLoading();
    hideError();
    hideResults();
    
    try {
        const response = await fetch('/classify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: content })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro na análise');
        }
        
        showResults(data);
        
    } catch (error) {
        showError(error.message);
    }
}

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

function readTextFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = e => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

document.getElementById('copy-btn').addEventListener('click', function() {
    const response = document.getElementById('suggested-response').textContent;
    navigator.clipboard.writeText(response).then(() => {
        const originalText = this.innerHTML;
        this.innerHTML = '<i class="fas fa-check"></i> Copiado!';
        setTimeout(() => {
            this.innerHTML = originalText;
        }, 2000);
    });
});

// Nova análise
document.getElementById('new-analysis').addEventListener('click', function() {
    document.getElementById('email-text').value = '';
    document.getElementById('file-input').value = '';
    document.getElementById('file-name').textContent = '';
    hideResults();
    hideError();
});