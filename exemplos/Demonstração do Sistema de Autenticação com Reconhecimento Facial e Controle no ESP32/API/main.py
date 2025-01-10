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


# Flask para criar a API e funções para lidar com requisições HTTP.
from flask import Flask, request, jsonify

# Importação da classe Commands, que contém as funções principais do sistema.
from comandos import Commands

# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam='http://192.168.0.20/800x600.jpg',  # Endereço da webcam para capturar frames usados no reconhecimento facial.
    host_database='localhost',  # Endereço do servidor MySQL, geralmente "localhost" para bancos locais.
    user_database='root',  # Nome de usuário usado para acessar o banco de dados.
    password='Isac1998',  # Senha do banco de dados. **Certifique-se de manter essa informação segura.**
    database_name='db_exemplo',  # Nome do banco de dados onde os dados de usuários estão armazenados.
    image_column='imagem',  # Nome da coluna no banco de dados onde as imagens dos usuários estão armazenadas.
    other_columns=('email', 'nome', 'senha'),  # Outras colunas no banco de dados relevantes para a autenticação.
    user_table='usuarios',  # Nome da tabela de usuários no banco de dados.
)

# Criação da instância Flask para criar a aplicação web.
app = Flask(__name__)

# ==============================================
# Endpoint para verificação facial
# ==============================================
@app.route('/face_verify', methods=['POST'])

def face_verify():
    
    """
    Verifica o rosto do usuário em tempo real utilizando a webcam configurada.
    Faz uso do método face_verify_database da classe Commands para comparar o rosto capturado
    com os dados armazenados no banco de dados.

    Returns:
        JSON: Resultado da verificação facial contendo informações do usuário, caso identificado.
    """
    
    # nivel de confiança
    trust = 60
    # Chama a função face_verify_database com timeout de 60 segundos.
    result = control.face_verify_database(trust)
    
    print(result)
    
    # Retorna os resultados da verificação facial em formato JSON.
    return jsonify(result)

# ==============================================
# Inicialização do servidor Flask
# ==============================================

if __name__ == '__main__':
    """
    Inicializa o servidor Flask, permitindo que ele aceite conexões externas.

    Configurações:
    - host='0.0.0.0': Permite conexões de qualquer endereço IP.
    - port=5002: O servidor será executado na porta 5002.
    - debug=False: Executa o servidor sem modo de depuração.
    """
    app.run(host='0.0.0.0', port=5002, debug=False)
    