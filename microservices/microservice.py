import json
import psycopg2
from paho.mqtt.client import Client
from datetime import datetime  # Para capturar o timestamp atual

# Configurações do broker MQTT
MQTT_BROKER = "e262a192434649b082007eb75e182f4a.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # Usando TLS (SSL)
MQTT_TOPIC = "monitoramento/solo/dados"
MQTT_USERNAME = "admin"  
MQTT_PASSWORD = "Admin1234"  

# Configurações do banco de dados PostgreSQL
DB_HOST = "dpg-ct51vrqlqhvc73a6he50-a.oregon-postgres.render.com"
DB_PORT = "5432"
DB_NAME = "katara"
DB_USER = "katara_user"
DB_PASSWORD = "IZNt1eGb0GEukZqq354aZZUJQuMejWdV"

# Conexão com o banco de dados
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

# Callback para conexão ao broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Erro ao conectar ao MQTT Broker, código: {rc}")

def on_message(client, userdata, msg):
    try:
        # Decodificar mensagem MQTT
        payload = msg.payload.decode("utf-8")
        print(f"Recebido do tópico {msg.topic}: {payload}")
        
        # Parsear JSON
        data = json.loads(payload)

        # Validar campos no JSON
        if not all(key in data for key in ("id_dispositivo", "umidade_solo", "temperatura_solo")):
            raise ValueError("JSON recebido não contém todos os campos obrigatórios.")

        # Obter o timestamp atual
        timestamp_atual = datetime.now()

        # Conectar ao banco
        conn = connect_db()
        cursor = conn.cursor()

        # Atribuir valores aos campos
        id_dispositivo = data["id_dispositivo"]
        temperatura_solo = data["temperatura_solo"]
        umidade_solo = data["umidade_solo"]

        # Certificar-se de que os valores são compatíveis com o banco de dados
        if not isinstance(id_dispositivo, str):
            raise ValueError("O campo 'id_dispositivo' deve ser uma string.")
        if not isinstance(temperatura_solo, (float, int)):
            raise ValueError("O campo 'temperatura_solo' deve ser um número.")
        if not isinstance(umidade_solo, (float, int)):
            raise ValueError("O campo 'umidade_solo' deve ser um número.")

        # Inserir no histórico_solo
        cursor.execute("""
            INSERT INTO historico_solo (id_dispositivo, datahora_leitura, temperatura_solo, umidade_solo)
            VALUES (%s, %s, %s, %s)
        """, (
            id_dispositivo,   # ID do dispositivo (string)
            timestamp_atual,  # Timestamp atual
            temperatura_solo, # Temperatura do solo (float)
            umidade_solo,     # Umidade do solo (float ou int)
        ))

        # Confirmar e fechar conexão
        conn.commit()
        cursor.close()
        conn.close()
        print("Dados inseridos no banco com sucesso!")

    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON recebido.")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")

# Configuração do cliente MQTT
def main():
    client = Client()

    # Configurar credenciais do HiveMQ
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Configurar callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Ativar TLS/SSL
    client.tls_set()

    try:
        # Conectar ao broker MQTT
        client.connect(MQTT_BROKER, MQTT_PORT)
        print("Iniciando o loop...")
        client.loop_forever()
    except KeyboardInterrupt:
        print("Encerrando o serviço...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
