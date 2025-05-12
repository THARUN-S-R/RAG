from fastapi import FastAPI, File, UploadFile, HTTPException
from langchain_funcs import get_rag_chain
from db_funcs import ins_application_log, get_chat_history,get_all_logs
from vector_funcs import load_documents
import os
import uvicorn
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid
import logging
import debugpy
from langchain.callbacks.tracers import LangChainTracer

# debugpy.listen(("0.0.0.0", 5690))  # Listen on port 5678
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client() 

logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI()
os.environ['GROQ_API_KEY']= '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'
os.environ['LANCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = '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'
os.environ['LANGCHAIN_PROJECT'] = 'danucore2'
tracer = LangChainTracer(project_name="danucore2")
#session_id = ''

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: str = Field(default='llama3-8b-8192')

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: str

class hist(BaseModel):
    user_query: str
    LLM_response : str
    session_id: str
    id : str
    created_at: datetime

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    #global session_id

    #if query_input.session_id:
    session_id = query_input.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model}")
    
    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(query_input.model)
    answer = rag_chain.invoke({
        "input": query_input.question,
        "chat_history": chat_history
    },config={"callbacks": [tracer]})['answer']
    ins_application_log(session_id, query_input.question, answer, query_input.model)
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)

@app.get("/hist", response_model=list[hist])
def get_hist():
    return get_all_logs()

def run_app():
    os.environ['GROQ_API_KEY']= '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'
    os.environ['LANCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_API_KEY'] = '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'
    os.environ['LANGCHAIN_PROJECT'] = 'danucore2'

    load_documents('D:\\danucore\\project_work\\docs')
    uvicorn.run(app,host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_app()
    
    


