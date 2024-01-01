from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {
        "item_id_list" : item_id
    }

@app.get('/')
def check_item():
    return {
        "sesuatu" : 'kenapa bisa begitu nilainya'
    }