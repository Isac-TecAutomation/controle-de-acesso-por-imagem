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
    host_webcam='<host_da_sua_webcam>',  # Exemplo: 'http://<endereço_ip>/800x600.jpg'
    dir_archive_json='<caminho_do_arquivo_json>',  # Exemplo: 'caminho/para/arquivo.json'
    image_column='<nome_da_coluna_de_imagem>'  # Exemplo: 'encoding'
)

# Parte principal do código
if __name__ == '__main__':

    # Aqui o usuário pode escolher entre registrar ou verificar um rosto.
    

    # IMPORTANTE: comente a parte que você não irá testar para evitaar conflitos

    # VERIFICAR ROSTO:
    # A função face_verify_json contém o parâmetro define o limite de confiança. Quanto mais alto o número, mais rigorosa será 
    # a verificação.

    Verificar = control.face_verify_json(60)
    
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
    Registrar = control.register_face_json(dados_novo_usuario)
    
    # A função register_face_json adiciona um novo rosto ao banco de dados. O arquivo JSON será atualizado com
    # o novo rosto e os dados relacionados.

    print(Registrar)
    
    # COMENTÁRIOS IMPORTANTES:
    # - Ao usar o método face_verify_json, o sistema verifica se o rosto capturado corresponde a um rosto já registrado.
    # - Caso use o método register_face_json, você poderá adicionar novos rostos ao banco de dados para futuras verificações.
    #
    # Observação:

    # - O arquivo 'dados.json' deve estar no formato correto, com os encodings das faces dos usuários.
  

   
