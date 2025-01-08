# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: Este módulo lida com as operações de banco de dados para registrar usuários, dispositivos,
#            históricos de acesso e busca de dados. Ele abstrai as interações com o banco de dados 
#            MySQL para facilitar o gerenciamento de dados relacionados ao controle de acesso além 
#            do procesamento e reconhecimennto facial.
# ==============================================

import mysql.connector as mysql  # Biblioteca para manipulação de MySQL
import face_recognition as fr    # Biblioteca para reconhecimento facial
from datetime import datetime    # Biblioteca para manipulação de data e hora
import numpy as np               # Biblioteca para manipulação de arrays
import cv2                       # Biblioteca para manipulação de imagens
import pytz                      # Biblioteca para manipulação de Fuso-hoario
import json                      # Bibloteca  para Manipulação de arquivos json

class Database:
    """
    Classe para realizar as operações de banco de dados no sistema de controle de acesso por imagem.
    Essa classe abstrai a manipulação do banco, permitindo registrar usuários, dispositivos e acessar dados.
    """

    def __init__(self, host, user, password, database):
        """
        Construtor da classe que inicializa a conexão com o banco de dados.

        :param host: Endereço do servidor MySQL.
        :param user: Nome de usuário para acessar o banco.
        :param password: Senha do banco de dados.
        :param database: Nome do banco de dados.
        """
        self.host = host  # Endereço do servidor de banco de dados
        self.user = user  # Nome de usuário
        self.password = password  # Senha
        self.database = database  # Nome do banco de dados

    def connection(self):
        """
        Estabelece a conexão com o banco de dados MySQL e retorna a conexão.

        :return: Conexão com o banco de dados ou None em caso de erro.
        """
        try:
            conn = mysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database)
            return conn  # Retorna a conexão
        except mysql.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return None  # Retorna None em caso de falha

    def register_user(self, image_encoding, user_data_json, image_column, table):
        """
        Registra um novo usuário no banco de dados, incluindo a codificação da imagem facial.

        :param image_encoding: Codificação da imagem do rosto do usuário.
        :param user_data_json: Dados do usuário (JSON com nome, CPF, etc.).
        :param image_column: Nome da coluna onde a imagem será armazenada no banco.
        :param table: Nome da tabela onde os dados do usuário serão registrados.
        :return: True se o registro for bem-sucedido, ou None em caso de erro.
        """
        conn = self.connection()  # Estabelece a conexão com o banco
        cursor = conn.cursor()  # Cria o cursor para execução de comandos

        if conn is None:
            return None  # Se não conseguiu se conectar, retorna None

        try:
            encoding_string = ','.join(map(str, image_encoding[0]))  # Converte a codificação da imagem para string

            # Cria a lista de colunas para o comando SQL
            columns = ','.join(user_data_json.keys()) + f', {image_column}'
            placeholders = ', '.join(['%s'] * (len(user_data_json)+1))  # Cria placeholders para os valores

            # Junta os valores do usuário com a imagem
            values = tuple(user_data_json.values()) + (encoding_string,)

            # Prepara o comando SQL para inserção de dados
            command = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(command, values)  # Executa o comando SQL
            conn.commit()  # Confirma a transação

            return True  # Retorna True em caso de sucesso

        except mysql.Error as err:
            print(f"Erro no banco de dados: {err}")
            return None  # Retorna None se ocorrer algum erro

        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco

    def get_database(self, image_column=None, other_columns=(), table=''):
        """
        Recupera dados do banco de dados, incluindo a imagem se necessário.

        :param image_column: Nome da coluna de imagem (opcional).
        :param other_columns: Outras colunas a serem recuperadas.
        :param table: Nome da tabela onde os dados serão consultados.
        :return: Lista de dados recuperados ou None em caso de erro.
        """
        conn = self.connection()  # Estabelece a conexão com o banco
        cursor = conn.cursor()  # Cria o cursor

        try:
            columns = list(other_columns)
            if image_column:
                columns.insert(0, image_column)  # Insere a coluna da imagem na consulta, se necessário

            columns_string = ', '.join(columns)  # Junta as colunas para o comando SQL
            command = f"SELECT {columns_string} FROM {table}"  # Comando SQL para selecionar dados
            cursor.execute(command)  # Executa o comando SQL

            result = []  # Lista para armazenar os resultados

            for row in cursor.fetchall():  # Para cada linha de resultado
                if image_column:
                    # Se houver coluna de imagem, processa a codificação
                    encoding = np.array(list(map(float, row[0].split(','))))  # Converte a string de volta para o array
                    user_data = {columns[i]: row[i] for i in range(1, len(columns))}  # Monta o dicionário de dados do usuário
                    result.append((encoding, user_data))  # Adiciona o resultado à lista
                else:
                    user_data = {columns[i]: row[i] for i in range(len(columns))}  # Sem imagem, apenas dados do usuário
                    result.append(user_data)

            return result  # Retorna a lista com os resultados

        except mysql.Error as err:
            print(f"Erro no banco de dados: {err}")
            return None  # Retorna None se ocorrer erro na consulta

        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco

    def register_device(self, device_data, table):
        """
        Registra um dispositivo no banco de dados.

        :param device_data: Dados do dispositivo a ser registrado.
        :param table: Nome da tabela onde o dispositivo será registrado.
        :return: Tupla contendo sucesso e mensagem.
        """
        conn = self.connection()  # Estabelece a conexão com o banco
        if conn is None:
            return False, 'Erro ao conectar ao banco de dados'  # Se não conseguir conectar, retorna erro

        cursor = conn.cursor()  # Cria o cursor

        try:
            # Prepara os dados para o comando SQL
            columns = ', '.join(device_data.keys())  # Cria a lista de colunas
            placeholders = ', '.join(['%s'] * len(device_data))  # Cria os placeholders para os valores
            values = tuple(device_data.values())  # Converte os valores para tupla

            command = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"  # Comando SQL para inserção

            cursor.execute(command, values)  # Executa o comando SQL
            conn.commit()  # Confirma a transação

            return True, 'Dispositivo registrado com sucesso'  # Retorna sucesso

        except mysql.Error as err:
            print(f"Erro no banco de dados: {err}")
            return False, 'Erro ao registrar dispositivo no banco de dados'  # Retorna erro se falhar

        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco

    def get_device_data(self, mac_column, mac_address, table):
        """
        Recupera dados de um dispositivo com base no seu endereço MAC.

        :param mac_address: Endereço MAC do dispositivo.
        :param table: Nome da tabela onde os dados do dispositivo estão armazenados.
        :return: Dados do dispositivo ou mensagem de erro.
        """
        conn = self.connection()  # Estabelece a conexão com o banco
        if conn is None:
            return None, 'Erro ao conectar ao banco de dados'  # Se não conseguir conectar, retorna erro

        cursor = conn.cursor()  # Cria o cursor

        try:
            command = f"SELECT * FROM {table} WHERE {mac_column} = %s"  # Comando SQL para buscar pelo MAC
            cursor.execute(command, (mac_address,))  # Executa o comando SQL

            result = cursor.fetchone()  # Recupera um único resultado

            if result:
                columns = [desc[0] for desc in cursor.description]  # Obtém os nomes das colunas
                device_data = dict(zip(columns, result))  # Cria um dicionário com os dados do dispositivo
                return device_data, None  # Retorna os dados do dispositivo
            else:
                return None, 'Dispositivo não encontrado'  # Se não encontrar, retorna mensagem de erro

        except mysql.Error as err:
            print(f"Erro no banco de dados: {err}")
            return None, 'Erro ao consultar dispositivo no banco de dados'  # Retorna erro se falhar

        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco

    def save_historic(self, user_data, device_data, table, date_column, time_column):
        """
        Salva um registro histórico com dados do usuário e do dispositivo.

        :param user_data: Dados do usuário.
        :param device_data: Dados do dispositivo.
        :param table: Nome da tabela onde o histórico será registrado.
        :param date_column: Nome da coluna de data.
        :param time_column: Nome da coluna de hora.
        :return: Dicionário com status e mensagem.
        """
        conn = self.connection()  # Estabelece a conexão com o banco
        if conn is None:
            return {'sucess': False, 'message': 'Erro ao conectar ao banco de dados'}  # Retorna erro se não conseguir conectar

        cursor = conn.cursor()  # Cria o cursor

        try:
            timezone = pytz.timezone('America/Belem')
            now = datetime.now(timezone)  # Obtém a data e hora atual
            combined_data = {
                date_column: now.strftime('%Y-%m-%d'),
                time_column: now.strftime('%H:%M:%S'),
                **user_data,
                **device_data
            }

            for key, value in combined_data.items():
                if isinstance(value, (dict, list, tuple)):
                    combined_data[key] = str(value)  # Converte objetos complexos para string

            columns = ', '.join(combined_data.keys())  # Cria a lista de colunas
            placeholders = ', '.join(['%s'] * len(combined_data))  # Cria os placeholders para os valores
            command = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"  # Comando SQL para inserção

            cursor.execute(command, tuple(combined_data.values()))  # Executa o comando SQL
            conn.commit()  # Confirma a transação

            return {'sucess': True, 'message': 'Histórico registrado com sucesso'}  # Retorna sucesso

        except mysql.Error as err:
            print(f"Erro no banco de dados: {err}")
            return {'sucess': False, 'message': f'Erro ao salvar no banco de dados: {err}'}  # Retorna erro

        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco


    def search_database(self, data_json, table, image_column=''):
        """
        Realiza uma consulta no banco de dados para buscar um usuário ou dispositivo baseado nas informações fornecidas no JSON.

        Parâmetros:
        data_json (dict): Um dicionário contendo os dados para a busca. A chave é o nome da coluna e o valor é o dado a ser filtrado.
        table (str): Nome da tabela onde a consulta será realizada.
        image_column (str): Nome da coluna que contém as imagens, caso seja necessário removê-la dos resultados. Default é uma string vazia.

        Retorna:
        dict: Um dicionário contendo o sucesso da operação, os dados encontrados e a mensagem de erro ou sucesso.
        """
    
        # Estabelece a conexão com o banco de dados
        conn = self.connection()
        
        # Verifica se a conexão foi bem-sucedida
        if conn is None:
            # Caso contrário, retorna um erro de conexão
            return False, 'Erro ao conectar ao banco de dados'

        # Cria o cursor para executar a consulta SQL
        cursor = conn.cursor()

        try:
            # Filtra o dicionário de entrada para remover entradas vazias e a coluna de imagem
            filter_json = {key: value for key, value in data_json.items() if value != '' and key != image_column}

            # Constrói a string de condições WHERE para a consulta SQL
            columns = ' AND '.join([f"{key} = %s" for key in filter_json.keys()])
            
            # Lista dos valores correspondentes às chaves filtradas
            values = list(filter_json.values())  # Usa os valores filtrados

            # Constrói a consulta SQL com a cláusula WHERE, se houver condições a serem aplicadas
            query = f"SELECT * FROM {table}" + (f" WHERE {columns};" if columns else ";")
            
            # Executa a consulta no banco de dados com os valores filtrados
            cursor.execute(query, values)

            # Obtém as descrições das colunas retornadas pela consulta
            all_columns = [desc[0] for desc in cursor.description]
            
            # Obtém todos os dados retornados pela consulta
            all_data = cursor.fetchall()

            # Verifica se a coluna de imagem existe nos resultados
            if image_column in all_columns:
                # Obtém o índice da coluna de imagem
                col_index = all_columns.index(image_column)
                
                # Remove a coluna de imagem da lista de colunas e dos dados retornados
                all_columns.pop(col_index)
                all_data = [tuple(value for idx, value in enumerate(row) if idx != col_index) for row in all_data]

            # Retorna um dicionário com as colunas e dados sem a coluna de imagem
            result = {'columns': all_columns, 'data': all_data}
            return result

        except Exception as e:
            # Caso ocorra um erro, captura a exceção e imprime uma mensagem de erro
            print(f"Erro ao pesquisar tal usuário: {e}")
            
            # Retorna um dicionário com a mensagem de erro
            return {'success': False, 'message': f"Erro ao pesquisar tal usuário: {e}"}

        finally:
            # Garante que o cursor e a conexão com o banco de dados sejam fechados
            cursor.close()
            conn.close()

    

