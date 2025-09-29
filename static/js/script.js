/**
 * Gerencia a navegação por abas, mostrando o conteúdo correto (Texto ou Arquivo)
 * e destacando o botão da aba ativa.
 * @param {string} tabName - O ID do conteúdo da aba a ser exibida.
 */
function openTab(tabName) {
    // Esconde todos os painéis de conteúdo
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    // Remove o destaque de todos os botões
    document.querySelectorAll('.tab-button').forEach(button => button.classList.remove('active'));
    
    // Mostra o painel de conteúdo selecionado
    document.getElementById(tabName).classList.add('active');
    // Adiciona o destaque no botão clicado
    event.currentTarget.classList.add('active');
}

// Escuta por mudanças no input de arquivo para mostrar o nome do arquivo selecionado na tela.
document.getElementById('file-input').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Nenhum arquivo selecionado';
    document.getElementById('file-name').textContent = fileName;
});

// Evento principal: é acionado quando o usuário clica no botão "Analisar Email".
document.getElementById('analyze-btn').addEventListener('click', async function() {
    const emailText = document.getElementById('email-text').value;
    const fileInput = document.getElementById('file-input');
    let content = '';

    // Verifica qual aba está ativa para determinar de onde pegar o conteúdo.
    if (document.getElementById('text-tab').classList.contains('active')) {
        content = emailText;
    } else {
        // Se a aba de arquivo estiver ativa, processa o arquivo.
        if (fileInput.files.length === 0) {
            showError('Por favor, selecione um arquivo');
            return;
        }
        const file = fileInput.files[0];
        // Por enquanto, só lemos arquivos .txt. Outros tipos mostram uma mensagem.
        if (file.type === 'text/plain') {
            content = await readTextFile(file);
        } else {
            // Placeholder para futuras implementações, como PDF.
            content = `Arquivo: ${file.name} - Processamento de PDF não implementado`;
        }
    }

    // Validação final para garantir que há texto para ser analisado.
    if (!content.trim()) {
        showError('Por favor, insira o conteúdo do email');
        return;
    }
    
    // Se tudo estiver certo, chama a função que se comunica com o backend.
    analyzeEmail(content);
});

/**
 * Envia o conteúdo do e-mail para o backend Flask e processa a resposta.
 * @param {string} content - O texto do e-mail a ser analisado.
 */
async function analyzeEmail(content) {
    showLoading(); // Mostra a animação de "Analisando..."
    hideError();   // Esconde qualquer erro anterior
    hideResults(); // Esconde qualquer resultado anterior
    
    try {
        // Envia a requisição para a rota '/classify' do nosso servidor Python.
        const response = await fetch('/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // Converte o texto para o formato JSON que o backend espera.
            body: JSON.stringify({ text: content })
        });
        
        const data = await response.json();
        
        // Se a resposta do servidor indicar um erro (ex: 400 ou 500), lança um erro.
        if (!response.ok) {
            throw new Error(data.error || 'Erro desconhecido na análise');
        }
        
        // Se a requisição foi um sucesso, exibe os resultados na tela.
        showResults(data);
        
    } catch (error) {
        // Se ocorrer qualquer erro na comunicação, mostra a mensagem de erro para o usuário.
        showError(error.message);
    }
}

// --- Funções Auxiliares para Manipular a Interface (UI) ---

/** Mostra o card de resultados e preenche com os dados da IA. */
function showResults(data) {
    hideLoading();
    const resultsDiv = document.getElementById('results');
    const classificationSpan = document.getElementById('classification');
    const responseDiv = document.getElementById('suggested-response');
    
    classificationSpan.textContent = data.classification;
    // Adiciona uma classe CSS para colorir a tag (ex: 'produtivo' fica verde).
    classificationSpan.className = `classification-badge ${data.classification.toLowerCase()}`;
    responseDiv.textContent = data.response;
    
    resultsDiv.classList.remove('hidden');
}

/** Ativa a visualização do spinner de carregamento. */
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

/** Esconde o spinner de carregamento. */
function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

/** Mostra uma mensagem de erro na tela. */
function showError(message) {
    hideLoading();
    const errorDiv = document.getElementById('error');
    document.getElementById('error-message').textContent = message;
    errorDiv.classList.remove('hidden');
    // Também registra o erro no console do navegador para depuração.
    console.error('Erro na aplicação:', message);
}

/** Esconde a caixa de erro. */
function hideError() {
    document.getElementById('error').classList.add('hidden');
}

/** Esconde a caixa de resultados. */
function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

/**
 * Lê o conteúdo de um arquivo de texto local usando a API FileReader do navegador.
 * @param {File} file - O objeto do arquivo selecionado pelo usuário.
 * @returns {Promise<string>} O conteúdo do arquivo como texto.
 */
function readTextFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = e => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

// Adiciona a funcionalidade de "Copiar para a Área de Transferência" ao botão.
document.getElementById('copy-btn').addEventListener('click', function() {
    const responseText = document.getElementById('suggested-response').textContent;
    // Usa a API do navegador para copiar o texto.
    navigator.clipboard.writeText(responseText).then(() => {
        const button = this;
        const originalContent = button.innerHTML;
        // Fornece feedback visual de que o texto foi copiado.
        button.innerHTML = '<i class="fas fa-check"></i> Copiado!';
        // Volta ao normal depois de 2 segundos.
        setTimeout(() => {
            button.innerHTML = originalContent;
        }, 2000);
    });
});

// Adiciona a funcionalidade de "Nova Análise" para limpar a tela e começar de novo.
document.getElementById('new-analysis').addEventListener('click', function() {
    document.getElementById('email-text').value = '';
    document.getElementById('file-input').value = '';
    document.getElementById('file-name').textContent = '';
    hideResults();
    hideError();
});