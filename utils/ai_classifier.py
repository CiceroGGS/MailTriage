"""
Módulo responsável por toda a interação com a Inteligência Artificial.
Ele contém a lógica para se comunicar com a API da Groq e processar a resposta.
"""
import os
import json
from groq import Groq

# Configura o cliente da API da Groq usando a chave do arquivo .env
# Este bloco é executado apenas uma vez, quando a aplicação inicia.
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    if not os.getenv("GROQ_API_KEY"):
        print("AVISO: A variável de ambiente GROQ_API_KEY não foi configurada.")
except Exception as e:
    print(f"Erro ao configurar a API da Groq: {e}")

def analyze_email_with_groq(email_content: str) -> dict:
    """
    Analisa um e-mail usando o modelo Llama 3 via Groq.

    Esta função envia o texto do e-mail para a IA e espera um objeto JSON
    de volta com a classificação e uma sugestão de resposta.

    Args:
        email_content: O texto do e-mail a ser analisado.

    Returns:
        Um dicionário contendo 'classification' e 'response'.
    """
    try:
        # Este é um prompt "Few-Shot". Damos exemplos para a IA "aprender"
        # o formato exato da resposta que queremos, tornando-a mais confiável.
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

        # Faz a chamada para a API da Groq
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Modelo de linguagem utilizado
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
            temperature=0.7,  # Controla a "criatividade" da IA
            response_format={"type": "json_object"}  # Garante que a resposta será um JSON
        )
        
        # Extrai o conteúdo da resposta e o converte de texto para um objeto Python
        response_content = chat_completion.choices[0].message.content
        result_json = json.loads(response_content)

        # Retorna um dicionário limpo para o app.py, com valores padrão para segurança
        return {
            'classification': result_json.get('classification', 'Não identificado'),
            'response': result_json.get('suggestion', 'Não foi possível gerar uma sugestão.')
        }

    except Exception as e:
        # Se a API falhar, registra o erro e retorna uma mensagem de falha
        print(f"Erro no processamento com Groq: {e}")
        return {
            'classification': 'Erro',
            'response': 'Falha ao se comunicar com a IA.'
        }