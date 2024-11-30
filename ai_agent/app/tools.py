import os
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_community.tools import Tool
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)

index_name = "agriculture-data"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)
embeddings = OpenAIEmbeddings()

def search_agriculture_data(query: str, top_k: int = 5):
    query_vector = embeddings.embed_query(query)
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return [res["metadata"]["content"] for res in results["matches"]]



def get_weather_forecast(city_name: str):
    api_key = os.getenv("HGBRASIL_API_KEY")
    url = f"https://api.hgbrasil.com/weather?key={api_key}&city_name={city_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["results"]["city"],
            "temperature": data["results"]["temp"],
            "condition": data["results"]["description"],
            "rain_probability": data["results"].get("rain", None),
            "humidity": data["results"]["humidity"],
            "wind_speed": data["results"]["wind_speedy"],
            "sunrise": data["results"]["sunrise"],
            "sunset": data["results"]["sunset"],
        }
    else:
        raise Exception("Erro ao buscar previsão do tempo.")

weather_tool = Tool(
    name="WeatherAPI",
    func=get_weather_forecast,
    description="Consulta a previsão do tempo para ajustar horários de irrigação."
)