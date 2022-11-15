# streamlit_app.py
import pandas as pd
import streamlit as st
import plotly.express as px


# from student_stacking import my_sql

## Planning
## Step 0 : load the data


def insight_layout():
    st.title("Insight of student in our program")

    try:
        data = pd.read_csv('./database/sample data.csv')
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
    insight_layout()
