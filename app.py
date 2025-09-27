from flask import Flask, render_template, request, jsonify
from utils.email_processor import process_email
from utils.ai_classifier import classify_email, generate_response
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    try:
        # Obter o conteúdo do email de forma mais robusta
        email_content = ""
        
        print("Recebendo requisição...")  # Debug
        
        # Verificar se é upload de arquivo
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                print(f"Processando arquivo: {file.filename}")  # Debug
                if file.filename.endswith('.txt'):
                    email_content = file.read().decode('utf-8')
                elif file.filename.endswith('.pdf'):
                    email_content = "Arquivo PDF - conteúdo será processado em breve"
                else:
                    return jsonify({'error': 'Formato de arquivo não suportado'}), 400
        # Verificar se é texto direto (JSON)
        elif request.is_json:
            data = request.get_json()
            email_content = data.get('text', '')
            print(f"Texto recebido: {email_content[:100]}...")  # Debug
        else:
            # Tentar obter de form-data
            email_content = request.form.get('text', '')
        
        print(f"Conteúdo do email: {len(email_content)} caracteres")  # Debug
        
        if not email_content or not email_content.strip():
            return jsonify({'error': 'Nenhum conteúdo de email fornecido'}), 400
        
        # Processar e classificar o email
        processed_text = process_email(email_content)
        classification = classify_email(email_content)  # Usar texto original para melhor análise
        response = generate_response(email_content, classification)
        
        return jsonify({
            'classification': classification,
            'response': response,
            'debug': {
                'processed_length': len(processed_text),
                'original_length': len(email_content)
            }
        })
        
    except Exception as e:
        print(f"Erro no processamento: {e}")
        import traceback
        print(traceback.format_exc())  # Debug detalhado
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)