from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import add_solo

app = FastAPI()

# Configurando CORS para permitir todas as origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Incluindo a rota de adicionar solo
app.include_router(add_solo.router)
