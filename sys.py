import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

st.set_page_config(page_title="DataSys – Smart Data System", layout="wide")

st.markdown("""
    <style>
        .title-container {
            background-color: #222;
            padding: 20px;
            border-radius: 12px;
            border: 2px solid goldenrod;
            text-align: center;
            margin-bottom: 30px;
        }
        .title-container h1 {
            color: goldenrod;
            font-size: 2.5em;
        }
        .stButton>button {
            background-color: #444;
            color: goldenrod;
            border: 1px solid goldenrod;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: goldenrod;
            color: black;
        }
    </style>
    <div class='title-container'>
        <h1>📊 DataSys – Smart Data Cleaner & Visualizer</h1>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# ✅ تنظيف البيانات + إزالة القيم الشاذة داخل نفس الدالة
def clean_data_with_report(df, threshold=0.7):
    total_rows = df.shape[0]
    report = []

    # تنظيف البيانات
    for col in df.columns:
        missing_ratio = df[col].isnull().sum() / total_rows
        if missing_ratio > threshold:
            df.drop(columns=col, inplace=True)
            report.append(f"🗑️ Column '{col}' dropped (missing: {missing_ratio:.0%})")
        else:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                fill_value = df[col].mode()[0]
                df[col].fillna(fill_value, inplace=True)
                report.append(f"🟠 Filled categorical column '{col}' with mode: {fill_value}")
            else:
                fill_value = df[col].mean()
                df[col].fillna(fill_value, inplace=True)
                report.append(f"🔵 Filled numeric column '{col}' with mean: {fill_value:.2f}")

    # إزالة outliers
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        original_count = df.shape[0]
        df = df[(df[col] >= lower) & (df[col] <= upper)]
        removed = original_count - df.shape[0]
        if removed > 0:
            report.append(f"⚠️ Removed {removed} outliers from column '{col}'")

    return df, report

# Scatter Plot
def plot_scatter_plots(df, title="Scatter Plots"):
    st.subheader(f"📈 {title}")
    numeric_cols = df.select_dtypes(include='number').columns
    pairs = list(combinations(numeric_cols, 2))
    if len(pairs) == 0:
        st.warning("⚠️ Not enough numeric columns to generate scatter plots.")
    else:
        for x, y in pairs:
            with st.expander(f"Scatter: {x} vs {y}"):
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=x, y=y, ax=ax)
                ax.set_title(f"{x} vs {y}")
                plt.tight_layout()
                st.pyplot(fig)

# Regression Plot
def plot_regression_plots(df, title="Regression Plots"):
    st.subheader(f"📉 {title}")
    numeric_cols = df.select_dtypes(include='number').columns
    pairs = list(combinations(numeric_cols, 2))
    if len(pairs) == 0:
        st.warning("⚠️ Not enough numeric columns to generate regression plots.")
    else:
        for x, y in pairs:
            with st.expander(f"Regression: {x} vs {y}"):
                fig, ax = plt.subplots()
                sns.regplot(data=df, x=x, y=y, ax=ax, scatter_kws={"s": 10}, line_kws={"color":"red"})
                ax.set_title(f"{x} vs {y} (Regression)")
                plt.tight_layout()
                st.pyplot(fig)

# واجهة التطبيق
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("🧾 Preview of the First 5 Rows")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)
    with col1:
        visualize_btn = st.button("🔍 Visualize Without Cleaning")
    with col2:
        clean_btn = st.button("🧼 Clean & Visualize")

    if visualize_btn:
        plot_scatter_plots(df, "Scatter Plots (Raw Data)")
        plot_regression_plots(df, "Regression Plots (Raw Data)")

    elif clean_btn:
        cleaned_df, report = clean_data_with_report(df.copy())
        st.subheader("🧾 Cleaning Report")
        for step in report:
            st.write("•", step)

        plot_scatter_plots(cleaned_df, "Scatter Plots (Cleaned Data)")
        plot_regression_plots(cleaned_df, "Regression Plots (Cleaned Data)")

        st.subheader("✅ Cleaned Data Preview (First 5 Rows)")
        st.dataframe(cleaned_df.head())

        csv = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Cleaned CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")
else:
    st.info("📌 Please upload a CSV file to begin.")
