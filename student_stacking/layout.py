import pandas as pd
import streamlit as st
from student_stacking.my_sql import run_query, convert_df
import plotly.express as px


def personal_info():
    """
    this is the personal information page of the database project
    1. select box to choose the student name
    2. see each student's skills from the graph
    3. filter the skill that you want
    
    :return: streamlit personal info page
    """

    ## Step 0 : load the data
    st.title("Information of Each Student")

    raw_code = """select * 
                          from Enrollment as e, Stacking as stk, Students as s, Skill_Types as skill
                          where e.stack_id = stk.stack_id and e.student_id = s.student_id and stk.skill_id = skill.skill_id;"""
    query_result = run_query(raw_code)
    data = pd.DataFrame(query_result)
    data = data.rename(columns={0: "enroll_id",
                                1: "student_id_",
                                2: "stack_id",
                                3: "stack_id",
                                4: "course_id",
                                5: "skill_id",
                                6: "student_id",
                                7: "uni_id",
                                8: "student_fName",
                                9: "student_lName",
                                10: "age",
                                11: "gender",
                                12: "email",
                                13: "preference",
                                14: "skill_id",
                                15: "skill_name",
                                16: "skill_type",
                                17: "skill_score"})
    data = data.fillna(0)
    students = list(data.student_fName.unique())

    # Step 1 Choose student
    selected_student = st.selectbox('Which Student You want to observe',
                                    students)

    # Step 2 show their dream company
    company_preference = data[data['student_fName'] == f'{selected_student}'].preference.to_list()
    st.metric(label='Dream Company',
              value=f'{company_preference[0]}')

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
    st.plotly_chart(score_spider_fig, use_container_width=True)

    # Step 5 Plot as a bar chart
    score_bar_fig = px.bar(skill_df, x=skill_df.index, y='skill_score')
    st.plotly_chart(score_bar_fig, use_container_width=True)


def insight_layout():
    """
    Insight page
    1. show the amount of skills that each student have
    2. show the amount of the class that each student join

    :return: streamlit insight layout
    """
    st.title("Insight of student in our program")

    try:
        raw_code: str = """select * 
                      from Enrollment as e, Stacking as stk, Students as s, Skill_Types as skill
                      where e.stack_id = stk.stack_id and e.student_id = s.student_id and stk.skill_id = skill.skill_id;"""
        query_result = run_query(raw_code)
        data = pd.DataFrame(query_result)
        data = data.rename(columns={0: "enroll_id",
                                    1: "student_id_",
                                    2: "stack_id",
                                    3: "stack_id",
                                    4: "course_id",
                                    5: "skill_id",
                                    6: "student_id",
                                    7: "uni_id",
                                    8: "student_fName",
                                    9: "student_lName",
                                    10: "age",
                                    11: "gender",
                                    12: "email",
                                    13: "preference",
                                    14: "skill_id",
                                    15: "skill_name",
                                    16: "skill_type",
                                    17: "skill_score"})
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

    show_filter_df = filter_df[filter_df['skill_type'] == f'{option}'][filter_df['skill_score'] >= score_ratio]
    st.dataframe(show_filter_df)


def admin_view():
    """
    Admin view
    1. show All student information
    2. All courses and its skill
    3. All lectuerer and their affiliation
    4 Company information
    :return: streamlit page of the admin view
    """
    ## Planning
    ## Step 0 : load the data
    st.title("SQL View for Each Group")

    st.header('Admin')

    st.write('1. All student information')
    raw_code = """select s.student_id, s.student_fName, s.student_lName, s.age, s.gender, s.email, s.preference, 
    u.uni_id, u.uni_name, u.uni_department, u.uni_program
    from Students s, University u
    where s.uni_id = u.uni_id;"""

    query_result = run_query(raw_code)
    data = pd.DataFrame(query_result)
    st.dataframe(data)

    csv = convert_df(data)
    st.download_button(
        label="Download data as csv",
        data=csv,
        file_name="all_student.csv",
        mime="text/csv"

    )

    st.write('2 All courses and its skill')
    raw_code = """select c.course_id as CourseID, c.course_name as Course, s.skill_id as SkillID, 
    t.skill_name as Skill, t.skill_type as Skill_Type, t.skill_score as Skill_Score
    from Courses c, Stacking s, Skill_Types t 
    where c.course_id = s.course_id and s.skill_id = t.skill_id;"""

    query_result = run_query(raw_code)
    data = pd.DataFrame(query_result)
    st.dataframe(data)

    csv = convert_df(data)
    st.download_button(
        label="Download data as csv",
        data=csv,
        file_name="all_courses_and_skills.csv",
        mime="text/csv"

    )


    st.write('3 All lectuerer and their affiliation')
    raw_code = """select l.*, c.course_id, c.course_name,u.uni_department, u.uni_program, u.uni_name
    from Lecturer l, Lecturer_Courses lc, University u, Courses c
    where l.uni_id = u.uni_id and l.lecturer_id = lc.lecturer_id and lc.course_id = c.course_id;"""

    query_result = run_query(raw_code)
    data = pd.DataFrame(query_result)
    st.dataframe(data)

    csv = convert_df(data)
    st.download_button(
        label="Download data as csv",
        data=csv,
        file_name="all_lectuerer_and_affiliation.csv",
        mime="text/csv"

    )

    st.write('4 Company information')
    raw_code = """select *
    from Company;"""

    query_result = run_query(raw_code)
    data = pd.DataFrame(query_result)
    st.dataframe(data)

    csv = convert_df(data)
    st.download_button(
        label="Download data as csv",
        data=csv,
        file_name="company_information.csv",
        mime="text/csv"

    )
