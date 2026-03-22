import random
import string
import json

# 1. Nossas funções Python puras
def calcular_imc(peso, altura):
    """Calcula o IMC e retorna a classificação."""
    imc = peso / (altura ** 2)
    if imc < 18.5: status = "Abaixo do peso"
    elif imc < 24.9: status = "Peso normal"
    elif imc < 29.9: status = "Sobrepeso"
    else: status = "Obesidade"
    
    return json.dumps({"imc": round(imc, 2), "classificacao": status})

def gerar_senha(tamanho=12):
    """Gera uma senha forte e aleatória."""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return json.dumps({"senha_gerada": senha})

# 2. O "Manual de Instruções" para a IA (JSON Schema)
minhas_ferramentas = [
    {
        "type": "function",
        "function": {
            "name": "calcular_imc",
            "description": "Calcula o Índice de Massa Corporal (IMC) do usuário. Use APENAS quando o usuário fornecer peso e altura.",
            "parameters": {
                "type": "object",
                "properties": {
                    "peso": {"type": "number", "description": "Peso em kg. Ex: 70.5"},
                    "altura": {"type": "number", "description": "Altura em metros. Ex: 1.75"}
                },
                "required": ["peso", "altura"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gerar_senha",
            "description": "Gera uma senha forte e aleatória. Use quando o usuário pedir uma nova senha.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tamanho": {"type": "integer", "description": "Tamanho da senha. Padrão é 12."}
                }
            }
        }
    }
]

# 3. Dicionário de mapeamento para executar a função correta
funcoes_disponiveis = {
    "calcular_imc": calcular_imc,
    "gerar_senha": gerar_senha
}