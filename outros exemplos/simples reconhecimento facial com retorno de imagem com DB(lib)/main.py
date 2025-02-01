# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: Este módulo cuida dos exemplos de demonstração de funcionamento dos arquivos.
# ==============================================

# Importação da classe Commands, que contém as funções principais do sistema.
from comandos import Commands
import cv2

# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam='http://192.168.0.20/800x600.jpg',  # Endereço da webcam para capturar frames usados no reconhecimento facial.
    host_database='localhost',  # Endereço do servidor MySQL, geralmente "localhost" para bancos locais.
    user_database='root',  # Nome de usuário usado para acessar o banco de dados.
    password='Isac1998',  # Senha do banco de dados. **Certifique-se de manter essa informação segura.**
    database_name='projeto_controle_de_acesso',  # Nome do banco de dados onde os dados de usuários estão armazenados.
    image_column='encoding',
    other_columns=('nome',),  # Outras colunas no banco de dados relevantes para a autenticação.
    user_table='usuarios',  # Nome da tabela de usuários no banco de dados.
)

# Bloco principal do script - Executa quando o arquivo é rodado diretamente.
if __name__ == '__main__':
    # ===========================================================
    # EXEMPLO 1: Registro de um novo usuário no banco de dados.
    # ===========================================================
    # O bloco de código abaixo está comentado, mas mostra como registrar um novo usuário no banco.
    # Para usar, descomente e preencha os dados do usuário no dicionário `dados`.

    # dados = {
    #     "nome": "João",  # Exemplo de nome.
    #     "email": "joao@email.com",  # E-mail do usuário.
    #     "senha": "@joao123"  # Senha para registro.
    # }
    # 
    # Registra o usuário no banco de dados.
    # success, message = control.register_user(dados)
    # 
    # Imprime a mensagem de resultado do registro (sucesso ou erro).
    # print(message)

    # ===========================================================
    # EXEMPLO 2: Verificação facial com dados armazenados no banco.
    # ===========================================================
    trust = 60  # Limite de confiança para a autenticação facial (percentual).

    # Chama a função para verificar os rostos capturados pela webcam em relação aos armazenados no banco de dados.
    result, frame = control.face_verify_database_image(trust)

    # Imprime o resultado da verificação.
    print(result)

    # Exibe o frame capturado com a verificação facial.
    cv2.imshow("Exemplo", frame)
    cv2.waitKey(0)
