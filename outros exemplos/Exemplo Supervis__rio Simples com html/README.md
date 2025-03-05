# Exemplo Supervisório Simples com HTML

## Objetivo do Projeto

O projeto "Exemplo Supervisório Simples com HTML" tem como objetivo fornecer uma interface básica de controle de acesso utilizando **HTML** e **JavaScript**. Este exemplo visa demonstrar como criar uma interface de **login** e um **painel inicial** com a exibição de mensagens dinâmicas, adequado para sistemas de controle de acesso, como o controle de usuários baseado em imagens.

Este projeto inclui duas páginas principais:

1. **Página de Login (login.html)**:
   - A página de login permite que os usuários se autentiquem inserindo seu **email** e **senha**.
   - Após a submissão do formulário, os dados são enviados para o servidor (via POST) e o sistema exibe uma mensagem de alerta com o resultado da tentativa de login.
   - A interface é simples e objetiva, com campos obrigatórios para garantir que o login só seja enviado com os dados completos.

2. **Página Inicial (home.html)**:
   - A página inicial é uma possível continuação do sistema de controle de acesso, onde os administradores ou usuários autenticados podem acessar informações sobre **histórico de acessos**, **dispositivos registrados** e outras funcionalidades relevantes.
   - Embora a página inicial não esteja completamente definida neste exemplo, ela pode ser expandida para incluir mais funcionalidades, como a visualização e adição de usuários, ou a exibição de registros e eventos de login.

## Funcionamento Geral do Sistema

O sistema de autenticação é composto por duas etapas principais: **autenticação de dispositivos** e **autenticação de usuários com reconhecimento facial**. 

### 1. **Autenticação de Dispositivos**: 
   Cada dispositivo (como o ESP32) possui um endereço **MAC** único, registrado no banco de dados. Quando o ESP32 faz uma requisição ao servidor Flask, ele envia seu endereço MAC. O servidor valida esse MAC, garantindo que apenas dispositivos autorizados possam realizar requisições.
   
### 2. **Autenticação de Usuário com Reconhecimento Facial**:
   Após o dispositivo ser autenticado, o servidor Flask processa a imagem facial do usuário, comparando-a com as imagens armazenadas no banco de dados. O servidor então retorna um status de autenticação, indicando se o usuário foi reconhecido ou não.

### 3. **Geração de Histórico de Acesso**:
   O sistema gera um **histórico de acessos**, que registra as ações dos usuários no sistema, incluindo o dispositivo utilizado, o IP do usuário, a confiança do reconhecimento facial, e a data e hora do acesso. Esses dados são registrados no banco de dados para análise posterior.

---

## Passos Detalhados para Implementação

### **Passo 1: Preparar o ESP32**

Antes de iniciar a integração, configure o **ESP32** corretamente. O ESP32 será o responsável por capturar eventos (como o pressionamento de um botão) e enviar requisições HTTP ao servidor Flask.

1. **Conectar o Botão ao ESP32**:
   O botão será conectado a um pino digital do ESP32, que envia uma requisição HTTP quando pressionado. Exemplo: GPIO 15.

2. **Configuração de Rede**:
   O ESP32 precisa estar configurado para se conectar à rede Wi-Fi e enviar requisições HTTP ao servidor Flask.

---

### **Passo 2: Criar as Tabelas no Banco de Dados**

O banco de dados precisa armazenar informações sobre **dispositivos**, **usuários** e **histórico de acessos**. Abaixo estão os códigos SQL para criar as tabelas necessárias(exemplos):

