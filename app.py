"""
Resume Analyzer - Updated Version (2025)
A modern Streamlit application that uses Google's Gemini AI via LangChain
to analyze resumes against job descriptions.

Key Updates:
- Uses ChatGoogleGenerativeAI (modern LangChain interface)
- Implements Pydantic models for structured output
- Uses .with_structured_output() for reliable parsing
- Updated Streamlit widgets and methods
- Improved error handling and user experience
- Better prompt engineering
"""

import streamlit as st
import PyPDF2
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os


# ============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# ============================================================================


class ResumeAnalysis(BaseModel):
    """
    Structured output model for resume analysis.
    Using Pydantic ensures type safety and consistent output format.
    """

    match_percentage: int = Field(
        description="Percentage match between resume and job description (0-100)",
        ge=0,
        le=100,
    )
    missing_keywords: List[str] = Field(
        description="List of important keywords missing from the resume (max 20)",
        max_length=20,
    )
    strengths: str = Field(
        description="Detailed analysis of why the candidate is a good fit"
    )
    improvements: str = Field(
        description="Specific, actionable suggestions to improve the resume"
    )
    overall_assessment: str = Field(
        description="Brief overall assessment of the candidate's fit"
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts text content from an uploaded PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text from all pages of the PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text_content = ""

        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"

        return text_content.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""


def analyze_resume(
    resume_text: str, job_description: str, api_key: str
) -> ResumeAnalysis:
    """
    Analyzes a resume against a job description using Google's Gemini AI.

    This function uses the latest LangChain patterns:
    - ChatGoogleGenerativeAI for chat-based models
    - ChatPromptTemplate for modern prompt construction
    - .with_structured_output() for reliable JSON parsing

    Args:
        resume_text: Text extracted from the resume PDF
        job_description: Job description provided by the user
        api_key: Google AI API key

    Returns:
        ResumeAnalysis: Structured analysis results
    """

    # Initialize the model with latest Gemini
    # Using gemini-2.0-flash for speed and efficiency
    # Temperature set to 0.3 for more consistent, factual outputs
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=api_key,
        temperature=0.3,
        convert_system_message_to_human=True,  # For better system message handling
    )

    # Create a structured output model
    # This ensures we always get consistent JSON format
    structured_llm = llm.with_structured_output(ResumeAnalysis)

    # Modern prompt template using ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert Application Tracking System (ATS) with deep knowledge of:
- Software Engineering
- Data Science & Machine Learning
- Data Analysis & Business Intelligence
- Full Stack Development
- Cloud Computing & DevOps
- Big Data Engineering

Your task is to provide thorough, accurate, and actionable resume analysis.""",
            ),
            (
                "human",
                """Analyze the following resume against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide a comprehensive analysis with:

1. **Match Percentage** (0-100): How well does this resume match the job requirements?
   - Consider skills, experience, education, and achievements
   - Be realistic and fair in your assessment

2. **Missing Keywords**: Identify up to 20 critical keywords/skills from the job description that are missing or underrepresented in the resume. Focus on:
   - Technical skills
   - Tools and technologies
   - Relevant certifications
   - Industry-specific terminology

3. **Strengths**: Explain in detail why this candidate IS a good fit:
   - Matching skills and experience
   - Relevant projects or achievements
   - Educational background
   - Transferable skills

4. **Improvements**: Provide specific, actionable recommendations:
   - How to better highlight existing relevant experience
   - Skills or certifications to acquire
   - Resume formatting or presentation improvements
   - Keywords to add for better ATS optimization
   - Ways to quantify achievements

5. **Overall Assessment**: Provide a brief 2-3 sentence summary of the candidate's overall fit.

Remember: The job market is highly competitive. Provide honest, constructive feedback that will genuinely help improve the candidate's chances.""",
            ),
        ]
    )

    # Create the analysis chain
    analysis_chain = prompt | structured_llm

    # Execute the analysis
    try:
        result = analysis_chain.invoke(
            {"resume_text": resume_text, "job_description": job_description}
        )
        return result
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        raise


# ============================================================================
# STREAMLIT UI
# ============================================================================


