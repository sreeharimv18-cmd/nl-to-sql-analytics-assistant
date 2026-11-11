import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq

# 1. Page Setup
st.set_page_config(page_title="NL-to-SQL Assistant", layout="centered")
st.title("Natural Language to SQL Assistant")
st.write("Ask questions about the student placement database in plain English.")

# 2. Sidebar for Groq API Key & Table Preview
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    
    st.subheader("Database Table: students")
    st.code("Columns: id, name, branch, cgpa, package_lpa")

# 3. Function to Ask Groq AI to Write SQL
def get_sql_from_ai(question, groq_key):
    client = Groq(api_key=groq_key)
    
    prompt = f"""
    Convert the user's question into a valid SQLite SELECT query for the table below.
    Table name: students
    Columns: id (INTEGER), name (TEXT), branch (TEXT), cgpa (REAL), package_lpa (REAL)
    
    Rules:
    - Return ONLY the raw SQL query. Do not add markdown (```sql) or explanations.
    - Only use SELECT queries. Never use DROP, DELETE, UPDATE, or INSERT.
    
    Question: {question}
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# 4. Main App Interface
sample_questions = [
    "Show all students in CSE branch",
    "Who has the highest package?",
    "Show average package by branch",
    "List students with CGPA above 8.5"
]

choice = st.selectbox("Pick a sample question (or type your own below):", [""] + sample_questions)
user_question = st.text_input("Your Question:", value=choice)

if st.button("Run Query", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API Key in the left sidebar first.")
    elif not user_question.strip():
        st.warning("Please type or select a question.")
    else:
        try:
            # Step A: Generate SQL using Groq
            sql_query = get_sql_from_ai(user_question, api_key)
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")
            
            # Step B: Safety Check (Allow only SELECT)
            if not sql_query.upper().startswith("SELECT"):
                st.error("Security Block: Only SELECT queries are allowed.")
            else:
                # Step C: Run SQL on placement.db and show table
                conn = sqlite3.connect("placement.db")
                df = pd.read_sql_query(sql_query, conn)
                conn.close()
                
                st.subheader("Results")
                st.dataframe(df, use_container_width=True)
                
                # Step D: Show a bar chart if there are 2 columns (text + number)
                if len(df.columns) == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                    st.subheader("Chart")
                    st.bar_chart(df.set_index(df.columns[0]))
                    
        except Exception as e:
            st.error(f"Something went wrong: {e}")