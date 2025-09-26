from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    email_text = data.get('email_text', '')

    if not email_text:
        return jsonify({'error': 'Nenhum texto de email fornecido.'}), 400

    # Logica temporaria 

    if "ajuda" in email_text.lower() or "suporte" in email_text.lower():
        classification = "Produtivo"
        suggestion = "Olá,\n\nObrigado por seu contato. Recebemos sua solicitação e nossa equipe irá analisá-la em breve.\n\nAtenciosamente,"
    else:
        classification = "Improdutivo"
        suggestion = "Olá,\n\nObrigado pela sua mensagem!\n\nAtenciosamente,"

    return jsonify({
        'classification': classification,
        'suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True)
