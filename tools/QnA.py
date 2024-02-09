import os

from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI, openai
import pickle

#load_dotenv()
#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

def create_vector_db_tool(llm: ChatOpenAI):
    with open("faiss_store_openai.pkl", "rb") as f:
        vectorStore = pickle.load(f)
        
    return RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorStore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
