# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: Este módulo lida com a renderização das paginas do supervisório do projeto e
#            e a api de comunicação entre os dispositivos do projeto
# ==============================================
# ======================================
# Chamada das bibliotecas para o programa
# ======================================

from flask import Flask, render_template, request, jsonify  # Importa as funcionalidades do Flask, incluindo renderização de templates HTML, tratamento de requisições e respostas JSON.
from comandos import Commands, Database  # Importa as classes 'Commands' e 'Database' de um arquivo externo chamado 'comandos.py'.

# ==================================================================================================
# Chamada das funções de controle das ferramentas para o servidor (control) e do banco de dados (db)
# ==================================================================================================

# Criação do objeto db para consultar o banco de dados do projeto
db = Database(
    database='db_controle_de_acesso_por_imagem',  # Nome do banco de dados.
    password='Isac1998',  # Senha do banco de dados.
    host='localhost',  # Endereço do servidor MySQL (aqui, localhost).
    user='root'  # Usuário do banco de dados.
)

# Criação do objeto control para interagir com as funcionalidades do servidor e banco de dados
control = Commands(
    host_webcam='http://192.168.0.20/800x600.jpg',  # Endereço da webcam para capturar imagem de reconhecimento facial.
    host_database='localhost',  # Endereço do servidor MySQL (localhost).
    user_database='root',  # Usuário do banco de dados.
    password='Isac1998',  # Senha do banco de dados.
    database_name='db_controle_de_acesso_por_imagem',  # Nome do banco de dados.
    image_column='imagem',  # Nome da coluna onde as imagens dos usuários estão armazenadas no banco.
    other_columns=('nome', 'cpf', 'email', 'auth'),  # Outras colunas que são relevantes para o controle de acesso (nome, cpf, email, nível de autorização).
    user_table='usuarios',  # Nome da tabela de usuários no banco de dados.
    device_table='dispositivos',  # Nome da tabela de dispositivos no banco de dados.
    mac_column='mac'  # Coluna que armazena os endereços MAC dos dispositivos.
)

# =====================================
# Conexão ao banco de dados do projeto
# =====================================

conn = db.connection()  # Estabelece a conexão com o banco de dados usando o método `connection` da classe `Database`.
cursor = conn.cursor()  # Cria um cursor para executar comandos SQL no banco de dados.

# ===============================
# Criação da aplicação Flask
# ===============================

app = Flask(__name__)  # Inicializa a aplicação Flask, que será usada para criar o webserver do projeto.

# ====================================
# Rota principal da aplicação ("/")
# ====================================

@app.route('/', methods=['GET'])  # Define a rota principal da aplicação com o método HTTP GET.
def index():
    return render_template('login_pages/login.html')  # Renderiza a página inicial de login.

# ====================================
# Rota para autenticação do usuário
# ====================================

