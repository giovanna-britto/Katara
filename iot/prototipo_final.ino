#include <Wire.h>
#include <LiquidCrystal_I2C.h>  // Biblioteca para o LCD I2C
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Configurações Wi-Fi
const char* ssid = "Marco_Ruas";
const char* password = "12345678";

// Configurações MQTT
const char* mqtt_server = "e262a192434649b082007eb75e182f4a.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;  // Porta segura
const char* mqtt_user = "admin";
const char* mqtt_password = "Admin1234";
const char* mqtt_topic_data = "monitoramento/solo/dados";  // Novo tópico para JSON

// Pinos dos sensores
#define SOIL_SENSOR_PIN 34
#define ONE_WIRE_BUS 25

// Inicializar LCD com o endereço 0x27 e tamanho 16x2
LiquidCrystal_I2C lcd(0x27, 16, 2);

WiFiClientSecure espClient;  // Conexão segura
PubSubClient client(espClient);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Função para obter o ID único do ESP32
String getDeviceId() {
  uint64_t chipid = ESP.getEfuseMac();  // Obtém o MAC address
  char id[13];
  snprintf(id, 13, "%04X%08X", (uint16_t)(chipid >> 32), (uint32_t)chipid);
  return String(id);
}

void setup() {
  Serial.begin(115200);

  // Iniciar comunicação I2C do LCD
  lcd.init();  
  lcd.backlight();  // Ligar luz de fundo
  lcd.setCursor(0, 0);
  lcd.print("Inicializando...");

  // Desativar verificação de certificado
  espClient.setInsecure();

  // Conectar ao Wi-Fi
  setup_wifi();

  // Configurar o broker MQTT
  client.setServer(mqtt_server, mqtt_port);

  // Iniciar sensor DS18B20
  sensors.begin();
  
  lcd.clear();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Ler umidade do solo
  int soil_moisture_value = analogRead(SOIL_SENSOR_PIN); // Valor bruto analógico
  float soil_moisture_percent = map(soil_moisture_value, 4095, 0, 0, 100); // Mapeamento correto

  // Ler temperatura do solo
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);

  if (temperature == -127.0 || temperature == 85.0) {
    Serial.println("Erro na leitura da temperatura!");
    temperature = 0.0;  // Definir um valor padrão em caso de erro
  }

  // Mostrar no Monitor Serial
  Serial.print("Umidade Bruta (ADC): ");
  Serial.print(soil_moisture_value);  // Mostra valor bruto
  Serial.print(" | Umidade (%): ");
  Serial.println(soil_moisture_percent);  // Mostra valor percentual
  Serial.print("Temperatura do solo: ");
  Serial.println(temperature);

  // Exibir no LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Umid: ");
  lcd.print(soil_moisture_percent, 1);  // Exibe umidade com 1 casa decimal
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temperature, 1);  // Exibe temperatura com 1 casa decimal
  lcd.print(" C");

  // Criar JSON
  String jsonPayload = "{";
  jsonPayload += "\"id_dispositivo\":\"" + getDeviceId() + "\",";
  jsonPayload += "\"umidade_solo\":" + String(soil_moisture_percent, 1) + ",";
  jsonPayload += "\"temperatura_solo\":" + String(temperature, 1);
  jsonPayload += "}";

  // Mostrar JSON no Monitor Serial
  Serial.println("JSON Enviado: " + jsonPayload);

  // Enviar JSON via MQTT
  client.publish(mqtt_topic_data, jsonPayload.c_str());

  // Aguardar 10 segundos
  delay(10000);
}

void setup_wifi() {
  delay(10);
  Serial.println("Conectando ao WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando se conectar ao broker MQTT...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Conectado ao broker MQTT!");
    } else {
      Serial.print("Falha ao conectar. Código de erro: ");
      Serial.println(client.state());
      delay(5000);
    }
  }
}
