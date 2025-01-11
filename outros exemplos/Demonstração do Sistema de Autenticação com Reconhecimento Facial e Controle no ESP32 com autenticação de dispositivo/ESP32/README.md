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

- imagem do circuito exemplo:

   ![CIRCUITO](/exemplos/Demonstração%20do%20Sistema%20de%20Autenticação%20com%20Reconhecimento%20Facial%20e%20Controle%20no%20ESP32/ESP32/Exemplo%20do%20circuito%20com%20o%20esp32.png)


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

### Sistema de Autenticação de Dispositivo

O sistema realiza autenticação baseada no endereço MAC do dispositivo. Cada dispositivo possui um ID único e informações associadas, como o local de instalação. Os dados são enviados em formato JSON para o servidor, que valida o acesso.

####  Exemplo de estrutura JSON enviado pelo dispositivo:

```json
{
  "mac": "00:1A:2B:3C:4D:5E",
  "local": "casa",
  "esp_id": "1234567890abcdef"
}
```

- **mac**: Endereço MAC do dispositivo.
- **local**: Identificação do local onde o dispositivo está instalado.
- **esp_id**: Identificador único do dispositivo (derivado do hardware).

#### Requisitos do Banco de Dados

No servidor, a tabela `dispositivos` armazena informações essenciais para autenticação. A estrutura SQL recomendada é:

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

> **OBS**: Lembrando que isso é apenas um exemplo e pode ser modificado de acorda a sua necessidade

#### Por que essa tabela é necessária?

1. **Autenticidade**: O uso do endereço MAC garante que apenas dispositivos autorizados podem acessar o sistema.
2. **Identificação Única**: Cada dispositivo é identificado de forma exclusiva pelo `esp_id`.
3. **Segurança**: Restrições, como validação do formato MAC, ajudam a evitar inconsistências e entradas inválidas.
4. **Organização**: O campo `local` facilita o monitoramento e gerenciamento de dispositivos distribuídos.

---

### Considerações Adicionais

- **LEDs**: Se você não tiver os LEDs, pode remover as partes do código relacionadas a eles, ou ainda, substituí-los por outras formas de feedback visual, como o uso de um display ou mensagens no terminal serial.
  
- **Botão**: O botão inicia a solicitação para verificar o status do acesso. Quando pressionado, o código fará uma requisição HTTP ao servidor, e dependendo da resposta, ativará o LED correspondente.

- **Testes**: Certifique-se de testar a conexão Wi-Fi do ESP32 e a resposta do servidor. Para isso, você pode fazer ajustes no servidor para simular diferentes tipos de resposta, como um código de acesso válido ou inválido.

- **Adaptação**: Todo o código aqui apresentado pode ser adaptado para outras aplicações conforme a sua necessidade. Basta ajustar os componentes de hardware, as variáveis de rede e o tratamento das respostas para atender aos requisitos específicos do seu projeto.
