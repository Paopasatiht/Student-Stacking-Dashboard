# streamlit_app.py
import streamlit as st
import mysql.connector


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