# Classe Webcam: Responsável por capturar imagens da webcam.
class Webcam:
    def __init__(self, host):
        """
        Inicializa a webcam com o host fornecido.
        :param host: Pode ser o índice da câmera ou a URL de uma câmera IP.
        """
        self.cam = cv2.VideoCapture(host)

    def image(self):
        """
        Captura uma imagem da webcam.
        :return: Uma lista contendo a imagem convertida para RGB e a imagem em formato BGR.
        """
        req, frame = self.cam.read()  # Captura o quadro da câmera
        verify = lambda x: [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), frame] if x else [None, None]
        return verify(req)


# Classe Commands: Contém comandos e lógica de autenticação, registro de usuários e dispositivos.
class Commands:
    def __init__(self, host_webcam, host_database, user_database, password, database_name,
                 image_column, other_columns, user_table, device_table, mac_column):
        """
        Inicializa os parâmetros necessários para conectar à webcam e ao banco de dados.
        :param host_webcam: Endereço ou índice da webcam.
        :param host_database: Endereço do servidor de banco de dados.
        :param user_database: Nome de usuário do banco de dados.
        :param password: Senha do banco de dados.
        :param database_name: Nome do banco de dados.
        :param image_column: Nome da coluna de imagem no banco de dados.
        :param other_columns: Outras colunas no banco de dados.
        :param user_table: Tabela de usuários no banco de dados.
        :param device_table: Tabela de dispositivos no banco de dados.
        :param mac_column: Nome da coluna de MAC no banco de dados.
        """
        self.image_column = image_column
        self.other_columns = other_columns
        self.database_name = database_name
        self.host_database = host_database
        self.user_database = user_database
        self.host_webcam = host_webcam
        self.user_table = user_table
        self.password = password
        self.device_table = device_table
        self.mac_column = mac_column

    def load_data(self):
        """
        Carrega os dados do banco de dados, incluindo imagens e outras informações dos usuários.
        :return: Dados dos usuários (imagem e outras colunas).
        """
        db = Database(host=self.host_database, user=self.user_database, password=self.password,
                      database=self.database_name)
        return db.get_database(self.image_column, self.other_columns, self.user_table)

    def face_verify_database(self, trust):
        """
        Realiza a verificação de face para autenticação.
        :param trust: O nível de confiança necessário para autenticação (percentual).
        :return: Resultado da autenticação com dados do usuário ou erro.
        """
        webcam = Webcam(self.host_webcam)  # Inicializa a webcam
        image_webcam = webcam.image()[0]  # Captura a imagem da webcam

        face_locate_webcam = fr.face_locations(image_webcam)  # Detecta as localizações de rostos na imagem

        if not face_locate_webcam:
            return {'Auth': False, 'Error': 'Nenhum Rosto Detectado'}  # Retorna erro se não detectar rosto

        data_users = self.load_data()  # Carrega os dados dos usuários

        encoding_data = [encoding for encoding, _ in data_users]  # Coleta os encodings das faces
        user_data = [data for _, data in data_users]  # Coleta os dados associados aos usuários
        face_encoding_webcam = fr.face_encodings(image_webcam, face_locate_webcam)  # Codifica o rosto detectado

        results = []

        # Calcula a distância entre os encodings da webcam e os encodings armazenados
        for face_encoding in face_encoding_webcam:
            distances = [int((-dist + 1) * 100) for dist in fr.face_distance(encoding_data, face_encoding)]
            results.append(distances)

        recognized_faces = []

        # Verifica se a confiança está acima do nível mínimo necessário
        for i in range(len(results[0])):
            if max(results[0]) == results[0][i]:
                if results[0][i] >= trust:
                    recognized_faces.append({'Dados do Usuario': user_data[i], 'trust': results[0][i],
                                             'Auth': True})
                else:
                    recognized_faces.append({'Dados do Usuario': 'unknown', 'trust': results[0][i],
                                             'Auth': False})

        if recognized_faces:
            return recognized_faces
        else:
            return {'Auth': False, 'Error': 'Nenhum Rosto Detectado'}

    def register_user(self, user_data_json):
        """
        Registra um novo usuário no banco de dados a partir de um JSON contendo os dados do usuário.
        :param user_data_json: JSON contendo as informações do usuário.
        :return: Resultado da operação de registro.
        """
        webcam = Webcam(self.host_webcam)
        image_webcam = webcam.image()[0]

        face_locate_webcam = fr.face_locations(image_webcam)

        if not face_locate_webcam:
            return False, 'Nenhum rosto detectado na webcam'

        face_encoding_webcam = fr.face_encodings(image_webcam, face_locate_webcam)

        if not face_encoding_webcam:
            return False, 'Erro ao processar encoding do rosto'

        db = Database(host=self.host_database, user=self.user_database, password=self.password,
                      database=self.database_name)

        success = db.register_user(image_encoding=face_encoding_webcam,
                                   image_column=self.image_column,
                                   table=self.user_table, user_data_json=user_data_json)

        if success:
            return True, 'Usuário registrado com sucesso'
        else:
            return False, 'Erro ao registrar usuário no banco de dados'

    def register_device(self, device_data_json):
        """
        Registra um dispositivo no banco de dados a partir de um JSON contendo os dados do dispositivo.
        :param device_data_json: JSON contendo as informações do dispositivo.
        :return: Resultado da operação de registro do dispositivo.
        """
        db = Database(host=self.host_database, user=self.user_database, password=self.password,
                      database=self.database_name)

        success, message = db.register_device(device_data_json, self.device_table)

        return {'resultado': success, 'mensagem': message}

    def authenticate_device(self, device_data_json):
        """
        Autentica um dispositivo no banco de dados a partir de um JSON contendo os dados do dispositivo.
        :param device_data_json: JSON contendo os dados do dispositivo, como o MAC address.
        :return: Resultado da autenticação do dispositivo.
        """
        mac_address = device_data_json.get('mac')
        if not mac_address:
            return {'Auth': False, 'Error': 'Endereço MAC não fornecido'}

        db = Database(host=self.host_database, user=self.user_database, password=self.password,
                      database=self.database_name)

        device_data, error_message = db.get_device_data(self.mac_column, mac_address, self.device_table)

        result = lambda x: {'Auth': True, 'device': device_data} if x is not None else {'Auth': False, 'device': 'unknow'}

        return result(device_data)

    def save_historic_data(self, user_data, device_data, table, date_column, time_column):
        """
        Salva os dados históricos de autenticação no banco de dados.
        :param user_data: Dados do usuário autenticado.
        :param device_data: Dados do dispositivo.
        :param table: Tabela onde os dados serão salvos.
        :param date_column: Coluna para data.
        :param time_column: Coluna para hora.
        :return: Resultado da operação de salvamento.
        """
        db = Database(host=self.host_database, user=self.user_database, password=self.password,
                      database=self.database_name)

        save = db.save_historic(user_data, device_data, table, date_column, time_column)

        return save

    def search_data(self, data_json, table, image_column=''):
        """
        Realiza uma busca no banco de dados a partir de um JSON contendo os dados de busca.
        :param data_json: JSON com os dados a serem buscados.
        :param table: Tabela onde a busca será realizada.
        :param image_column: Coluna de imagem (opcional).
        :return: Resultado da busca no banco de dados.
        """
        db = Database(host=self.host_database, user=self.user_database, password=self.password,
                      database=self.database_name)

        try:
            # Realiza a busca no banco de dados
            result = db.search_database(data_json=data_json, table=table, image_column=image_column)

            if not result['data']:
                # Retorno padrão para ausência de resultados
                return {"success": False, "result": None, "message": "Nenhum registro encontrado."}

            # Retorno em caso de sucesso
            return {"success": True, "result": result, "message": "Busca realizada com sucesso."}

        except Exception as e:
            # Tratamento de exceções e falhas no processo
            return {"success": False, "result": None, "message": f"Erro ao acessar o banco de dados: {str(e)}"}
    

    def face_verify_json(self, trust_threshold, name_archive_encoding_json, key_encoding):
        webcam = Webcam(self.host_webcam)
        image_webcam = webcam.image()[0]

        # Detectar rosto na webcam
        face_locate_webcam = fr.face_locations(image_webcam)
        if not face_locate_webcam:
            return {
                "message": "Nenhum rosto detectado na webcam",
                "success": False,
                "results": []
            }

        # Obter encoding do rosto capturado
        face_encoding_webcam = fr.face_encodings(image_webcam, face_locate_webcam)
        if not face_encoding_webcam:
            return {
                "message": "Erro ao processar encoding do rosto",
                "success": False,
                "results": []
            }

        # Carregar encodings armazenados no arquivo JSON
        try:
            with open(name_archive_encoding_json, 'r') as file:
                data_json = json.load(file)
        except Exception as e:
            return {
                "message": f"Erro ao carregar arquivo JSON: {str(e)}",
                "success": False,
                "results": []
            }

        results = []
        overall_success = True  # Flag para verificar se o processo foi concluído com sucesso

        # Iterar sobre os rostos detectados pela webcam
        for index, encoding in enumerate(face_encoding_webcam):
            best_match = None
            highest_trust = -1

            # Comparar com os encodings armazenados no JSON
            for data in data_json:
                # Verificar se a chave com os encodings existe no JSON
                if key_encoding not in data:
                    continue

                # Converter o valor da chave "encoding" de string para lista de floats
                try:
                    stored_encoding = list(map(float, data[key_encoding].split(',')))
                except Exception as e:
                    overall_success = False
                    results.append({
                        "message": f"Erro ao converter encoding: {str(e)}",
                        "success": False,
                        "trust": 0,
                        "dados": None
                    })
                    continue

                # Calcular distância e confiança
                try:
                    distance = fr.face_distance([stored_encoding], encoding)[0]
                    current_trust = int((-distance + 1) * 100)

                    # Verificar se esta é a melhor correspondência até agora
                    if current_trust > highest_trust:
                        highest_trust = current_trust
                        best_match = data

                except Exception as e:
                    overall_success = False
                    results.append({
                        "message": f"Erro ao calcular distâncias: {str(e)}",
                        "success": False,
                        "trust": 0,
                        "dados": None
                    })
                    continue

            # Determinar sucesso com base no trust_threshold
            success = highest_trust >= trust_threshold

            if success:
                results.append({
                    "message": "Rosto processado com sucesso",
                    "success": success,
                    "trust": highest_trust,
                    "dados": best_match
                })
            
            else:
                results.append({
                    "message": "Nenhum rosto correspondente encontrado",
                    "success": success,
                    "trust": highest_trust,
                    "dados": []
                })
        # Determinar mensagem geral e sucesso geral
        overall_message = "Processamento concluído com sucesso" if overall_success else "Erros ocorreram durante o processamento"

        return {
            "message": overall_message,
            "success": overall_success,
            "results": results
        }




    
    def register_face_json(self, name_archive_encoding_json, key_encoding, data_user_dict):
        webcam = Webcam(self.host_webcam)
        image_webcam = webcam.image()[0]

        # Detectar rosto na webcam
        face_locate_webcam = fr.face_locations(image_webcam)
        if not face_locate_webcam:
            return False, 'Nenhum rosto detectado na webcam'

        # Obter encoding do rosto capturado
        face_encoding_webcam = fr.face_encodings(image_webcam, face_locate_webcam)
        if not face_encoding_webcam:
            return False, 'Erro ao processar encoding do rosto'

        # Converter encoding para string
        encoding_string = ','.join(map(str, face_encoding_webcam[0]))
        data_user_dict[key_encoding] = encoding_string

        # Carregar dados existentes do arquivo JSON
        try:
            with open(name_archive_encoding_json, 'r') as file:
                try:
                    data = json.load(file)
                except (json.JSONDecodeError, ValueError):
                    data = []  # Inicializa como uma lista vazia se o arquivo estiver vazio ou inválido
        except FileNotFoundError:
            data = []  # Cria um novo arquivo JSON se ele não existir
        except Exception as e:
            return False, f'Erro ao carregar arquivo JSON: {str(e)}'

        # Adicionar o novo usuário aos dados
        if not isinstance(data, list):
            return False, 'Formato de arquivo JSON inválido, esperado uma lista'
        data.append(data_user_dict)

        # Gravar os dados atualizados no arquivo JSON
        try:
            with open(name_archive_encoding_json, 'w') as file:
                json.dump(data, file, indent=4)
            return True, 'Rosto registrado com sucesso'
        except Exception as e:
            return False, f'Erro ao gravar arquivo JSON: {str(e)}'
