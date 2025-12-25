## Hello, world!
## Resumer.ai is an LLM based app that can analyze your resume and based on the job description provided it give you crucial feedback such as -
- #### Percentage Matched
- #### Reason for your profile is fit for that job role or not
- #### Missing Keywords from your resume
- #### Points on how you can improve your profile 

# Setup & Quick Start Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Getting Your API Key](#getting-your-api-key)
4. [Running the Application](#running-the-application)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** (Python 3.10+ recommended)
- **pip** (Python package installer)
- **Git** (optional, for cloning)
- **Google AI API Key** (free to get)

### Check Your Python Version:
```bash
python --version
# or
python3 --version
```

---

## Installation

### Method 1: Using Git (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd resume-analyzer

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Manual Setup

```bash
# Create a new directory
mkdir resume-analyzer
cd resume-analyzer

# Create a virtual environment
python -m venv venv

# Activate it (see above)

# Install dependencies manually
pip install streamlit>=1.41.1
pip install langchain-google-genai>=4.1.2
pip install langchain-core>=0.3.21
pip install pydantic>=2.10.5
pip install PyPDF2>=3.0.1
```

### Verify Installation:
```bash
pip list | grep -E "streamlit|langchain|pydantic|PyPDF2"
```

You should see all packages installed.

---

## Getting Your API Key

### Step 1: Go to Google AI Studio
Visit: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Step 2: Sign In
- Use your Google account
- Accept the terms of service

### Step 3: Create API Key
1. Click "Create API Key"
2. Select "Create API key in new project" (or use existing)
3. Copy the API key immediately (you won't see it again!)

### Step 4: Keep It Safe
⚠️ **IMPORTANT:** Never share your API key or commit it to GitHub!

#### Option A: Use Environment Variables (Recommended)
Create a `.env` file:
```bash
GOOGLE_API_KEY=your_api_key_here
```

Update the code to load from .env:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

#### Option B: Enter in the App
Simply paste it in the sidebar when running the app.

---

## Running the Application

### Basic Run:
```bash
# Make sure you're in the project directory
cd resume-analyzer

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the app
streamlit run resume_analyzer_updated.py
```

### Expected Output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Open in Browser:
The app should automatically open in your default browser. If not, manually navigate to `http://localhost:8501`

---

## Usage Guide

### Step 1: Enter API Key
1. Look at the sidebar on the left
2. Find the "⚙️ Configuration" section
3. Paste your Google AI API key in the password field

### Step 2: Upload Resume
1. Click "📤 Upload Resume" area
2. Select a PDF file from your computer
3. Supported format: **PDF only**
4. File should have readable text (not scanned images)

### Step 3: Paste Job Description
1. Find the "📝 Job Description" text area
2. Copy the entire job description from the job posting
3. Paste it into the text area
4. Include all sections: requirements, responsibilities, qualifications

### Step 4: Analyze
1. Click the "🚀 Analyze Resume" button
2. Wait 10-30 seconds for analysis
3. Watch the progress indicators

### Step 5: Review Results
The analysis is displayed in 5 tabs:

1. **📊 Match Score**
   - Overall percentage match
   - Visual progress bar
   - Interpretation (Excellent/Good/Needs Improvement)

2. **🔑 Missing Keywords**
   - Keywords from JD not in resume
   - Organized in 3 columns
   - Up to 20 critical keywords

3. **💪 Strengths**
   - Why you're a good fit
   - Matching qualifications
   - Relevant experience

4. **📈 Improvements**
   - Specific, actionable suggestions
   - Skills to highlight
   - Resume optimization tips

5. **📝 Overall Assessment**
   - Brief summary
   - 2-3 sentence evaluation

### Step 6: Download Report
- Click "📥 Download Analysis Report"
- Saves as a `.txt` file
- Contains all analysis results

---

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade

# Or install missing package specifically
pip install <package-name>
```

### Issue: "API key not valid" error

**Solutions:**
1. Verify your API key is correct (no extra spaces)
2. Check if your API key has expired
3. Ensure you're using the correct Google AI Studio key (not Vertex AI)
4. Generate a new key if needed

### Issue: "Could not extract text from PDF"

**Possible Causes & Solutions:**
1. **Scanned PDF (Image-based):**
   - Use OCR software first to convert to text
   - Or use a different PDF with selectable text

2. **Password-protected PDF:**
   - Remove password protection first

3. **Corrupted PDF:**
   - Try re-downloading or re-creating the PDF

### Issue: Streamlit won't start

**Solutions:**
```bash
# Check if port is already in use
# Kill existing Streamlit processes
pkill -9 streamlit

# Run on different port
streamlit run resume_analyzer_updated.py --server.port 8502
```

### Issue: Very slow analysis

**Possible Causes:**
1. **Large resume file:**
   - Keep resumes under 10 pages
   - Remove unnecessary graphics

2. **Network issues:**
   - Check your internet connection
   - API calls require stable connection

3. **API rate limits:**
   - Wait a few minutes
   - Free tier has rate limits

### Issue: Inconsistent or strange results

**Solutions:**
1. **Check your inputs:**
   - Ensure job description is complete
   - Resume should be well-formatted

2. **Try different temperature:**
   - Edit line: `temperature=0.3`
   - Lower (0.1) = more conservative
   - Higher (0.7) = more creative

3. **Try again:**
   - AI can vary slightly between runs
   - This is normal for LLMs

---

## Advanced Configuration

### Customizing the Model

Edit `resume_analyzer_updated.py`:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Try: gemini-2.5-pro-preview-03-25
    google_api_key=api_key,
    temperature=0.3,  # Adjust: 0.0 (deterministic) to 1.0 (creative)
    max_tokens=8192,  # Max response length
    convert_system_message_to_human=True
)
```

### Running on Custom Port

```bash
streamlit run resume_analyzer_updated.py --server.port 8080
```

### Running with Dark Theme

```bash
streamlit run resume_analyzer_updated.py --theme.base dark
```

### Deploying to Streamlit Cloud

1. Push your code to GitHub (without API keys!)
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secrets (API key) in the dashboard
5. Deploy!

### Environment Variables Setup

Create `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["GOOGLE_API_KEY"]
```

---

## 📊 Performance Tips

### For Best Results:
1. ✅ Use well-formatted, text-based PDFs
2. ✅ Provide complete job descriptions (300+ words)
3. ✅ Include all relevant sections in resume
4. ✅ Ensure stable internet connection
5. ✅ Run during non-peak hours for faster response

### For Faster Processing:
1. Keep resumes under 3-4 pages
2. Remove unnecessary graphics/images
3. Use shorter job descriptions (focus on key points)
4. Consider using Gemini Flash vs Pro models

---

## 🔒 Security Best Practices

1. **Never commit API keys to Git:**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

2. **Use environment variables:**
   - Store sensitive data outside code
   - Use `.env` files locally
   - Use secrets management in production

3. **Rotate API keys regularly:**
   - Create new keys periodically
   - Delete old/unused keys

4. **Monitor API usage:**
   - Check Google AI Studio dashboard
   - Set up billing alerts if using paid tier

---

## 📞 Getting Help

### Resources:
- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **LangChain Docs:** [python.langchain.com](https://python.langchain.com)
- **Gemini API Docs:** [ai.google.dev](https://ai.google.dev)

### Community:
- **Streamlit Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **LangChain Discord:** [discord.gg/langchain](https://discord.gg/langchain)

### Issues:
If you encounter bugs, please:
1. Check this troubleshooting guide first
2. Search existing issues on GitHub
3. Create a new issue with details:
   - Error message
   - Python version
   - Package versions
   - Steps to reproduce

---
