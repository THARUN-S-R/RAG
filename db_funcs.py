import sqlite3
from datetime import datetime

DB_NAME = 'danucore.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     user_query TEXT,
                     LLM_response TEXT,
                     model TEXT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

def ins_application_log(session_id,user_query,llm_response,model):
    conn = get_db_connection()
    conn.execute('INSERT INTO application_logs (session_id, user_query, LLM_response, model) VALUES (?, ?, ?, ?)',
                 (session_id, user_query, llm_response, model))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, LLM_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role": "human", "content": row['user_query']},
            {"role": "ai", "content": row['LLM_response']}
        ])
    conn.close()
    return messages
def get_all_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, LLM_response,session_id,id,created_at FROM application_logs  ORDER BY created_at desc LIMIT 9')
    messages = []
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        messages.extend([
            {"user_query": row['user_query'], "id": str(row['id']),'LLM_response':row['LLM_response'],'created_at':row['created_at'],'session_id':row['session_id']},
            #{"role": "ai", "content": row['LLM_response']}
        ])
    return messages
    
    
    

create_application()