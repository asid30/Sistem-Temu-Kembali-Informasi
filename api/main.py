from fastapi import FastAPI
from typing import Union
import numpy as np
import search_engine

app = FastAPI()
# uvicorn main:app --reload

@app.get("/cari")
def read_root(kueri:Union[str, None] = None):
    if kueri == None:
        return ['Anda tidak memberikan kueri!']
    else:
        return search_engine.search(kueri)

@app.get("/")
def abdul():
    return {'Hallo Guys'}