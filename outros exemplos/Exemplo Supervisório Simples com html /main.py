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
from flask import Flask, request, jsonify, render_template

# Importação da classe Commands, que contém as funções principais do sistema de controle de acesso.
from comandos import Commands
import json

# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam='<url_da_webcam>',  # Substitua pelo endereço da webcam para capturar frames usados no reconhecimento facial.
    other_columns=('<coluna_adicional_1>', '<coluna_adicional_2>', '<coluna_adicional_3>'),  # Substitua pelas colunas relevantes para autenticação no banco de dados.
    device_table='<nome_tabela_dispositivos>',  # Nome da tabela de dispositivos no banco de dados.
    historic_table='<nome_tabela_historico>',   # Nome da tabela para o histórico de acessos no banco de dados.
    database_name='<nome_do_banco_de_dados>',  # Nome do banco de dados onde os dados de usuários estão armazenados.
    host_database='<host_do_banco_de_dados>',  # Endereço do servidor do banco de dados (ex.: localhost).
    user_table='<nome_tabela_usuarios>',  # Nome da tabela de usuários no banco de dados.
    image_column='<coluna_imagem>',  # Nome da coluna no banco de dados onde as imagens dos usuários estão armazenadas.
    user_database='<usuario_banco_de_dados>',  # Nome de usuário usado para acessar o banco de dados.
    password='<senha_banco_de_dados>'  # Senha do banco de dados.
)

# Criação da instância Flask para a aplicação web, que gerenciará as requisições e respostas HTTP.
app = Flask(__name__)

def load_tables():
    # Substitua pelas colunas e tabelas relevantes do seu banco de dados.
    columns_table_historic = ('<coluna_historico_1>', '<coluna_historico_2>', '<coluna_historico_3>')
    columns_table_device = ('<coluna_dispositivo_1>', '<coluna_dispositivo_2>', '<coluna_dispositivo_3>')
    columns_table_user = ('<coluna_usuario_1>', '<coluna_usuario_2>')

    table_historic = control.get_database('', columns_table_historic, '<nome_tabela_historico>')
    table_device = control.get_database('', columns_table_device, '<nome_tabela_dispositivos>')
    table_user = control.get_database('', columns_table_user, '<nome_tabela_usuarios>')

    values_tables = lambda table_data: [list(d.values()) for d in table_data]

    return {
        "columns_table_historic": columns_table_historic,
        "columns_table_device": columns_table_device,
        "columns_table_user": columns_table_user,
        "data_table_historic": values_tables(table_historic),
        "data_table_device": values_tables(table_device),
        "data_table_users": values_tables(table_user),
    }

@app.route('/', methods=['GET'])
def index():
    return render_template('/login.html')  # Opcional: página inicial de login.

@app.route('/login', methods=['POST'])
def login():
    d = control.load_data_users()
    req = request.form

    for data in d:
        for data_user in data:
            if isinstance(data_user, dict):
                result = (data_user['email'] == req['email']
                             and data_user['senha'] == req['password'])
 
                if result:
                    tables = load_tables()
                    return render_template('/home.html', **tables)  # Opcional: página inicial do sistema.
    else:
        return render_template('/login.html', message='Email e Senha Incorreto !')  # Opcional: mensagem de erro no login.

@app.route('/register_user', methods=['POST'])
def register_user():
    req = request.form
    req = dict(req)

    register = control.register_user(req)

    tables = load_tables()

    return render_template('/home.html', message=register[1], **tables)  # Opcional: renderiza a página inicial após o registro.

@app.route('/tables', methods=['POST'])
def tables():
    tables = load_tables()
    return render_template('/home.html', **tables)  # Opcional: página inicial do sistema com tabelas carregadas.

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

        # Define o nível de confiança para o reconhecimento facial (quanto maior, mais precisa a verificação).
        trust = 60
        # Chama a função face_verify_database para comparar a face do usuário com os dados do banco de dados.
        result = control.face_verify_database(trust)
     
         # Verificar se deu erro na webcam previamente
        if isinstance(result, dict):
            return jsonify(result)
        
        # Caso não tiver nenhum erro na webcam ele continua o processo

        else:
            for data_user in result:
              
                # Se a verificação facial for bem-sucedida (Auth=True), o usuário foi identificado.
                if data_user['Auth']:
                    
                    # Filtra os dados do usuário para remover a senha e enviar apenas informações relevantes.
                    filter_json = {key: value for key, value in data_user['data'].items() 
                    if key != 'senha'}
                    
                    # Adiciona o nível de confiança da verificação ao resultado.
                    filter_json['trust'] = data_user['trust']

                    # Salva o histórico de acesso do usuário no banco de dados.
                    save_historic = control.save_historic_data(filter_json,
                                req, 'data_acesso', 'horario_acesso', 
                                'America/Belem')
                    
                    # Verifica se o salvamento do histórico foi bem-sucedido.
                    if not save_historic['sucess']:
                        return jsonify(save_historic)  # Se falhar, retorna a mensagem de erro.
            
                    else:
                        print(save_historic['message'])  # Exibe a mensagem no console, indicando sucesso.
                        return jsonify(result)  # Retorna o resultado da verificação facial como resposta em formato JSON.
                else:
                    print(data_user)  # Exibe a mensagem no console, indicando erro.
                    return jsonify(data_user)  # Retorna o resultado da verificação facial como resposta em formato JSON.
    
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
    app.run(host='0.0.0.0', port=5000, debug=True)
