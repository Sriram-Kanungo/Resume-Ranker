from fastapi import FastAPI, File, UploadFile, HTTPException

import uvicorn
from extractors import extract_text
from scorer import score_resumes
from utils import load_extracted_criteria

app = FastAPI()

extracted_criteria = []

@app.post("/extract-criteria")
async def extract_criteria(file: UploadFile = File(...)):
    global extracted_criteria
    text = extract_text(file)
    extracted_criteria = load_extracted_criteria(text)  
    return {"criteria": extracted_criteria}

@app.post("/score-resumes")
async def score_resumes_endpoint(files: list[UploadFile] = File(...)):
    global extracted_criteria
    if not extracted_criteria:
        raise HTTPException(status_code=400, detail="No criteria found. Please upload a job description first.")

    return await score_resumes(files, extracted_criteria)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
