
# Agenda de Contatos - API Flask

Este projeto é uma **API** desenvolvida com **Flask** para gerenciar uma agenda de contatos. A aplicação permite **criar**, **editar**, **listar** e **excluir** contatos através de requisições **HTTP** (CRUD), e também inclui uma interface web simples para gerenciar os contatos.

## Funcionalidades

- Adicionar novos contatos com nome, telefone e email.
- Listar todos os contatos.
- Editar contatos existentes.
- Excluir contatos.
- Interface web para facilitar a gestão.
- Autenticação por chave de API.

## Tecnologias Utilizadas

- **Python** (Flask)
- **SQLite** (Banco de Dados)
- **Bootstrap** (Interface Web)
- **Font Awesome** (Ícones)
- **JavaScript** (Fetch API para consumir as rotas)

## Instalação e Configuração

Siga os passos abaixo para rodar o projeto localmente:

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv
```

Ative o ambiente virtual:

- No Windows:
  ```bash
  venv\Scripts\activate
  ```

- No Linux/MacOS:
  ```bash
  source venv/bin/activate
  ```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Crie o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```
DATABASE_PATH=/caminho/para/database.db
API_KEY=sua-chave-secreta-aqui
```

### 5. Inicialize o Banco de Dados

Antes de rodar a aplicação, inicialize o banco de dados com as tabelas necessárias:

```bash
python
```

Dentro do shell Python, execute:

```python
from app import init_db
init_db()
exit()
```

### 6. Rode a Aplicação

Para rodar a aplicação Flask localmente:

```bash
flask run
```

A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Uso da API

A API é protegida por uma chave de API. Adicione a chave no cabeçalho `x-api-key` para consumir as rotas.

### Listar todos os contatos

```
GET /contacts
```

Exemplo de requisição usando **cURL**:

```bash
curl -X GET http://127.0.0.1:5000/contacts -H "x-api-key: sua-chave-api"
```

### Adicionar um novo contato

```
POST /contacts
```

Body da requisição (JSON):

```json
{
  "nome": "João Silva",
  "telefone": "123456789",
  "email": "joao@example.com"
}
```

### Editar um contato existente

```
PUT /contacts/<id>
```

Body da requisição (JSON):

```json
{
  "nome": "João Silva",
  "telefone": "987654321",
  "email": "joao_novo@example.com"
}
```

### Excluir um contato

```
DELETE /contacts/<id>
```

## Interface Web

A aplicação também inclui uma interface web simples. Acesse a interface em `http://127.0.0.1:5000/` para gerenciar os contatos visualmente.

## Rotas Disponíveis

Para listar todas as rotas disponíveis no projeto, use o comando:

```bash
flask routes
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma **issue** ou enviar um **pull request** com melhorias.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
