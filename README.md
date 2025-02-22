# Controle de Acesso por Imagem

## Descrição do Projeto

O **Controle de Acesso por Imagem** é um sistema que utiliza inteligência artificial e processamento de imagem para realizar o reconhecimento facial de usuários, proporcionando um método seguro e eficiente de controle de acesso.

## Funcionalidades

- **Reconhecimento facial**: Autenticação de usuários por meio de IA.
- **Banco de dados**: Integração para armazenamento e gerenciamento de usuários.
- **Painel administrativo**: Interface para gerenciar acessos e permissões.

## Tecnologias Utilizadas

- **Python 3.9+**: Linguagem principal do projeto.
- **Docker (opcional)**: Para criação de contêineres e ambiente isolado (versão 27.4.1).
- **MySQL**: Sistema de gerenciamento de banco de dados (SGDB) responsável pelo gerenciamento dinâmico de dados.
- **phpMyAdmin (opcional)**: Interface para gerenciar o SGDB MySQL.

## Bibliotecas Utilizadas no Python

- **mysql-connector-python**: Biblioteca para conexão e manipulação do banco de dados (MySQL).
- **face-recognition**: Biblioteca responsável pela detecção e autenticação facial por meio de inteligência artificial.
- **opencv-python**: Biblioteca para o processamento de imagens no Python.
- **flask**: Para criação de um servidor e conexão da API na rede de comunicação.

## Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

- Python 3.9 ou superior.
- Sistema operacional **Linux** (recomendado: GNOME).
- Pip (gerenciador de pacotes do Python).
- CMake e suas dependências (siga o tutorial abaixo, se necessário).
- Docker e suas dependências (opcional).

### Observações

- Este tutorial foi testado em sistemas Linux com interface GNOME e KDE.
- **Problemas conhecidos**: Em sistemas Linux com interface KDE, podem ocorrer erros na instalação de dependências.

## Instalação

Siga os passos abaixo para configurar o projeto em sua máquina:

### Passo 1: Atualizar e instalar dependências

Execute o comando abaixo para instalar todas as dependências necessárias para o projeto:

```bash
sudo apt update -y && sudo apt install -y \
    build-essential \
    cmake \
    python3-pip \
    python3-dev \
    libboost-python-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    apt-utils \
    libgl1-mesa-glx \
    libx11-dev \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    libpng-dev
```

### Passo 2: Criação de um ambiente virtual Python (venv) e instalação das bibliotecas necessárias

1. Crie uma pasta para o projeto e entre nela:
   
   ```bash
   mkdir <nome-para-pasta-do-seu-projeto> && cd <nome-para-pasta-do-seu-projeto>
   ```

2. Crie um ambiente virtual Python para a instalação correta e segura das bibliotecas para o projeto:

   ```bash
   python3 -m venv <nome-do-seu-ambiente>
   ```

3. Clone o arquivo `requirements.txt`:

   ```bash
   curl -O https://raw.githubusercontent.com/Isac-TecAutomation/controle-de-acesso-por-imagem-repositorio/refs/heads/main/requirements.txt?token=GHSAT0AAAAAAC4DZWF3Y5GYEGXUFYVFHN2QZ3TK4ZA
   ```


4. execute por meio do pip o arquivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

5. clone o arquivo `comandos.py`:
 
   ```bash
   curl -O https://raw.githubusercontent.com/Isac-TecAutomation/controle-de-acesso-por-imagem-repositorio/refs/heads/main/comandos.py?token=GHSAT0AAAAAAC4DZWF2HW2BQVYK4FB5KFVUZ3TLGIA](https://raw.githubusercontent.com/Isac-TecAutomation/controle-de-acesso-por-imagem-repositorio/refs/heads/main/comandos.py
   ```

6. pronto! Agora basta seguir o passo a passo dos exemplos para poder usufruir da bibloteca


7. Créditos:

   - https://github.com/ageitgey/face_recognition

