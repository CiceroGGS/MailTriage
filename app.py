from flask import Flask, render_template, request, jsonify
from utils.ai_classifier import analyze_email_with_groq # Importa a nova função
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        email_content = data.get('text', '')
        
        if not email_content.strip():
            return jsonify({'error': 'Nenhum conteúdo de email fornecido'}), 400
        
        result = analyze_email_with_groq(email_content)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Erro inesperado no servidor: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Ocorreu um erro interno no servidor.'}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)