# SOBRE O EXEMPLO

## Informação:

Este exemplo demonstra como fazer um sistema de autenticação json que retorna o print do resultado coletado pela webcam, um exemplo classico na bibloteca face-recoginition

- **Autenticação**: O sistema verifica se a face capturada corresponde a um rosto registrado no arquivo JSON.

-**opencv**: Além de processar a imagem na parte principal do `main.py` o opencv retorna a imagem coletada no processa e editada demarcando os rostos na imagem com seu respectivos resultados

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

   - No arquivo `main.py`, mude os valores das variaveis `host_webcam`,  
   `dir_data_json` e `key_encoding` com seus respectivos valores pedido. 

   - Para **verificar** um rosto, forneça o arquivo JSON com os encodings dos rostos registrados. A função `face_verify` irá tentar identificar o rosto e retornar os dados correspondentes(não se esqueça do parâmetros estabelecidos).


6. **Execução**:
   - Após a configuração, execute o arquivo `main.py` para iniciar o sistema de controle de acesso por imagem.

     ```bash
     python main.py
     ```

