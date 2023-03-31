import streamlit as st
import boto3
import os
import pandas as pd
import plotly.express as px

'''
# Baby Name Popularity Explorer :baby: :telescope:

An app to explore the popularity of U.S. baby names over time, from 1880 to 2020
'''

# Initialize S3 client for loading data
s3_client = boto3.client('s3')

@st.cache_data
def load_data(file_name):
    if not os.path.exists('data.csv'):
        s3_client.download_file('mostpoisonedname2020', file_name, 'data.csv')
    df = pd.read_csv('data.csv', index_col='year')
    names = df.columns
    return df, names

df, names = load_data('babynames_pcts_abrg.csv')

selected_names = st.multiselect('Type to select baby names to explore', names)

if len(selected_names) != 0:

    chart_data = df[selected_names]

    fig = px.line(
        chart_data, 
        labels={"year":"Year",  "value":"Percentage of year's total baby names", "variable":"Name"},
    )

    st.plotly_chart(fig)

'''
This app is based on data made available by the [U.S. Social Security Administration](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data)

To see the full code and statistical analyses behind this, check out the [Github repo](https://github.com/williecostello/MostPoisonedName2020)
'''