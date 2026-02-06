# MailTriage 🚀

**Aplicação web de alta performance que utiliza a API da Groq e o modelo Llama 3.1 para classificar e-mails e gerar respostas inteligentes em tempo real.**

Projeto desenvolvido para o desafio prático do processo seletivo da **AutoU**.

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Tecnologia](https://img.shields.io/badge/Backend-Python%20%7C%20Flask-blue)
![IA](https://img.shields.io/badge/IA-Groq%20%7C%20Llama%203.1-blueviolet)

---

## 📝 Visão Geral

O MailTriage foi projetado para resolver o problema de alto volume de e-mails em ambientes corporativos. A aplicação utiliza o poder do modelo de linguagem **Llama 3.1**, servido através da **API de alta velocidade da Groq**, para analisar o conteúdo de um e-mail, classificá-lo como **Produtivo** (requer ação) ou **Improdutivo** (não requer ação), e gerar uma resposta dinâmica e contextual em tempo real. A arquitetura é modular e otimizada para performance e manutenibilidade.

---

## ✨ Funcionalidades Principais

* **Análise Inteligente com Llama 3.1:** Utiliza um dos modelos de linguagem mais avançados para entender a intenção e o contexto de cada e-mail.
* **Respostas Dinâmicas e Contextuais:** Gera sugestões de resposta únicas e apropriadas para cada e-mail, ao contrário de respostas fixas.
* **Alta Performance com Groq:** As respostas da IA são geradas em uma fração de segundo, proporcionando uma experiência de usuário fluida e instantânea.
* **Interface Web Moderna:** Frontend intuitivo com feedback visual claro (loading/error) e ações úteis como "Copiar Resposta" e "Nova Análise".

---

## 🧠 Arquitetura e Fluxo de Análise

O projeto foi construído com uma arquitetura de software moderna, focada na separação de responsabilidades.

### Estrutura Modular
O código foi organizado para garantir a clareza e a escalabilidade:
* `app.py`: Controla as rotas da web com Flask e serve como o ponto de entrada da aplicação.
* `utils/ai_classifier.py`: Centraliza toda a lógica de comunicação com a API da Groq, incluindo a construção do prompt e o tratamento da resposta da IA.

### Fluxo de Análise com IA
Para cada e-mail, o sistema segue um fluxo direto e eficiente:

1.  **Entrada do Usuário** (Texto do e-mail).
2.  **Chamada à API da Groq:** O `app.py` envia o texto para a função em `ai_classifier.py`.
3.  **Processamento pelo Llama 3.1:** O modelo analisa o texto e gera um objeto JSON contendo tanto a `classification` quanto a `suggestion`.
4.  **Exibição do Resultado:** O frontend recebe o JSON e exibe os resultados de forma organizada para o usuário.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * Python 3.11+
    * Flask (Servidor Web)
    * Gunicorn (Servidor WSGI para produção)
    * python-dotenv (Gerenciamento de variáveis de ambiente)
    * Groq SDK

* **Frontend:**
    * HTML5, CSS3, JavaScript

* **Inteligência Artificial:**
    * **Groq Cloud API**
    * **Modelo:** `llama-3.1-8b-instant`
---

## ▶️ Como Executar Localmente

Siga os passos abaixo para rodar o projeto no seu ambiente.

**Pré-requisitos:**
* Python 3.11+
* Uma chave de API da [Groq](https://console.groq.com/keys)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/](https://github.com/)[SEU-USUARIO]/[SEU-REPOSITORIO].git
    cd [SEU-REPOSITORIO]
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # .\\venv\\Scripts\\activate  # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua chave de API:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Dentro dele, adicione sua chave da Groq:
        ```env
        GROQ_API_KEY="gsk_SUA_CHAVE_AQUI"
        ```

5.  **Inicie o servidor local:**
    ```bash
    python app.py
    ```

6.  **Acesse a aplicação:**
    * Abra seu navegador e acesse `http://127.0.0.1:5000`

---

## 📜 Licença

Este projeto está sob a licença MIT.

---
Desenvolvido por **Cicero Guilherme Gonzaga Silvestre**
