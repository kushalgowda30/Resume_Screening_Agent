import os
import tempfile
import pandas as pd
import streamlit as st
import plotly.express as px

from src.resume_parser import extract_resume_text
from src.jd_parser import read_job_description
from src.similarity import calculate_similarity
from src.llm_reason import analyze_resume

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

h1{
    color:#4CAF50;
    text-align:center;
}

h3{
    text-align:center;
}

div[data-testid="metric-container"]{
    background:#1E293B;
    padding:20px;
    border-radius:15px;
    border:1px solid #3B82F6;
    box-shadow:0px 0px 10px rgba(0,0,0,.3);
}

.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    background:#2563EB;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.stDownloadButton>button{
    width:100%;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Resume Screening Dashboard")
st.markdown("### AI-powered Resume Ranking System")

st.divider()

jd_file = st.file_uploader(
    "📄 Upload Job Description (.txt)",
    type=["txt"]
)

resume_files = st.file_uploader(
    "📁 Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("🚀 Analyze Resumes"):

    if jd_file is None or len(resume_files) == 0:
        st.warning("Please upload both Job Description and Resume PDFs.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_jd:
        temp_jd.write(jd_file.read())
        jd_path = temp_jd.name

    jd_text = read_job_description(jd_path)

    results = []

    progress = st.progress(0)
    status = st.empty()

    for i, resume in enumerate(resume_files):

        status.write(f"Analyzing {resume.name}...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_resume:
            temp_resume.write(resume.read())
            resume_path = temp_resume.name

        resume_text = extract_resume_text(resume_path)

        raw_score = calculate_similarity(resume_text, jd_text)

        score = raw_score * 0.5 + 60
        score = min(score, 97)

        if score >= 95:
            recommendation = "Excellent Match"
        elif score >= 90:
            recommendation = "Strong Match"
        elif score >= 80:
            recommendation = "Good Match"
        else:
            recommendation = "Needs Improvement"

        results.append({
        "Resume": resume.name,
        "Score": round(score, 2),
        "Recommendation": recommendation,
        "ResumeText": resume_text
        })

        progress.progress((i + 1) / len(resume_files))

    status.empty()

    progress.empty()    

    df = pd.DataFrame(results)
    df = df.sort_values("Score", ascending=False).reset_index(drop=True)

    df.insert(0, "Rank", range(1, len(df) + 1))

    # Save results in session
    st.session_state["df"] = df
    st.session_state["jd_text"] = jd_text

    st.success("✅ Analysis Completed!")

    st.balloons()

    st.divider()

    # Metrics
    highest = df.iloc[0]["Score"]
    average = round(df["Score"].mean(), 2)
    best = df.iloc[0]["Resume"]
    total = len(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Total", total)
    col2.metric("🏆 Highest", f"{highest:.2f}%")
    col3.metric("📈 Average", f"{average:.2f}%")
    col4.metric("🥇 Best", best)

    st.info(
    f"🏆 Best Candidate: **{best}** with **{highest:.2f}%** match."
    )

    st.divider()

    # -----------------------------
    # Search & Filter
    # -----------------------------
    st.subheader("🔍 Search & Filter")

    search = st.text_input("Search Candidate")

    recommendation_filter = st.selectbox(
        "Recommendation",
        ["All"] + sorted(df["Recommendation"].unique())
    )

    minimum_score = st.slider(
        "Minimum Score",
        60,
        100,
        80
    )

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Resume"].str.contains(search, case=False)
        ]

    if recommendation_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Recommendation"] == recommendation_filter
        ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= minimum_score
    ]

    display_df = filtered_df.drop(columns=["ResumeText"])

    st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

    st.divider()

    # -----------------------------
    # Top Candidates Chart
    # -----------------------------
    st.subheader("📈 Top 10 Candidates")

    fig = px.bar(
    df.head(10),
    x="Score",
    y="Resume",
    orientation="h",
    color="Score",
    text=df.head(10)["Score"].round(2),
    title="Top 10 Candidates"
)

    fig.update_layout(
    height=700,
    font=dict(size=14),
    title_x=0.5
)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Recommendation Distribution
    # -----------------------------
    st.subheader("🥧 Recommendation Distribution")

    pie = px.pie(
    df,
    names="Recommendation",
    title="Recommendation Distribution"
    )

    pie.update_layout(title_x=0.5)

    pie.update_traces(
    textposition="inside",
    textinfo="percent+label"
    )

    st.plotly_chart(pie, use_container_width=True)

    st.divider()

    # -----------------------------
    # Save Reports
    # -----------------------------
    os.makedirs("output", exist_ok=True)

    excel_path = "output/screening_results.xlsx"

    export_df = df.drop(columns=["ResumeText"])

    export_df.to_excel(excel_path, index=False)

    with open(excel_path, "rb") as file:

        st.download_button(
            label="📥 Download Excel",
            data=file,
            file_name="screening_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    csv = export_df.to_csv(index=False).encode()

    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name="screening_results.csv",
        mime="text/csv"
    )

    st.divider()

    # -----------------------------
    # Footer
    # -----------------------------
    st.markdown(
        """
        <center>
        <h4>Developed by Suhas Gowda</h4>
        AI Resume Screening Dashboard | Rooman HireAI Project
        </center>
        """,
        unsafe_allow_html=True
    )