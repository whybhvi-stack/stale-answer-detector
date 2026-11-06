import sys
import streamlit as st

sys.path.append("src")
from pipeline import check_answer

st.set_page_config(page_title="Stale-Answer Detector", layout="wide")
st.title("🕒 Stale-Answer Detector")
st.write("Paste an AI answer. We check which claims may be outdated.")

answer = st.text_area("AI-generated answer", height=200)

if st.button("Check freshness") and answer.strip():
    with st.spinner("Checking claims against live sources..."):
        report = check_answer(answer)
        if not report:
         st.success("No time-sensitive claims found, so nothing in this answer can go stale.")
    for r in report:
        icon = {"green": "🟢", "orange": "🟡", "red": "🔴"}[r["color"]]
        st.markdown(f"### {icon} {r['claim']}")
        st.write(f"**Verdict:** {r['verdict']}  |  **Freshness score:** {r['score']}/100")
        st.write(r["reason"])
        if r["correct_info"]:
            st.info(f"Up-to-date info: {r['correct_info']}")
        elif r["verdict"] == "outdated":
            st.warning("This claim looks outdated, but we could not confirm the current answer.")
        if r["source"]:
            st.markdown(f"[Source]({r['source']})  |  Source date: {r['source_date']}")
        st.divider()