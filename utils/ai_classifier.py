import requests
import os
from typing import Dict, List
import json

class AIClassifier:
    def __init__(self):
        # Configuração da API do Hugging Face
        self.hf_api_key = os.getenv('HF_API_KEY', 'your_huggingface_key_here')
        self.headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        
    def classify_email(self, text: str) -> str:
        """Classifica o email usando Hugging Face Zero-Shot Classification"""
        
        # Primeiro, tentamos usar a API avançada
        hf_result = self._classify_with_huggingface(text)
        if hf_result:
            return hf_result
        
        # Fallback para classificação baseada em regras
        return self._classify_with_keywords(text)
    
    def _classify_with_huggingface(self, text: str) -> str:
        """Classificação usando modelo pré-treinado do Hugging Face"""
        try:
            # API para classificação zero-shot
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
            
            payload = {
                "inputs": text[:1000],  # Limitar tamanho para a API
                "parameters": {
                    "candidate_labels": [
                        "solicitação de suporte técnico, problema, erro, dúvida, requisição, ajuda",
                        "cumprimento, agradecimento, felicitação, mensagem social, saudação"
                    ],
                    "multi_label": False
                }
            }
            
            response = requests.post(
                API_URL, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Debug: mostrar resultado completo
                print("Hugging Face API Response:", json.dumps(result, indent=2))
                
                labels = result['labels']
                scores = result['scores']
                
                # Encontrar a label com maior score
                best_index = scores.index(max(scores))
                best_label = labels[best_index]
                best_score = scores[best_index]
                
                print(f"Classificação: {best_label} (Score: {best_score:.3f})")
                
                # LÓGICA MELHORADA DE CLASSIFICAÇÃO
                productive_indicators = [
                    'problema', 'erro', 'dúvida', 'requisição', 'ajuda', 'suporte', 
                    'solicitação', 'técnico', 'funcionamento', 'assistência', 'ajudar',
                    'preciso', 'necessito', 'urgente', 'importante'
                ]
                
                # Verificar palavras-chave produtivas no texto
                text_lower = text.lower()
                has_productive_words = any(word in text_lower for word in productive_indicators)
                
                # Lógica de decisão melhorada
                if has_productive_words and "solicitação" in best_label:
                    return "Produtivo"
                elif has_productive_words and best_score < 0.7:  # Baixa confiança + palavras produtivas
                    return "Produtivo"
                elif "solicitação" in best_label and best_score > 0.6:
                    return "Produtivo"
                elif has_productive_words:  # Palavras produtivas mesmo com classificação diferente
                    return "Produtivo"
                else:
                    return "Improdutivo"
                    
            else:
                print(f"Erro na API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Erro na classificação Hugging Face: {e}")
            return None
    
    def _classify_with_keywords(self, text: str) -> str:
        """Fallback: classificação baseada em palavras-chave"""
        text_lower = text.lower()
        
        productive_keywords = [
            'problema', 'ajuda', 'suporte', 'erro', 'solicitação', 'urgente',
            'atualização', 'status', 'caso', 'sistema', 'técnico', 'suporte',
            'requisição', 'andamento', 'dúvida', 'questão', 'assistência',
            'bug', 'falha', 'não funciona', 'como fazer', 'preciso de ajuda',
            'contato', 'chamado', 'ticket', 'incidente', 'resolver', 'conserto',
            'defeito', 'avaria', 'pané', 'quebrado', 'parou'
        ]
        
        unproductive_keywords = [
            'obrigado', 'obrigada', 'parabéns', 'feliz', 'natal', 'ano novo',
            'comemoração', 'agradecimento', 'cumprimento', 'saudações',
            'bom dia', 'boa tarde', 'boa noite', 'olá', 'oi', 'felicitações',
            'ótimo trabalho', 'excelente', 'thanks', 'thank you', 'greetings',
            'cumprimentos', 'saudação', 'felicidades', 'abraço', 'beijo'
        ]
        
        productive_count = sum(1 for word in productive_keywords if word in text_lower)
        unproductive_count = sum(1 for word in unproductive_keywords if word in text_lower)
        
        print(f"Contagem keywords - Produtivo: {productive_count}, Improdutivo: {unproductive_count}")
        
        # Lógica de decisão com pesos
        if productive_count > 0 and unproductive_count == 0:
            return "Produtivo"
        elif productive_count > unproductive_count * 2:  # Muito mais palavras produtivas
            return "Produtivo"
        elif productive_count > unproductive_count:
            return "Produtivo"
        elif unproductive_count > productive_count:
            return "Improdutivo"
        else:
            # Empate: considerar contexto
            if any(word in text_lower for word in ['?', 'como', 'porque', 'quando']):
                return "Produtivo"
            else:
                return "Improdutivo"
    
    def generate_response(self, original_text: str, classification: str) -> str:
        """Gera resposta mais inteligente baseada no conteúdo"""
        try:
            # Tentar gerar resposta com Hugging Face
            hf_response = self._generate_with_huggingface(original_text, classification)
            if hf_response and len(hf_response) > 10:  # Verificar se a resposta é válida
                return hf_response
        except Exception as e:
            print(f"Erro na geração com IA: {e}")
        
        # Fallback para respostas pré-definidas
        return self._generate_contextual_response(original_text, classification)
    
    def _generate_with_huggingface(self, text: str, classification: str) -> str:
        """Gera resposta usando modelo de geração de texto"""
        try:
            # Usar modelo de geração de texto
            API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
            
            # Prompt mais específico e em português
            if classification == "Produtivo":
                prompt = f"""
                Gere uma resposta profissional em português para um email de suporte técnico.
                
                Email recebido: "{text[:300]}"
                
                A resposta deve ser: curta, simpática, informar que a solicitação será analisada.
                Não incluir detalhes técnicos. Máximo 2 linhas.
                Resposta:
                """
            else:
                prompt = f"""
                Gere uma resposta profissional em português para um email de cumprimentos.
                
                Email recebido: "{text[:300]}"
                
                A resposta deve ser: breve, educada, agradecer o contato.
                Manter tom profissional mas caloroso. Máximo 2 linhas.
                Resposta:
                """
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7,
                    "do_sample": True,
                    "num_return_sequences": 1
                }
            }
            
            response = requests.post(
                API_URL, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0]['generated_text']
                    
                    # Limpar a resposta - remover o prompt
                    if 'Resposta:' in generated_text:
                        generated_text = generated_text.split('Resposta:')[-1].strip()
                    
                    # Garantir que a resposta seja adequada
                    if len(generated_text) > 10 and not generated_text.startswith('Gere'):
                        return generated_text.strip()
                
        except Exception as e:
            print(f"Erro específico na geração com Hugging Face: {e}")
        
        return None
    
    def _generate_contextual_response(self, text: str, classification: str) -> str:
        """Gera resposta contextual baseada no conteúdo do email"""
        text_lower = text.lower()
        
        if classification == "Produtivo":
            # Respostas mais específicas para tipos de problemas
            if any(word in text_lower for word in ['problema', 'erro', 'bug', 'não funciona']):
                responses = [
                    "Identificamos que você está enfrentando um problema técnico. Nossa equipe já está analisando a situação e retornará com uma solução em breve.",
                    "Agradecemos por reportar o problema. Estamos investigando a questão e entraremos em contato em até 2 horas úteis.",
                    "Sua solicitação de suporte técnico foi recebida. Priorizaremos a análise deste caso e retornaremos rapidamente."
                ]
            elif any(word in text_lower for word in ['dúvida', 'como', 'pergunta']):
                responses = [
                    "Obrigado pela sua dúvida. Nossa equipe preparará uma resposta completa e retornará em até 1 dia útil.",
                    "Agradecemos seu questionamento. Estamos reunindo as informações necessárias para respondê-lo da melhor forma.",
                    "Sua dúvida foi registrada. Retornaremos com orientações claras e detalhadas em breve."
                ]
            elif any(word in text_lower for word in ['urgente', 'importante', 'prioridade']):
                responses = [
                    "✅ SOLICITAÇÃO URGENTE IDENTIFICADA - Nossa equipe está tratando este caso com máxima prioridade. Retornaremos em até 30 minutos.",
                    "Entendemos a urgência da sua solicitação. Estamos alocando recursos para resolver esta questão rapidamente.",
                    "Caso prioritário detectado. Ativamos nosso protocolo de resposta acelerada para seu atendimento."
                ]
            else:
                responses = [
                    "Agradecemos seu contato. Nossa equipe técnica analisará sua solicitação e retornará em breve.",
                    "Recebemos sua mensagem. Estamos processando sua requisição e retornaremos em até 24h.",
                    "Sua solicitação foi registrada com sucesso. Um de nossos especialistas entrará em contato."
                ]
        else:
            # Respostas para emails improdutivos
            if any(word in text_lower for word in ['obrigado', 'agradeço', 'agradecimento']):
                responses = [
                    "Agradecemos seu feedback! Ficamos felizes em poder ajudar.",
                    "Obrigado pelo retorno! É um prazer atendê-lo.",
                    "Agradecemos o reconhecimento! Continuaremos trabalhando para oferecer o melhor serviço."
                ]
            elif any(word in text_lower for word in ['parabéns', 'felicitações', 'excelente']):
                responses = [
                    "Agradecemos as felicitações! Ficamos contentes com seu feedback positivo.",
                    "Obrigado pelo reconhecimento! Isso nos motiva a continuar melhorando.",
                    "Agradecemos suas gentis palavras! É um prazer tê-lo como cliente."
                ]
            elif any(word in text_lower for word in ['bom dia', 'boa tarde', 'ola', 'oi']):
                responses = [
                    "Agradecemos seu contato! Estamos disponíveis para ajudá-lo com assuntos técnicos.",
                    "Olá! Em caso de necessidade técnica, nossa equipe está à disposição.",
                    "Obrigado pela mensagem! Retornaremos ao trabalho prioritário agora."
                ]
            else:
                responses = [
                    "Agradecemos sua mensagem! Retornaremos ao trabalho normal em breve.",
                    "Obrigado pelo contato! Estamos focados em demandas técnicas prioritárias.",
                    "Agradecemos sua gentil mensagem. Nossa equipe retornará para assuntos produtivos."
                ]
        
        import random
        import hashlib
        
        # Usar hash do texto para escolha determinística (mas aparentemente aleatória)
        text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
        chosen_index = text_hash % len(responses)
        
        return responses[chosen_index]

# Funções de interface
def classify_email(text: str) -> str:
    classifier = AIClassifier()
    return classifier.classify_email(text)

def generate_response(text: str, classification: str) -> str:
    classifier = AIClassifier()
    return classifier.generate_response(text, classification)