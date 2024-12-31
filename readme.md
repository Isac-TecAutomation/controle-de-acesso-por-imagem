# Controle de Acesso por Imagem

## Descrição do Projeto

O **Controle de Acesso por Imagem** é um sistema que utiliza inteligência artificial e processamento de imagem para realizar o reconhecimento facial de usuários, proporcionando um método seguro e eficiente de controle de acesso.

## Funcionalidades

- Reconhecimento facial para autenticação de usuários.
- Integração com banco de dados para armazenamento de usuários.
- Painel administrativo para gerenciamento de acessos(Exemplos)

## Tecnologias Utilizadas

- **Python 3.9+**: Linguagem principal do projeto.
- **docker 27.4.1**: Para criação de container (opcional)

## Pré-requisitos

Certifique-se de ter instalado em sua máquina:
- Python 3.9 ou superior.
- Sistema operacional Linux (recomendado).
- Pip (gerenciador de pacotes do Python).
- cmake e suas dependências (caso não estiver instalado siga o tutorial abaixo)
## Instalação

- observação: o tutorial testado apenas numa interface linux (gnome)
- houve problemas na instalação das depedencias em sistema linux com interface KDE

1. instale as depedências necessárias:
  ```bash sudo apt update -y && sudo apt install -y cmake python3-pip python3-dev apt-utils libgl1-mesa-glx ```

  