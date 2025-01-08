# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: Este módulo cuida da captura de imagem através da webcam e realiza a verificação 
#            do rosto de usuários, comparando com dados armazenados em um arquivo JSON.
# ==============================================

import mysql.connector as mysql  # Importa a biblioteca mysql.connector para conectar ao banco de dados MySQL.
import face_recognition as fr    # Importa a biblioteca face_recognition para detecção e comparação de rostos.
import numpy as np               # Importa o numpy para manipulação de dados numéricos.
import json                      # Importa a biblioteca json para ler e escrever dados em arquivos JSON.
import cv2                       # Importa a biblioteca OpenCV (cv2) para captura de vídeo e manipulação de imagens.

# ================================================================================================================
# Função para carregar os dados dos usuários e os encodings das faces a partir de um arquivo JSON
# ================================================================================================================

def get_client(archive_json, key_encoding):
    """
    Tenta carregar os dados dos usuários a partir de um arquivo JSON e extrair as informações necessárias.
    
    :param archive_json: Caminho para o arquivo JSON contendo os dados dos usuários.
    :param key_encoding: Chave correspondente ao encoding da face.
    :return: Dados do cliente, incluindo a lista de encodings e informações do usuário.
    """

    list_data = []

    try:
        # Tenta abrir e carregar o arquivo JSON com os dados dos usuários
        with open(archive_json, 'r') as file:
            try:
                data = json.load(file)

                # Verifica se o arquivo JSON está vazio
                if not data:
                    return {
                        "message": "Lista de Usuarios vazia",
                        "success": False,
                        "results": []
                    }
                else:
                    # Para cada usuário no arquivo JSON, filtra os dados e os encodings das faces
                    for data_users in data:
                        filter_json = {key: value for key, value in data_users.items() 
                                       if value != '' and key != key_encoding}
                        
                        list_data.append({"data": filter_json, "encoding": 
                                        data_users[key_encoding]})
                    
                    return {
                        "message": "Coleta realizada com sucesso !",
                        "success": True,
                        "results": list_data
                    }

            except (json.JSONDecodeError, ValueError):
                # Se o arquivo JSON estiver vazio ou inválido, retorna erro
                return {
                    "message": "Arquivo invalido ou Vazio",
                    "success": False,
                    "results": []
                }
    
    except FileNotFoundError:
        # Se o arquivo JSON não for encontrado, retorna erro
        return {
            "message": "Arquivo não encontrado",
            "success": False,
            "results": []
        }
        
    except Exception as e:
        # Se houver erro ao carregar o arquivo JSON, retorna mensagem de erro
        return {
            "message": f"Erro ao carregar arquivo JSON: {str(e)}",
            "success": False,
            "results": []
        }

# ================================================================================================================
# Função para verificar rostos em um frame da webcam comparando com os encodings do arquivo JSON
# ================================================================================================================

def face_verify(trust_threshold, encoding_json, frame):
    """
    Verifica rostos em um frame capturado pela webcam, comparando com os encodings dos rostos 
    registrados no arquivo JSON. Realiza a comparação e retorna os resultados de verificação.

    :param trust_threshold: Limite de confiança para a verificação de correspondência facial.
    :param encoding_json: Lista de encodings extraídos do arquivo JSON.
    :param frame: Frame capturado da webcam.
    :return: Lista de resultados de verificação de rostos e o frame anotado.
    """
    # Converte o frame para o formato esperado pelo OpenCV
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Localiza os rostos no frame e extrai os encodings
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)
    
    results = []  # Lista para armazenar os resultados da verificação

    # Itera sobre os encodings de rostos encontrados no frame
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        best_match = None
        best_distance = float('inf')

        # Compara o encoding do rosto detectado com os encodings dos usuários registrados
        for entry in encoding_json:
            try:
                server_encoding = list(map(float, entry["encoding"].split(',')))  # Converte o encoding para lista de floats
                user_data = entry["data"]  # Dados do usuário

                # Calcula a distância entre os encodings do rosto capturado e os registrados
                distance = fr.face_distance([server_encoding], face_encoding)[0]

                # Verifica se encontrou a melhor correspondência
                if distance < best_distance:
                    best_distance = distance
                    best_match = (user_data, distance)
            except Exception as e:
                print(f"Erro ao processar entrada do JSON: {str(e)}")
                continue

        # Se a correspondência for bem-sucedida, marca o rosto com verde e exibe as informações
        if best_match and (1 - best_distance) * 100 >= trust_threshold:
            user_data, distance = best_match
            confidence = int((1 - best_distance) * 100)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Marca o rosto com um retângulo verde

            # Exibe o nível de confiança no frame
            cv2.putText(frame, f'Auth: True trust: {confidence} %', (left, bottom + 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Exibe os dados do usuário no frame
            cv2.putText(frame, f'Dados: {user_data}', (left, bottom + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            results.append({"data": user_data, "auth": True, "confidence": confidence})
        else:
            # Se não houver correspondência, marca o rosto com vermelho
            confidence = int((1 - best_distance) * 100) if best_match else 0
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, 'Unknown', (left, bottom + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.putText(frame, f'Auth: False', (left, bottom + 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            results.append({"data": {}, "auth": False, "confidence": confidence})

    return results, frame  # Retorna os resultados e o frame anotado com as informações de verificação

# ================================================================================================================
# Função principal para executar o reconhecimento facial
# ================================================================================================================

if __name__ == '__main__':

    # Valores obrigatório para o exemplo

    host_webcam = '<host da sua webcam>'
    dir_data_json = '<diretório do arquivo json onde tá os dados>'
    key_encoding = '<nome da chave onde se encontra os encoding>'

    trust = 60 # nivel de confiança (recomendado 60)

    # Carrega os dados dos usuários a partir do arquivo JSON
    client_data = get_client(dir_data_json, 
                             key_encoding)

    # Verifica se os dados foram carregados corretamente
    if client_data['success']:
        print(client_data['message'])
        
        # Captura o frame da webcam (substitua pelo endereço da sua câmera real)
        web = cv2.VideoCapture(host_webcam)  # Endereço da webcam
        ret, frame = web.read()

        # Se o frame for capturado com sucesso, realiza a verificação facial
        if ret:
            results, annotated_frame = face_verify(trust, client_data["results"], frame)
            print("Resultados:", results)  # Exibe os resultados da verificação

            # Exibe o frame anotado com as informações no OpenCV
            cv2.imshow("Frame", annotated_frame)
            cv2.waitKey(0)

        else:
            print("Erro ao capturar frame.")  # Caso não consiga capturar o frame da webcam

        # Libera os recursos da webcam e fecha as janelas do OpenCV
        
        web.release()
        cv2.destroyAllWindows()
    else:
        print(client_data["message"])  # Exibe mensagem de erro caso não consiga carregar os dados