@app.route('/login', methods=['POST'])  # Define a rota para a página de login com o método HTTP POST.
def login():
    result_all = []  # Lista para armazenar os resultados de validação das credenciais do usuário.

    form = request.form  # Obtém os dados enviados pelo formulário HTML (email e senha do usuário).

    # ===============================
    # Leitura de dados do banco
    # ===============================
    data = db.get_database(
        image_column='imagem',  # Nome da coluna onde as imagens de usuários estão armazenadas.
        other_columns=('cpf', 'email', 'nome', 'auth', 'senha'),  # Outras colunas relevantes.
        table='usuarios'  # Nome da tabela no banco de dados que contém os dados dos usuários.
    )
    
    cursor.close()  # Fecha o cursor para liberar recursos.
    conn.close()  # Fecha a conexão com o banco de dados.

    # Verifica se a consulta ao banco de dados falhou.
    if data is None:
        return render_template('login_pages/login.html', message='erro ao ler db')  # Retorna a página de login com uma mensagem de erro.

    # ==================================================
    # Validação das credenciais do usuário no banco
    # ==================================================

    for i in data:  # Itera sobre os registros retornados da tabela.
        for data_user in i:  # Itera sobre os dados individuais de cada usuário.
            if isinstance(data_user, dict):  # Verifica se os dados do usuário estão no formato de dicionário.

                # Verifica se o email e a senha enviados pelo formulário correspondem aos dados do banco.
                result = (data_user['email'] == form['email'] 
                          and str(data_user['senha']) == form['password'])
  
                result_all.append(result)  # Adiciona o resultado da validação à lista.

                if result:  # Se as credenciais forem válidas:
                    # Redireciona o usuário para a página correspondente ao seu nível de permissão.
                    if data_user['auth'] == 'admin':  # Caso o usuário seja administrador.
                        return render_template('admin_pages/historico.html')
                    elif data_user['auth'] == 'docente':  # Caso o usuário seja docente.
                        return render_template('docente_pages/historico.html')
                    else:  # Caso o usuário não tenha permissão para acessar o sistema.
                        return render_template('login_pages/login.html', message='usuário não autorizado')

    # ================================================================
    # Caso nenhuma das credenciais seja válida
    # ================================================================
    if all(result == False for result in result_all):  # Verifica se todos os resultados são falsos.
        return render_template('login_pages/login.html', message='email e senha incorretos!')  # Retorna a página de login com uma mensagem de erro.



# ===================================================
# Rota para exibição do histórico de acessos (Admin)
# ===================================================

@app.route('/topnav/historico', methods=['POST'])  # Define a rota para a página de histórico no menu superior.
def historico_page():
    # Consulta os dados da tabela 'historico' no banco de dados.
    historic_data = db.get_database(
        other_columns=('cpf', 'nome', 'email', 'trust', 'mac', 'ip', 'localização', 'data_acesso', 'hora_acesso'),
        table='historico'
    )
    historic_table_data = []  # Lista para armazenar os valores das linhas da tabela.
    historic_table_keys = []  # Lista para armazenar os nomes das colunas da tabela.

    if historic_data:  # Verifica se os dados foram obtidos com sucesso.
        for historic_item in historic_data:  # Itera pelos registros da tabela.
            if isinstance(historic_item, dict):  # Verifica se o registro está no formato de dicionário.
                historic_table_data.append(list(historic_item.values()))  # Adiciona os valores do registro à lista.
                historic_table_keys.append(list(historic_item.keys()))  # Adiciona as chaves do registro à lista.

    # Renderiza a página de histórico com os dados obtidos.
    return render_template('admin_pages/historico.html', 
                           data_table_historic=historic_table_data, 
                           column_names_historic=historic_table_keys[0])

# =====================================================
# Rota para busca de usuários no histórico (Admin)
# =====================================================

@app.route('/search_user', methods=['POST'])  # Define a rota para a busca de usuários no histórico.
def search_user():
    req = request.form  # Obtém os dados enviados pelo formulário HTML.
    search = control.search_data(req, 'historico')  # Realiza a busca no banco de dados usando o método `search_data`.

    if search['result'] is None:  # Verifica se a busca falhou.
        return render_template('admin_pages/historico.html', message=search['message'])  # Retorna a página com mensagem de erro.
    else:
        historic_table_data = []  # Lista para armazenar os resultados da busca.
        for data in search['result']['data']:
            historic_table_data.append(list(data))  # Adiciona os dados retornados à lista.

        # Renderiza a página de histórico com os resultados da busca.
        return render_template('admin_pages/historico.html',  
                               data_table_historic=historic_table_data,
                               column_names_historic=search['result']['columns'])

# ===================================================
# Rota para exibição da tabela de usuários (Admin)
# ===================================================

