# Ponto de entrada da aplicação Flask. Gerencia as rotas e orquestra as chamadas.
from flask import Flask, render_template, request, jsonify
from utils.ai_classifier import analyze_email_with_groq
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF para leitura de PDFs

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    """Recebe o e-mail (texto ou arquivo), chama a IA e retorna a análise."""
    try:
        email_content = ""
        
        # Lida com upload de arquivos (.txt e .pdf)
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            
            if file.filename.endswith('.txt'):
                email_content = file.read().decode('utf-8')
            
            elif file.filename.endswith('.pdf'):
                pdf_document = fitz.open(stream=file.read(), filetype="pdf")
                for page in pdf_document:
                    email_content += page.get_text()
                pdf_document.close()
            else:
                return jsonify({'error': 'Formato de arquivo não suportado. Use .txt ou .pdf'}), 400
        
        # Lida com input de texto direto via JSON
        elif request.is_json:
            data = request.get_json()
            email_content = data.get('text', '')
        
        if not email_content.strip():
            return jsonify({'error': 'Nenhum conteúdo de email fornecido'}), 400
        
        # Chama o módulo de IA
        result = analyze_email_with_groq(email_content)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Erro inesperado no servidor: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Ocorreu um erro interno no servidor.'}), 500

# Inicia o servidor de desenvolvimento
if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)