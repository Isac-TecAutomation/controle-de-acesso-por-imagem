# Demonstração do Sistema de Autenticação com Reconhecimento Facial e Controle no ESP32 com autenticação de dispositivos

## Visão Geral
Este exemplo demonstra como integrar o servidor com um **ESP32** para autenticação de usuários e controle com **reconhecimento facial**. O servidor Flask é responsável pela comunicação e autenticação de usuários, enquanto o ESP32 interage com o hardware e o sistema ao pressionar um botão. Ao pressionar o botão, o ESP32 envia uma requisição ao servidor para verificar a autenticidade do usuário e recebe o resultado de volta.

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


## Passos para Usar o Sistema

### **Passo 1: Preparar o ESP32**

Antes de seguir com esta demonstração, é necessário configurar o seu **ESP32** corretamente. Para isso, siga o tutorial de preparação do **ESP32** disponível [aqui](#).

---

#### **passo 2: Preparar as tabelas no Banco de dados

Após o preparo do esp32 deve se criar as tabelas que cuidará das informações sobre os usuarios 
e outra sobre os dipositivos autorizados a fazer a requisições no sistema. 

caso queria basta copiar o código abaixo que gera duas tabelas, a tabela `usuarios` e a tabela `dispositivos` 
para seu  projeto:

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

CREATE TABLE usuarios (
    nome VARCHAR(100) NOT NULL, -- Nome completo do usuário
    email VARCHAR(255) UNIQUE CHECK (email LIKE '%_@__%.__%'), -- Email único, validado por padrão de formato
    senha VARCHAR(255) CHECK (senha REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'), -- Senha com validação de complexidade
    imagem TEXT NOT NULL, -- Caminho ou dados da imagem de rosto do usuário para reconhecimento facial
    PRIMARY KEY (email) -- Email como identificador único do usuário
) ENGINE=InnoDB;


```

> **OBS**: Lembrando que isso é apenas um exemplo e pode ser modificado de acorda a sua necessidade

---

#### Por que essa tabela é necessária?

1. **Autenticidade**: O uso do endereço MAC garante que apenas dispositivos autorizados podem acessar o sistema.
2. **Identificação Única**: Cada dispositivo é identificado de forma exclusiva pelo `esp_id`.
3. **Segurança**: Restrições, como validação do formato MAC, ajudam a evitar inconsistências e entradas inválidas.
4. **Organização**: O campo `local` facilita o monitoramento e gerenciamento de dispositivos distribuídos.

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