1. **Tabela de Dispositivos**: Registra os dispositivos autorizados a realizar requisições no sistema.

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
) ENGINE = InnoDB;
```

2. **Tabela de Usuários**: Armazena informações de cada usuário, incluindo a imagem facial para reconhecimento.

```sql
CREATE TABLE usuarios (
    nome VARCHAR(100) NOT NULL,  
    email VARCHAR(255) UNIQUE CHECK (email LIKE '%_@__%.__%'),  
    senha VARCHAR(255) CHECK (senha REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'),  
    imagem TEXT NOT NULL,
    PRIMARY KEY (email)
) ENGINE=InnoDB;
```

3. **Tabela de Histórico**: Registra cada acesso de um usuário ao sistema, incluindo detalhes como IP, dispositivo utilizado e a confiança no reconhecimento facial.

```sql
CREATE TABLE `historico` (
    `nome` varchar(100) NOT NULL,  
    `email` varchar(255) NOT NULL,  
    `mac` varchar(20) DEFAULT NULL,  
    `ip` varchar(15) NOT NULL,  
    `local` varchar(100) DEFAULT NULL,  
    `esp_id` varchar(30) DEFAULT NULL,  
    `trust` int NOT NULL,  
    `data_acesso` date DEFAULT NULL,  
    `horario_acesso` time DEFAULT NULL, 
    KEY `esp_id` (`esp_id`),
    KEY `local` (`local`),
    KEY `email` (`email`),
    CONSTRAINT `historico_ibfk_1` FOREIGN KEY (`esp_id`) REFERENCES `dispositivos` (`esp_id`) ON DELETE SET NULL,
    CONSTRAINT `historico_ibfk_2` FOREIGN KEY (`local`) REFERENCES `dispositivos` (`local`) ON DELETE SET NULL,
    CONSTRAINT `historico_ibfk_3` FOREIGN KEY (`email`) REFERENCES `usuarios` (`email`) ON DELETE CASCADE,
    CONSTRAINT `historico_chk_1` CHECK (
        regexp_like(
            `ip`,
            _utf8mb4 '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'  
        )
    ),
    CONSTRAINT `historico_chk_2` CHECK ((`trust` between 0 and 100))  
) ENGINE = InnoDB;
```

---

### **Passo 3: Subir o Servidor Flask**

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

### **Passo 4: Configuração do Circuito no ESP32**

1. **Conectar o Botão**:

   O botão será conectado ao pino GPIO 15 do ESP32. Quando pressionado, o ESP32 enviará uma requisição HTTP ao servidor Flask para autenticação de dispositivos e usuários.

2. **Configuração do Código do ESP32**:

   No código do ESP32, implemente a funcionalidade de enviar uma requisição HTTP para o servidor Flask. Isso pode ser feito com a biblioteca **HTTPClient** do Arduino.

---

### **Passo 5: Executando o Sistema**

1. **Pressionar o Botão**:

   Quando o botão é pressionado, o ESP32 envia uma requisição ao servidor Flask, incluindo o endereço MAC do dispositivo.

2. **Processamento no Servidor Flask**:

   O servidor Flask valida o endereço MAC, processa a imagem facial do usuário e retorna o status de autenticação.

3. **Resultado no Terminal do ESP32**:

   O resultado da autenticação será exibido no terminal do ESP32:

   - **Autenticação bem-sucedida**:

     ```bash
     Acesso Autorizado
     ```

   - **Falha na autenticação**:

     ```bash
     Não foi possível identificar o usuário.
     ```

---

### **Passo 6: Geração de Histórico de Acesso**

O sistema gera um histórico detalhado de cada acesso, que é armazenado na tabela `historico` do banco de dados. Isso pode incluir informações como o nome do usuário, o IP do dispositivo, o nível de confiança no reconhecimento facial e o dispositivo utilizado. 

---

## Considerações Finais

Este sistema de autenticação facial com controle no ESP32 oferece uma solução inovadora, eficiente e de baixo custo para controle de acesso, combinando autenticação de dispositivos e reconhecimento facial. A utilização do ESP32, aliado ao Flask para a criação da API e ao banco de dados para registro dos acessos, garante um sistema robusto e seguro, com possibilidade de monitoramento em tempo real. A geração de um histórico detalhado de acessos, incluindo informações como dispositivo utilizado, IP do usuário, e o nível de confiança no reconhecimento facial, proporciona uma camada adicional de segurança e possibilita o rastreamento de eventuais falhas ou tentativas fraudulentas de acesso.

Este modelo de controle de acesso pode ser facilmente adaptado e expandido conforme as necessidades do projeto, permitindo a inclusão de novas funcionalidades, como integração com outras formas de autenticação (como PIN ou QR code), e a melhoria contínua da segurança. A solução é especialmente adequada para ambientes onde a acessibilidade e a praticidade são essenciais, oferecendo uma alternativa eficiente para sistemas de segurança convencionais.