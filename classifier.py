from llm_client import gerar_resposta
from validator import validar_resposta_llm

CATEGORIAS = ["Suporte", "Vendas", "Financeiro", "Geral"]

def classificar_mensagem(mensagem, temperature=0.2):
    prompt = f"""
        Classifique a mensagem abaixo em uma das seguintes categorias: {', '.join(CATEGORIAS)}.
        Retorne apenas um JSON no formato:
        {{
            "categoria": "nome_categoria"
        }}

        Mensagem: "{mensagem}"
    """
    
    # Obtém a resposta em texto do LLM
    resposta_bruta = gerar_resposta(prompt, temperature)
    
    # Passa a resposta pelo validador junto com a lista de categorias permitidas
    resposta_validada = validar_resposta_llm(resposta_bruta, CATEGORIAS)
    
    return resposta_validada
