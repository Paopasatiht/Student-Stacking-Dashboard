# streamlit_app.py
import pandas as pd
import streamlit as st
import plotly.express as px


# from student_stacking import my_sql

## Planning
## Step 0 : load the data


def feature_layout():
    st.title("SQL Playground Adaptation")

    try:
        data = pd.read_csv('./database/sample data.csv')
    except:
        data = pd.read_csv('./database/sample data.csv')

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


if __name__ == '__main__':
    # conn = my_sql.init_connection()
    feature_layout()
