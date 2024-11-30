from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DB_HOST = "dpg-ct51vrqlqhvc73a6he50-a.oregon-postgres.render.com"
DB_PORT = "5432"
DB_NAME = "katara"
DB_USER = "katara_user"
DB_PASSWORD = "IZNt1eGb0GEukZqq354aZZUJQuMejWdV"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