def main():
    """
    Main Streamlit application function.
    Includes modern Streamlit patterns and better UX.
    """

    # Page configuration - must be the first Streamlit command
    st.set_page_config(
        page_title="Resumer.ai",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for better styling
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Main header
    st.markdown('<h1 class="main-header">📄 Resumer.ai</h1>', unsafe_allow_html=True)
    st.markdown("##### Powered by Google Gemini 3.0 & LangChain")
    st.markdown("---")

    # Sidebar for API key and information
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key input with password masking
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            placeholder="Enter your Gemini API key",
            help="Get your free API key from Google AI Studio",
        )

        st.markdown("### 🔑 Get Your API Key")
        st.markdown(
            """
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Click "Create API Key"
        3. Copy and paste it above
        """
        )

        st.markdown("---")

        st.markdown("### ℹ️ About")
        st.info(
            """
        This app uses Google's **Gemini 3.0 Flash** model to analyze your resume against job descriptions.
        
        **Features:**
        - ✅ ATS Match Scoring
        - 🔍 Keyword Analysis
        - 💪 Strength Identification
        - 📈 Improvement Suggestions
        """
        )

        st.markdown("---")

        st.markdown("### ⚠️ Note")
        st.warning(
            """
        AI-powered analysis may occasionally produce unexpected results. 
        Always review suggestions critically.
        """
        )

        st.markdown("---")

        st.markdown("### 👨‍💻 Credits")
        st.markdown(
            """
        **Updated Version (2025)**
        - Modern LangChain integration
        - Pydantic output parsing
        - Enhanced prompts
        
        **Original by:** [Shreya Chaudhari](https://github.com/rahulNetkar)
        """
        )

    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📤 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload your resume in PDF format",
            label_visibility="collapsed",
        )

        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")

            # Show file details
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type,
            }
            with st.expander("📋 File Details"):
                for key, value in file_details.items():
                    st.text(f"{key}: {value}")

    with col2:
        st.subheader("📝 Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="Paste the complete job description including requirements, responsibilities, and qualifications...",
            label_visibility="collapsed",
        )

        if job_description:
            word_count = len(job_description.split())
            st.caption(f"Word count: {word_count}")

    # Analysis button
    st.markdown("---")

    # Center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button(
            "🚀 Analyze Resume", type="primary", use_container_width=True
        )

    # Analysis logic
    if analyze_button:
        # Validation
        if not api_key:
            st.error("⚠️ Please enter your Google AI API key in the sidebar.")
            return

        if not uploaded_file:
            st.error("⚠️ Please upload a resume PDF file.")
            return

        if not job_description:
            st.error("⚠️ Please paste the job description.")
            return

        # Show progress
        with st.spinner("🔍 Analyzing your resume... This may take 10-30 seconds."):
            try:
                # Extract text from PDF
                with st.status("Extracting text from PDF...", expanded=True) as status:
                    resume_text = extract_text_from_pdf(uploaded_file)

                    if not resume_text:
                        st.error(
                            "Could not extract text from PDF. Please ensure the PDF contains readable text."
                        )
                        return

                    st.write(f"✅ Extracted {len(resume_text)} characters")
                    status.update(label="Text extraction complete!", state="complete")

                # Perform analysis
                with st.status("Analyzing with Gemini AI...", expanded=True) as status:
                    result = analyze_resume(resume_text, job_description, api_key)
                    status.update(label="Analysis complete!", state="complete")

                # Display results
                st.success("✅ Analysis Complete!")
                st.markdown("---")

                # Create tabs for organized display
                tab1, tab2, tab3, tab4, tab5 = st.tabs(
                    [
                        "📊 Match Score",
                        "🔑 Missing Keywords",
                        "💪 Strengths",
                        "📈 Improvements",
                        "📝 Overall Assessment",
                    ]
                )

                with tab1:
                    st.subheader("Match Percentage")

                    # Display progress bar with custom color
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.progress(result.match_percentage / 100)
                        st.metric(
                            label="Match Score",
                            value=f"{result.match_percentage}%",
                            delta=(
                                "Good fit"
                                if result.match_percentage >= 70
                                else "Needs improvement"
                            ),
                        )

                    # Interpretation
                    if result.match_percentage >= 80:
                        st.success(
                            "🎉 Excellent match! You're a strong candidate for this position."
                        )
                    elif result.match_percentage >= 60:
                        st.info(
                            "👍 Good match! With some improvements, you could be a top candidate."
                        )
                    else:
                        st.warning(
                            "⚠️ Consider gaining more relevant skills or highlighting your experience better."
                        )

                with tab2:
                    st.subheader("Missing Keywords")

                    if result.missing_keywords:
                        st.write("Consider adding these keywords to your resume:")

                        # Display in columns for better layout
                        cols = st.columns(3)
                        for idx, keyword in enumerate(result.missing_keywords):
                            with cols[idx % 3]:
                                st.markdown(f"- **{keyword}**")
                    else:
                        st.success("✅ No major keywords missing!")

                with tab3:
                    st.subheader("Your Strengths")
                    st.markdown(result.strengths)

                with tab4:
                    st.subheader("Recommended Improvements")
                    st.markdown(result.improvements)

                with tab5:
                    st.subheader("Overall Assessment")
                    st.info(result.overall_assessment)

                # Download button for results
                st.markdown("---")

                # Create downloadable report
                report = f"""
RESUME ANALYSIS REPORT
======================

Match Score: {result.match_percentage}%

MISSING KEYWORDS:
{chr(10).join('- ' + k for k in result.missing_keywords)}

STRENGTHS:
{result.strengths}

IMPROVEMENTS:
{result.improvements}

OVERALL ASSESSMENT:
{result.overall_assessment}

Generated by Resume Analyzer AI
Powered by Google Gemini 2.0 & LangChain
"""

                st.download_button(
                    label="📥 Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Tip: Try again or check if your API key is valid.")


if __name__ == "__main__":
    main()
