import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from ferramentas import minhas_ferramentas, funcoes_disponiveis
from memoria import salvar_historico

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def enviar_mensagem_com_memoria(mensagens):
    try:
        # 1. Envia a conversa inteira e as ferramentas para a IA
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensagens,
            tools=minhas_ferramentas,
            tool_choice="auto", # Deixa a IA decidir se precisa usar uma função
            temperature=0.7
        )
        
        resposta_msg = response.choices[0].message
        
        # 2. A IA decidiu usar uma função Python?
        if resposta_msg.tool_calls:
            # Salvamos o pedido da IA no histórico (formato seguro)
            mensagens.append({
                "role": "assistant",
                "content": resposta_msg.content or "",
                "tool_calls": [
                    {"id": t.id, "type": "function", "function": {"name": t.function.name, "arguments": t.function.arguments}} 
                    for t in resposta_msg.tool_calls
                ]
            })
            
            # 3. Executamos a função no nosso computador
            for tool_call in resposta_msg.tool_calls:
                nome_funcao = tool_call.function.name
                argumentos = json.loads(tool_call.function.arguments)
                
                funcao_python = funcoes_disponiveis.get(nome_funcao)
                if funcao_python:
                    print(f"⚙️  [Executando função Python: {nome_funcao}]")
                    resultado = funcao_python(**argumentos)
                    
                    # 4. Devolvemos o resultado para a IA ler
                    mensagens.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": nome_funcao,
                        "content": str(resultado)
                    })
                    
            # 5. A IA gera a resposta final baseada no resultado da função
            response_final = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensagens
            )
            resposta_texto = response_final.choices[0].message.content
            
        else:
            # Resposta normal (bate-papo)
            resposta_texto = resposta_msg.content

        # ---> ADICIONE ESTA LINHA AQUI <---
        # Remove qualquer lixo de tag <function> que o modelo deixe vazar no texto final
        resposta_texto = re.sub(r'<function=.*?</function>', '', resposta_texto).strip()

        # Salva a resposta final no histórico
        mensagens.append({"role": "assistant", "content": resposta_texto})
        salvar_historico(mensagens)
        
        return resposta_texto
    
    except Exception as e:
        return f"Erro na API da Groq: {e}"