@app.route('/topnav/usuarios', methods=['POST'])  # Define a rota para a página de usuários no menu superior.
def usuarios_page():
    # Consulta os dados da tabela 'usuarios' no banco de dados.
    historic_data = db.get_database(
        other_columns=('cpf', 'nome', 'email', 'auth'),
        table='usuarios'
    )
    historic_table_data = []  # Lista para armazenar os valores das linhas da tabela.
    historic_table_keys = []  # Lista para armazenar os nomes das colunas da tabela.

    if historic_data:  # Verifica se os dados foram obtidos com sucesso.
        for historic_item in historic_data:  # Itera pelos registros da tabela.
            if isinstance(historic_item, dict):  # Verifica se o registro está no formato de dicionário.
                historic_table_data.append(list(historic_item.values()))  # Adiciona os valores do registro à lista.
                historic_table_keys.append(list(historic_item.keys()))  # Adiciona as chaves do registro à lista.

    # Renderiza a página de usuários com os dados obtidos.
    return render_template('admin_pages/usuarios.html', 
                           data_table_historic=historic_table_data, 
                           column_names_historic=historic_table_keys[0])

# ====================================================
# Rota para busca de usuários cadastrados (Admin)
# ====================================================

@app.route('/search_user_cad', methods=['POST'])  # Define a rota para busca de usuários cadastrados.
def search_user_cad():
    req = request.form  # Obtém os dados enviados pelo formulário HTML.
    search = control.search_data(req, 'usuarios', image_column='imagem')  # Realiza a busca no banco de dados.

    if search['result'] is None:  # Verifica se a busca falhou.
        return render_template('admin_pages/usuarios.html', message=search['message'])  # Retorna a página com mensagem de erro.
    else:
        historic_table_data = []  # Lista para armazenar os resultados da busca.
        for data in search['result']['data']:
            historic_table_data.append(list(data))  # Adiciona os dados retornados à lista.

        # Renderiza a página de usuários com os resultados da busca.
        return render_template('admin_pages/usuarios.html',  
                               data_table_historic=historic_table_data,
                               column_names_historic=search['result']['columns'])

# =====================================================
# Rota para a página de cadastro de usuários (Admin)
# =====================================================

@app.route('/topnav/cadastro', methods=['POST'])  # Define a rota para a página de cadastro no menu superior.
def cadastro():
    return render_template('admin_pages/cadastro.html')  # Renderiza a página de cadastro.

# ==========================================
# Rota para registrar um novo usuário
# ==========================================

@app.route('/register_user', methods=['POST'])  # Define a rota para o registro de um novo usuário.
def register_user():
    form = request.form  # Obtém os dados enviados pelo formulário HTML.
    registro = control.register_user(user_data_json=form)  # Registra o usuário no banco de dados.

    # Renderiza a página de cadastro com a mensagem do resultado.
    return render_template('admin_pages/cadastro.html', message=registro[1])

# ===================================================
# Rota para exibição do histórico de docentes
# ===================================================

@app.route('/topnav/historico_docente', methods=['POST'])  # Define a rota para a página de histórico de docentes no menu superior.
def historico_docente_page():
    # Consulta os dados da tabela 'historico' relacionados a docentes no banco de dados.
    historic_data = db.get_database(
        other_columns=('cpf', 'nome', 'email', 'localização', 'data_acesso', 'hora_acesso'),
        table='historico'
    )
    historic_table_data = []  # Lista para armazenar os valores das linhas da tabela.
    historic_table_keys = []  # Lista para armazenar os nomes das colunas da tabela.

    if historic_data:  # Verifica se os dados foram obtidos com sucesso.
        for historic_item in historic_data:  # Itera pelos registros da tabela.
            if isinstance(historic_item, dict):  # Verifica se o registro está no formato de dicionário.
                historic_table_data.append(list(historic_item.values()))  # Adiciona os valores do registro à lista.
                historic_table_keys.append(list(historic_item.keys()))  # Adiciona as chaves do registro à lista.

    # Renderiza a página de histórico para docentes com os dados obtidos.
    return render_template('docente_pages/historico.html', 
                           data_table_historic=historic_table_data, 
                           column_names_historic=historic_table_keys[0])



