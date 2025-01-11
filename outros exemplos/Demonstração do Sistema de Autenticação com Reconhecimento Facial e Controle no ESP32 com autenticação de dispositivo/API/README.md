# Controle de Acesso com LEDs e Botão

Este projeto utiliza um botão para iniciar uma solicitação HTTP que verifica se o usuário está autorizado. Dependendo da resposta do servidor, LEDs indicam o status:

- **LED Azul**: Acesso autorizado.
- **LED Amarelo**: Acesso negado ou erro.

## Requisitos

### Hardware:
- ESP32 ou ESP8266
- LEDs (Azul e Amarelo) (opcionais)
- Botão
- Resistores adequados

### Software:
- **Thonny IDE** (Recomendado)
- Suporte ao **Micropython** no dispositivo (caso não tenha o Thonny)

## Vantagens do Micropython:

- **Facilidade de manutenção** e **rápida transmissão de dados** em comparação ao C++ com o framework Arduino (Testado).
- **Compilação rápida** dos arquivos e **ausência da necessidade de conhecimento em C++** para usar com Arduino.

## Como Usar

### 1. Instalação do Ambiente Micropython

1. Verifique se o **Thonny IDE** está instalado no seu PC. Caso não tenha, siga este tutorial para instalá-lo:

   [Tutorial de instalação do Thonny e Micropython](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/)

   - O tutorial também ensina como instalar o **firmware Micropython** no seu dispositivo.

2. Faça o download dos seguintes arquivos:
   - `main.py`
   - A biblioteca `urequests.py`

3. Após baixar os arquivos, **copie-os para o ESP32**:
   - Clique com o botão direito do mouse nos arquivos, no menu que abrir, selecione a opção **Enviar para/** e escolha o ESP32.

4. **Configure as variáveis importantes** no código:
   - Substitua os valores nas variáveis do código, conforme indicado com o comentário **variáveis importantes**.

5. Após a configuração, **aperte em RUN**. O ESP32 estará pronto para ser usado no seu projeto.

---

## Sistema de Autenticação de Dispositivos

O sistema de autenticação de dispositivos é usado para validar os dispositivos ESP32 conectados à API do servidor Flask. Isso garante que apenas dispositivos autorizados possam interagir com o sistema.

### Funcionamento:

1. Cada dispositivo possui um endereço **MAC** único.
2. Esse endereço é registrado no banco de dados em uma tabela chamada `dispositivos`.
3. Quando o ESP32 faz uma solicitação ao servidor, ele envia o endereço MAC como parte do corpo da requisição.
4. O servidor valida o MAC comparando-o com os registros no banco de dados.
5. Caso o MAC seja válido, o dispositivo é autenticado, e a requisição continua sendo processada. Caso contrário, a solicitação é rejeitada.

Esse mecanismo reforça a segurança, garantindo que apenas dispositivos confiáveis possam interagir com o sistema de controle de acesso.

### Exemplo de Estrutura JSON:

```json
{
  "mac": "AA:BB:CC:DD:EE:FF",
  "esp_id": "ESP32_001",
  "local": "Porta Principal"
}
```

### Adicionando um Dispositivo à API:

- Na API a uma função chamada de `register_device` que registra dipositivos novos no
banco de dados, basta chamar seu endpoint no codigo do esp32, o o colocando na variavel `DIR` no código em micropython retornando à API as informações correta do dispositivo.


---

## Exemplo de Tabela SQL no Banco de Dados:

A tabela `dispositivos` é usada para armazenar informações sobre os dispositivos autorizados. O código abaixo mostra como criar essa tabela:

```sql
CREATE TABLE `dispositivos` (
    `mac` varchar(20) NOT NULL,
    `esp_id` varchar(20) NOT NULL,
    `local` varchar(255) NOT NULL,
    PRIMARY KEY (`mac`),
    UNIQUE KEY `esp_id` (`esp_id`),
    UNIQUE KEY `local` (`local`),
    CONSTRAINT `dispositivos_chk_1` CHECK (
        regexp_like(
            `mac`,
            _utf8mb4 '^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$'
        )
    )
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
```

### Importância da Tabela:

1. **Validação dos Dispositivos:** Garante que apenas dispositivos previamente registrados possam acessar o sistema.
2. **Identificação Única:** Cada dispositivo é associado a um endereço MAC único e informações como `esp_id` e `local`.
3. **Segurança:** O uso de validações e restrições no banco de dados previne inconsistências e entradas inválidas.

---

## Considerações Adicionais

- **LEDs**: Se você não tiver os LEDs, pode remover as partes do código relacionadas a eles, ou ainda, substituí-los por outras formas de feedback visual, como o uso de um display ou mensagens no terminal serial.
  
- **Botão**: O botão inicia a solicitação para verificar o status do acesso. Quando pressionado, o código fará uma requisição HTTP ao servidor, e dependendo da resposta, ativará o LED correspondente.

- **Testes**: Certifique-se de testar a conexão Wi-Fi do ESP32 e a resposta do servidor. Para isso, você pode fazer ajustes no servidor para simular diferentes tipos de resposta, como um código de acesso válido ou inválido.

- **Adaptação**: Todo o código aqui apresentado pode ser adaptado para outras aplicações conforme a sua necessidade. Basta ajustar os componentes de hardware, as variáveis de rede e o tratamento das respostas para atender aos requisitos específicos do seu projeto.
