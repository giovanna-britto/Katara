from fastapi import FastAPI
from app.routes import add_solo

app = FastAPI()

# Incluindo a rota de adicionar solo
app.include_router(add_solo.router)
