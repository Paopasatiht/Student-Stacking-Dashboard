import pandas as pd
import streamlit as st
import plotly.express as px
import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
## Planning
## Step 0 : load the data
st.title("SQL View for Each Group")

st.write('Admin')

st.write('1. All student information')
raw_code = """select s.student_id, s.student_fName, s.student_lName, s.age, s.gender, s.email, s.preference, 
u.uni_id, u.uni_name, u.uni_department, u.uni_program
from Students s, University u
where s.uni_id = u.uni_id;"""

query_result = run_query(raw_code)
data = pd.DataFrame(query_result)
st.dataframe(data)

st.write('2 All courses and its skill')
raw_code = """select c.course_id as CourseID, c.course_name as Course, s.skill_id as SkillID, 
t.skill_name as Skill, t.skill_type as Skill_Type, t.skill_score as Skill_Score
from Courses c, Stacking s, Skill_Types t 
where c.course_id = s.course_id and s.skill_id = t.skill_id;"""

query_result = run_query(raw_code)
data = pd.DataFrame(query_result)
st.dataframe(data)


st.write('3 All lectuerer and their affiliation')
raw_code = """select l.*, c.course_id, c.course_name,u.uni_department, u.uni_program, u.uni_name
from Lecturer l, Lecturer_Courses lc, University u, Courses c
where l.uni_id = u.uni_id and l.lecturer_id = lc.lecturer_id and lc.course_id = c.course_id;"""

query_result = run_query(raw_code)
data = pd.DataFrame(query_result)
st.dataframe(data)

st.write('#4 Company information')
raw_code = """select *
from Company;"""

query_result = run_query(raw_code)
data = pd.DataFrame(query_result)
st.dataframe(data)

