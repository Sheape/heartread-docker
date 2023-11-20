from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import ecg_predict, create_plot
from app.model.model import __version__ as model_version
from starlette.middleware.cors import CORSMiddleware
# from app.cloudflare_r2 import

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class FileInput(BaseModel):
    filename: str


@app.get("/")
def home():
    return {"status": "OK", "model_version": model_version}

@app.post("/predict/ecg")
def ecg_classify(payload: FileInput):
    classifications = ecg_predict(payload.filename)
    return {"classifications": classifications}

@app.post("/plot")
def plot_ecg(payload: FileInput):
    create_plot(payload.filename)
    return {"message": "successfully created image"}
