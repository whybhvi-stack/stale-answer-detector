import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))
from main import run_stale_answer_detector

st.set_page_config(page_title="Stale-Answer Detector", page_icon="🔍", layout="wide")

st.title("🔍 Stale-Answer Detector")
st.markdown("Paste any AI-generated answer below, and we will extract its claims, search the live web, and score its freshness.")

with st.form("check_form"):
    ai_answer = st.text_area(
        "Paste AI Answer Here:",
        height=150,
        placeholder="Example: Twitter is currently led by CEO Jack Dorsey. The OpenAI GPT-4 API currently costs 0.03 per 1,000 input tokens. Water boils at 100 degrees Celsius at sea level."
    )
    submitted = st.form_submit_button("Check Freshness", type="primary", use_container_width=True)

if submitted:
    if not ai_answer.strip():
        st.warning("Please paste an AI answer first!")
    else:
        with st.spinner("Extracting claims, searching the web, and verifying facts..."):
            results = run_stale_answer_detector(ai_answer)
            
            if results:
                st.success("Analysis Complete!")
                
                total_score = sum(r["freshness_score"] for r in results)
                avg_score = total_score / len(results)
                
                if avg_score >= 80:
                    st.metric("Overall Freshness Score", f"{avg_score:.1f}/100", delta="Excellent")
                elif avg_score >= 40:
                    st.metric("Overall Freshness Score", f"{avg_score:.1f}/100", delta="Mixed Accuracy", delta_color="inverse")
                else:
                    st.metric("Overall Freshness Score", f"{avg_score:.1f}/100", delta="Highly Outdated", delta_color="inverse")
                
                st.divider()
                st.subheader("Detailed Claim Analysis")
                
                for i, r in enumerate(results, 1):
                    score = r["freshness_score"]
                    
                    if score >= 80:
                        st.success(f"**Claim {i}:** {r['claim']}")
                        st.info(f"Status: {r['status']} | Score: {score}/100")
                    elif score < 40:
                        st.error(f"**Claim {i}:** {r['claim']}")
                        st.warning(f"Status: {r['status']} | Score: {score}/100")
                    else:
                        st.warning(f"**Claim {i}:** {r['claim']}")
                        st.info(f"Status: {r['status']} | Score: {score}/100")
                    
                    st.markdown(f"*Reason:* {r['reason']}")
                    
                    if r['sources']:
                        st.markdown("**Sources:**")
                        for src in r['sources']:
                            st.markdown(f"- [{src['title']}]({src['url']}) _(Published: {src['date']})_")
                    
                    st.divider()
