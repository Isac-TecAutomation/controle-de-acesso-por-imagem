# ==============================================
# PROJETO: CONTROLE DE ACESSO POR IMAGEM
# ==============================================
# AUTOR: Isac Eugenio, Estevão, prof° Israel Peixoto, prof° Everaldo Santos
#
# ORIENTADORES: prof° Israel Peixoto, prof° Everaldo Santos
#
# OBJETIVO: Desenvolver um sistema de controle de acesso utilizando reconhecimento facial.
#
# DESCRIÇÃO: este módulo cuida dos exemplos de demonstração de funcionamento dos arquivos

# ==============================================

from comandos import Commands

# Inicializa o objeto de controle de acesso com as configurações específicas.
control = Commands(
    host_webcam= 'http://192.168.0.20/800x600.jpg',     #'<host da sua webcam>',  # Endereço da webcam para capturar imagem de reconhecimento facial.
    host_database='<host do seu database>',  # Endereço do servidor MySQL (localhost).
    user_database='<usuario do seu banco de dados>',  # Usuário do banco de dados (troque por seu usuário).
    password='<sua senha usuario do DB>',  # Senha do banco de dados (troque por sua senha).
    database_name='db_controle_de_acesso_por_imagem',  # Nome do banco de dados.
    image_column='<coluna de encoding no DB>',  # Nome da coluna onde as imagens dos usuários estão armazenadas no banco.
    other_columns= 'tupla com as outras colunas do tabela',  # Outras colunas que são relevantes para o controle de acesso.
    user_table='<nome da tabela pertecente a usuarios>',  # Nome da tabela de usuários no banco de dados.
    device_table='<tabela de dispositivos permitidos para o acesso>',  # Nome da tabela de dispositivos no banco de dados.
    mac_column='<coluna com mac para esse dispositivos>'  # Coluna que armazena os endereços MAC dos dispositivos.
)

# Parte principal do código
if __name__ == '__main__':

    # Aqui o usuário pode escolher entre registrar ou verificar um rosto.
    

    # IMPORTANTE: comente a parte que você não irá testar para evitaar conflitos

    # VERIFICAR ROSTO:
    # A função face_verify_json recebe o limite de confiança, o caminho do arquivo JSON com os dados 
    # e o nome da chave (encoding). Este método será usado para verificar se um rosto capturado 
    # corresponde a algum rosto registrado no banco de dados.
    #
    # O primeiro parâmetro define o limite de confiança. Quanto mais alto o número, mais rigorosa será 
    # a verificação.

    Verificar = control.face_verify_json('<nivel de confiança minimo (int)>', 
                                        '<diretório>dados.json', '<chave correspondente aos encodings>')
    
    # Exibe o resultado da verificação de rosto. Se a correspondência for bem-sucedida, serão mostrados os dados
    # do usuário correspondente.

    print(Verificar)
    
    # REGISTRAR ROSTO:
    # Para registrar um novo rosto, basta descomentar a linha abaixo e fornecer o caminho do arquivo JSON
    # para registrar o novo rosto e dados do usuário. A função register_face_json registra a face
    # e os dados fornecidos no JSON.
    
    # Registrar o rosto de um novo usuário (exemplo de registro):
    #adicione informações manualmente sobre o novo usuario sendo o dados respectivo tipo nome como chave
    dados_novo_usuario = {}
     
    # essa é disposição correta:
    Registrar = control.register_face_json('<diretório>dados.json', '<chave correspondente aos encodings>', dados_novo_usuario)
    
    # A função register_face_json adiciona um novo rosto ao banco de dados. O arquivo JSON será atualizado com
    # o novo rosto e os dados relacionados.

    print(Registrar)
    
    # COMENTÁRIOS IMPORTANTES:
    # - Ao usar o método face_verify_json, o sistema verifica se o rosto capturado corresponde a um rosto já registrado.
    # - Caso use o método register_face_json, você poderá adicionar novos rostos ao banco de dados para futuras verificações.
    #
    # Observação:

    # - O arquivo 'dados.json' deve estar no formato correto, com os encodings das faces dos usuários.
  

   
