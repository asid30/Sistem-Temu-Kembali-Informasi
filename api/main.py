from fastapi import FastAPI, Form
from typing import Union
import numpy as np
import search_engine

app = FastAPI()
# uvicorn main:app --reload

@app.post("/cari2")
def carijurnal_post(kueri:str = Form(...)):
    try:
        if kueri.strip() == None:
            return {"hasil" :'Anda tidak memberikan kueri atau hasil pencarian tidak ditemukan!', 
                    "panjang list" : 0}
        else:
            return {"hasil" : search_engine.search(kueri), 
                    "panjang list" : len(search_engine.search(kueri))}
    except:
        return {"hasil" : 'Anda tidak memberikan kueri atau hasil pencarian tidak ditemukan!', 
                "panjang list" : 0}

@app.get("/")
def welcome():
    return {"hasil" : 'Api siap digunakan!', 
            "panjang list" : 0}