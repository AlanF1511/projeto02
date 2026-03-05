import math
import re
from llm_client import gerar_embedding

# Memória vetorial do sistema
memoria_vetorial = []

def calcular_similaridade(vetor1, vetor2):
    """Cálculo matemático de similaridade de cosseno."""
    produto_escalar = sum(a * b for a, b in zip(vetor1, vetor2))
    norma1 = math.sqrt(sum(a * a for a in vetor1))
    norma2 = math.sqrt(sum(b * b for b in vetor2))
    
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return produto_escalar / (norma1 * norma2)

def iniciar_sistema(caminho_arquivo):
    """Lê o arquivo de conhecimento, divide em blocos e gera os embeddings."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        texto_conhecimento = f.read()

    # Divide o texto usando as numerações das seções (ex: "1. POLÍTICA...")
    chunks = re.split(r'\n(?=\d+\.\s)', texto_conhecimento)
    
    for chunk in chunks:
        if chunk.strip():
            texto_limpo = chunk.strip()
            vetor = gerar_embedding(texto_limpo)
            memoria_vetorial.append({"texto": texto_limpo, "vetor": vetor})
            
    print(f"Base de conhecimento carregada! {len(memoria_vetorial)} blocos vetorizados.")

def buscar_contexto(pergunta):
    """Compara a pergunta com a memória e retorna o texto mais relevante."""
    vetor_pergunta = gerar_embedding(pergunta)
    
    melhor_score = -1
    melhor_texto = ""
    
    for item in memoria_vetorial:
        score = calcular_similaridade(vetor_pergunta, item["vetor"])
        if score > melhor_score:
            melhor_score = score
            melhor_texto = item["texto"]
            
    return melhor_texto