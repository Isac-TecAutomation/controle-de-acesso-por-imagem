# Projeto: Controle de Acesso por Imagem

## Descrição
Este exemplo demonstra como integrar um banco de dados ao projeto para realizar **autenticação** e **registro de usuários** com base em reconhecimento facial. Ele serve como uma base para entender e implementar as funções disponíveis no arquivo `main.py`.

### Funcionalidades principais:
- **Autenticação**: O sistema verifica se a face capturada corresponde a um rosto registrado no banco de dados.
- **Registro de Usuários**: Permite adicionar novos usuários ao banco, armazenando seus dados e imagens faciais para futuras autenticações.

---

## Instalação e Configuração

### 1. Instalação Principal do Projeto
Certifique-se de seguir todas as instruções de instalação do projeto principal. Isso inclui:
- Instalar dependências do Python necessárias para reconhecimento facial e manipulação de banco de dados

- Configurar corretamente os requisitos descritos no projeto.

### 2. Clonando o Repositório do Projeto

Para obter os arquivos do projeto, use o comando abaixo se estiver utilizando Git:

```bash
git clone <URL_DO_REPOSITORIO>
```

- Alternativamente, faça o download direto dos arquivos.

### 3. Configurando o Banco de Dados
Este exemplo utiliza um banco de dados relacional (MySQL) para armazenar os dados dos usuários. A seguir está um modelo de tabela que pode ser usado no seu banco de dados.

#### Estrutura da Tabela (Exemplo)

```sql
CREATE TABLE usuarios (
    nome VARCHAR(100) NOT NULL, -- Nome completo do usuário
    email VARCHAR(255) UNIQUE CHECK (email LIKE '%_@__%.__%'), -- Email único, validado por padrão de formato
    senha VARCHAR(255) CHECK (senha REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'), -- Senha com validação de complexidade
    encoding TEXT NOT NULL, -- Dados de codificação facial para reconhecimento
    PRIMARY KEY (email) -- Email como identificador único do usuário
) ENGINE=InnoDB;
```

### Observações sobre a Tabela:
- **Email**: Deve ser único e seguir um padrão válido de email.
- **Senha**: Deve ter pelo menos 8 caracteres, incluindo um número e um caractere especial.
- **Encoding**: Armazena os dados codificados para reconhecimento facial.

> **Nota:** Você pode personalizar o esquema da tabela conforme as necessidades do seu projeto.

---

### 4. Uso do `main.py`
O arquivo `main.py` contém funções para registro e autenticação de usuários. Siga as instruções abaixo para utilizá-lo:

#### Registro de Usuários
Para registrar um novo usuário:
1. Descomente o código que chama a função `register_user`.
2. Passe os dados do novo usuário no formato de dicionário (dict).
3. Execute o script para realizar o registro no banco de dados.

#### Autenticação de Usuários
Para autenticar um usuário:
1. Defina o valor de `trust` (percentual de confiança).
2. Chame a função `face_verify_database_image` para capturar a imagem e verificar correspondência.
3. A função verificará a correspondência no banco de dados e retornará o resultado.

Exemplo:

```python
trust = 60  # Limite de confiança para autenticação
result, frame = control.face_verify_database_image(trust)
print(result)
```

---

## Execução
Após configurar o banco de dados e ajustar o arquivo `main.py`, inicie o sistema executando o seguinte comando:

```bash
python main.py
```

---

## Recursos Adicionais
- **Banco de Dados Relacional**: MySQL foi utilizado neste exemplo, mas pode ser adaptado para outros SGBDs.
- **Segurança**: Certifique-se de proteger os dados dos usuários, especialmente senhas, utilizando técnicas como hash seguro (ex: bcrypt).

---

Com essas orientações, você está pronto para desenvolver e testar o sistema de controle de acesso por imagem.
