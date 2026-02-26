# Classificador de Mensagens com IA Generativa (LLM)

Este repositório contém um sistema de classificação automatizada de mensagens de clientes, desenvolvido em Python. O projeto utiliza a API de LLMs (Groq/OpenAI) para categorizar intenções de usuários e implementa uma arquitetura robusta de validação para garantir a integridade das respostas geradas pela Inteligência Artificial.

## 🚀 Funcionalidades

- **Classificação Inteligente:** Categoriza mensagens nas áreas de `Suporte`, `Vendas`, `Financeiro` ou `Geral`.
- **Validador JSON (`validator.py`):** Intercepta e limpa a resposta do LLM, removendo formatações indesejadas (como blocos markdown) antes de realizar o *parse*.
- **Prevenção de Alucinações:** Verifica se a categoria retornada pelo modelo existe na lista de categorias permitidas, barrando invenções da IA.
- **Fallback Seguro:** Em caso de indisponibilidade da API, falha no formato JSON (`JSONDecodeError`) ou erro inesperado, o sistema assume automaticamente a categoria `Geral` para evitar quebra (crash) da aplicação.
- **Testes Automatizados (`test_temperaturas.py`):** Script dedicado para avaliar o comportamento e a consistência do modelo sob diferentes níveis de temperatura (0.0, 0.5 e 1.0) com múltiplas repetições.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **OpenAI Python SDK** (conectado via *base_url* à API da Groq)
- **Dotenv** (para gerenciamento seguro de variáveis de ambiente)

## ⚙️ Como Executar o Projeto

### 1. Clonar o repositório

git clone https://github.com/AlanF1511/projeto02.git
cd projeto02

### 2. Instalar dependências

pip install -r requirements.txt

### 3. Configurar Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto e adicione suas chaves de API:

OPENAI_API_KEY=sua_chave_aqui
GROQ_API_KEY=sua_chave_groq_aqui

### 4. Executar os Scripts
Para rodar a classificação principal com as mensagens de exemplo:

python main.py

Para rodar a bateria de testes de temperatura:

python test_temperaturas.py

