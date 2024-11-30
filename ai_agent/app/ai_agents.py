# Rename this file to ai_agents.py
from app.tools import weather_tool, search_agriculture_data
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

# Inicializa o modelo LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Configuração do agente
def create_react_agent():
    tools = [
        weather_tool,
        Tool(
            name="AgricultureRAG",
            func=search_agriculture_data,
            description="Busca informações confiáveis sobre práticas agrícolas."
        )
    ]
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

def create_chatbot_agent():
    tools = [
        Tool(
            name="AgricultureRAG",
            func=search_agriculture_data,
            description="Busca informações confiáveis sobre práticas agrícolas."
        )
    ]
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )