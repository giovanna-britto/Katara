from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.db.models import solo_table, engine
import cloudinary.uploader

router = APIRouter()

@router.post("/add-solo/")
async def add_solo(
    nome: str = Form(...),
    tamanho: str = Form(...),
    tipo_cultura: str = Form(...),
    cidade_solo: str = Form(...),
    id_dispositivo: str = Form(...),
    imagem: UploadFile = None,
):
    try:
        if imagem:
            upload_result = cloudinary.uploader.upload(
                await imagem.read(), folder="solos", public_id=imagem.filename.split('.')[0]
            )
            img_url = upload_result["secure_url"]
        else:
            raise HTTPException(status_code=400, detail="Imagem é obrigatória.")

        with engine.connect() as conn:
            insert_query = solo_table.insert().values(
                nome=nome,
                tamanho=tamanho,
                tipo_cultura=tipo_cultura,
                cidade_solo=cidade_solo,
                id_dispositivo=id_dispositivo,
                imagem=img_url,
            )
            result = conn.execute(insert_query)
            conn.commit()

        return JSONResponse(
            content={"message": "Solo adicionado com sucesso!", "id_solo": result.inserted_primary_key[0]},
            status_code=201,
        )
    except SQLAlchemyError as e:
        return HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Erro: {str(e)}")
