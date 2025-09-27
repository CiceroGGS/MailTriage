import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download necessário do NLTK (executar uma vez)
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
    
    def clean_text(self, text):
        # Remover cabeçalhos de email
        text = re.sub(r'From:.*?\n', '', text)
        text = re.sub(r'To:.*?\n', '', text)
        text = re.sub(r'Subject:.*?\n', '', text)
        text = re.sub(r'Date:.*?\n', '', text)
        
        # Remover caracteres especiais e números
        text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚãõâêîôûàèìòùç\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        # Converter para minúsculas
        text = text.lower()
        
        return text
    
    def tokenize_and_stem(self, text):
        tokens = word_tokenize(text)
        filtered_tokens = [self.stemmer.stem(token) for token in tokens 
                          if token not in self.stop_words and len(token) > 2]
        return ' '.join(filtered_tokens)
    
    def process(self, email_text):
        cleaned_text = self.clean_text(email_text)
        processed_text = self.tokenize_and_stem(cleaned_text)
        return processed_text

def process_email(email_text):
    processor = EmailProcessor()
    return processor.process(email_text)