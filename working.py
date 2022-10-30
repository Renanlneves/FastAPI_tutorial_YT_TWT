import re
import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class Update_item(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

app = FastAPI()

inventory = {}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="O ID do item que vc gostaria de ver", gt= 0)):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(name:str = Query(None, title="Name", description="Name of item.", max_length=10, min_length=2)):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail= "Nome não encontrado.")

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail= "ID já existente.")
    
    inventory[item_id] = item
    return inventory[item_id]
    
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item:Update_item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail= "ID não existente.")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]



@app.delete("/delete-item")   
def delete_item(item_id: int = Query(..., description="O ID do item a ser excluido", gt= 0 )):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail= "ID não existente.")
    
    del inventory[item_id]
    return {"Sucesso" : "Item excluido"}





if __name__ == "__main__":
    uvicorn.run("working:app", host="127.0.0.1", port=8037, reload=True)
