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

# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam='<host da sua webcam>',  # Endereço da webcam para capturar frames usados no reconhecimento facial.
    host_database='<host do seu DB>',  # Endereço do servidor MySQL, geralmente "localhost" para bancos locais.
    user_database='<nome do usuario DB',  # Nome de usuário usado para acessar o banco de dados.
    password='<senha do usuario DB>',  # Senha do banco de dados. **Certifique-se de manter essa informação segura.**
    database_name='<nome do Banco de dados>',  # Nome do banco de dados onde os dados de usuários estão armazenados.
    image_column='<nome da coluna reservada aos encodings>',  # Nome da coluna no banco de dados onde as imagens dos usuários estão armazenadas.
    other_columns='<tupla com nome das outras colunas>',  # Outras colunas no banco de dados relevantes para a autenticação.
    user_table='<nome da tabela correspodente>',  # Nome da tabela de usuários no banco de dados.
)

# Bloco principal do script - Executa quando o arquivo é rodado diretamente.
if __name__ == '__main__':
    # ===========================================================
    # EXEMPLO 1: Registro de um novo usuário no banco de dados.
    # ===========================================================
    # O bloco de código abaixo está comentado, mas mostra como registrar um novo usuário no banco.
    # Para usar, descomente e preencha os dados do usuário no dicionário `dados`.

    # dados =   { 
    #      "nome": "João",               #exemplo
    #      "email": "joao@email.com",
    #      "senha": "@joao123"
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
    verificar = control.face_verify_database(trust)

    # Imprime o resultado da verificação.
    print(verificar)
