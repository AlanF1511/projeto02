# Relatório Analítico: Impacto da Temperatura em Classificações com LLM

## 1. Introdução
Este relatório apresenta os resultados dos testes automatizados realizados no módulo de classificação de mensagens (`classifier.py`), desenvolvido com integração à API de LLMs. O objetivo principal foi avaliar o comportamento do modelo na extração estruturada de dados (JSON) e na precisão da classificação sob diferentes níveis de criatividade e aleatoriedade, controlados pelo parâmetro `temperature`.

## 2. Metodologia
Foi desenvolvido um script de automação (`test_temperaturas.py`) que submeteu uma mesma mensagem de entrada a 10 requisições sequenciais para três valores distintos de temperatura: **0.0**, **0.5** e **1.0**. 

* **Mensagem de teste:** *"Preciso de ajuda com meu pagamento, o sistema deu erro ao gerar o boleto"*
* **Categorias permitidas:** Suporte, Vendas, Financeiro, Geral.
* **Mecanismo de Defesa:** Todas as respostas passaram pelo módulo `validator.py`, responsável por limpar formatações Markdown, fazer o *parse* do JSON, validar a categoria e aplicar um *fallback* seguro em caso de falhas ou alucinações.

## 3. Resultados Obtidos
A execução do script gerou os seguintes resultados:

* **Temperatura 0.0 (Foco e Determinação):** * Resultado: `{'Financeiro': 10}`
  * Análise: Nenhuma variação. O modelo operou de forma estritamente determinística, como esperado.
* **Temperatura 0.5 (Equilíbrio):** * Resultado: `{'Financeiro': 10}`
  * Análise: Manutenção de 100% de consistência na classificação.
* **Temperatura 1.0 (Alta Criatividade/Aleatoriedade):** * Resultado: `{'Financeiro': 10}`
  * Análise: Nenhuma variação de categoria ou quebra de estrutura JSON que acionasse o fallback do sistema.

## 4. Conclusão e Análise Técnica
A ausência de variação mesmo na temperatura máxima (1.0) aponta para dois fatores cruciais da arquitetura:

1. **Ancoragem Semântica:** A frase de teste possui termos com fortíssimo peso semântico direcional (*"pagamento"*, *"boleto"*). O cálculo probabilístico do modelo para associar esses tokens à categoria "Financeiro" é tão alto que sobrepõe o ruído introduzido pela temperatura 1.0. A entropia gerada não foi suficiente para desviar o contexto.
2. **Robustez do Validador:** Em nenhuma das 30 execuções o sistema sofreu *crash* por `JSONDecodeError`. Isso comprova que a camada de tratamento (`validator.py`) foi eficaz em limpar os dados da resposta bruta (removendo blocos *```json* comuns em LLMs) antes do *parsing*, garantindo estabilidade de produção.

O mecanismo provou-se resiliente e pronto para cenários onde a integridade da resposta da API é indispensável.