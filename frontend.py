import streamlit as st
import requests

API_URL = "https://hireflow-api.onrender.com"

st.title("🚀 HireFlow AI - Job Tracker")

# MENU
menu = st.sidebar.selectbox("Menu", ["Add Job", "View Jobs", "Resume Analyzer"])

# ---------------- ADD JOB ----------------
if menu == "Add Job":
    st.header("Add Job Application")

    company = st.text_input("Company Name")
    role = st.text_input("Role")
    status = st.selectbox("Status", ["Applied", "Interview", "Rejected"])

    if st.button("Submit"):
        if not company or not role:
            st.warning("Please fill all fields")
        else:
            try:
                response = requests.post(f"{API_URL}/add-job", json={
                    "company": company,
                    "role": role,
                    "status": status
                })

                st.write("Status Code:", response.status_code)
                st.write("Response:", response.text)

                if response.status_code == 200:
                    st.success("Job added successfully")
                else:
                    st.error("Failed to add job")

            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- VIEW JOBS ----------------
elif menu == "View Jobs":
    st.header("All Applications")

    # Debug button
    if st.button("Test API"):
        try:
            res = requests.get(f"{API_URL}/get-jobs")
            st.write("Status Code:", res.status_code)
            st.write("Response:", res.text)
        except Exception as e:
            st.error(f"Error: {e}")

    # Fetch jobs safely
    try:
        response = requests.get(f"{API_URL}/get-jobs")

        if response.status_code == 200:
            jobs = response.json()

            if not jobs:
                st.info("No jobs found. Add a job first.")
            else:
                for job in jobs:
                    st.write(f"🏢 {job.get('company')} | 💼 {job.get('role')} | 📌 {job.get('status')}")
        else:
            st.error("Failed to fetch jobs")

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- AI RESUME ----------------
elif menu == "Resume Analyzer":
    st.header("AI Resume Analyzer")

    resume = st.text_area("Paste Resume Text")

    if st.button("Analyze"):
        if not resume:
            st.warning("Please paste resume text")
        else:
            try:
                response = requests.post(f"{API_URL}/analyze-resume", json={
                    "resume_text": resume
                })

                if response.status_code == 200:
                    st.write("Result:")
                    st.success(response.json().get("result", "No result"))
                else:
                    st.error("Analysis failed")

            except Exception as e:
                st.error(f"Error: {e}")