from memoria import carregar_historico, limpar_memoria
from llm_client import enviar_mensagem_com_memoria

def executar_chat():
    print("--- ASSISTENTE COM MEMÓRIA E FERRAMENTAS ---")
    print("Comandos: /limpar (apaga memória) | sair (encerra)\n")
    
    # Parte 5 - Carrega o histórico ao reiniciar
    mensagens = carregar_historico()
    
    while True:
        pergunta = input("Você: ")
        
        if pergunta.lower() in ['sair', 'exit']:
            break
            
        # Parte 1 - Comando de limpeza
        if pergunta.lower() == '/limpar':
            mensagens = limpar_memoria()
            print("🤖 Assistente: Memória da conversa apagada.\n")
            continue
            
        # Adiciona a pergunta do usuário na lista de mensagens
        mensagens.append({"role": "user", "content": pergunta})
        
        # Chama a API
        resposta = enviar_mensagem_com_memoria(mensagens)
        print(f"🤖 Assistente: {resposta}\n")

if __name__ == "__main__":
    executar_chat()