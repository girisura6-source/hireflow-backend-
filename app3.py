import streamlit as st
import hashlib
import pandas as pd
from database import conn, cursor

st.set_page_config(page_title="HireFlow AI", layout="centered")

st.title("🚀 HireFlow AI - Job Tracker (Shared)")

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

    # SIGNUP
    if option == "Signup":
        if st.button("Create Account"):
            if not username or not password:
                st.warning("⚠️ Fill all fields")
            else:
                hashed = hash_password(password)
                try:
                    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
                    conn.commit()
                    st.success("✅ Account created! Please login")
                except:
                    st.error("❌ User already exists")

    # LOGIN
    if option == "Login":
        if st.button("Login"):
            hashed = hash_password(password)
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, hashed)
            )
            user = cursor.fetchone()

            if user:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# ---------------- MAIN APP ----------------
else:
    st.success(f"Welcome {st.session_state.user} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Add Job", "View Jobs", "Resume Analyzer"]
    )

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":
        st.header("📊 Dashboard (All Users Data)")

        cursor.execute("SELECT company, role, status FROM jobs")
        jobs = cursor.fetchall()

        if not jobs:
            st.info("No data available")
        else:
            df = pd.DataFrame(jobs, columns=["Company", "Role", "Status"])

            total = len(df)
            applied = (df["Status"] == "Applied").sum()
            interview = (df["Status"] == "Interview").sum()
            rejected = (df["Status"] == "Rejected").sum()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", total)
            col2.metric("Applied", applied)
            col3.metric("Interview", interview)
            col4.metric("Rejected", rejected)

            st.divider()
            st.subheader("📈 Status Distribution")
            st.bar_chart(df["Status"].value_counts())

    # ---------------- ADD JOB ----------------
    elif menu == "Add Job":
        st.header("➕ Add Job")

        company = st.text_input("Company Name")
        role = st.text_input("Role")
        status = st.selectbox("Status", ["Applied", "Interview", "Rejected"])

        if st.button("Submit"):
            if not company.strip() or not role.strip():
                st.warning("⚠️ Fill all fields")
            else:
                cursor.execute(
                    "INSERT INTO jobs (username, company, role, status) VALUES (?, ?, ?, ?)",
                    (st.session_state.user, company.strip(), role.strip(), status)
                )
                conn.commit()

                st.success(f"✅ Job added as '{status}'")

    # ---------------- VIEW JOBS ----------------
    elif menu == "View Jobs":
        st.header("📋 All Jobs (Shared)")

        cursor.execute("SELECT username, company, role, status FROM jobs")
        jobs = cursor.fetchall()

        if not jobs:
            st.info("No jobs found")
        else:
            for job in jobs:
                user, company, role, status = job

                if status == "Applied":
                    st.write(f"🟡 👤 {user} | 🏢 {company} | 💼 {role} | 📌 {status}")
                elif status == "Interview":
                    st.write(f"🟢 👤 {user} | 🏢 {company} | 💼 {role} | 📌 {status}")
                elif status == "Rejected":
                    st.write(f"🔴 👤 {user} | 🏢 {company} | 💼 {role} | 📌 {status}")

    # ---------------- RESUME ANALYZER ----------------
    elif menu == "Resume Analyzer":
        st.header("🤖 Resume Analyzer")

        resume = st.text_area("Paste Resume Text")

        if st.button("Analyze"):
            if not resume.strip():
                st.warning("⚠️ Paste resume text first")
            else:
                words = len(resume.split())
                st.success(f"📄 Resume has {words} words")
