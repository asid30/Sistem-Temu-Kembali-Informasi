from fastapi import FastAPI
from typing import Union
import search_engine

app = FastAPI()
# uvicorn main:app --reload
dicari = 'intro kembang KRISAN POTONG DI DESA pesawaran'

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {
#         "item_id_list" : item_id
#     }

@app.get("/")
def read_root():
    return search_engine.search('intro kembang KRISAN POTONG DI DESA pesawaran')