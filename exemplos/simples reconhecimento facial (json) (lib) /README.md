# SOBRE O EXEMPLO

## Informação:

Este exemplo simples demonstra como usar um arquivo JSON diretamente no projeto sem a necessidade de um banco de dados relacional. Ele serve como um exemplo de como realizar **autenticação** e **registro de usuários** utilizando JSON para armazenar e consultar as informações dos usuários.

- **Autenticação**: O sistema verifica se a face capturada corresponde a um rosto registrado no arquivo JSON.
- **Registro de Usuários**: Permite adicionar novos usuários ao arquivo JSON, registrando seus dados e imagens faciais para autenticação futura.

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

4. **Configuração do arquivo JSON**:
   - O arquivo JSON será usado para armazenar os rostos e dados dos usuários. Garanta que o arquivo JSON esteja configurado corretamente, conforme o exemplo a seguir:
     ```json
     [
       {
         "nome": "João",
         "cpf": "12345678900",
         "email": "joao@email.com",
         "auth": "admin",
         "imagem": "caminho_da_imagem/joao.jpg(opcional)",
         "encoding": "dados_do_encoding"
       }
     ]
     ```
   - Este arquivo será lido para registrar ou verificar usuários.

5. **Uso do `main.py`**:

   - No arquivo `main.py`, você poderá descomentar as linhas para escolher entre **registrar** ou **verificar** rostos.

   - Para **verificar** um rosto, forneça o arquivo JSON com os encodings dos rostos registrados. A função `face_verify_json` irá tentar identificar o rosto e retornar os dados correspondentes.

   - Para **registrar** um novo rosto, basta descomentar a parte que chama `register_face_json`, e o sistema adicionará o novo rosto e dados ao arquivo JSON.

6. **Execução**:
   - Após a configuração, execute o arquivo `main.py` para iniciar o sistema de controle de acesso por imagem.

     ```bash
     python main.py
     ```

