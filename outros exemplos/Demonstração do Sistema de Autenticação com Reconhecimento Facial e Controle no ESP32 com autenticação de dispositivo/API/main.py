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
import json

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
    device_table='dispositivos',  # Nome da tabela de dispositivos no banco de dados.
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
    # Recebe os dados da requisição HTTP POST e faz o parsing para JSON.
    req = request.get_data()
    req = json.loads(req)

    # Autentica o dispositivo utilizando o método authenticate_device.
    auth_device = control.authenticate_device(req)

    # Exibe no console o resultado da autenticação do dispositivo.
    print(auth_device)

    # Verifica se o dispositivo foi autenticado com sucesso.
    if auth_device['Auth']:
        # Define o nível de confiança para o reconhecimento facial.
        trust = 60

        # Chama a função face_verify_database com timeout de 60 segundos.
        result = control.face_verify_database(trust)

        # Exibe no console o resultado da verificação facial.
        print(result)

        # Retorna os resultados da verificação facial em formato JSON.
        return jsonify(result)
    else:
        # Retorna o resultado da autenticação do dispositivo em caso de falha.
        return jsonify(auth_device)

# ==============================================
# Endpoint para registro de dispositivos
# ==============================================
@app.route('/register_device', methods=['POST'])
def register_device():
    """
    Registra um novo dispositivo no sistema.
    Faz uso do método register_device da classe Commands para adicionar o dispositivo ao banco de dados.

    Returns:
        JSON: Resultado do registro do dispositivo contendo status e mensagem de sucesso ou erro.
    """
    # Recebe os dados da requisição HTTP POST em formato JSON.
    req = request.get_json()

    # Registra o dispositivo utilizando o método register_device.
    results = control.register_device(req)

    # Exibe no console o resultado do registro do dispositivo.
    print(results)

    # Retorna o resultado do registro em formato JSON.
    return jsonify(results)

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
