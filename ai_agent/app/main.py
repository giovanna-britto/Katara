from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Importando o CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from app.prompts import recommendation_prompt, chatbot_prompt
from app.ai_agents import create_react_agent, create_chatbot_agent

app = FastAPI()

# Configuração do CORS para liberar todas as origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite qualquer método (GET, POST, etc.)
    allow_headers=["*"],  # Permite qualquer cabeçalho
)

class InputData(BaseModel):
    plant_type: str
    soil_humidity: float
    temperature: float
    city_name: str

class ChatInput(BaseModel):
    message: str

@app.post("/recommendation/")
async def recommendation(data: InputData):
    try:
        agent = create_react_agent()

        timestamp = datetime.now().isoformat()

        forecast = agent.run(f"Qual a previsão do tempo para {data.city_name}?")

        rag_data = agent.run(f"Busque informações confiáveis sobre {data.plant_type}.")

        recommendation_input = recommendation_prompt.format(
            timestamp=timestamp,
            plant_type=data.plant_type,
            soil_humidity=data.soil_humidity,
            temperature=data.temperature,
            forecast=forecast,
            rag_data=rag_data
        )
        recommendation = agent.run(recommendation_input)

        return {"recommendation": recommendation}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar recomendação: {str(e)}")

@app.post("/chatbot/")
async def chatbot(data: ChatInput):
    try:
        agent = create_chatbot_agent()
        timestamp = datetime.now().isoformat()

        # Get RAG data based on user message
        rag_data = agent.run(f"Busque informações confiáveis sobre '{data.message}'.")

        # Prepare the chatbot input
        chatbot_input = chatbot_prompt.format(
            timestamp=timestamp,
            user_message=data.message,
            rag_data=rag_data
        )

        # Generate the response
        response = agent.run(chatbot_input)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no chatbot: {str(e)}")
