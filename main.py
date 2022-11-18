# streamlit_app.py
import pandas as pd
import streamlit as st
from PIL import Image
from student_stacking.my_sql import run_query
import time

def homepage_layout():
    st.title("SQL Playground Adaptation")
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


if __name__ == '__main__':
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

    homepage_layout()





