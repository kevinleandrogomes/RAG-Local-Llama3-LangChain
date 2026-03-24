import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# Configurações de interface e identidade do projeto
st.set_page_config(page_title="Assistente de IA RAG - Local", layout="centered")
st.title("🤖 Assistente de IA - Consulta de Documentos")
st.markdown("---")

# 1. GESTÃO DE ESTADO DA CONVERSA
# Inicializa o histórico para permitir diálogos contextuais (Memory-enabled RAG)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def configurar_sistema_rag():
    """
    Configura o motor de IA utilizando LangChain Expression Language (LCEL).
    Otimizado para execução em hardware local (NVIDIA RTX 2060).
    """
    # Provedor de modelos locais (Ollama)
    embeddings = OllamaEmbeddings(model="llama3")
    llm = OllamaLLM(model="llama3", temperature=0.7)
    
    # Conexão com a base de conhecimento vetorial (ChromaDB)
    db = Chroma(persist_directory="./banco_vetorial", embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Definição do Prompt com injeção de Contexto e Histórico
    template = """Você é um assistente técnico especializado. Use os fragmentos do documento e o 
    histórico da conversa para fornecer uma resposta precisa.
    
    Contexto do Documento:
    {context}
    
    Histórico da Conversa:
    {chat_history}
    
    Pergunta Atual: {question}
    
    Resposta:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Pipeline LCEL: Estrutura modular para processamento da consulta
    chain = (
        {
            "context": retriever, 
            "question": RunnablePassthrough(), 
            "chat_history": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

# Inicialização do motor
ia_engine = configurar_sistema_rag()

# 2. RENDERIZAÇÃO DA INTERFACE DE CHAT
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

# 3. PROCESSAMENTO DE ENTRADA
if pergunta := st.chat_input("Pergunte algo sobre o PDF (Autores, métodos, resultados...):"):
    st.chat_message("user").write(pergunta)
    
    with st.chat_message("assistant"):
        with st.spinner("Consultando base de conhecimento..."):
            # Formatação do histórico para o modelo de linguagem
            texto_historico = "\n".join([
                f"{'Usuário' if isinstance(m, HumanMessage) else 'IA'}: {m.content}" 
                for m in st.session_state.chat_history
            ])
            
            try:
                # Execução do pipeline RAG
                resposta = ia_engine.invoke(pergunta)
                st.write(resposta)
                
                # Atualização da memória da sessão
                st.session_state.chat_history.append(HumanMessage(content=pergunta))
                st.session_state.chat_history.append(AIMessage(content=resposta))
                
            except Exception as e:
                st.error(f"Erro na inferência: {e}")

# Painel Lateral: Especificações de Hardware e Software
st.sidebar.info(f"""
### 🛠️ Hardware & Stack
- **GPU:** NVIDIA RTX 2060 (6GB VRAM)
- **CPU:** AMD Ryzen 5 3600
- **RAM:** 16GB DDR4 2666MHz
- **LLM:** Llama 3 (Ollama)
- **Framework:** LangChain (LCEL)
""")