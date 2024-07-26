import secrets
import uvicorn
from fastapi import FastAPI,HTTPException,status,Depends
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from typing import Annotated,Optional,List,Dict
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import openai
 
 
## app defintion
app = FastAPI(title="Anoushka's API",
              description="This API generates the summary for the input text.",
              version="0.01")
 
## base function ready
openai.api_key = ''
os.environ['OPENAI_API_KEY'] = ''
openai.api_key = os.getenv("OPENAI_API_KEY")
 
def summaryGenerate(transcript):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    #response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": """You are an expert professor.
          - Output the summary and title in the following JSON format without markdown like ``` or ```json
          - Output only the JSON and nothing else in the given format
            Format:
          {"Title": "This is an example title", "Summary": "This is an example summary"}
         """},
        {"role": "user", "content": f"Summarize the following text: {transcript}."}
 
    ]
  )
  print(response)
  summary = eval(response['choices'][0]['message']['content'])  ## json.loads()
  return summary
 
 
## Data validation module
class RequestInput(BaseModel):
    input_text: str  = None 
 
class Response(BaseModel):
    Title: str
    Summary: str
 
## routes
@app.get("/get")
def getCall():
    return RedirectResponse(url="/docs")
 
@app.post("/summary")
def predict_api(data: RequestInput) -> Response:
    print(data)
    input = data.input_text
    output=summaryGenerate(input)
    return output
 
#server
if __name__ == "__main__":
    #uvicorn.run(app,port=10449,host='0.0.0.0')
    print(summaryGenerate("Anoushka goes to Dhirubhai Ambani International School"))