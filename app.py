# app.py
import os
import json
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# --- CARREGANDO O MODELO DE IA LOCALMENTE ---
try:
    print("Carregando o modelo de IA... Isso pode levar um momento.")
    classifier = pipeline("text2text-generation", model="t5-small")
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    classifier = None
# ---------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if not classifier:
        return jsonify({'error': 'Modelo de IA não foi carregado corretamente.'}), 500

    data = request.get_json()
    email_text = data.get('email_text', '')

    if not email_text:
        return jsonify({'error': 'Nenhum texto de email fornecido.'}), 400

    try:
        # --- PROMPT MELHORADO COM EXEMPLOS (FEW-SHOT) ---
        prompt = f"""
        task: Classify the email as "Produtivo" or "Improdutivo" and suggest a short professional response in Portuguese.
        format: CLASSIFICATION: [category] | SUGGESTION: [response]

        example 1:
        email text: "Olá, poderiam me ajudar com o problema no sistema?"
        output: CLASSIFICATION: Produtivo | SUGGESTION: Olá! Recebemos sua solicitação de suporte e nossa equipe irá verificar o problema em breve. Atenciosamente.

        example 2:
        email text: "Obrigado por tudo!"
        output: CLASSIFICATION: Improdutivo | SUGGESTION: Olá! Agradecemos o seu contato. Atenciosamente.

        ---

        Now, complete the following:
        email text: "{email_text}"
        output:
        """

        result = classifier(prompt, max_length=150, min_length=20, do_sample=False)
        generated_text = result[0]['generated_text']
        
        # --- LÓGICA DE EXTRAÇÃO MAIS ROBUSTA ---
        # Procura pelos marcadores no texto gerado
        class_marker = "CLASSIFICATION:"
        sugg_marker = "SUGGESTION:"
        
        class_start_index = generated_text.find(class_marker)
        sugg_start_index = generated_text.find(sugg_marker)

        # Se ambos os marcadores forem encontrados, extrai o conteúdo
        if class_start_index != -1 and sugg_start_index != -1:
            class_end_index = generated_text.find("|", class_start_index)
            classification = generated_text[class_start_index + len(class_marker) : class_end_index].strip()
            suggestion = generated_text[sugg_start_index + len(sugg_marker) :].strip()
        else:
            # Se o formato não for seguido, define um resultado padrão para evitar erros
            classification = "Não identificado"
            suggestion = "Não foi possível gerar uma sugestão."
        
        result_json = {
            "classification": classification,
            "suggestion": suggestion
        }

        return jsonify(result_json)

    except Exception as e:
        print(f"Erro ao processar o texto: {e}")
        return jsonify({'error': 'Falha ao processar o e-mail com a IA local.'}), 500

if __name__ == '__main__':
    app.run(debug=True)