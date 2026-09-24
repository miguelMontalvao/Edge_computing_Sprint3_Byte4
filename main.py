import time
import network
import urequests
from machine import Pin, SoftI2C
import dht
from i2c_lcd import I2cLcd

# --- CONFIGURAÇÕES DE PINOS ---
DHT_PIN = Pin(15)
I2C_SDA = Pin(21)
I2C_SCL = Pin(22)

# Configuração Wi-Fi e ThingSpeak
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""
THINGSPEAK_API_KEY = "T8HTGFRTG5Z08OLR"  
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# Parâmetros de Intervalo e Média Móvel (Edge Computing)
HISTORICO_TAMANHO = 5
historico_temp = []
historico_umid = []

# Inicialização dos Periféricos
sensor = dht.DHT22(DHT_PIN)
i2c = SoftI2C(scl=I2C_SCL, sda=I2C_SDA, freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def conectar_wifi():
    lcd.clear()
    lcd.putstr("Conectando WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    
    tentativas = 0
    while not wlan.isconnected() and tentativas < 10:
        time.sleep(1)
        tentativas += 1
        
    lcd.clear()
    if wlan.isconnected():
        lcd.putstr("WiFi Conectado!")
    else:
        lcd.putstr("WiFi Desconectado")
    time.sleep(1)

def calcular_media(lista, novo_valor):
    lista.append(novo_valor)
    if len(lista) > HISTORICO_TAMANHO:
        lista.pop(0)
    return sum(lista) / len(lista)

def determinar_status(temp_media, umid_media):
    if 18 <= temp_media <= 23 and 40 <= umid_media <= 60:
        return "IDEAL"
    elif temp_media > 25:
        return "QUENTE"
    elif temp_media < 18:
        return "FRIO"
    elif umid_media < 40:
        return "AR SECO"
    elif umid_media > 60:
        return "AR HUMIDO"
    else:
        return "MODERADO"

def enviar_thingspeak(temp, umid):
    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temp:.1f}&field2={umid:.1f}"
        resposta = urequests.get(url)
        resposta.close()
    except Exception as e:
        print("Erro ao enviar para ThingSpeak:", e)

# --- EXECUÇÃO PRINCIPAL ---
conectar_wifi()

while True:
    try:
        # 1. Aquisição de Dados
        sensor.measure()
        temp_atual = sensor.temperature()
        umid_atual = sensor.humidity()
        
        # 2. Processamento Local na Borda (Média Móvel)
        temp_med = calcular_media(historico_temp, temp_atual)
        umid_med = calcular_media(historico_umid, umid_atual)
        status = determinar_status(temp_med, umid_med)
        
        # 3. Formatação IHM sem sobreposição (Uso de :<16 para alinhamento à esquerda com preenchimento)
        texto_linha1 = f"T:{temp_med:.1f}C U:{umid_med:.0f}%"
        texto_linha2 = f"Status: {status}"
        
        # Garante exatamente 16 caracteres em cada linha limpando os espaços excedentes
        linha1_formatada = f"{texto_linha1:<16}"[:16]
        linha2_formatada = f"{texto_linha2:<16}"[:16]
        
        lcd.clear()
        lcd.putstr(f"{linha1_formatada}\n{linha2_formatada}")
        
        # 4. Telemetria
        enviar_thingspeak(temp_med, umid_med)
        
    except Exception as e:
        lcd.clear()
        lcd.putstr("Erro de Leitura")
        print("Erro:", e)
        
    time.sleep(15)
