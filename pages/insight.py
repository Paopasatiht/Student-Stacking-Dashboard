# streamlit_app.py
import pandas as pd
import streamlit as st
import plotly.express as px
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
## Planning
## Step 0 : load the data


def insight_layout():
    st.title("Insight of student in our program")

    try:
        raw_code: str = """select * 
                      from Enrollment as e, Stacking as stk, Students as s, Skill_Types as skill
                      where e.stack_id = stk.stack_id and e.student_id = s.student_id and stk.skill_id = skill.skill_id;"""
        query_result = run_query(raw_code)
        data = pd.DataFrame(query_result)
        data = data.rename(columns={0:"enroll_id",
                           1:"student_id_",
                           2:"stack_id",
                           3:"stack_id",
                           4:"course_id",
                           5:"skill_id",
                           6:"student_id",
                           7:"uni_id",
                           8:"student_fName",
                           9:"student_lName",
                           10:"age",
                           11:"gender",
                           12:"email",
                           13:"preference",
                           14:"skill_id",
                           15:"skill_name",
                           16:"skill_type",
                           17:"skill_score"})
        data = data.fillna(0)
    except:
        data = pd.read_csv('./database/sample data.csv')

    skill_count = data.groupby(['skill_name'])[['student_id']].count()

    # Step 1 skill in the bar chart format
    skill_bar_fig = px.bar(skill_count, x=skill_count.index, y='student_id')
    st.plotly_chart(skill_bar_fig, use_container_width=True)

    # Step 2 enroll bar chart
    enroll_count = data.groupby(['course_id'])[['student_id']].count()
    enroll_bar_fig = px.bar(enroll_count, x=enroll_count.index, y='student_id')
    st.plotly_chart(enroll_bar_fig, use_container_width=True)

    # Step 3 filter the ratio skill that you want
    filter_df = data.groupby(['student_fName', 'skill_type'])[['skill_score']].sum()
    filter_df = filter_df.reset_index()

    option = st.selectbox(
        'Skill that you want to filter',
        filter_df.skill_type.unique().tolist()
    )

    score_ratio = st.slider('Score that you want', 0, 3, 1)

    show_filteref_df = filter_df[filter_df['skill_type'] == f'{option}'][filter_df['skill_score'] >= score_ratio]
    st.dataframe(show_filteref_df)


if __name__ == '__main__':
    # conn = my_sql.init_connection()
    conn = init_connection()
    insight_layout()
