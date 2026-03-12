import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Healthcare Data Quality & Bias Audit Dashboard")

uploaded_files = st.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)

        st.subheader(file.name)

        st.dataframe(df.head())

        st.subheader("Missing Values Heatmap")

        fig, ax = plt.subplots()
        sns.heatmap(df.isnull(), cbar=False, yticklabels=False)
        st.pyplot(fig)
