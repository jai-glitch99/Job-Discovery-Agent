import streamlit as st
import pandas as pd
from src.input_module import parse_excel_input, parse_text_input
from src.pipeline import run_basic_pipeline

def main():
    st.set_page_config(page_title="AI Job Discovery Agent", page_icon="🕵️‍♂️", layout="wide")
    
    st.title("🕵️‍♂️ AI Job Discovery Agent")
    st.markdown("Welcome! This agent helps you find the best job matches based on your profile and preferences.")
    
    st.sidebar.header("Settings")
    api_key = st.sidebar.text_input("OpenAI API Key (Phase 2 Insights)", type="password")
    
    st.sidebar.header("User Input")
    input_method = st.sidebar.radio("Choose Input Method", ("Upload Excel file", "Direct Text / LinkedIn URL"))
    
    parsed_data = None
    
    if input_method == "Upload Excel file":
        st.subheader("Upload your Preferences/Skills Excel Sheet")
        uploaded_file = st.file_uploader("Choose an Excel file (.xlsx)", type=["xlsx"])
        
        if uploaded_file is not None:
            with st.spinner("Parsing Excel file..."):
                parsed_data = parse_excel_input(uploaded_file)
            
            if parsed_data.get("success"):
                st.success("File uploaded and parsed successfully!")
                with st.expander("View Extracted Data"):
                    st.write(parsed_data["data"])
            else:
                st.error(f"Error parsing file: {parsed_data.get('error')}")
                
    elif input_method == "Direct Text / LinkedIn URL":
        st.subheader("Enter your LinkedIn URL or a list of your skills")
        user_text = st.text_area("Input (e.g., https://linkedin.com/in/johndoe OR Python, React, Data Analysis)")
        
        if user_text:
            parsed_data = parse_text_input(user_text)
            st.success("Text input received!")

    # Action Button to run pipeline
    st.divider()
    if st.button("🔍 Discover Jobs", type="primary"):
        if not parsed_data:
            st.warning("Please provide some input (Excel or Text) before discovering jobs.")
        else:
            with st.spinner("Running AI Pipeline... (this may take a moment if generating insights)"):
                # Run the basic pipeline with mock data
                result = run_basic_pipeline(parsed_data, api_key=api_key)
                
            if result["status"] == "success":
                st.subheader(result["message"])
                jobs = result["jobs"]
                
                if not jobs:
                    st.info("No matching jobs found in our mock database.")
                
                # Display jobs
                for i, job in enumerate(jobs):
                    with st.container():
                        st.markdown(f"### {i+1}. {job['title']} at {job['company']}")
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Description:** {job['description']}")
                        st.write(f"**Required Skills:** {', '.join(job['skills_required'])}")
                        st.markdown(f"[View Job / LinkedIn Link]({job['link']})")
                        
                        # Display Phase 2 AI Insights if available
                        if "insights" in job:
                            with st.expander("✨ AI Job Insights"):
                                st.write(f"**Role Fit:** {job['insights'].get('role_fit', 'N/A')}")
                                st.write(f"**Skills to Gain:** {job['insights'].get('skills_gained', 'N/A')}")
                                st.write(f"**Work Culture:** {job['insights'].get('work_culture', 'N/A')}")
                                st.write(f"**Career Path:** {job['insights'].get('career_path', 'N/A')}")
                        elif api_key:
                            st.warning("Insights could not be generated.")
                        
                        st.divider()

if __name__ == "__main__":
    main()
