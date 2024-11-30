from fastapi import FastAPI
from app.routes import solo_routes

app = FastAPI()

# Incluindo as rotas relacionadas a 'solo'
app.include_router(solo_routes.router)
    