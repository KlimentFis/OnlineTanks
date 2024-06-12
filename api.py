from fastapi import FastAPI, HTTPException
from models import Tank

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Это моя игра, в неё нужно играть вдвоем, это API, для передачи данных между игроками.\nРепо с игрой: https://github.com/KlimentFis/OnlineTanks"}

@app.get("/game")
async def data():
    return

@app.post("/game")
async def data():
    return