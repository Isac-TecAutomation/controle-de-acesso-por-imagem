### Demonstração Completa do Sistema de Autenticação com Reconhecimento Facial, Controle no ESP32 e Geração de Histórico de Acesso

## Visão Geral

Este projeto utiliza o **ESP32** e o **reconhecimento facial** para autenticação de usuários. Ele se baseia em uma aplicação desenvolvida com o framework **Flask** (Python) e um sistema de controle com um **botão físico** conectado ao ESP32. O objetivo é criar um sistema de controle de acesso que autentique usuários com base em imagens faciais, retornando a autenticação ao pressionar o botão.

### Objetivo

O sistema simula um controle de acesso onde o **ESP32** interage com um servidor Flask para autenticar usuários via reconhecimento facial. Quando o botão no circuito do ESP32 é pressionado, o dispositivo envia uma requisição HTTP ao servidor Flask, que então verifica a identidade do usuário e retorna uma resposta, seja de sucesso ou falha na autenticação.

---

## Estrutura do Projeto

O projeto está dividido em três partes principais:

1. **Servidor Flask**:
   - Responsável por processar as imagens faciais e verificar a autenticidade dos usuários.
   - Utiliza **Python** com o framework **Flask** para fornecer uma API simples.
   - Responde a requisições HTTP vindas do ESP32, retornando informações sobre a autenticação do usuário.

2. **ESP32**:
   - Conectado a um circuito com um **botão físico**.
   - Envia uma requisição HTTP ao servidor Flask ao pressionar o botão para verificar se a imagem facial corresponde a um usuário autenticado.

3. **Sistema de Histórico**:
   - Armazena registros de todas as tentativas de acesso, sejam elas bem-sucedidas ou falhas.
   - Inclui informações como:
     - Endereço **MAC** do dispositivo que fez a requisição.
     - Resultado da autenticação (sucesso ou falha).
     - Data e hora da tentativa.
   - Permite que administradores analisem padrões de acesso e identifiquem possíveis fraudes ou acessos não autorizados.

---

### Funcionamento:

1. Cada dispositivo possui um endereço **MAC** único.
2. Esse endereço é registrado no banco de dados em uma tabela chamada `dispositivos`.
3. Quando o ESP32 faz uma solicitação ao servidor, ele envia o endereço MAC como parte do corpo da requisição.
4. O servidor valida o MAC comparando-o com os registros no banco de dados.
5. Caso o MAC seja válido, o dispositivo é autenticado, e a requisição continua sendo processada. Caso contrário, a solicitação é rejeitada.

6. Após a autenticação do dispositivo, o servidor Flask processa a imagem facial e verifica se o usuário está autenticado (supondo que as imagens faciais estejam previamente cadastradas no sistema).

7. O servidor registra o resultado da autenticação no sistema de histórico, incluindo o endereço MAC, o status da autenticação e o horário da tentativa.

8. O servidor retorna um **status de autenticação** que é exibido no terminal do **ESP32**. O resultado pode ser:
   - **Autenticação bem-sucedida** (acesso autorizado).
   - **Falha na autenticação** (não identificado).

---

### Sistema de Histórico

O sistema de histórico é um componente crítico para monitorar as atividades de autenticação. Ele funciona da seguinte forma:

1. **Registro de Tentativas**:
   - Cada tentativa de acesso é registrada no banco de dados, independente de seu sucesso.
   - Informações como endereço MAC, data, hora e resultado da autenticação são armazenadas.

2. **Consulta ao Histórico**:
   - Um painel administrativo (ou API) permite que os administradores acessem o histórico.
   - Filtros como período de tempo, endereço MAC e resultado da autenticação ajudam a refinar as consultas.

3. **Segurança e Auditoria**:
   - O histórico serve como uma camada extra de segurança, ajudando a identificar dispositivos não autorizados ou atividades suspeitas.
   - Também possibilita auditorias para verificar a conformidade do sistema com políticas de acesso.

---

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

4. O registro da tentativa será automaticamente salvo no histórico para futuras consultas.

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

Esse projeto fornece um exemplo simples de como o **ESP32** pode ser integrado a um sistema de autenticação facial, onde a comunicação é feita via **HTTP** entre o ESP32 e o servidor Flask. O sistema de histórico reforça a segurança e confiabilidade, permitindo monitorar as tentativas de acesso e identificar padrões ou irregularidades. O sistema pode ser expandido e adaptado para diferentes aplicações de controle de acesso com **reconhecimento facial** e autenticação de usuários em tempo real.

---

## Licença

Este projeto é licenciado sob a Licença MIT - consulte o arquivo LICENSE para mais detalhes.
