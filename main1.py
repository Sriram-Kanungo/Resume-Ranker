from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import fitz  
import docx
import io
import json
import pandas as pd
from openai import OpenAI
import uvicorn
import re
app = FastAPI()
client = OpenAI(api_key="")  # Replace with actual API key

def extract_text(file: UploadFile):
    """Extracts text from a PDF or DOCX file."""
    file.file.seek(0) 
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=file.file.read(), filetype="pdf")
        return "\n".join([page.get_text("text") for page in doc])
    elif file.filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(file.file.read()))
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Only PDF and DOCX are allowed.")



def extract_criteria_from_text(text: str):
    """Extracts hiring criteria using GPT and ensures valid JSON."""
    prompt = f"""
    Extract key hiring criteria such as skills, certifications, experience, and qualifications from the job description below.
    Provide the response in **pure JSON format**, as a list of strings.
    
    Example Output:
    ["Python", "Machine Learning", "5+ years experience", "Deep Learning"]
    
    Job Description:
    {text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an expert in HR and recruitment."},
                  {"role": "user", "content": prompt}]
    )

    raw_response = response.choices[0].message.content.strip()
 
    cleaned_response = re.sub(r"^```json\s*|\s*```$", "", raw_response, flags=re.MULTILINE)

    try:
        criteria = json.loads(cleaned_response) 
        if not isinstance(criteria, list):  
            raise ValueError("GPT returned an invalid format.")
        return criteria
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON response from GPT: {cleaned_response}")



@app.post("/extract-criteria")
async def extract_criteria(file: UploadFile = File(...)):
    """Extracts hiring criteria from a job description and stores it globally."""
    global extracted_criteria
    text = extract_text(file)
    extracted_criteria = extract_criteria_from_text(text)  # Store criteria in memory
    return {"criteria": extracted_criteria}

@app.post("/score-resumes")
async def score_resumes(files: list[UploadFile] = File(...)):
    """Scores resumes based on stored criteria from the previous API call."""
    global extracted_criteria
    if not extracted_criteria:
        raise HTTPException(status_code=400, detail="No criteria found. Please upload a job description first.")

    results = []
    for file in files:
        resume_text = extract_text(file).lower()
        prompt = f"""
        Given the following resume text:
        {resume_text}

        You are an HR expert. Score the resume for the following criteria:
        0 = No mention of the criteria in the resume
        1 = Minimal mention, not strong experience
        3 = Moderate mention, good experience
        5 = Strong mention with relevant experience

        Criteria:
        {json.dumps(extracted_criteria)}

        Provide the scores in JSON format like this:
        {{
            "Artificial Intelligence": 3,
            "Machine Learning": 5,
            ...
        }}
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an expert in HR and recruitment."},
                      {"role": "user", "content": prompt}]
        )

        cleaned_response = response.choices[0].message.content.strip()
        cleaned_response = cleaned_response.strip("```json").strip("```")  
        
        try:
            scores = json.loads(cleaned_response) 
        except json.JSONDecodeError:
            print("Error parsing JSON, defaulting to 0 for all criteria.")
            scores = {criterion: 0 for criterion in extracted_criteria}

        scores = {k: max(0, min(v, 5)) for k, v in scores.items()}

        total_score = sum(scores.values())
        results.append({"Candidate Name": file.filename, **scores, "Total Score": total_score})

    df = pd.DataFrame(results)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=resume_scores.xlsx"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
