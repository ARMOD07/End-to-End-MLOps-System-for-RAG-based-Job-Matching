import streamlit as st
import requests
import json
from pathlib import Path
import plotly.graph_objects as go

st.set_page_config(page_title="Job Matching System", layout="wide")

# API endpoint
API_URL = "http://localhost:8000"

st.title("🚀 AI-Powered Job Matching System")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_endpoint = st.text_input("API Endpoint", API_URL)
    
    st.header("About")
    st.info("""
    This system uses:
    - Sentence Transformers for embeddings
    - FAISS for similarity search
    - LLM for reasoning
    - MLflow for experiment tracking
    """)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Job Offer")
    job_input_method = st.radio("Input method:", ["Upload PDF", "Paste Text"])
    
    job_text = ""
    if job_input_method == "Upload PDF":
        job_file = st.file_uploader("Upload job description", type=['pdf', 'txt'])
        if job_file:
            job_text = job_file.read().decode()
            st.text_area("Preview", job_text[:500], height=200)
    else:
        job_text = st.text_area("Paste job description", height=300)

with col2:
    st.subheader("👤 CV / Resume")
    cv_input_method = st.radio("Input method:", ["Upload PDF", "Paste Text"])
    
    cv_text = ""
    if cv_input_method == "Upload PDF":
        cv_file = st.file_uploader("Upload CV", type=['pdf', 'txt'])
        if cv_file:
            cv_text = cv_file.read().decode()
            st.text_area("Preview", cv_text[:500], height=200)
    else:
        cv_text = st.text_area("Paste CV", height=300)

# Match button
if st.button("🔍 Analyze Match", type="primary"):
    if job_text and cv_text:
        with st.spinner("Analyzing..."):
            response = requests.post(
                f"{api_endpoint}/api/v1/match",
                json={"job_text": job_text, "cv_text": cv_text}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.success("Analysis Complete!")
                
                # Metrics row
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Match Score", f"{result['match_score']}%")
                with col2:
                    st.metric("Similarity", f"{result['similarity_score']}%")
                with col3:
                    st.metric("Skills Match", f"{result['skills_match_score']}%")
                with col4:
                    st.metric("Decision", result['decision'])
                
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['match_score'],
                    title={'text': "Overall Match"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [
                               {'range': [0, 40], 'color': "red"},
                               {'range': [40, 70], 'color': "orange"},
                               {'range': [70, 100], 'color': "green"}]}
                ))
                st.plotly_chart(fig)
                
                # Strengths and Gaps
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Strengths")
                    for strength in result['strengths']:
                        st.success(f"• {strength}")
                
                with col2:
                    st.subheader("⚠️ Gaps")
                    for gap in result['gaps']:
                        st.warning(f"• {gap}")
                
                # Suggestions
                st.subheader("📈 Improvement Suggestions")
                for suggestion in result['improvement_suggestions']:
                    st.info(f"💡 {suggestion}")
                
            else:
                st.error(f"Error: {response.status_code}")
    else:
        st.warning("Please provide both job offer and CV")