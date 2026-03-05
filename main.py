from rag import iniciar_sistema, buscar_contexto
from validator import detectar_prompt_injection
from llm_client import gerar_resposta_llm
from dotenv import load_dotenv
load_dotenv()

def executar_chat():
    print("--- INICIANDO SISTEMA LOJA VIRTUAL ---")
    # 1. Carrega o txt e cria a memória vetorial
    iniciar_sistema('conhecimento/conhecimento.txt')
    print("-" * 40)
    
    while True:
        # 2. Recebe a pergunta
        pergunta = input("\nDigite sua dúvida sobre reembolso (ou 'sair'): ")
        if pergunta.lower() == 'sair':
            break
        
        # 3. Validação de Segurança (Prompt Injection)
        if detectar_prompt_injection(pergunta):
            print("❌ Erro de Segurança: Tentativa de manipulação de prompt detectada. Ação bloqueada.")
            continue # Pula para a próxima iteração do loop
            
        # 4. Busca o contexto no RAG
        print("🔍 Buscando na base de conhecimento...")
        contexto_recuperado = buscar_contexto(pergunta)
        
        # 5. Monta o prompt protegido
        prompt_final = f"""
        Você é o assistente de suporte da loja virtual. Responda a pergunta do usuário baseando-se APENAS no contexto fornecido.
        Se a resposta não estiver no contexto, diga que não tem essa informação.
        
        Contexto: {contexto_recuperado}
        
        Pergunta: {pergunta}
        """
        
        # 6. Chama o LLM para responder
        resposta = gerar_resposta_llm(prompt_final)
        print(f"\n🤖 Assistente: \n{resposta}")

if __name__ == "__main__":
    executar_chat()