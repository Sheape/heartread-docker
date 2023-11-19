from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import ecg_predict
from app.model.model import __version__ as model_version
# from app.cloudflare_r2 import

app = FastAPI()


class FileInput(BaseModel):
    filename: str


@app.get("/")
def home():
    return {"status": "OK", "model_version": model_version}

@app.post("/predict/ecg")
def ecg_classify(payload: FileInput):
    classifications = ecg_predict(payload.filename)
    return {"clasifications": classifications}
