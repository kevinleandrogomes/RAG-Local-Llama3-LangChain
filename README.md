# 🤖 Local RAG Assistant: Inteligência de Documentos com Llama 3 & LCEL

Este projeto consiste em um assistente de inteligência artificial de alto desempenho, capaz de realizar leitura e análise de documentos PDF de forma 100% local. Utilizando a arquitetura **RAG (Retrieval-Augmented Generation)**, o sistema garante respostas precisas e fundamentadas nos fragmentos do documento fornecido, eliminando alucinações e mantendo a total privacidade dos dados.

---

## 📸 Interface do Sistema (Em Execução)

Abaixo, a demonstração do assistente operando em ambiente local. Note a barra lateral detalhando o hardware utilizado e a capacidade do modelo em manter o contexto da conversa, respondendo perguntas subsequentes com base no histórico.

![Demonstração da Interface do Chatbot RAG Local](imgs/RAG_Funcionando.png)
*(Interface Streamlit com inferência acelerada por hardware)*

---

## 🚀 Diferenciais Técnicos

- **Privacidade e Soberania de Dados:** Execução totalmente local via Ollama, sem envio de informações para nuvem.
- **Memória Contextual (Conversational RAG):** Implementação de histórico de chat que permite diálogos fluidos (o bot compreende pronomes e referências a mensagens anteriores).
- **Arquitetura LCEL (LangChain Expression Language):** Utilização do padrão mais moderno e modular do framework LangChain para a orquestração do pipeline.
- **Processamento em GPU (CUDA):** Otimizado para inferência acelerada por hardware utilizando os núcleos CUDA da NVIDIA.

---

## 💻 Infraestrutura de Hardware (Lab Local)

O projeto foi otimizado para rodar com baixa latência em hardware intermediário, provando a viabilidade técnica de LLMs locais:

- **GPU:** NVIDIA GeForce RTX 2060 (6GB VRAM) - *Inferência do LLM e Embeddings*
- **CPU:** AMD Ryzen 5 3600 (6 Cores / 12 Threads) - *Orquestração e ETL*
- **RAM:** 16GB DDR4 2666MHz - *Gerenciamento de Estado e Vetores*
- **Storage:** SSD NVMe - *Persistência de alta performance do banco vetorial*

---

## 🛠️ Stack Tecnológica

- **LLM:** Llama 3 (8B Parameters) via Ollama
- **Embeddings:** Ollama Embeddings (Llama 3)
- **Framework:** LangChain v0.3+ (LCEL)
- **Interface UI:** Streamlit
- **Banco Vetorial:** ChromaDB
- **Ambiente:** Python 3.13

---

## 🔧 Como Executar

### 1. Pré-requisitos
- Ter o [Ollama](https://ollama.com/) instalado e o modelo Llama 3 baixado (`ollama run llama3`).
- Python 3.13 instalado.

### 2. Configuração do Ambiente
```powershell
# Clone o repositório
git clone [https://github.com/seu-usuario/RAG-Local-Llama3-LangChain.git](https://github.com/seu-usuario/RAG-Local-Llama3-LangChain.git)

# Entre na pasta
cd RAG-Local-Llama3-LangChain

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

### 3. Preparação dos Dados (ETL)
Coloque seu arquivo PDF na pasta `docs/` e execute o script de indexação para gerar o banco vetorial no SSD:

```powershell
python indexar.py

### 4. Execução do Assistente
Com o banco vetorial gerado, inicie a interface para começar a interagir com o documento em tempo real:

```powershell
streamlit run app.py

📂 Estrutura do Repositório
Nesta seção, detalhamos a organização dos arquivos para facilitar a manutenção e o entendimento da arquitetura do projeto:

app.py: Interface do usuário desenvolvida em Streamlit, contendo a lógica de conversação RAG e o gerenciamento de memória contextual.

indexar.py: Script responsável pelo pipeline de ETL (Extração, Transformação e Carga), realizando o chunking inteligente e a vetorização dos documentos.

docs/: Diretório destinado ao armazenamento dos arquivos PDF originais que servirão como base de conhecimento.

banco_vetorial/: Diretório (ignorado via .gitignore) onde os embeddings do ChromaDB são persistidos localmente.

requirements.txt: Arquivo contendo todas as dependências e versões das bibliotecas para replicação do ambiente.