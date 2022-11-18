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
st.title("SQL Playground Adaptation")

raw_code = """select * 
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

students = list(data.student_fName.unique())
# Step 1 Choose student
selected_student = st.selectbox('Which Student You want to observe',
                                    students)
# Step 2 show their dream company
company_preference = data[data['student_fName'] == f'{selected_student}'].preference.to_list()
st.metric(label = 'Dream Company',
              value = f'{company_preference[0]}')

# Step 3 Show the dataframe of their skill stack
show_df = data.groupby(['student_fName', 'skill_type'])[['skill_score']].sum()
show_df = show_df.filter(regex=f'{selected_student}', axis=0)
st.write('Pure Stack Table')
st.dataframe(show_df)

# Step 4 Plot the stack skills
skill_df = data[data['student_fName'] == f'{selected_student}'].groupby('skill_type')[['skill_score']].sum()
score_list = skill_df.skill_score.to_list()
skill_list = skill_df.index.to_list()

score_df = pd.DataFrame(dict(
                                    r=score_list,
                                    theta=skill_list))
score_spider_fig = px.line_polar(score_df, r='r', theta='theta', line_close=True)
score_spider_fig.update_traces(fill='toself')
# Plot!
st.plotly_chart(score_spider_fig, use_container_width=True)

# Step 5 Plot as a bar chart
score_bar_fig = px.bar(skill_df, x=skill_df.index , y='skill_score')
st.plotly_chart(score_bar_fig, use_container_width=True)
