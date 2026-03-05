# Assistente RAG e Classificador de Mensagens com IA Generativa

Este repositório contém um sistema inteligente desenvolvido em Python que combina duas grandes frentes da IA Generativa: um Classificador Automatizado de Intenções e um Assistente Baseado em RAG (Retrieval-Augmented Generation) com proteção de segurança. O projeto utiliza LLMs de alta performance via API da Groq para interagir e categorizar mensagens.

## 🚀 Funcionalidades

### 🔍 Módulo 1: Classificador e Validador (Aula 02)

- **Classificação Inteligente:** Categoriza mensagens nas áreas de `Suporte`, `Vendas`, `Financeiro` ou `Geral`.
- **Validador JSON (`validator.py`):** Intercepta e limpa a resposta do LLM, removendo formatações indesejadas (como blocos markdown) antes de realizar o *parse*.
- **Prevenção de Alucinações:** Verifica se a categoria retornada pelo modelo existe na lista permitida, barrando invenções da IA.
- **Fallback Seguro:** Em caso de falha da API ou erro de JSON, o sistema assume a categoria `Geral` para evitar quebra (crash) da aplicação.
- **Testes de Temperatura (`test_temperaturas.py`):** Script para avaliar a consistência do modelo sob diferentes níveis de criatividade (0.0, 0.5 e 1.0).

### 🛡️ Módulo 2: RAG e Segurança (Aula 03)

- **Motor RAG In-Memory (`rag.py`):** Lê documentos locais (`conhecimento/conhecimento.txt`), divide em blocos (*chunks*) e realiza busca semântica utilizando cálculo de similaridade de cosseno.
- **Proteção contra Prompt Injection:** Camada de segurança heurística no `validator.py` que detecta e bloqueia tentativas de manipulação das instruções do sistema (ex: "ignore regras anteriores" ou "me diga sua system prompt").
- **Embeddings Customizados:** Implementação matemática em Python puro para gerar e comparar vetores, contornando a ausência de endpoints nativos de embedding na API da Groq para fins educacionais.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Groq Python SDK** (Integração direta com modelos ultrarrápidos como Llama 3)
- **OpenAI Python SDK** (Estrutura legada/alternativa suportada)
- **Dotenv** (Para gerenciamento seguro de variáveis de ambiente)
- **Módulos Nativos:** `math` e `re` (para cálculos vetoriais e regex).

## ⚙️ Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/AlanF1511/projeto02.git
cd projeto02
```

### 2. Instalar dependências
Certifique-se de ter o Python instalado e execute:
```bash
pip install -r requirements.txt
pip install groq python-dotenv
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione suas chaves de API:
```env
OPENAI_API_KEY=sua_chave_aqui
GROQ_API_KEY=sua_chave_groq_aqui
```
*(Nota: O arquivo `.env` já está listado no `.gitignore` para garantir a segurança das credenciais).*

### 4. Executar os Scripts
Para rodar o assistente interativo de loja virtual com RAG e proteção contra injeções:
```bash
python main.py
```

Para rodar a bateria de testes de temperatura:
```bash
python test_temperaturas.py
```

## 📄 Relatório de Testes
O projeto inclui documentação das análises de impacto da variação de temperature e agora comporta uma base de conhecimento escalável (conhecimento.txt) para testes de recuperação de informação por IA.

---
**Autor:** Alan Felipe Ribeiro


