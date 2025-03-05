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

# Importação das bibliotecas necessárias para a criação da API web e manipulação de dados.
# Flask para criar a API e funções para lidar com requisições HTTP.
from flask import Flask, request, jsonify

# Importação da classe Commands, que contém as funções principais do sistema de controle de acesso.
from comandos import Commands
import json



# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam='<host da sua webcam>',  # Endereço da webcam para capturar frames usados no reconhecimento facial.
    other_columns='<tupla com as colunas da tabela usuarios>',  # Outras colunas no banco de dados relevantes para a autenticação.
    device_table='<nome da tabela de dispositivos>',  # Nome da tabela de dispositivos no banco de dados.
    database_name='<nome do seu database>',  # Nome do banco de dados onde os dados de usuários estão armazenados.
    host_database='<host do seu Banco de Dado>',  # Endereço do servidor MySQL, geralmente "localhost" para bancos locais.
    user_table='<nome da tabela de usuarios>',  # Nome da tabela de usuários no banco de dados.
    image_column='<nome da coluna de encoding>',  # Nome da coluna no banco de dados onde as imagens dos usuários estão armazenadas.
    user_database='<nome do usuario DB>',  # Nome de usuário usado para acessar o banco de dados.
    password='<senha do usuario do DB>'  # Senha do banco de dados. **Certifique-se de manter essa informação segura.**
)

# Criação da instância Flask para a aplicação web, que gerenciará as requisições e respostas HTTP.
app = Flask(__name__)

# ==============================================
# variaveis Importantes !
# ==============================================

time_column = '<nome da coluna para o horario>'  # Nome da coluna com armazenamento do horário no historico
date_column = '<nome da coluna para a data>' # Nome da coluna com armazenamento da data no historico
timerzone = '<sua timerzone>' # Exemplo 'America/Belem'
trust = 60   #nivel de confiança



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
    req = request.get_data()  # Recebe a requisição bruta.
    req = json.loads(req)  # Converte os dados da requisição para formato JSON.
    
    # Filtra o JSON para remover o campo 'ip', que não é necessário para a verificação facial.
    filter_json = {key: value for key, value in req.items() 
                   if key != 'ip'}
    
    # Realiza a autenticação do dispositivo com base nos dados filtrados da requisição.
    auth_device = control.authenticate_device(filter_json)

    # Verifica se o dispositivo foi autenticado com sucesso.
    if auth_device['Auth']:

        # Chama a função face_verify_database para comparar a face do usuário com os dados do banco de dados.
        result = control.face_verify_database(trust)
     
        for data_user in result:
            # Se a verificação facial for bem-sucedida (Auth=True), o usuário foi identificado.
            if data_user['Auth']:
                 
                # Filtra os dados do usuário para remover a senha e enviar apenas informações relevantes.
                filter_json = {key: value for key, value in data_user['data'].items() 
                   if key != 'senha'}
                
                # Adiciona o nível de confiança da verificação ao resultado.
                filter_json['trust'] = data_user['trust']

                # Salva o histórico de acesso do usuário no banco de dados.
                save_historic = control.save_historic_data(filter_json,req, date_column, 
                                                           time_column, timerzone)
                
                # Verifica se o salvamento do histórico foi bem-sucedido.
                if not save_historic['sucess']:
                    return jsonify(save_historic)  # Se falhar, retorna a mensagem de erro.
        
                else:
                    print(save_historic['message'])  # Exibe a mensagem no console, indicando sucesso.
                    return jsonify(result)  # Retorna o resultado da verificação facial como resposta em formato JSON.
    else:
        # Se a autenticação do dispositivo falhar, retorna o erro da autenticação.
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

    # Registra o dispositivo no sistema utilizando o método register_device.
    results = control.register_device(req)

    # Exibe no console o resultado do registro do dispositivo.
    print(results)

    # Retorna o resultado do registro do dispositivo em formato JSON para a resposta HTTP.
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
