import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # Header Section
    st.title("📧 AI-Powered Email Generator")
    st.markdown(
        """<div style='background-color:#f0f2f6; padding:15px; border-radius:5px;'>
            Easily generate professional cold emails tailored to job postings or outreach with our AI-powered tool.
        </div>""",
        unsafe_allow_html=True
    )

    # Input Section
    st.header("Provide a Job  URL")
    url_input = st.text_input(
        "Enter a URL:", 
        value="https://jobs.nike.com/fr/job/R-45775?from=job%20search%20funnel",
        placeholder="Paste the job or target URL here..."
    )
    submit_button = st.button("Generate Email")

    # Process Submission
    if submit_button:
        with st.spinner("Processing... Please wait."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.subheader("Generated Email")
                    st.code(email, language='markdown')
            except Exception as e:
                st.error(f"An Error Occurred: {e}")



if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
