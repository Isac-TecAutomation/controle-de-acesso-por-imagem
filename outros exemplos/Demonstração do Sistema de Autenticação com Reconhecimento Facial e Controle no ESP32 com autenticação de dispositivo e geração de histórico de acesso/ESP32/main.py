# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: Demonstração do código para o esp32 (cliente)

# ==============================================

from utime import ticks_ms, ticks_diff, sleep_ms  # Temporização para controlar os LEDs e medir intervalos de tempo
import urequests as req  # Biblioteca para realizar requisições HTTP
from machine import Pin  # Controle de pinos GPIO do ESP32
import network  # Biblioteca para gerenciar conexões Wi-Fi
from machine import unique_id  # Obtenção do identificador único do dispositivo
import ubinascii  # Biblioteca para manipular dados binários em formato ASCII
import ujson  # Biblioteca para manipulação de JSON no MicroPython
import sys  # Biblioteca para saída do programa

# ==============================================
# Configurações iniciais
# ==============================================
# ID único do chipset, usado para identificar o dispositivo na rede
chip_id = ubinascii.hexlify(unique_id()).decode()

# Pinos GPIO do ESP32 utilizados no projeto
BTN_PIN = 21  # Botão
LED_AMARELO_PIN = 23  # LED amarelo (indica falha ou acesso negado)
LED_AZUL_PIN = 22  # LED azul (indica sucesso ou acesso autorizado)

# Configuração dos pinos como entrada ou saída
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)  # Configura o botão com pull-up interno
led_amarelo = Pin(LED_AMARELO_PIN, Pin.OUT)  # Configura o LED amarelo como saída
led_azul = Pin(LED_AZUL_PIN, Pin.OUT)  # Configura o LED azul como saída

# Inicializa os LEDs como desligados
led_amarelo.off()
led_azul.off()

# ==============================================
# Variáveis de configuração destacadas
# ==============================================
SSID = "Familiabuscape"  # Nome da rede Wi-Fi (SSID)
PASSWORD = "Elephant33"  # Senha da rede Wi-Fi
API_HOST = "http://192.168.0.30:5002"  # URL base do servidor da API
DIR = "/face_verify" #diretório para o endpoint na API

# ==============================================
# Função para conexão Wi-Fi
# ==============================================
def wifi(ssid, password, timeout_ms):
    """
    Conecta o dispositivo a uma rede Wi-Fi.

    Args:
        ssid (str): Nome da rede Wi-Fi.
        password (str): Senha da rede Wi-Fi.
        timeout_s (int): Tempo limite para tentar a conexão (em segundos).

    Returns:
        tuple: Status da conexão (True ou False) e dados da conexão (MAC e IP).
    """
    net = network.WLAN(network.STA_IF)  # Configura o Wi-Fi em modo estação
    net.active(True)  # Ativa a interface Wi-Fi
    net.connect(ssid, password)  # Conecta à rede com o SSID e senha fornecidos

    try:
        # Tenta conectar dentro do tempo limite
        for i in range(timeout_ms * 2):
            if net.isconnected():
                mac = ':'.join(['{:02x}'.format(byte) for byte in net.config('mac')])  # Obtém o MAC address
                ip = net.ifconfig()[0]  # Obtém o endereço IP
                return True, (mac, ip)

            print('.', end="", flush=True)  # Exibe progresso na tentativa de conexão
            sleep_ms(500)  # Aguarda 500 ms antes de verificar novamente

        # Se não conectar dentro do tempo limite, interrompe o programa
        print("\nErro: Falha na conexão Wi-Fi. Programa interrompido.")
        sys.exit()

    except Exception as e:
        # Em caso de erro crítico, interrompe o programa
        print(f"\nErro crítico: {e}. Programa interrompido.")
        sys.exit()

# ==============================================
# Função para gerenciar LEDs
# ==============================================
def manage_leds(led, other_led, start_time, duration_ms):
    """
    Gerencia o estado de um LED com base na duração especificada.

    Args:
        led (Pin): LED que será gerenciado.
        other_led (Pin): Outro LED que será desligado para evitar conflitos.
        start_time (int): Tempo de início em milissegundos.
        duration_ms (int): Duração em milissegundos para manter o LED ligado.
    """
    now = ticks_ms()  # Obtém o tempo atual em milissegundos
    if ticks_diff(now, start_time) >= duration_ms:  # Verifica se o tempo expirou
        led.off()  # Desliga o LED
    else:
        other_led.off()  # Garante que o outro LED está desligado

# ==============================================
# Função principal
# ==============================================
if __name__ == '__main__':
    """
    Programa principal para controle de acesso utilizando LEDs e requisições HTTP.
    """
    # Tenta conectar à rede Wi-Fi
    conn = wifi(SSID, PASSWORD, 10)  # Configurações de rede Wi-Fi

    print(f'Dados do ESP: {conn[1]}')  # Exibe os dados da conexão (IP e MAC)

    # Dados do dispositivo para envio via requisição HTTP
    data = {
        "mac": conn[1][0],  # Endereço MAC do dispositivo
        "local": "casa",  # Local onde o dispositivo está instalado
        "esp_id": chip_id,  # ID único do dispositivo
    }

    # Variáveis de controle para os LEDs
    led_amarelo_start = None  # Tempo de início do LED amarelo
    led_azul_start = None  # Tempo de início do LED azul
    led_duration = 2000  # Duração para manter os LEDs ligados (em ms)

    while True:
        # Verifica se o botão foi pressionado
        if not btn.value():  # Botão pressionado (valor lógico invertido por pull-up)
            try:
                payload = ujson.dumps(data)  # Converte os dados para JSON

                # Fazendo a requisição POST para o servidor
                response = req.post(API_HOST+DIR, data=payload)

                if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                    resp_data = response.json()  # Converte a resposta para JSON
                    if isinstance(resp_data, list) and any(
                        user.get("Auth") for user in resp_data
                    ):
                        # Acesso autorizado
                        print("Acesso autorizado")
                        led_amarelo.off()
                        led_azul.on()
                        led_azul_start = ticks_ms()  # Registra o tempo de início do LED azul
                    else:
                        # Acesso negado
                        print("Acesso negado")
                        led_azul.off()
                        led_amarelo.on()
                        led_amarelo_start = ticks_ms()  # Registra o tempo de início do LED amarelo
                else:
                    # Erro na requisição
                    print("Erro na requisição:", response.status_code)
                    led_amarelo.on()
                    led_azul.off()
                    led_amarelo_start = ticks_ms()

            except Exception as e:
                # Trata erros durante a execução
                print("Erro:", e)
                led_azul.off()
                led_amarelo.on()
                led_amarelo_start = ticks_ms()

        # Gerencia o estado do LED azul com base no tempo de duração
        if led_azul_start:
            manage_leds(led_azul, led_amarelo, led_azul_start, led_duration)

        # Gerencia o estado do LED amarelo com base no tempo de duração
        if led_amarelo_start:
            manage_leds(led_amarelo, led_azul, led_amarelo_start, led_duration)

