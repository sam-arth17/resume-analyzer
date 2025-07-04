import streamlit as st
import json
from resume_parser import extract_text_from_pdf

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")
st.subheader("Upload your resume and select a job role")

# File uploader
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

# Dropdown for job role
job_role = st.selectbox(
    "Select Job Role",
    ["Choose Role", "Software Engineer", "Data Scientist", "Web Developer"]
)

# Analyze button
if st.button("Analyze Resume"):
    if uploaded_file is not None and job_role != "Choose Role":
        st.success("Resume uploaded and role selected")
        st.info(f"Selected Role: {job_role}")

        # Load required skills from roles.json
        with open("roles.json") as f:
            role_data = json.load(f)

        # Extract resume text
        resume_text = extract_text_from_pdf(uploaded_file)

        # Get required skills for selected role
        required_skills = role_data.get(job_role, [])

        # Skill matching logic
        matched = [skill for skill in required_skills if skill.lower() in resume_text.lower()]
        score = int((len(matched) / len(required_skills)) * 100)
        missing = list(set(required_skills) - set(matched))

        # Display results
        st.markdown("---")
        st.subheader("Analysis Results")
        st.write(f"Match Score: {score}%")
        st.write("Matched Skills:", matched)

        if missing:
            st.warning("Missing Skills:")
            st.write(missing)
        else:
            st.success("All key skills found in your resume!")

        # Score feedback
        if score >= 80:
            st.success("Excellent resume! You're ready to apply.")
        elif 50 <= score < 80:
            st.info("Your resume is decent. Consider adding more relevant skills.")
        else:
            st.warning("Resume needs improvement. Add more job-specific skills.")

        # Learning tips for missing skills
        if missing:
            st.markdown("### Learning Resources:")
            for skill in missing:
                st.markdown(f"- **{skill.title()}**: [Search on W3Schools](https://www.w3schools.com/howto/howto_search.asp?q={skill})")
    else:
        st.error("Please upload a resume and select a role.")
