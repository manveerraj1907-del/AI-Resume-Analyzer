# =========================================================
# AI Resume Analyzer
# Powered by Hire Nexus
# Author: M.R
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pypdf import PdfReader
from google import genai
import os
import json
import re
from dotenv import load_dotenv

# Load secret API key from .env file
load_dotenv()

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="AI Resume Analyzer | M.R",
    page_icon="🤖",
    layout="wide"
)

# ----------------- Styling -----------------
st.markdown("""
    <style>
    :root {
        --neon-cyan: #22d3ee;
        --neon-lime: #a3e635;
        --neon-violet: #c084fc;
        --ink: #070b12;
        --panel: #0d1520;
        --muted: #8fa3b8;
    }

    /* Global */
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(34,211,238,0.10), transparent 28rem),
            radial-gradient(circle at 92% 12%, rgba(163,230,53,0.07), transparent 24rem),
            var(--ink);
    }
    body {
        background: var(--ink);
        color: #e5e7eb;
        font-family: "Inter", system-ui, -apple-system, sans-serif;
    }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(34,211,238,0.14), rgba(163,230,53,0.08));
        border: 1px solid rgba(34,211,238,0.35);
        box-shadow: 0 0 32px rgba(34,211,238,0.08);
        border-radius: 20px;
        padding: 36px 28px;
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: clamp(2rem, 4vw, 3.4rem);
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0;
        margin-bottom: 6px;
    }
    .hero::after {
        content: "AI / SCREENING / SIGNAL";
        position: absolute;
        top: 18px;
        right: 22px;
        color: rgba(34,211,238,0.6);
        font: 700 0.65rem/1 "Courier New", monospace;
        letter-spacing: 0.18em;
    }
    .hero-kicker {
        color: var(--neon-lime);
        font: 700 0.7rem/1 "Courier New", monospace;
        letter-spacing: 0.2em;
        margin-bottom: 14px;
        text-transform: uppercase;
    }
    .hero-title span {
        color: var(--neon-cyan);
        text-shadow: 0 0 18px rgba(34,211,238,0.45);
    }
    .hero-sub {
        color: #9ca3af;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Section titles */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin: 22px 0 10px 0;
    }
    .section-number {
        display: inline-grid;
        place-items: center;
        width: 28px;
        height: 28px;
        border: 1px solid rgba(34,211,238,0.55);
        border-radius: 8px;
        color: var(--neon-cyan);
        font: 700 0.72rem/1 "Courier New", monospace;
        box-shadow: 0 0 12px rgba(34,211,238,0.14);
    }

    /* Cards */
    .card {
        background: rgba(13,21,32,0.86);
        border: 1px solid rgba(34,211,238,0.14);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .card-title {
        color: #f3f4f6;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .card-text {
        color: #9ca3af;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Footer credit */
    .mr-credit {
        position: fixed;
        bottom: 10px;
        right: 14px;
        font-size: 0.75rem;
        color: #6b7280;
        opacity: 0.8;
        z-index: 9999;
    }

    .stButton > button[kind="primary"] {
        background: var(--neon-cyan);
        border-color: var(--neon-cyan);
        color: var(--ink);
        box-shadow: 0 0 18px rgba(34,211,238,0.28);
        font-weight: 800;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--neon-lime);
        border-color: var(--neon-lime);
        box-shadow: 0 0 22px rgba(163,230,53,0.34);
    }
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stTextArea"] textarea,
    [data-baseweb="select"] > div {
        background: var(--panel);
        border-color: rgba(34,211,238,0.24);
    }
    [data-testid="stMetricValue"] {
        color: var(--neon-lime);
        text-shadow: 0 0 14px rgba(163,230,53,0.3);
    }
    [data-testid="stMetric"] {
        background: rgba(13,21,32,0.72);
        border: 1px solid rgba(34,211,238,0.16);
        border-radius: 12px;
        padding: 14px 16px;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(34,211,238,0.18);
        border-radius: 12px;
        overflow: hidden;
    }
    .stDownloadButton > button {
        border-color: rgba(34,211,238,0.28);
        background: rgba(13,21,32,0.8);
    }
    .stDownloadButton > button:hover {
        border-color: var(--neon-lime);
        color: var(--neon-lime);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Helpers -----------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "
    return text.strip()

# ---------------------------------------------------------
# AI Resume Analyzer - Core Logic
# Author: M.R
# ---------------------------------------------------------

def evaluate_resume_with_gemini(filename, resume_text, role, job_desc=""):
    api_keys = [
        os.getenv("GEMINI_API_KEY_1", "").strip("'\""),
        os.getenv("GEMINI_API_KEY_2", "").strip("'\""),
        os.getenv("GEMINI_API_KEY_3", "").strip("'\""),
    ]
    api_keys = [key for key in api_keys if key]

    if not api_keys:
        return {
            "Candidate File": filename,
            "ATS Score": 0,
            "Experience Score": 0,
            "Skill Score": 0,
            "Status": "API Keys Missing ❌",
            "Top Strengths": "N/A",
            "Skill Gaps": "N/A",
            "Ranking Explanation": "No API keys found in .env file.",
        }

    prompt = f"""
You are an expert resume screening AI.

Analyze this resume for the role: {role}
Job requirements: {job_desc or "Standard qualifications for " + role}
Resume: {resume_text}

Use only information present in the resume. Return only valid JSON with these keys:
ats_score, experience_score, skill_score, top_strengths, skill_gaps, explanation.
"""

    last_error = ""
    for api_key in api_keys:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            raw_text = re.sub(r"```(?:json)?", "", response.text, flags=re.IGNORECASE).strip()
            json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if not json_match:
                raise ValueError("AI did not return valid JSON.")

            data = json.loads(json_match.group(0))
            ats_score = max(0, min(100, int(data.get("ats_score", 50))))
            experience_score = max(0, min(100, int(data.get("experience_score", 50))))
            skill_score = max(0, min(100, int(data.get("skill_score", 50))))
            status = (
                "Tier 1: High Fit 🟢" if ats_score >= 75
                else "Tier 2: Medium Fit 🟡" if ats_score >= 50
                else "Tier 3: Low Fit 🔴"
            )
            return {
                "Candidate File": filename,
                "ATS Score": ats_score,
                "Experience Score": experience_score,
                "Skill Score": skill_score,
                "Status": status,
                "Top Strengths": data.get("top_strengths", "N/A"),
                "Skill Gaps": data.get("skill_gaps", "N/A"),
                "Ranking Explanation": data.get("explanation", "Evaluation completed successfully."),
            }
        except Exception as error:
            last_error = str(error)

    error_text = last_error.lower()
    if "resource_exhausted" in error_text or "resource exhausted" in error_text or "quota" in error_text or "429" in error_text:
        failure_status = "API Quota Exhausted ⚠️"
        failure_explanation = (
            "Gemini rejected the request because the API quota or rate limit was reached. "
            "Check your Google AI Studio billing, quota, or wait before trying again. "
            "Last error: " + last_error
        )
    else:
        failure_status = "All API Keys Failed ❌"
        failure_explanation = "All configured API keys failed. Last error: " + last_error

    return {
        "Candidate File": filename,
        "ATS Score": 0,
        "Experience Score": 0,
        "Skill Score": 0,
        "Status": failure_status,
        "Top Strengths": "N/A",
        "Skill Gaps": "N/A",
        "Ranking Explanation": failure_explanation,
    }

# ----------------- Hero Section -----------------
st.markdown(
    """
  <div class="hero">
      <div class="hero-kicker">Hire Nexus / Candidate intelligence</div>
        <div class="hero-title">AI Resume <span>Analyzer</span></div>
        <div class="hero-sub">
            Structured screening for modern hiring teams.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Controls -----------------
st.markdown('<div class="section-title"><span class="section-number">01</span> Set job role & requirements</div>', unsafe_allow_html=True)

col_role, col_jd = st.columns([1, 2], gap="large")

with col_role:
    target_role = st.selectbox(
        "Target Job Role",
        [
            "Software Engineer",
            "Data Scientist",
            "AI/ML Engineer",
            "Web Developer",
            "DevOps Engineer",
            "Backend Engineer",
            "Frontend Engineer",
            "Full Stack Engineer",
        ],
    )

with col_jd:
    custom_jd = st.text_area(
        "Optional: Paste key requirements / keywords",
        placeholder="e.g., Python, SQL, REST APIs, Docker, AWS, system design...",
        height=80,
    )

st.markdown('<div class="section-title"><span class="section-number">02</span> Upload candidate resumes (PDF)</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} resume(s) uploaded.")
    if st.button("⚡ Analyze & Rank Candidates", type="primary", use_container_width=True):
        evaluations = []
        with st.spinner("Analyzing resumes with Hire Nexus AI..."):
            for pdf in uploaded_files:
                txt = extract_text_from_pdf(pdf)
                res = evaluate_resume_with_gemini(pdf.name, txt, target_role, custom_jd or "")
                evaluations.append(res)

        df = pd.DataFrame(evaluations)
        df = df.sort_values(by="ATS Score", ascending=True).reset_index(drop=True)
        df.insert(0, "Rank", range(1, 1 + len(df)))
        st.session_state["eval_df"] = df
        st.rerun()

# ----------------- Results -----------------
if "eval_df" in st.session_state:
    df = st.session_state["eval_df"]

    st.markdown('<div class="section-title"><span class="section-number">03</span> Ranked candidates</div>', unsafe_allow_html=True)

    # Top metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Resumes", len(df))
    m2.metric("Best ATS Score", f"{df['ATS Score'].max()}%" if not df.empty else "0%")
    m3.metric("Average ATS Score", f"{round(df['ATS Score'].mean(), 1)}%" if not df.empty else "0%")

    st.divider()

    # Leaderboard table
    st.markdown('<div class="card"><div class="card-title">🏆 Candidate Leaderboard</div></div>', unsafe_allow_html=True)
    st.dataframe(
        df[["Rank", "Candidate File", "ATS Score", "Status", "Top Strengths", "Skill Gaps"]],
        use_container_width=True,
        hide_index=True,
    )

    # Export buttons
    col_csv, col_txt = st.columns(2)
    with col_csv:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export as CSV",
            data=csv_data,
            file_name="ai_resume_analyzer_rankings.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_txt:
        rep_text = f"=== AI RESUME ANALYZER REPORT ({target_role}) ===\nGenerated by Hire Nexus\n\n"
        for _, row in df.iterrows():
            rep_text += (
                f"RANK {row['Rank']}: {row['Candidate File']}\n"
                f"Score: {row['ATS Score']}%\n"
                f"Status: {row['Status']}\n"
                f"Strengths: {row['Top Strengths']}\n"
                f"Gaps: {row['Skill Gaps']}\n"
                f"Explanation: {row['Ranking Explanation']}\n\n"
            )
        st.download_button(
            "📄 Export Summary (.TXT)",
            data=rep_text,
            file_name="ai_resume_analyzer_summary.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # Optional: simple chart
    st.markdown('<div class="section-title">Score breakdown</div>', unsafe_allow_html=True)
    if not df.empty:
        fig = px.bar(
            df,
            x="Candidate File",
            y=["ATS Score", "Skill Score", "Experience Score"],
            barmode="group",
            color_discrete_sequence=["#22d3ee", "#a3e635", "#c084fc"],
        )
        fig.update_layout(
            paper_bgcolor="#0b0f19",
            plot_bgcolor="#0f1420",
            font_color="#e5e7eb",
            legend_title_text="Score Type",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed justifications
    st.markdown('<div class="section-title">Detailed AI explanations</div>', unsafe_allow_html=True)
    for _, row in df.iterrows():
        with st.expander(
            f"Rank {row['Rank']}: {row['Candidate File']} — {row['ATS Score']}% ({row['Status']})"
        ):
            st.write(f"**Explanation:** {row['Ranking Explanation']}")
            st.write(f"**Top Strengths:** {row['Top Strengths']}")
            st.write(f"**Missing Skill Gaps:** {row['Skill Gaps']}")

else:
    st.info("Upload resumes above and click “Analyze & Rank Candidates” to see results.")

# ----------------- Footer Credit (M.R) -----------------
st.markdown(
    """
    <div class="mr-credit">
        Hire Nexus · AI Resume Analyzer
    </div>
    """,
    unsafe_allow_html=True,
)



# ---------------------------------------------------------
# AI Resume Analyzer - End of Core Logic
# Author: M.R
#---------------------------------------------------------
