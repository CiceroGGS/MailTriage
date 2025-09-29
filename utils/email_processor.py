"""
Módulo para pré-processamento de texto de e-mails.
Utiliza a biblioteca NLTK para limpar, tokenizar e normalizar o texto.
(Nota: Não está sendo ativamente usado na lógica principal com o Llama 3,
mas está aqui para demonstrar a capacidade de pré-processamento).
"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Bloco para garantir que os pacotes necessários do NLTK sejam baixados na primeira execução
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EmailProcessor:
    """Uma classe para encapsular as lógicas de processamento de texto."""
    def __init__(self):
        """Prepara as ferramentas: lista de stopwords e o stemmer."""
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = PorterStemmer()
    
    def clean_text(self, text):
        """Remove partes irrelevantes do e-mail e caracteres especiais."""
        text = re.sub(r'From:.*?\n|To:.*?\n|Subject:.*?\n|Date:.*?\n', '', text, flags=re.IGNORECASE)
        text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚãõâêîôûàèìòùç\s]', '', text)
        text = text.lower()
        return text
    
    def tokenize_and_stem(self, text):
        """Quebra o texto em palavras (tokens), remove palavras comuns e aplica a radicalização."""
        tokens = word_tokenize(text)
        filtered_tokens = [self.stemmer.stem(token) for token in tokens 
                          if token not in self.stop_words and len(token) > 2]
        return ' '.join(filtered_tokens)
    
    def process(self, email_text):
        """Orquestra o processo completo de limpeza e normalização."""
        cleaned_text = self.clean_text(email_text)
        processed_text = self.tokenize_and_stem(cleaned_text)
        return processed_text

def process_email(email_text):
    """Função auxiliar para facilitar o uso da classe EmailProcessor."""
    processor = EmailProcessor()
    return processor.process(email_text)