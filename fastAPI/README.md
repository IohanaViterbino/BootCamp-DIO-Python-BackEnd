# Projeto com FastAPI

## Visão Geral

Este projeto é uma aplicação FastAPI projetada e adaptada para o desafio de projeto da plataforma [DIO](https://github.com/digitalinnovationone).

## Funcionalidades

- **Operações CRUD para Atletas**: Criar, ler, atualizar e deletar registros de atletas.
- **Gerenciamento de Categorias e Centros de Treinamento**: Vincular atletas às suas respectivas categorias e centros de treinamento.
- **Paginação**: Paginar os resultados de maneira eficiente usando `fastapi_pagination`.
- **Tratamento de Exceções**: Manipular erros de integridade do SQL e outras exceções de forma graciosa.

## Configuração

### Pré-requisitos

- Python 3.12+
- MySQL
- Poetry (para gerenciamento de dependências)

### Instalação

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/IohanaViterbino/BootCamp-DIO-Python-BackEnd
    cd BootCamp-DIO-Python-BackEnd/fastAPI
    ```

2. **Instale as dependências**:
    ```bash
    poetry install
    ```

3. **Configure o Banco de Dados**:
    - Certifique-se de que o MySQL está em execução.
    - Atualize o arquivo `alembic.ini` com os detalhes da conexão do MySQL:
        ```ini
        sqlalchemy.url = mysql+aiomysql://<user>:<password>@localhost/<database_name>
        ```

4. **Execute as Migrações do Banco de Dados**:
    ```bash
    poetry run run-migrations
    ```

### Executando a Aplicação

1. **Inicie o servidor FastAPI**:
    ```bash
    poetry run serv
    ```

2. **Acesse a documentação da API**:
    - Acesse `http://localhost:8000/docs` no seu navegador para visualizar e interagir com a documentação da API gerada automaticamente pelo Swagger UI.

## Estrutura do Projeto

- **atleta**: Contém modelos, esquemas e controladores relacionados aos atletas.
- **categoria**: Contém modelos e esquemas relacionados às categorias.
- **centro_treinamento**: Contém modelos e esquemas relacionados aos centros de treinamento.
- **contrib**: Contém dependências e utilitários compartilhados.
- **alembic**: Diretório de configurações e scripts de migração de banco de dados.


## Licença

[MIT](https://choosealicense.com/licenses/mit/)

