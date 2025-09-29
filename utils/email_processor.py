# Módulo para pré-processamento de texto com NLTK.
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Garante que os pacotes necessários do NLTK sejam baixados
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EmailProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = PorterStemmer()
    
    # Remove cabeçalhos, caracteres especiais e converte para minúsculas
    def clean_text(self, text):
        text = re.sub(r'From:.*?\n|To:.*?\n|Subject:.*?\n|Date:.*?\n', '', text, flags=re.IGNORECASE)
        text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚãõâêîôûàèìòùç\s]', '', text)
        text = text.lower()
        return text
    
    # Quebra o texto em palavras, remove stopwords e aplica radicalização (stemming)
    def tokenize_and_stem(self, text):
        tokens = word_tokenize(text)
        filtered_tokens = [self.stemmer.stem(token) for token in tokens 
                          if token not in self.stop_words and len(token) > 2]
        return ' '.join(filtered_tokens)
    
    # Orquestra o processo completo de limpeza
    def process(self, email_text):
        cleaned_text = self.clean_text(email_text)
        processed_text = self.tokenize_and_stem(cleaned_text)
        return processed_text

# Função auxiliar para facilitar o uso da classe
def process_email(email_text):
    processor = EmailProcessor()
    return processor.process(email_text)