# ====================================================
# Rotas para funcionalidades de controle de usuários
# ====================================================

# Rota: /topnav/usuarios_docente
# Descrição: Renderiza a página que lista os usuários do tipo "docente" cadastrados no sistema. 
#            Os dados são extraídos do banco de dados e organizados em tabelas.
@app.route('/topnav/usuarios_docente', methods=['POST'])
def usuarios_docente_page():
    # Recupera dados históricos de usuários da tabela 'usuarios'
    historic_data = db.get_database(
        other_columns=('cpf', 'nome', 'email', 'auth'),  # Colunas específicas a serem recuperadas
        table='usuarios'  # Tabela no banco de dados
    )

    # Inicializa listas para armazenar os dados e os nomes das colunas
    historic_table_data = []
    historic_table_keys = []

    # Organiza os dados retornados do banco em formato de tabela
    if historic_data:
        for historic_item in historic_data:
            if isinstance(historic_item, dict):  # Garante que o item seja um dicionário
                historic_table_data.append(list(historic_item.values()))  # Valores como linhas
                historic_table_keys.append(list(historic_item.keys()))  # Chaves como cabeçalhos

    # Renderiza a página HTML com os dados organizados
    return render_template(
        'docente_pages/usuarios.html',  # Template da página HTML
        data_table_historic=historic_table_data,  # Dados da tabela
        column_names_historic=historic_table_keys[0]  # Nomes das colunas
    )


# Rota: /search_user_docente_cad
# Descrição: Realiza a busca de um usuário "docente" cadastrado e exibe os resultados na página.
@app.route('/search_user_docente_cad', methods=['POST'])
def search_user_docente_cad():
    # Recupera os dados do formulário enviado pela página
    req = request.form
    # Executa a busca no banco de dados, incluindo a coluna 'imagem'
    search = control.search_data(req, 'usuarios', image_column='imagem')

    # Caso não encontre resultados
    if search['result'] is None:
        return render_template(
            'docente_pages/usuarios.html',  # Template da página
            message=search['message']  # Mensagem de erro ou status
        )

    else:
        # Inicializa as listas para dados filtrados e nomes de colunas
        historic_table_data = []
        filter_columns = [
            column for column in search['result']['columns'] if column != 'senha'  # Remove a coluna 'senha'
        ]

        # Função para calcular o índice da coluna 'senha' (excluindo-a)
        number_index_senha = lambda lst, value: len([item for item in lst if item != value])
        index_number = number_index_senha(search['result']['columns'], 'senha')

        # Organiza os dados em tabela, excluindo a coluna 'senha'
        for data in search['result']['data']:
            historic_table_data.append([i for idx, i in enumerate(data) if idx != index_number])

        # Renderiza a página com os resultados filtrados
        return render_template(
            'docente_pages/usuarios.html',
            data_table_historic=historic_table_data,  # Dados ajustados
            column_names_historic=filter_columns  # Colunas ajustadas
        )

# Rota: /search_user_docente
# Descrição: Realiza a busca no histórico de acessos de um usuário "docente" e exibe os resultados.
@app.route('/search_user_docente', methods=['POST'])
def search_user_docente():
    # Recupera os dados do formulário enviado pela página
    req = request.form
    # Executa a busca no histórico (tabela 'historico')
    search = control.search_data(req, 'historico')

    # Caso não encontre resultados
    if search['result'] is None:
        return render_template(
            'docente_pages/historico.html',  # Template da página
            message=search['message']  # Mensagem de erro ou status
        )

    else:
        # Lista de colunas a serem excluídas
        columns_to_exclude = ['ip', 'mac', 'trust']  # Exemplos de colunas sensíveis ou desnecessárias
        empty_value = ''  # Valor considerado "vazio" para filtragem

        # Organiza os dados retornados em tabela
        historic_table_data = []
        for data in search['result']['data']:
            historic_table_data.append(list(data))

        # Cria um dicionário mapeando colunas e dados
        dict_filter = dict(zip(search['result']['columns'], zip(*historic_table_data)))

        # Filtra o dicionário, excluindo colunas indesejadas e valores vazios
        filtered_dict = {
            key: value
            for key, value in dict_filter.items()
            if key not in columns_to_exclude and all(val != empty_value for val in value)
        }

        # Reconstrói as colunas e dados ajustados
        filtered_columns = list(filtered_dict.keys())
        filtered_data = list(zip(*filtered_dict.values()))

        # Renderiza a página com os dados filtrados
        return render_template(
            'docente_pages/historico.html',
            data_table_historic=filtered_data,  # Dados ajustados
            column_names_historic=filtered_columns  # Colunas ajustadas
        )

