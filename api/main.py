from fastapi import FastAPI, Form
import search_engine

app = FastAPI()
# uvicorn main:app --reload

@app.post("/cari2")
def carijurnal_post(kueri:str = Form(...), fakultas:str = Form(...)):
    try:
        if kueri.strip() == None:
            return {"hasil" :'Anda tidak memberikan kueri atau hasil pencarian tidak ditemukan!', 
                    "panjang list" : 0}
        else:
            hasil_kueri = search_engine.search(kueri, fakultas)
            return {"hasil" : hasil_kueri, 
                    "panjang list" : len(hasil_kueri)}
    except:
        return {"hasil" : 'Anda tidak memberikan kueri atau hasil pencarian tidak ditemukan!', 
                "panjang list" : 0}

@app.get("/")
def welcome():
    return {"hasil" : 'Api siap digunakan!', 
            "panjang list" : 0}