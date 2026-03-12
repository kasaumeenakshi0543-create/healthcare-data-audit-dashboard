import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Healthcare Data Quality & Bias Audit Dashboard")

st.write("Upload healthcare datasets to generate automated quality and bias reports.")

uploaded_files = st.file_uploader(
    "Upload CSV datasets",
    type=["csv"],
    accept_multiple_files=True
)

def detect_issues(df):

    issues = {}

    missing = df.isnull().sum()
    issues["missing_values"] = missing[missing > 0].to_dict()

    duplicates = df.duplicated().sum()
    issues["duplicates"] = duplicates

    if "Age" in df.columns:
        issues["age_under_18"] = len(df[df["Age"] < 18])
        issues["age_over_45"] = len(df[df["Age"] > 45])

    if "LOS" in df.columns:
        issues["los_less_2"] = len(df[df["LOS"] < 2])

    return issues


def calculate_score(issues):

    score = 100

    score -= len(issues["missing_values"]) * 5
    score -= issues["duplicates"] * 0.5
    score -= issues.get("age_under_18",0)
    score -= issues.get("age_over_45",0)
    score -= issues.get("los_less_2",0)

    return max(score,0)


results = []

if uploaded_files:

    for file in uploaded_files:

        df = pd.read_csv(file)

        st.header(file.name)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        issues = detect_issues(df)

        score = calculate_score(issues)

        st.subheader("Quality Score")
        st.metric("Dataset Quality Score", score)

        st.subheader("Issues Detected")
        st.write(issues)

        st.subheader("Missing Values Heatmap")

        fig, ax = plt.subplots(figsize=(8,4))
        sns.heatmap(df.isnull(), cbar=False, yticklabels=False)
        st.pyplot(fig)

        recommendations = []

        if issues["missing_values"]:
            recommendations.append("Handle missing values using imputation.")

        if issues["duplicates"] > 0:
            recommendations.append("Remove duplicate records.")

        if issues.get("age_under_18",0) > 0:
            recommendations.append("Check unrealistic age values.")

        if issues.get("los_less_2",0) > 0:
            recommendations.append("Verify short hospital stays.")

        if not recommendations:
            recommendations.append("Dataset appears clean.")

        st.subheader("Recommendations")

        for r in recommendations:
            st.write("-", r)

        results.append({
            "File": file.name,
            "Score": score,
            "Duplicates": issues["duplicates"]
        })

    st.header("Dataset Comparison Table")

    comparison = pd.DataFrame(results)

    st.dataframe(comparison)
