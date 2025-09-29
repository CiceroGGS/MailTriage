# Módulo para interagir com a API de Inteligência Artificial da Groq.
import os
import json
from groq import Groq

# Configura o cliente da API da Groq na inicialização do app
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    if not os.getenv("GROQ_API_KEY"):
        print("AVISO: A variável de ambiente GROQ_API_KEY não foi configurada.")
except Exception as e:
    print(f"Erro ao configurar a API da Groq: {e}")

def analyze_email_with_groq(email_content: str) -> dict:
    """Analisa um e-mail usando o modelo Llama 3 via Groq, retornando um JSON estruturado."""
    try:
        # Prompt aprimorado com exemplos ("Few-Shot") para garantir a precisão do formato
        prompt = f'''
Você é um assistente de IA especialista em análise de e-mails. Sua única função é analisar o e-mail de um usuário e retornar um objeto JSON com as chaves "classification" e "suggestion".

Siga os exemplos abaixo para formatar sua resposta.

# Exemplo 1:
[E-MAIL DO USUÁRIO]
Olá, estou com um problema para acessar minha conta, poderiam me ajudar?
[OBJETO JSON DE SAÍDA]
{{
  "classification": "Produtivo",
  "suggestion": "Olá! Agradecemos por relatar o problema. Nossa equipe de suporte técnico já está investigando o caso e retornará em breve. Atenciosamente."
}}

# Exemplo 2:
[E-MAIL DO USUÁRIO]
Muito obrigado pela ajuda de ontem! Foi ótimo.
[OBJETO JSON DE SAÍDA]
{{
  "classification": "Improdutivo",
  "suggestion": "Olá! Ficamos felizes em poder ajudar. Agradecemos o seu contato e desejamos um ótimo dia!"
}}

---

# TAREFA ATUAL:

Agora, analise o seguinte e-mail e gere o objeto JSON de saída correspondente.

[E-MAIL DO USUÁRIO]
{email_content}
[OBJETO JSON DE SAÍDA]
'''

        # Faz a chamada para a API, solicitando o formato JSON na resposta
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Siga estritamente as instruções e os exemplos para retornar um objeto JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        response_content = chat_completion.choices[0].message.content
        result_json = json.loads(response_content)

        return {
            'classification': result_json.get('classification', 'Não identificado'),
            'response': result_json.get('suggestion', 'Não foi possível gerar uma sugestão.')
        }

    except Exception as e:
        # Em caso de falha na API, retorna uma resposta de erro padronizada
        print(f"Erro no processamento com Groq: {e}")
        return {
            'classification': 'Erro',
            'response': 'Falha ao se comunicar com a IA.'
        }