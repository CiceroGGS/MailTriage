# MailTriage 🚀

**Aplicação web que utiliza um sistema de IA híbrido para classificar e-mails e sugerir respostas inteligentes, focando em robustez e alta disponibilidade.**

Projeto desenvolvido para o desafio prático do processo seletivo da **AutoU**.

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Tecnologia](https://img.shields.io/badge/Backend-Python%20%7C%20Flask-blue)
![IA](https://img.shields.io/badge/IA-Hugging%20Face%20%7C%20NLTK-orange)

---

## 🔗 Links Rápidos

* **Ver a Aplicação Online:** **[LINK-DA-APLICACAO-ONLINE-AQUI]**
* **Assistir Vídeo de Apresentação:** **[LINK-PARA-O-VIDEO-NO-YOUTUBE-AQUI]**

---

## 🖥️ Demonstração

*(Substitua o link abaixo por um GIF da sua aplicação em funcionamento)*
![Demonstração do MailTriage](https://i.imgur.com/vj5nC14.gif)

---

## 📝 Visão Geral

O MailTriage foi projetado para resolver o problema de alto volume de e-mails em ambientes corporativos. A aplicação analisa o conteúdo de um e-mail, o classifica como **Produtivo** (requer ação) ou **Improdutivo** (não requer ação), e sugere uma resposta apropriada. A principal característica do projeto é sua **arquitetura híbrida e tolerante a falhas**, garantindo que o usuário sempre tenha uma experiência funcional e de alta qualidade.

---

## ✨ Funcionalidades Principais

* **Classificação Híbrida Inteligente:** Utiliza a API do Hugging Face como primeira opção e um sistema robusto de palavras-chave como fallback, garantindo 100% de disponibilidade.
* **Geração de Resposta Dinâmica:** Tenta gerar respostas contextuais com IA e, em caso de falha, recorre a um banco de templates inteligentes para sempre fornecer a melhor sugestão.
* **Pré-processamento de Texto com NLTK:** O texto dos e-mails é limpo, tokenizado e processado para otimizar a análise da IA.
* **Interface Web Moderna:** Frontend intuitivo com suporte para entrada de texto, feedback visual claro (loading/error) e ações úteis como "Copiar Resposta".

---

## 🧠 Arquitetura e Lógica Híbrida

A decisão de engenharia mais importante deste projeto foi a criação de um sistema "fail-safe" (à prova de falhas).

### Estrutura Modular
O código foi organizado em módulos para garantir a separação de responsabilidades e a manutenibilidade:
* `app.py`: Controla as rotas Flask e a interface com o usuário.
* `utils/email_processor.py`: Realiza todo o pré-processamento de texto (limpeza, remoção de stopwords, etc.) usando NLTK.
* `utils/ai_classifier.py`: Contém toda a lógica de classificação e geração de resposta.

### Fluxo de Análise Híbrido
Para cada e-mail, o sistema segue os seguintes passos, garantindo que uma resposta de qualidade seja sempre entregue:

1.  **Entrada do Usuário** (Texto)
2.  **Pré-processamento com `email_processor`**
3.  **Classificação:**
    * **Tentativa 1:** Classificar usando a API Zero-Shot do Hugging Face.
    * **Fallback:** Se a API falhar ou demorar, classificar usando o sistema de palavras-chave.
4.  **Geração da Resposta:**
    * **Tentativa 1:** Gerar resposta dinâmica com a API do Hugging Face, usando o contexto do e-mail.
    * **Fallback:** Se a API falhar, selecionar a melhor resposta de um banco de templates contextuais com base na classificação e no conteúdo.
5.  **Exibição do Resultado** para o usuário.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * Python 3.11+
    * Flask (Servidor Web)
    * Gunicorn (Servidor WSGI para produção)
    * NLTK (Processamento de Linguagem Natural)
    * python-dotenv (Gerenciamento de variáveis de ambiente)

* **Frontend:**
    * HTML5
    * CSS3
    * JavaScript

* **Inteligência Artificial:**
    * Hugging Face Inference API
    * Modelo de Classificação: `facebook/bart-large-mnli`
    * Modelo de Geração: `google/flan-t5-base`

* **DevOps:**
    * Git & GitHub
    * Hospedagem: [EX: Render, Vercel, etc.]

---

## ▶️ Como Executar Localmente

Siga os passos abaixo para rodar o projeto no seu ambiente.

**Pré-requisitos:**
* Python 3.11+
* Uma chave de API (Token) do [Hugging Face](https://huggingface.co/settings/tokens)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    cd SEU-REPOSITORIO
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

4.  **Configure a sua chave de API:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Dentro dele, adicione sua chave do Hugging Face:
        ```
        HF_API_KEY="hf_SUA_CHAVE_AQUI"
        ```

5.  **Inicie o servidor local:**
    ```bash
    python app.py
    ```
    *Na primeira execução, o NLTK pode baixar alguns pacotes necessários.*

6.  **Acesse a aplicação:**
    * Abra seu navegador e acesse `http://127.0.0.1:5000`

---

## 📜 Licença

Este projeto está sob a licença MIT.

---
Desenvolvido por **Cicero Guilherme Gonzaga Silvestre**
