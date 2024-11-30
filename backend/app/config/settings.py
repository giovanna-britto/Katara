import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from dotenv import load_dotenv
import cloudinary

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

# Configurações do Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Configurações do Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

solo_table = Table(
    "solo",
    metadata,
    Column("id_solo", Integer, primary_key=True, autoincrement=True),
    Column("nome", String(255), nullable=False),
    Column("tamanho", String(255), nullable=False),
    Column("tipo_cultura", String(255), nullable=False),
    Column("cidade_solo", String(255), nullable=False),
    Column("imagem", String(255), nullable=False),
    Column("id_dispositivo", String(255), nullable=False),
)

