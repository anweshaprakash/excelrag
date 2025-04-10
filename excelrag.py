from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import pandas as pd
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))
embedding_model = OpenAIEmbeddings(model='text-embedding-3-small', api_key=os.getenv('OPENAI_API_KEY'))

def load_data(file_path):
    df = pd.read_excel(file_path)
    documents = []
    for _, row in df.iterrows():
        content = "\n".join([f"{col}: {val}" for col, val in row.items()])
        metadata = {"columns": list(df.columns), "index": _}
        documents.append(Document(page_content=content, metadata=metadata))
    return df, documents

def save_data(df, file_path):
    df.to_excel(file_path, index=False)

file_path = 'Historicalinvesttemp.xlsx'
df, documents = load_data(file_path)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
all_split = text_splitter.split_documents(documents)

vector_db = FAISS.from_documents(all_split, embedding_model)

system_prompt = (
    "You are a data analyst assistant. Analyze and modify this tabular data containing columns: {columns}. "
    "When asked to edit data, respond with EXACTLY: EDIT||row_index||column_name||new_value. "
    "The data shows measurements with numerical values and possible NaN entries. "
    "Use this structure to answer questions about the dataset. Context:\n{context}\n\n"
    "Chat History:\n{chat_history}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

retriever = vector_db.as_retriever(search_kwargs={"k": 3})
question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

chat_history = []
while True:
    question = input("\nAsk your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    
    response = chain.invoke({
        "input": question,
        "chat_history": "\n".join(chat_history),
        "columns": list(df.columns)
    })
    
    answer = response['answer']
    print(f"\nAssistant: {answer}")
    
    if answer.startswith("EDIT||"):
        _, row_idx, col_name, new_value = answer.split("||")
        df.at[int(row_idx), col_name.strip()] = new_value.strip()
        save_data(df, file_path)
        df, documents = load_data(file_path)
        all_split = text_splitter.split_documents(documents)
        vector_db = FAISS.from_documents(all_split, embedding_model)
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        answer = f"Updated row {row_idx}, column {col_name} to {new_value}"
    
    chat_history.append(f"Human: {question}\nAssistant: {answer}")
