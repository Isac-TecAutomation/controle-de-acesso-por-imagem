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

   ![CIRCUITO](/exemplos/Demonstração do Sistema de Autenticação com Reconhecimento Facial e Controle no ESP32/ESP32/Exemplo do circuito com o esp32.png)




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

### Considerações Adicionais

- **LEDs**: Se você não tiver os LEDs, pode remover as partes do código relacionadas a eles, ou ainda, substituí-los por outras formas de feedback visual, como o uso de um display ou mensagens no terminal serial.
  
- **Botão**: O botão inicia a solicitação para verificar o status do acesso. Quando pressionado, o código fará uma requisição HTTP ao servidor, e dependendo da resposta, ativará o LED correspondente.

- **Testes**: Certifique-se de testar a conexão Wi-Fi do ESP32 e a resposta do servidor. Para isso, você pode fazer ajustes no servidor para simular diferentes tipos de resposta, como um código de acesso válido ou inválido.

- **Adaptação**: Todo o código aqui apresentado pode ser adaptado para outras aplicações conforme a sua necessidade. Basta ajustar os componentes de hardware, as variáveis de rede e o tratamento das respostas para atender aos requisitos específicos do seu projeto.
