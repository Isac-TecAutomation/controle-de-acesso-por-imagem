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
- **Bibliotecas**: 
  - OpenCV
  - NumPy
  - Matplotlib
  - Flask (possivelmente)
  - MongoDB (possivelmente)

## Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

- Python 3.9 ou superior.
- Sistema operacional **Linux** (recomendado: GNOME).
- Pip (gerenciador de pacotes do Python).
- CMake e suas dependências (siga o tutorial abaixo, se necessário).
- Docker e suas dependências (opcional).

### Observações:
- Este tutorial foi testado apenas em sistemas Linux com interface GNOME.
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