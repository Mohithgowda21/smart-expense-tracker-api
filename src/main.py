
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import json
from typing import Optional

app=FastAPI(title="Smart Expense Tracker API")

DB=Path(__file__).parent/"expenses.json"

class Expense(BaseModel):
    title:str=Field(...,min_length=1)
    amount:float=Field(...,gt=0)
    category:str=Field(...,min_length=1)
    date:str

def load():
    if not DB.exists():
        DB.write_text("[]")
    with open(DB,"r") as f:
        return json.load(f)

def save(data):
    with open(DB,"w") as f:
        json.dump(data,f,indent=2)

@app.post("/expenses",status_code=201)
def add(expense:Expense):
    data=load()
    nid=max([e["id"] for e in data],default=0)+1
    obj={"id":nid,**expense.model_dump()}
    data.append(obj)
    save(data)
    return obj

@app.get("/expenses")
def get_expenses(category:Optional[str]=None):
    data=load()
    if category:
        data=[e for e in data if e["category"].lower()==category.lower()]
    return data

@app.get("/expenses/total")
def total():
    data=load()
    return {"total":sum(float(e["amount"]) for e in data)}

@app.get("/expenses/total/{category}")
def total_cat(category:str):
    data=load()
    return {"category":category,"total":sum(float(e["amount"]) for e in data if e["category"].lower()==category.lower())}

@app.delete("/expenses/{expense_id}")
def delete(expense_id:int):
    data=load()
    for e in data:
        if e["id"]==expense_id:
            data.remove(e)
            save(data)
            return {"message":"Expense deleted"}
    raise HTTPException(status_code=404,detail="Expense not found")
