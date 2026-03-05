import json
import logging

# Configuração simples de log para visualizar os erros no terminal
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def validar_resposta_llm(resposta_texto, categorias_permitidas):
    """
    Valida a resposta do LLM garantindo que é um JSON válido e contém uma categoria permitida.
    """
    # 4. Fallback seguro -> Se tudo falhar, retorna "Geral"
    fallback = {"categoria": "Geral"}

    if not resposta_texto:
        logging.warning("A resposta do LLM veio vazia.")
        return fallback

    # Limpeza preventiva: LLMs costumam retornar o JSON dentro de blocos Markdown
    texto_limpo = resposta_texto.strip()
    if texto_limpo.startswith("```json"):
        texto_limpo = texto_limpo.replace("```json", "").replace("```", "").strip()
    elif texto_limpo.startswith("```"):
        texto_limpo = texto_limpo.replace("```", "").strip()

    try:
        # 1. Criar parser JSON e 2. Tratar erro de JSON inválido
        dados = json.loads(texto_limpo)
        
        # Verifica se o JSON tem a estrutura esperada
        if "categoria" not in dados:
            logging.warning("Chave 'categoria' ausente no JSON retornado.")
            return fallback

        categoria_extraida = dados["categoria"]

        # 3. Criar validação contra lista permitida
        if categoria_extraida in categorias_permitidas:
            return dados
        else:
            logging.warning(f"Categoria inventada pelo LLM: '{categoria_extraida}'. Acionando fallback.")
            return fallback

    except json.JSONDecodeError as e:
        logging.warning(f"Falha no Parser JSON. O modelo retornou texto inválido: {e}")
        return fallback
    except Exception as e:
        logging.error(f"Erro inesperado durante a validação: {e}")
        return fallback
    
def detectar_prompt_injection(prompt):
    """
    Verifica se o prompt contém tentativas de injeção ou manipulação das regras.
    """
    termos_bloqueados = [
        "system prompt", "ignore as instruções", "esqueça as regras",
        "aja como", "bypass", "instruções anteriores"
    ]
    
    prompt_min = prompt.lower()
    for termo in termos_bloqueados:
        if termo in prompt_min:
            return True # Injeção detectada
            
    return False # Prompt seguro