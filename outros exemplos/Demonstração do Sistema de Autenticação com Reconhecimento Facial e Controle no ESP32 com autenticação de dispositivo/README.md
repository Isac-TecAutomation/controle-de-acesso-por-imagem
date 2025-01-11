# Demonstração do Sistema de Autenticação com Reconhecimento Facial e Controle no ESP32 com Autenticação de dispositivo

## Visão Geral

Este projeto utiliza o **ESP32** e o **reconhecimento facial** para autenticação de usuários. Ele se baseia em uma aplicação desenvolvida com o framework **Flask** (Python) e um sistema de controle com um **botão físico** conectado ao ESP32. O objetivo é criar um sistema de controle de acesso que autentique usuários com base em imagens faciais, retornando a autenticação ao pressionar o botão.

### Objetivo

O sistema simula um controle de acesso onde o **ESP32** interage com um servidor Flask para autenticar usuários via reconhecimento facial. Quando o botão no circuito do ESP32 é pressionado, o dispositivo envia uma requisição HTTP ao servidor Flask, que então verifica a identidade do usuário e retorna uma resposta, seja de sucesso ou falha na autenticação.

---

## Estrutura do Projeto

O projeto está dividido em duas partes principais:

1. **Servidor Flask**:
   - Responsável por processar as imagens faciais e verificar a autenticidade dos usuários.
   - Utiliza **Python** com o framework **Flask** para fornecer uma API simples.
   - Responde a requisições HTTP vindas do ESP32, retornando informações sobre a autenticação do usuário.

2. **ESP32**:
   - Conectado a um circuito com um **botão físico**.
   - Envia uma requisição HTTP ao servidor Flask ao pressionar o botão para verificar se a imagem facial corresponde a um usuário autenticado.

---

### Funcionamento:

1. Cada dispositivo possui um endereço **MAC** único.
2. Esse endereço é registrado no banco de dados em uma tabela chamada `dispositivos`.
3. Quando o ESP32 faz uma solicitação ao servidor, ele envia o endereço MAC como parte do corpo da requisição.
4. O servidor valida o MAC comparando-o com os registros no banco de dados.
5. Caso o MAC seja válido, o dispositivo é autenticado, e a requisição continua sendo processada. Caso contrário, a solicitação é rejeitada.

3. após a autenticação de dispositivos o servidor Flask processa a imagem facial e verifica se o usuário está autenticado (supondo que as imagens faciais estejam previamente cadastradas no sistema).

4. O servidor retorna um **status de autenticação** que é exibido no terminal do **ESP32**. O resultado pode ser:
   - **Autenticação bem-sucedida** (acesso autorizado).
   - **Falha na autenticação** (não identificado).


Esse mecanismo reforça a segurança, garantindo que apenas dispositivos confiáveis possam interagir com o sistema de controle de acesso.

Além disso, a autenticação de dispositivos é importante para evitar a falsificação de requisições por dispositivos não autorizados. Assim, mesmo que o sistema seja exposto a ataques, apenas dispositivos previamente registrados poderão se comunicar com a API, aumentando a confiabilidade e segurança do projeto.

## Requisitos

### Hardware

- **ESP32**
- **Botão físico**
- **Circuito de conexão do botão ao ESP32** (qualquer pino digital pode ser utilizado)

### Software

- **Python** (para rodar o servidor Flask)

- **Bibliotecas para o ESP32**:
  - **urequests** para envio de requisições HTTP

---

## Instruções de Uso

### 1. Configuração do Circuito no ESP32

1. Conecte o botão a um pino digital do **ESP32** (exemplo: GPIO 15).
2. Configure o código no **ESP32** para enviar uma requisição HTTP ao servidor Flask sempre que o botão for pressionado.
3. Faça o upload do código para o ESP32.

### 2. Executando o Sistema

1. Com o servidor Flask já rodando e o ESP32 configurado, pressione o botão no circuito.
2. O **ESP32** enviará uma requisição HTTP ao servidor Flask para verificar a autenticidade do usuário.
3. O resultado da autenticação será exibido no terminal do **ESP32**:
   - **Acesso autorizado**: Quando o usuário for autenticado com sucesso.
   - **Não foi possível identificar o usuário**: Quando a autenticação falhar.

---

## Exemplo de Saída no Terminal do ESP32

Após pressionar o botão, o terminal do **ESP32** exibirá um dos seguintes resultados:

- **Acesso autorizado**:
  ```bash
  Acesso Autorizado
  ```

- **Não foi possível identificar o usuário**:
  ```bash
  Não foi possível identificar o usuário.
  ```

---

## Conclusão

Esse projeto fornece um exemplo simples de como o **ESP32** pode ser integrado a um sistema de autenticação facial, onde a comunicação é feita via **HTTP** entre o ESP32 e o servidor Flask. O sistema pode ser expandido e adaptado para diferentes aplicações de controle de acesso com **reconhecimento facial** e autenticação de usuários em tempo real.

---

## Licença

Este projeto é licenciado sob a Licença MIT - consulte o arquivo LICENSE para mais detalhes.

---
