# Demonstração do Sistema de Autenticação com Reconhecimento Facial e Controle no ESP32

## Visão Geral
Este exemplo demonstra como integrar o servidor com um **ESP32** para autenticação de usuários e controle com **reconhecimento facial**. O servidor Flask é responsável pela comunicação e autenticação de usuários, enquanto o ESP32 interage com o hardware e o sistema ao pressionar um botão. Ao pressionar o botão, o ESP32 envia uma requisição ao servidor para verificar a autenticidade do usuário e recebe o resultado de volta.

---

## Passos para Usar o Sistema

### **Passo 1: Preparar o ESP32**

Antes de seguir com esta demonstração, é necessário configurar o seu **ESP32** corretamente. Para isso, siga o tutorial de preparação do **ESP32** disponível [aqui](#).

---

### **Passo 2: Subir o Servidor Flask**

1. **Instalar a API:**

   Faça o download do arquivo do arquivo `main.py` na pasta API e adicione ao seu ambiente Python. Caso ainda não tenha preparado o ambiente, siga o tutorial [aqui](https://github.com/Isac-TecAutomation/controle-de-acesso-por-imagem/blob/main/README.md).

2. **Iniciar o servidor Flask:**

   Execute o arquivo `main.py` para iniciar o servidor Flask. O servidor será iniciado na porta 5000, e você pode acessar o sistema localmente em:

   ```bash
   python main.py
   ```

3. **Verificar o funcionamento do servidor:**

   O servidor deve agora estar pronto para receber requisições HTTP. Acesse `http://127.0.0.1:5002` no navegador para garantir que tudo esteja funcionando corretamente.

---

### **Passo 3: Configurar o Circuito no ESP32**

1. **Botão:**

   O botão será conectado a um dos pinos digitais do ESP32. Ao ser pressionado, o ESP32 enviará uma requisição HTTP ao servidor Flask para verificar a autenticidade do usuário.

2. **Conexões do Circuito:**

   Conecte o botão a um pino digital do ESP32 (exemplo: GPIO 15) e o circuito estará pronto.

---

### **Passo 4: Executando o Sistema**

Agora que o ESP32 e o servidor Flask estão configurados, siga os passos abaixo para realizar a autenticação:

1. **Pressione o botão**: Quando você pressionar o botão no circuito conectado ao ESP32, o ESP32 enviará uma requisição HTTP ao servidor Flask, pedindo para verificar a imagem facial capturada.

2. **Aguarde o resultado**: O servidor Flask processará a requisição e retornará o resultado no terminal do ESP32.

---

### **Passo 5: Resultados no Terminal do ESP32**

Após pressionar o botão, o ESP32 retornará o resultado no terminal. Você verá uma das seguintes mensagens dependendo do sucesso ou falha da autenticação:

- **Autenticação bem-sucedida**:

   ```bash
   Acesso Autorizado
   ```

- **Falha na autenticação**:

   ```bash
   Não foi possível identificar o usuário.
   ```

---

### **Passo 6: Teste Completo**

1. **Pressione o botão** no circuito conectado ao ESP32.
2. **Observe o terminal** do ESP32 para ver a resposta da autenticação.
3. **Verifique no servidor Flask** se o processamento da imagem facial foi feito corretamente e se os dados do usuário foram retornados.

---

## Considerações Finais

Este sistema de **autenticação facial com controle em ESP32** é uma base excelente para aplicações de controle de acesso com baixo custo. O ESP32 comunica-se com o servidor Flask e responde a eventos como o pressionamento do botão, permitindo a autenticação do usuário com base nas imagens faciais armazenadas no banco de dados.

---
