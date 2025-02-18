import json
import re
from openai import OpenAI
from fastapi import HTTPException


client = OpenAI(api_key="")  # Replace with actual API key

def load_extracted_criteria(text: str):
    """Extracts hiring criteria using GPT and ensures valid JSON."""
    prompt = f"""
    Extract key hiring criteria such as skills, certifications, experience, and qualifications from the job description below.
    Provide the response in **pure JSON format**, as a list of strings.
    
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

def clean_gpt_response(response,extracted_criteria):
    """Clean GPT response and parse it into a dictionary."""
    cleaned_response = response.choices[0].message.content.strip()
    cleaned_response = cleaned_response.strip("```json").strip("```")  
    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        print("Error parsing JSON, defaulting to 0 for all criteria.")
        return {criterion: 0 for criterion in extracted_criteria}
