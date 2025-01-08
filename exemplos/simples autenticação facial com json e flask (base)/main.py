# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: Este módulo implementa endpoints Flask para demonstrar as funcionalidades
# de registro e autenticação de usuários com base em reconhecimento facial.
# ==============================================

# Importação das bibliotecas necessárias.
from flask import Flask, request, jsonify  # Flask para criar a API e funções para lidar com requisições HTTP.
from comandos import Commands              # Importa a classe Commands, que contém a lógica do sistema de controle.

# ==============================================
# Inicialização do objeto de controle de acesso
# ==============================================
control = Commands(
    host_webcam='<host_da_sua_webcam>',  # Exemplo: 'http://<endereço_ip>/800x600.jpg'
    dir_archive_json='<caminho_do_arquivo_json>',  # Exemplo: 'caminho/para/arquivo.json'
    image_column='<nome_da_coluna_de_imagem>'  # Exemplo: 'encoding'
)

# Criação da instância Flask para criar a aplicação web.
app = Flask(__name__)

# ==============================================
# Endpoint para verificação facial
# ==============================================
@app.route('/face_verify', methods=['GET'])
def face_verify():
    """
    Verifica o rosto do usuário em tempo real.
    Faz uso de um método na classe Commands que analisa as imagens capturadas pela webcam
    para encontrar correspondências no banco de dados.
    """
    # Chama a função face_verify_json com timeout de 60 segundos.
    # Esta função realiza a verificação facial e retorna os resultados.
    result = control.face_verify_json(60)

    # Retorna os resultados da verificação facial como uma resposta JSON.
    return jsonify(result)

# ==============================================
# Endpoint para registro de usuários
# ==============================================
@app.route('/register_user', methods=['GET'])
def register_user():
    """
    Registra um novo usuário com base nos dados enviados via URL.
    Espera receber dados do usuário no formato JSON através do parâmetro 'data'.
    """
    # Obtém o parâmetro 'data' enviado na URL (exemplo: ?data={"name":"John","age":30}).
    json_data = request.args.get("data")  
    
    try:
        # Converte o JSON recebido para um dicionário Python.
        # Nota: eval() é usado aqui, mas seu uso não é recomendado devido a questões de segurança.
        # Uma alternativa mais segura seria usar json.loads().
        user_data = eval(json_data) if json_data else {}
    except:
        # Retorna um erro em formato JSON caso o formato seja inválido.
        return jsonify({"error": "Invalid JSON format"}), 400
    
    # Chama a função register_face_json da classe Commands para registrar o usuário no sistema.
    # O dicionário `user_data` contém os dados do usuário a serem registrados.
    result = control.register_face_json(data_user_dict=user_data)
                                   
    # Retorna o resultado do registro como uma resposta JSON.
    return jsonify(result)

# ==============================================
# Inicialização do servidor Flask
# ==============================================
if __name__ == '__main__':
    """
    Inicializa o servidor Flask, permitindo que ele aceite conexões externas.
    - host='0.0.0.0': O servidor aceitará conexões de qualquer endereço IP.
    - port=5000: O servidor será executado na porta 5000.
    """
    app.run(host='0.0.0.0', port=5000, debug=False)