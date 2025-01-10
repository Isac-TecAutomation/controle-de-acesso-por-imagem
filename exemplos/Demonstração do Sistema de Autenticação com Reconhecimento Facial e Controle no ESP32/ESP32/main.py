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

from utime import ticks_ms, ticks_diff, sleep_ms  # Importa funções para temporização
import urequests as req  # Importa a biblioteca para fazer requisições HTTP
from machine import Pin, reset  # Importa funções para controle de pinos e reset do dispositivo
import network  # Importa a biblioteca de rede

# Definição dos pinos de entrada e saída para o botão e LEDs
BTN_PIN = 21  # Pino de entrada do botão
LED_AMARELO_PIN = 23  # Pino de saída do LED amarelo
LED_AZUL_PIN = 22  # Pino de saída do LED azul

# Configuração do botão e LEDs como objetos Pin
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)  # Configura o botão como entrada com pull-up
led_amarelo = Pin(LED_AMARELO_PIN, Pin.OUT)  # Configura o LED amarelo como saída
led_azul = Pin(LED_AZUL_PIN, Pin.OUT)  # Configura o LED azul como saída

# Desliga os LEDs inicialmente
led_amarelo.off()
led_azul.off()


# variaveis importante

timeout = "<o tempo limite para o esp conectar na rede>  (int)"
password = "<a senha da sua rede>"
host_api = "<host da sua api>"
ssid = "<o nome da sua rede>"
led_duration = 500  # Define o tempo de duração que os LEDs permanecem ligados (500ms)

def wifi(ssid, password, timeout_ms):
    """
    Função para conectar o ESP32 a uma rede Wi-Fi.
    Retorna o status da conexão e os dados de IP e MAC em caso de sucesso.
    """
    # Ativa a interface Wi-Fi e tenta se conectar
    net = network.WLAN(network.STA_IF)
    net.active(True)
    net.connect(ssid, password)

    try:
        # Tenta a conexão até o tempo limite (timeout_s), verificando a cada 500ms
        for i in range(timeout_ms * 2):  # Multiplicamos por 2 para verificar a cada 500ms
            if net.isconnected():  # Se conectado, retorna os dados de conexão
                mac = ':'.join(['{:02x}'.format(byte) for byte in net.config('mac')])  # Converte o MAC para string
                ip = net.ifconfig()[0]  # Pega o endereço IP da interface de rede
                return True, (mac, ip)  # Retorna True e os dados de MAC e IP

            print('.', end="", flush=True)  # Exibe um ponto a cada tentativa
            sleep_ms(500)  # Aguarda 500ms antes de tentar novamente
        
        # Se o tempo limite for atingido, retorna uma mensagem de erro
        return False, f'Erro: conexão mal-sucedida à rede {ssid}'
    
    except Exception as e:  # Em caso de erro, captura a exceção e retorna
        return False, f'Erro: {e}'


def manage_leds(led, other_led, start_time, duration_ms):
    """
    Função para gerenciar o tempo de ativação dos LEDs.
    Garante que o LED 'led' fique ligado por 'duration_ms' milissegundos e desliga o outro LED.
    """
    now = ticks_ms()  # Pega o tempo atual em milissegundos
    if ticks_diff(now, start_time) >= duration_ms:  # Verifica se o tempo de duração passou
        led.off()  # Desliga o LED
    else:
        other_led.off()  # Desliga o outro LED enquanto o tempo ainda não passou


if __name__ == '__main__':
    
    # Tenta conectar à rede Wi-Fi
    conn = wifi(ssid, password, timeout)
    
    if not conn[0]:  # Se a conexão falhar
        print(conn[1])  # Exibe a mensagem de erro
        reset()  # Faz o reset do dispositivo
    
    else:  # Se a conexão for bem-sucedida
        print(f'Dados do ESP: {conn[1]}')  # Exibe o endereço IP e MAC do dispositivo

        # Variáveis para controlar os tempos de ativação dos LEDs
        led_amarelo_start = None
        led_azul_start = None

        while True:
            if not btn.value():  # Se o botão for pressionado
                try:
                    # Faz uma requisição POST para a API para verificar o acesso
                    response = req.post('http://192.168.0.30:5002/face_verify')
                    data = response.json()  # Converte a resposta em JSON

                    if isinstance(data, list) and any(user.get("Auth") for user in data):  # Se a resposta for válida
                        print("Acesso autorizado")
                        led_amarelo.off()  # Desliga o LED amarelo
                        led_azul.on()  # Liga o LED azul
                        led_azul_start = ticks_ms()  # Inicia o temporizador para o LED azul
                        
                    else:  # Se o acesso for negado
                        print("Acesso negado")
                        led_azul.off()  # Desliga o LED azul
                        led_amarelo.on()  # Liga o LED amarelo
                        led_amarelo_start = ticks_ms()  # Inicia o temporizador para o LED amarelo
                    
                except Exception as e:  # Se ocorrer algum erro durante a requisição
                    print("Erro:", e)
                    led_azul.off()  # Desliga o LED azul em caso de erro
                    led_amarelo.on()  # Liga o LED amarelo
                    led_amarelo_start = ticks_ms()  # Inicia o temporizador para o LED amarelo

            # Chama a função de gerenciamento dos LEDs de forma não bloqueante
            if led_azul_start:  # Se o LED azul foi acionado
                manage_leds(led_azul, led_amarelo, led_azul_start, led_duration)
            
            if led_amarelo_start:  # Se o LED amarelo foi acionado
                manage_leds(led_amarelo, led_azul, led_amarelo_start, led_duration)
