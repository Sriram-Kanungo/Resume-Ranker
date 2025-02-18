import json
import pandas as pd
import io
from openai import OpenAI
from extractors import extract_text
from utils import clean_gpt_response
from fastapi.responses import StreamingResponse

client = OpenAI(api_key="")  # Replace with actual API key

async def score_resumes(files: list, extracted_criteria: list):
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

        scores = clean_gpt_response(response,extracted_criteria)
        total_score = sum(scores.values())
        results.append({"Candidate Name": file.filename, **scores, "Total Score": total_score})

    df = pd.DataFrame(results)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=resume_scores.xlsx"})
