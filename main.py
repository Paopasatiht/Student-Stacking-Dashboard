# streamlit_app.py
import pandas as pd
import streamlit as st
from PIL import Image
import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def homepage_layout():
    st.title("SQL Playground Adaptation")

    menu = ['Home', "About us"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Homepage")

        image = Image.open('./assets/images/ER Diagram.png')
        st.image(image, caption='ER Diagram')

        # Column / Layout
        col1, col2 = st.columns(2)

        with col1:
            with st.form(key="query_form"):
                raw_code = st.text_area("SQL Code Here")
                submit_code = st.form_submit_button("Execute")

            if submit_code:
                query_result = run_query(raw_code)
                # Result
                with st.expander('Results'):
                    st.write(query_result)

        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(submit_code)
                with st.expander("Cool Dataframe"):
                    query_df = pd.DataFrame(query_result)
                    st.dataframe(query_df)

    elif choice == "About us":
        st.subheader("About us")
        st.write('''
        - Example Each type of user what data they gonna see
            \n-> Lecturer
            \n-> Out source
            \n-> Student

        1) Dashboard for Student
        -> INPUT
            \n-> Name of the student
        -> OUTPUT
            \n-> Stack of the student
                - dataframe
                - spider graph
                - bar plot 
                - Company Preference

        2) Insight summary
            \n- How many student possess the ... skills
                - bar plot
                    python 100
                    sql 20

            \n- How many student enroll the ... class
                - bar plot 
                    scim 2000 200
                    scim 2001 10

        3) Job Fair Feature
            \n- Who have sql score >= ... ( rank by each skills )
                - input 
                    skill
                    score_ratio
                - output
                    list of student name which pass the ratio
        ''')



if __name__ == '__main__':
    # conn = my_sql.init_connection()
    conn = init_connection()
    homepage_layout()





