# SOBRE O EXEMPLO

## Informação:

Este exemplo simples demonstra como usar um arquivo JSON diretamente no projeto sem a necessidade de um banco de dados relacional. Ele serve como um modelo de **autenticação**, **registro de usuários**, e **exposição do sistema para a rede utilizando Flask**.  

Além de gerenciar usuários, o Flask expõe o sistema como uma API acessível em rede local, permitindo que o controle de acesso seja testado diretamente no navegador ou via ferramentas como Postman.

- **Autenticação**: O sistema verifica se a face capturada corresponde a um rosto registrado no arquivo JSON.
- **Registro de Usuários**: Permite adicionar novos usuários ao arquivo JSON, registrando seus dados e imagens faciais para autenticação futura.
- **Demonstração no Navegador**: O Flask expõe o sistema como uma API acessível na rede, permitindo enviar requisições HTTP de forma prática.

---

## Instalação

1. **Siga a instalação principal do projeto**:
   - Certifique-se de seguir as instruções de instalação do projeto principal para garantir que todas as dependências e configurações necessárias estejam corretas.

2. **Clone o arquivo `main.py`**:
   - Faça o download ou clone o arquivo `main.py` desta pasta para o seu ambiente Python. Ele estará localizado na pasta principal do projeto.
   - Se você estiver utilizando Git, execute o comando:
     ```bash
     git clone <URL_DO_REPOSITORIO>
     ```
   - Se preferir, baixe diretamente o arquivo `main.py` e coloque-o na pasta do seu projeto.

3. **Configuração do arquivo JSON**:
   - O arquivo JSON será usado para armazenar os rostos e dados dos usuários. A organização dos dados é **flexível** e pode ser adaptada às necessidades do projeto, mas um formato recomendado seria:

     ```json
     [
       {
         "nome": "João",
         "cpf": "12345678900",
         "email": "joao@email.com",
         "auth": "admin",
         "imagem": "caminho_da_imagem/joao.jpg (opcional)",
         "encoding": "dados_do_encoding"
       }
     ]
     ```
   - Este formato é apenas uma sugestão. Desde que o sistema seja ajustado para interpretar os campos conforme a estrutura definida, qualquer organização do JSON é válida.

4. **Uso do `main.py`**:

   O arquivo `main.py` contém a lógica para os endpoints Flask e o processamento dos dados faciais. O sistema inclui duas funcionalidades principais:

   - **Autenticação de Usuários**: Verifica se um rosto capturado corresponde a algum registro existente no arquivo JSON.
   - **Registro de Usuários**: Adiciona novos rostos e informações ao arquivo JSON.

---

## Como Funcionam as Funções no Flask

### **Estrutura do Flask**

O Flask é usado para criar uma API simples que expõe dois endpoints principais. Ambos são configuráveis e podem ser testados por ferramentas HTTP ou diretamente no navegador.

---

### **1. Autenticação de Usuários**

- **Endpoint**: `/face_verify`  
- **Método HTTP**: `POST`  
- **Descrição**:  
  Este endpoint recebe uma imagem facial capturada e compara seu encoding com os encodings registrados no arquivo JSON.

- **Funcionamento**:
  1. O sistema carrega o arquivo JSON com os dados dos usuários registrados.
  2. A imagem facial enviada é processada, e seu encoding é extraído.
  3. O encoding é comparado com os registros no arquivo JSON.
  4. Resultado:
     - **Sucesso**: Retorna as informações do usuário correspondente.
     - **Erro**: Retorna uma mensagem indicando que o rosto não foi identificado.

---

### **2. Registro de Usuários**

- **Endpoint**: `/register_user`  
- **Método HTTP**: `POST`  
- **Descrição**:  
  Este endpoint permite registrar um novo usuário no sistema, adicionando seus dados e o encoding facial ao arquivo JSON.

- **Funcionamento**:
  1. O cliente envia os dados do usuário (nome, CPF, email etc.) exemplo ?data={"name":"John","age":30}.
  2. O sistema processa a imagem para gerar o encoding facial.
  3. Os dados e o encoding são adicionados ao arquivo JSON.
  4. Resultado:
     - O sistema retorna uma mensagem indicando que o usuário foi registrado com sucesso.

---

### **Demonstração no Navegador**

O Flask permite que o sistema seja acessado diretamente no navegador, facilitando testes e demonstrações. Por exemplo:

- **Autenticação**: Envie uma imagem facial ao endpoint `/face_verify` e visualize o resultado (usuário autenticado ou não identificado).
- **Registro**: Envie os dados e a imagem facial de um novo usuário ao endpoint `/register_user`.

O uso de ferramentas como Postman ou cURL também é recomendado para testar os endpoints.

---

## Execução

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

Este exemplo é flexível e pode ser usado para estudar ou implementar sistemas de controle de acesso baseados em processamento de imagem e APIs Flask. A estrutura do JSON pode ser ajustada conforme as necessidades específicas do seu projeto.

