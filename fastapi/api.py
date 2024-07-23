import secrets
import uvicorn
from fastapi import FastAPI,HTTPException,status,Depends
from pydantic import BaseModel,Field

from starlette.responses import RedirectResponse

from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import spacy
import bcrypt

app = FastAPI()
security = HTTPBasic()


spacy.cli.download("en_core_web_sm")

#load model
nlp = spacy.load('en_core_web_sm')
  
##infer/predict function
def ner_extract(sentence):
    out = {"ner":[]}
    ner = []
    doc = nlp(sentence) 
    for ent in doc.ents: 
        ner.append({"ner":ent.text,"label":ent.label_}) 
    out["ner"]= ner
    print("Received")
    #time.sleep(60)
    return out

## Data validation module
class Request(BaseModel):
    sentence: str = Field(default=None,description="Sentence to run NER model on")
    threshold: int = Field(default=0.6,description="Threshold for NER model")
    max_out: int = Field(default=5,description="Max number of entity to output")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sentence": "Sam Altman is the CEO of OpenAI",
                    "threshold": 0.6,
                    "max_out": 5,
                },

            ]
        }
    }


class Response(BaseModel):
    ner: list = []

def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

    input_username = credentials.username ## USER INPUT
    print("Typed username:",input_username)
    input_password= credentials.password

    print("Typed password",input_password)
    correct_password = "password"
    is_correct_password = secrets.compare_digest(input_password.encode('utf-8'), correct_password.encode('utf-8'))
    if not (is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(get_current_username)]):
    return RedirectResponse(url="/docs")

@app.post("/infer")
async def predict_api(request: Request,
                      credentials: Annotated[HTTPBasicCredentials, Depends(get_current_username)]) -> Response:  #{"sentence": "sdgjowegoew"}
    sentence = request.sentence
    out = ner_extract(sentence)
    return out





if __name__ == "__main__":
    uvicorn.run(app,port=10449,host='0.0.0.0')