# ========================================
# Rotas para funcionalidades de autenticação e registro de dispositivos
# ========================================

# Rota: /register_device
# Descrição: Registra um novo dispositivo no sistema com base nos dados de MAC e localização.
#           Os dados são recebidos via JSON no formato GET.
@app.route('/register_device', methods=['GET'])
def register_device():
    # Recupera os dados enviados no corpo da requisição (JSON)
    req = request.get_json()
    
    # Prepara os dados para o registro do dispositivo, incluindo MAC e localização
    data = {'mac': req['mac'], 'localização': req['local']}
    
    # Chama a função para registrar o dispositivo e obtém o resultado
    result = control.register_device(data)
    
    # Retorna o resultado do registro
    return result


# Rota: /verify_user
# Descrição: Verifica a autenticação de um usuário a partir de um dispositivo e do reconhecimento facial.
#           Os dados são enviados via POST, incluindo MAC, localização e IP.
@app.route('/verify_user', methods=['POST'])
def verify_user():
    # Recupera os dados enviados via JSON no corpo da requisição
    req = request.get_json()
    
    # Prepara os dados do dispositivo, incluindo MAC, localização e IP
    data_device = {'mac': req['mac'], 'localização': req['local'], 'ip': req['ip']}

    # Chama a função de autenticação do dispositivo, retornando um resultado
    result = control.authenticate_device(data_device)

    # Caso o dispositivo seja autenticado
    if result:
        try:
            # Tenta realizar a verificação facial do usuário
            face_result = control.face_verify_database(60)  # O número 60 pode ser o limite de segundos para a verificação de rosto

            # Caso a verificação facial retorne resultados
            if face_result:
                # Itera sobre os resultados de verificação facial
                for data in face_result:
                    if data['Auth']:  # Se o campo 'Auth' for verdadeiro
                        # Prepara os dados do usuário para salvar no histórico de acessos
                        user = {
                            'email': data['Dados do Usuario']['email'],
                            'nome': data['Dados do Usuario']['nome'],
                            'auth': data['Dados do Usuario']['auth'],
                            'cpf': data['Dados do Usuario']['cpf'],
                            'trust': data['trust']
                        }
                        
                        # Chama a função para salvar os dados históricos do usuário
                        save = control.save_historic_data(
                            user_data=user,  # Dados do usuário
                            time_column='hora_acesso',  # Coluna de hora do acesso
                            date_column='data_acesso',  # Coluna da data do acesso
                            device_data=data_device,  # Dados do dispositivo
                            table='historico'  # Tabela para salvar o histórico
                        )
                        
                        print(save)  # Exibe o resultado do salvamento no console

                # Retorna os resultados da verificação facial em formato JSON
                return jsonify(face_result)
        
        # Caso ocorra uma exceção durante a verificação facial
        except Exception as e:
            return jsonify({'Auth': None, 'Error': str(e)})  # Retorna erro no formato JSON

    else:
        # Caso o dispositivo não seja autenticado, retorna erro no formato JSON
        return jsonify({'Auth': False, 'Error': 'Dispositivo não autorizado'})


# ========================================
# Inicializa o servidor Flask
# ========================================

# Roda o servidor Flask no IP local (0.0.0.0)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
