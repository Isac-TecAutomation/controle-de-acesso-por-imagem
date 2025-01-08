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

# Importação de bibliotecas necessárias
from comandos import Commands  # Importa a classe Commands responsável pelas operações de reconhecimento facial.
import cv2  # OpenCV, usado para exibir e processar imagens.

# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam='http://192.168.0.20/800x600.jpg',  # Endereço da webcam. Substituir pelo endereço da sua webcam.
    image_column='encoding',  # Nome da coluna no JSON que contém os encodings faciais registrados.
    dir_archive_json='exemplos produção/simples reconhecimento facial json/dados.json' 
    # Caminho do arquivo JSON que contém os dados de encodings faciais e informações dos usuários.
)

# Parte principal do código - Executa o programa
if __name__ == '__main__':
    # Executa a verificação facial com um limite de confiança de 60%.
    # O método retorna os resultados da verificação e o frame anotado.
    result, frame = control.face_verify_json_image(60)

    # Imprime os resultados no console para análise e debugging.
    print(result)

    # Exibe o frame anotado em uma janela chamada "exemplo".
    # As anotações incluem informações como se a face foi autenticada, nível de confiança, etc.
    cv2.imshow("exemplo", frame)

    # Aguarda uma tecla ser pressionada antes de fechar a janela.
    cv2.waitKey(0)
    cv2.destroyAllWindows()
