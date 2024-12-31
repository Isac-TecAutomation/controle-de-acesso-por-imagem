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
- **mysql**: SGDB de banco dados responsável pelo gerenciamento dinâmico de dados
- **phpmyadmin (opcional)**: interface para gerenciar o SGDB mysql

## Biblotecas utilizadas no python

- **mysql-conector-python**: Bibloteca para conexão e manipulação do banco de dados (mysql)
- **face-recognition**: Bibloteca responsável pela detectação e autenticação facial por meio de 
inteligência artificial
- **opencv-python**: Bibloteca para o processamento de imagens no python
- **flask**: para criação de um servidor e conexão da API na rede de comunicação


## Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

- Python 3.9 ou superior.
- Sistema operacional **Linux** (recomendado: GNOME).
- Pip (gerenciador de pacotes do Python).
- CMake e suas dependências (siga o tutorial abaixo, se necessário).
- Docker e suas dependências (opcional).

### Observações:
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
  
  ## passo 2: criação de um ambiente virtual python (venv) e instalação das biblotecas necessárias

  1- crie uma pasta para criação do ambiente antes de executar o comando abaixo e se redirecione para tal:

  ```bash mkdir <nome-para-pasta-do-seu--projeto> && cd <nome-para-pasta-do-seu--projeto>```
   
  2- Após isso crie um ambiente virtual python para a instalação correta e segura das biblotecas para
  o projeto:
  
  ```bash python3 -m venv <nome-do-seu-ambiente>```

  3- clone o arquivo requirements.txt e execute com pip para instalar as biblotecas python do projeto:

  ```bash curl -O https://raw.githubusercontent.com/Isac-TecAutomation/controle-de-acesso-por-imagem-repositorio/refs/heads/main/requirements.txt?token=GHSAT0AAAAAAC4DZWF24EIYL6RV2IMXLYO4Z3TKPNA ```

