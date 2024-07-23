import secrets
import uvicorn
from fastapi import FastAPI,HTTPException,status,Depends
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from typing import Annotated,Optional,List,Dict
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import spacy


## app defintion
app = FastAPI(title="Anoushka's API",
              description="This API gets the Named Entity Recoginition(NER) for a given sentence.",
              version="0.01")




## base function ready
#spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
def ner_extract(sentence):
    out = {"out_ner":[]}
    ner = []
    doc = nlp(sentence) 
    for ent in doc.ents: 
        ner.append({"ner":ent.text,"label":ent.label_}) 
    out["out_ner"]= ner 
    return out





## Data validation module
class RequestInput(BaseModel):
    sentence: str  = None 
    threshold: float = 0.6
    file_url: str = None


"""
{
    "out_ner": [
        {
            "ner": "Anoushka",
            "label": "GPE"
        },
        {
            "ner": "Dhirubhai Ambani International School",
            "label": "ORG"
        }
    ]
}

  """

data = {
    "chatbot_options": [
        {
            "id": 12330,
            "question_id": 9036,
            "answer_text": True,
            "answer_weight": 100,
            "next_question_id": 0,
            "next_dropdown_que_id": 0,
            "created_at": None
        },
        {
            "id": 12331,
            "question_id": 9036,
            "answer_text": False,
            "answer_weight": 0,
            "next_question_id": 0,
            "next_dropdown_que_id": 0,
            "created_at": None
        }],
    "next_question": 12,
    "next_column_question": 455
}

from datetime import datetime
class ChatbotOption(BaseModel):
    id: int
    question_id: int
    answer_text: bool
    answer_weight: int
    next_question_id: int
    next_dropdown_que_id: int
    created_at: datetime = None
class Response(BaseModel):
    chatbot_options: List[ChatbotOption]
    next_question: int
    next_column_question: int




## ner: [1,2,3,4]
class NERItems(BaseModel):
    ner: str
    label: str
class Response(BaseModel):
    out_ner: List[NERItems]




## routes
@app.get("/")
def docsgjwojgowejg():
    return RedirectResponse(url="/docs")


def func1(input) -> str:
    return "Hello World"

@app.post("/ner")  ###{"sentece":"Anoushka goes to Dhirubhai Ambani International School","threshold":'0.3'}
async def predict_api(data: RequestInput) -> Response: 
    sentence = data.sentence  # or data['sentence']
    threshold = data.threshold ## or data['treshold']
    out = ner_extract(sentence)
    return out


#server
if __name__ == "__main__":
    uvicorn.run(app,port=10449,host='0.0.0.0')
    print(ner_extract("Anoushka goes to Dhirubhai Ambani International School"))
