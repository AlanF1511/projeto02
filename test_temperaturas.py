from classifier import classificar_mensagem
import time

def executar_testes():
    # Escolhemos uma mensagem que pode gerar dúvida no modelo
    mensagem_teste = "Vocês trabalham no sábado?"
    
    # 3 Valores diferentes de temperatura
    temperaturas = [0.0, 0.5, 1.0]
    
    # Múltiplas execuções
    repeticoes = 3

    print(f"Iniciando testes automatizados...\n")
    print(f"Mensagem avaliada: '{mensagem_teste}'\n")

    for temp in temperaturas:
        print(f"--- Testando com Temperatura: {temp} ---")
        
        # Dicionário para contabilizar os resultados desta temperatura
        contagem_categorias = {
            "Suporte": 0, 
            "Vendas": 0, 
            "Financeiro": 0, 
            "Geral": 0
        }

        for i in range(1, repeticoes + 1):
            try:
                # O seu classificar_mensagem já aceita o parâmetro temperature!
                resultado = classificar_mensagem(mensagem_teste, temperature=temp)
                categoria_retornada = resultado["categoria"]
                
                # Incrementa o contador da categoria retornada
                if categoria_retornada in contagem_categorias:
                    contagem_categorias[categoria_retornada] += 1
                else:
                    # Se por algum motivo o fallback falhasse, cairia aqui (não deve acontecer)
                    contagem_categorias["Geral"] += 1
                    
                print(f"  Execução {i}/10 -> {categoria_retornada}")
                
            except Exception as e:
                print(f"  Execução {i}/10 -> Erro inesperado: {e}")
                contagem_categorias["Geral"] += 1
            
            # Pausa de 1 segundo entre as requisições para evitar bloqueio da API do Groq (Rate Limit)
            time.sleep(1)

        print(f"> Resumo (Temp {temp}): {contagem_categorias}\n")

if __name__ == "__main__":
    executar_testes()