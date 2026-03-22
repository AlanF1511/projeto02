import json
import os

ARQUIVO_HISTORICO = "historico.json"
LIMITE_MENSAGENS = 10

# A Persona do Assistente (Mensagem de Sistema)
PERSONA = {
    "role": "system",
    "content": "Você é um Desenvolvedor Sênior sarcástico, porém muito prestativo. Você adora resolver problemas de lógica, mas sempre solta uma piadinha leve sobre códigos ruins antes de ajudar. Responda de forma concisa."
}

def carregar_historico():
    """Carrega o histórico do JSON ou cria um novo com a Persona."""
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                historico = json.load(f)
                # Garante que a persona é sempre a regra número 1
                if not historico or historico[0].get("role") != "system":
                    historico.insert(0, PERSONA)
                return historico
        except:
            pass
    return [PERSONA]

def salvar_historico(mensagens):
    """Salva no JSON e aplica o limite de memória (janela deslizante)."""
    # Se passou do limite (Persona + 10 mensagens = 11), cortamos as mais antigas
    if len(mensagens) > LIMITE_MENSAGENS + 1:
        # Mantém a Persona (índice 0) e pega as últimas 10 mensagens
        mensagens = [mensagens[0]] + mensagens[-(LIMITE_MENSAGENS):]

    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=4)

    return mensagens

def limpar_memoria():
    """Apaga o histórico e reinicia apenas com a Persona."""
    mensagens = [PERSONA]
    salvar_historico(mensagens)
    return mensagens