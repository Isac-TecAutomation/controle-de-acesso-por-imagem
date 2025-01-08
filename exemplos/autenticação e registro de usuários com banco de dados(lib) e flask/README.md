# Exemplo: Autenticação e Registro de Usuários com Banco de Dados(lib) e flask

## Descrição
Este exemplo demonstra como integrar um banco de dados ao projeto para realizar **autenticação** e **registro de usuários** com base em reconhecimento facial. Ele serve como uma base para entender e implementar as funções disponíveis no arquivo `main.py`.

Também a adição do framework Flask para subir a API na rede assim podendo ser usada em sistemas de IOT

### Funcionalidades principais:
- **Autenticação**: O sistema verifica se a face capturada corresponde a um rosto registrado no banco de dados.
- **Registro de Usuários**: Permite adicionar novos usuários ao banco, armazenando seus dados e imagens faciais para futuras autenticações.

---

## Instalação e Configuração

### 1. Instalação Principal do Projeto
Certifique-se de seguir todas as instruções de instalação do projeto principal. Isso inclui:
- Instalar dependências do Python necessárias para reconhecimento facial e manipulação de banco de dados.
- Configurar corretamente os requisitos descritos no projeto.

### 2. Clonando o Arquivo `main.py`

O arquivo `main.py` contém as funções de autenticação e registro de usuários. Para utilizá-lo:

- Faça o download ou clone o arquivo do repositório oficial. Use o comando abaixo se estiver utilizando Git:

```bash
git clone <URL_DO_REPOSITORIO>
```

- Caso prefira, baixe diretamente o arquivo `main.py` e coloque-o na pasta principal do seu projeto.

### 3. Configurando o Banco de Dados
Este exemplo utiliza um banco de dados relacional (MySQL) para armazenar os dados dos usuários. A seguir está um modelo de tabela que pode ser usado no seu banco de dados.

#### Estrutura da Tabela (Exemplo)

```sql
CREATE TABLE usuarios (
    nome VARCHAR(100) NOT NULL, -- Nome completo do usuário
    email VARCHAR(255) UNIQUE CHECK (email LIKE '%_@__%.__%'), -- Email único, validado por padrão de formato
    senha VARCHAR(255) CHECK (senha REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'), -- Senha com validação de complexidade
    imagem TEXT NOT NULL, -- Caminho ou dados da imagem de rosto do usuário para reconhecimento facial
    PRIMARY KEY (email) -- Email como identificador único do usuário
) ENGINE=InnoDB;
```

### Observações sobre a Tabela:
- **Email**: Deve ser único e segue um padrão válido de email.
- **Senha**: Deve ter pelo menos 8 caracteres, incluindo um número e um caractere especial.
- **Imagem**: Armazena o caminho ou os dados da imagem facial do usuário.

> **Nota:** Você pode personalizar o esquema da tabela conforme as necessidades do seu projeto.

---


## Como Funcionam as Funções no Flask

### **Estrutura do Flask**

O Flask é usado para criar uma API simples que expõe dois endpoints principais. Ambos são configuráveis e podem ser testados por ferramentas HTTP ou diretamente no navegador.

---

### **1. Autenticação de Usuários**

- **Endpoint**: `/face_verify`  
- **Método HTTP**: `GET` #recomendado POST  
- **Descrição**:  
  Este endpoint recebe uma imagem facial capturada e compara seu encoding com os encodings registrados no banco de dados.

- **Funcionamento**:
  1. O sistema acessa o banco de dados configurado, onde estão armazenados os dados dos usuários registrados.
  2. A imagem facial capturada é processada, e seu encoding é extraído.
  3. O encoding é comparado com os registros no banco de dados.
  4. Resultado:
     - **Sucesso**: Retorna as informações do usuário correspondente.
     - **Erro**: Retorna uma mensagem indicando que o rosto não foi identificado.

---

### **2. Registro de Usuários**

- **Endpoint**: `/register_user`  
- **Método HTTP**: `GET` #recomendado POST 
- **Descrição**:  
  Este endpoint permite registrar um novo usuário no sistema, adicionando seus dados e o encoding facial ao arquivo JSON.

- **Funcionamento**:
  1. O cliente envia os dados do usuário (nome, CPF, email etc.) exemplo ?data={"name":"John","age":30}.
  2. O sistema processa a imagem para gerar o encoding facial.
  3. Os dados e o encoding são adicionados ao arquivo banco de dados.
  4. Resultado:
     - O sistema retorna uma mensagem indicando que o usuário foi registrado com sucesso.
  
- Exemplo de JSON com dados do usuário:
  
     ```json
       {
         "nome": "João",
         "email": "joao@email.com",
         "senha": "@Joao123"
       }
    ```
---

### **Demonstração no Navegador**

O Flask permite que o sistema seja acessado diretamente no navegador, facilitando testes e demonstrações. Por exemplo:

- **Autenticação**: Envie uma imagem facial ao endpoint `/face_verify` e visualize o resultado (usuário autenticado ou não identificado).
- **Registro**: Envie os dados e a imagem facial de um novo usuário ao endpoint `/register_user`.

O uso de ferramentas como Postman ou cURL também é recomendado para testar os endpoints.

---

### 4. Uso do `main.py`
O arquivo `main.py` contém funções para registro e autenticação de usuários. Siga as instruções abaixo para utilizá-lo:

1. Certifique-se de que o ambiente está configurado corretamente.
2. Execute o sistema com o comando:
   ```bash
   python main.py
   ```
3. O Flask iniciará um servidor local, normalmente acessível em:
   ```
   http://127.0.0.1:5000
   ```
4. Teste os endpoints utilizando ferramentas como:
   - Navegador: Acesse o endereço para verificar a conexão..

---

Este exemplo é flexível e pode ser usado para estudar ou implementar sistemas de controle de acesso baseados em processamento de imagem e APIs Flask.

## Estrutura do Banco de Dados (Exemplo SQL)
Para facilitar, segue novamente a estrutura SQL do banco de dados:

```sql
CREATE TABLE usuarios (
    nome VARCHAR(100) NOT NULL, -- Nome completo do usuário
    email VARCHAR(255) UNIQUE CHECK (email LIKE '%_@__%.__%'), -- Email único, validado por padrão de formato
    senha VARCHAR(255) CHECK (senha REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'), -- Senha com validação de complexidade
    imagem TEXT NOT NULL, -- Caminho ou dados da imagem de rosto do usuário para reconhecimento facial
    PRIMARY KEY (email) -- Email como identificador único do usuário
) ENGINE=InnoDB;
```

---

## Recursos Adicionais
- **Banco de Dados Relacional**: MySQL foi utilizado neste exemplo,  ainda não há suporte para outros SGBD's

- **Segurança**: Certifique-se de proteger os dados dos usuários, especialmente senhas, utilizando técnicas como hash seguro (ex: bcrypt).

---

