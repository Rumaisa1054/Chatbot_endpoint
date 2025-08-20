# FLASK API CREATED: http://13.60.25.63:8000/search?prompt=what%20is%20gerd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
HF_TOKEN = os.environ.get("HF_TOKEN")
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

## Uncomment the following files if you're not using pipenv as your virtual environment manager
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())


# Step 1: Setup LLM (Mistral with HuggingFace)
#HF_TOKEN=os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"

def load_llm(huggingface_repo_id):
    groq_llm=ChatGroq(model="mixtral-8x7b-32768",api_key="GROK_API_HERE")
    return groq_llm

# Step 2: Connect LLM with FAISS and Create chain

CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

# Load Database
DB_FAISS_PATH="vectorstore/db_faiss"
embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db=FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# Create QA chain
qa_chain=RetrievalQA.from_chain_type(
    llm=load_llm(HUGGINGFACE_REPO_ID),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k':3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

def response(prompt):
    user_query = prompt
    response = qa_chain.invoke({'query': user_query})
    return ("RESULT: ", response["result"])
    #print("SOURCE DOCUMENTS: ", response["source_documents"])

ch = 'y'
while(ch != 'n'):
    print(response(input("Query : ")))
    ch = input("continue")

