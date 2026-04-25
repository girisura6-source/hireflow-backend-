import streamlit as st
import hashlib
from database import conn, cursor

st.set_page_config(page_title="HireFlow AI", layout="centered")

st.title("🚀 HireFlow AI - Job Tracker")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- HASH FUNCTION ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- LOGIN / SIGNUP ----------------
if not st.session_state.logged_in:
    st.subheader("🔐 Login / Signup")

    option = st.radio("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            if not username or not password:
                st.warning("Fill all fields")
            else:
                hashed = hash_password(password)
                try:
                    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
                    conn.commit()
                    st.success("Account created! Login now")
                except:
                    st.error("User already exists")

    if option == "Login":
        if st.button("Login"):
            hashed = hash_password(password)
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
            user = cursor.fetchone()

            if user:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
else:
    st.success(f"Welcome {st.session_state.user} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    menu = st.sidebar.selectbox("Menu", ["Add Job", "View Jobs", "Resume Analyzer"])

    # ---------------- ADD JOB ----------------
    if menu == "Add Job":
        st.header("Add Job")

        company = st.text_input("Company")
        role = st.text_input("Role")
        status = st.selectbox("Status", ["Applied", "Interview", "Rejected"])

        if st.button("Submit"):
            if not company or not role:
                st.warning("Fill all fields")
            else:
                cursor.execute(
                    "INSERT INTO jobs (username, company, role, status) VALUES (?, ?, ?, ?)",
                    (st.session_state.user, company, role, status)
                )
                conn.commit()
                st.success("Job added")

    # ---------------- VIEW JOBS ----------------
    elif menu == "View Jobs":
        st.header("Your Jobs")

        cursor.execute("SELECT company, role, status FROM jobs WHERE username=?", (st.session_state.user,))
        jobs = cursor.fetchall()

        if not jobs:
            st.info("No jobs found")
        else:
            for job in jobs:
                st.write(f"🏢 {job[0]} | 💼 {job[1]} | 📌 {job[2]}")

    # ---------------- RESUME ANALYZER ----------------
    elif menu == "Resume Analyzer":
        st.header("Resume Analyzer")

        resume = st.text_area("Paste Resume")

        if st.button("Analyze"):
            if not resume:
                st.warning("Paste resume first")
            else:
                words = len(resume.split())
                st.success(f"Resume has {words} words")