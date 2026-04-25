import streamlit as st

st.set_page_config(page_title="HireFlow AI", layout="centered")

st.title("🚀 HireFlow AI - Job Tracker")

# Memory storage
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# MENU
menu = st.sidebar.selectbox("Menu", ["Add Job", "View Jobs", "Resume Analyzer"])

# ---------------- ADD JOB ----------------
if menu == "Add Job":
    st.header("Add Job Application")

    company = st.text_input("Company Name")
    role = st.text_input("Role")
    status = st.selectbox("Status", ["Applied", "Interview", "Rejected"])

    if st.button("Submit"):
        if company.strip() == "" or role.strip() == "":
            st.warning("⚠️ Fill all fields")
        else:
            st.session_state.jobs.append({
                "company": company,
                "role": role,
                "status": status
            })
            st.success("✅ Job added successfully")

# ---------------- VIEW JOBS ----------------
elif menu == "View Jobs":
    st.header("All Applications")

    if len(st.session_state.jobs) == 0:
        st.info("No jobs added yet")
    else:
        for job in st.session_state.jobs:
            st.write(
                f"🏢 {job['company']} | "
                f"💼 {job['role']} | "
                f"📌 {job['status']}"
            )

# ---------------- RESUME ANALYZER ----------------
elif menu == "Resume Analyzer":
    st.header("AI Resume Analyzer")

    resume = st.text_area("Paste Resume Text")

    if st.button("Analyze"):
        if not resume.strip():
            st.warning("Paste resume text first")
        else:
            # Simple analysis (no API needed)
            words = len(resume.split())
            st.success(f"📄 Resume has {words} words")