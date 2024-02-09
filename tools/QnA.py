from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI, openai
import pickle

def create_vector_db_tool(llm: ChatOpenAI):
    with open("data/dso_vectors.pkl", "rb") as f:
        vectorStore = pickle.load(f)
        
    return RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorStore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
