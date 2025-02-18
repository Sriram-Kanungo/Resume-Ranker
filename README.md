Resume Scoring API

Overview

The Resume Scoring API is a high-performance solution built with FastAPI that automates the process of candidate screening by scoring resumes against hiring criteria extracted from job descriptions. Utilizing OpenAI GPT models, the API extracts relevant skills, qualifications, and experience from job descriptions, then evaluates uploaded resumes to match these criteria. The API generates a comprehensive score for each resume and provides an easily downloadable Excel report for recruiters and HR professionals.

Features
Job Description Analysis: Extracts key hiring criteria (skills, qualifications, and experience) from a job description.
Resume Scoring: Scores multiple resumes against the extracted criteria, providing a clear evaluation of candidate suitability.
Excel Report: Generates an Excel file containing scores for each resume, which can be easily reviewed and shared.
Swagger UI Integration: Provides an interactive documentation interface for easy testing and understanding of the API endpoints.

Technologies Used
FastAPI: Web framework for building the API.
OpenAI GPT: AI-powered models for extracting criteria and scoring resumes.
Pandas: Data manipulation and Excel report generation.
Uvicorn: ASGI server for fast asynchronous communication.

Setup Instructions
Prerequisites
Python 3.8 or higher
pip (Python package installer)
Step 1: Clone the Repository

git clone https://github.com/yourusername/resume-scoring-api.git
cd resume-scoring-api
Step 2: Install Dependencies
Create and activate a virtual environment, then install the required dependencies:


# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Step 3: Set Up OpenAI API Key
To use the OpenAI GPT model for text extraction and scoring, you'll need to set up your OpenAI API key:

Sign up at OpenAI.
Generate an API key from the OpenAI Dashboard.
Set the API key in the environment variables or directly in the code.

export OPENAI_API_KEY="your-api-key"  # On macOS/Linux
set OPENAI_API_KEY="your-api-key"     # On Windows
Alternatively, you can hard-code the key in the client = OpenAI(api_key="your-api-key") section, but environment variables are recommended for security.

Step 4: Run the Application
Start the FastAPI server using Uvicorn:

uvicorn app:app --reload
The API will be accessible at http://127.0.0.1:8000.

Step 5: Access Swagger UI
Once the server is running, you can access the interactive API documentation:

Swagger UI: http://127.0.0.1:8000/docs
API Endpoints
1. POST /extract-criteria
Extracts hiring criteria from a job description.

Request:
file: Job description file (PDF or DOCX)
Response:
criteria: List of skills, qualifications, and experience extracted from the job description.
Example Response:

{
  "criteria": [
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Python",
    "Java"
  ]
}
2. POST /score-resumes
Scores multiple resumes based on the extracted criteria.

Request:
files: List of resume files (PDF or DOCX)
Response:
An Excel file with candidate names and their respective scores for each criterion.
Example Response:
An Excel file will be generated and returned containing the following columns:

Candidate Name
Criteria (e.g., Artificial Intelligence, Machine Learning)
Total Score
Example Usage
Extract Criteria from a Job Description
To extract criteria from a job description, upload the job description file via the /extract-criteria endpoint.

curl -X 'POST' \
  'http://127.0.0.1:8000/extract-criteria' \
  -F 'file=@job_description.pdf'
Score Resumes Based on Extracted Criteria
After extracting the criteria, upload multiple resumes to the /score-resumes endpoint to get scores.

curl -X 'POST' \
  'http://127.0.0.1:8000/score-resumes' \
  -F 'files=@resume1.pdf' \
  -F 'files=@resume2.docx'
Contributing
We welcome contributions! If you'd like to improve the project, feel free to fork the repository and submit a pull request. Here are some ways you can contribute:

Bug fixes and improvements.
Enhancements to API documentation.
New features or optimizations.
Please ensure your code passes the tests and follows the project's coding conventions before submitting a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
