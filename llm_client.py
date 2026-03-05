import os
from groq import Groq
import math
from dotenv import load_dotenv 

# 1. Força o carregamento do arquivo .env ANTES de iniciar a Groq
load_dotenv()

# Inicializa o cliente da Groq 

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def gerar_resposta_llm(prompt_final):
    """
    Chama a API da Groq para responder a pergunta baseada no contexto do RAG.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente de suporte focado em políticas de reembolso."
                },
                {
                    "role": "user",
                    "content": prompt_final
                }
            ],
            model="llama-3.1-8b-instant", # Pode usar "mixtral-8x7b-32768" também
            temperature=0.2, # Temperatura baixa é ideal para RAG (evita alucinação)
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Erro na API da Groq: {e}"

def gerar_embedding(texto):
    """
    Como a Groq NÃO possui API de embeddings, usamos um gerador rudimentar baseado no tamanho 
    do texto só para a matemática do RAG funcionar no exercício.
    (No mundo real, usaríamos a biblioteca 'sentence-transformers' aqui).
    """
    # Cria um vetor simples pseudo-aleatório baseado no próprio texto
    import random
    random.seed(abs(hash(texto))) 
    vetor = [random.random(), random.random(), random.random()]
    
    # Normalizando o vetor para a busca por cosseno funcionar melhor
    norma = math.sqrt(sum(a * a for a in vetor))
    return [a / norma for a in vetor]