from fastapi import FastAPI, Form
from typing import Union
import numpy as np
import search_engine

app = FastAPI()
# uvicorn main:app --reload

@app.get("/cari")
def carijurnal_get(kueri:Union[str, None] = None):
    if kueri == None:
        return ['Anda tidak memberikan kueri!']
    else:
        return {"hasil":search_engine.search(kueri), 
                "panjang list":len(search_engine.search(kueri))}

@app.post("/cari2")
def carijurnal_post(kueri:str = Form(...)):
    if kueri == None:
        return ['Anda tidak memberikan kueri!']
    else:
        return {"hasil":search_engine.search(kueri), 
                "panjang list":len(search_engine.search(kueri))}

@app.get("/")
def welcome():
    return {'Hallo Guys'}