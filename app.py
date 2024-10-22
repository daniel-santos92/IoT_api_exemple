from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from functools import wraps
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Usar as variáveis de ambiente
API_KEY = os.getenv('API_KEY')
DATABASE_PATH = os.getenv('DATABASE_PATH')

# Função para verificar a chave de API
def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized"}), 401
    return decorated_function

# Rota principal
@app.route('/')
def main():
    return render_template('index.html')

# Rota para CRUD de contatos
@app.route('/contacts', methods=["GET", "POST"])
@require_api_key
def contacts():
    if request.method == "POST":
        # Inserir um novo contato
        if request.json and all(k in request.json for k in ('nome', 'telefone', 'email')):
            nome = request.json.get('nome')
            telefone = request.json.get('telefone')
            email = request.json.get('email')
            return insert_contact(nome, telefone, email)
        else:
            return jsonify({"message": "Dados incompletos"}), 400
    elif request.method == "GET":
        # Buscar todos os contatos
        return select_all_contacts()

@app.route('/contacts/<int:id>', methods=["GET", "PUT", "DELETE"])
@require_api_key
def contact(id):
    if request.method == "GET":
        # Buscar um contato específico por ID
        return select_contact(id)
    elif request.method == "PUT":
        # Atualizar um contato existente
        if request.json and all(k in request.json for k in ('nome', 'telefone', 'email')):
            nome = request.json.get('nome')
            telefone = request.json.get('telefone')
            email = request.json.get('email')
            return update_contact(id, nome, telefone, email)
        else:
            return jsonify({"message": "Dados incompletos"}), 400
    elif request.method == "DELETE":
        # Deletar um contato por ID
        return delete_contact(id)
    
# Rota para busca de contatos por qualquer campo (nome, telefone ou email)
@app.route('/contacts/search', methods=["GET"])
@require_api_key
def search_contacts():
    query = request.args.get('q')
    
    if query:
        conn = sqlite3.connect(DATABASE_PATH)
        curs = conn.cursor()
        search_query = f"%{query}%"
        curs.execute("""
            SELECT id, nome, telefone, email
            FROM contatos
            WHERE nome LIKE ? OR telefone LIKE ? OR email LIKE ?
        """, (search_query, search_query, search_query))
        result = curs.fetchall()
        conn.close()
        
        items = [{'id': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3]} for row in result]
        return jsonify(items)
    else:
        return jsonify({"message": "Parâmetro de busca não fornecido"}), 400

# Funções de banco de dados
def select_all_contacts():
    conn = sqlite3.connect(DATABASE_PATH)
    curs = conn.cursor()
    curs.execute("SELECT id, nome, telefone, email FROM contatos")
    result = curs.fetchall()
    items = [{'id': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3]} for row in result]
    conn.close()
    return jsonify(items)

def select_contact(id):
    conn = sqlite3.connect(DATABASE_PATH)
    curs = conn.cursor()
    curs.execute("SELECT id, nome, telefone, email FROM contatos WHERE id = ?", (id,))
    row = curs.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3]})
    else:
        return jsonify({"message": "Contato não encontrado"}), 404

def insert_contact(nome, telefone, email):
    conn = sqlite3.connect(DATABASE_PATH)
    curs = conn.cursor()
    sql = "INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)"
    val = (nome, telefone, email)
    curs.execute(sql, val)
    conn.commit()
    conn.close()
    return jsonify({"message": "Contato inserido com sucesso!"})

def update_contact(id, nome, telefone, email):
    conn = sqlite3.connect(DATABASE_PATH)
    curs = conn.cursor()
    sql = "UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?"
    val = (nome, telefone, email, id)
    curs.execute(sql, val)
    conn.commit()
    conn.close()
    if curs.rowcount > 0:
        return jsonify({"message": "Contato atualizado com sucesso!"})
    else:
        return jsonify({"message": "Contato não encontrado"}), 404

def delete_contact(id):
    conn = sqlite3.connect(DATABASE_PATH)
    curs = conn.cursor()
    sql = "DELETE FROM contatos WHERE id = ?"
    curs.execute(sql, (id,))
    conn.commit()
    conn.close()
    if curs.rowcount > 0:
        return jsonify({"message": "Contato excluído com sucesso!"})
    else:
        return jsonify({"message": "Contato não encontrado"}), 404

# Configuração do banco de dados SQLite
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    curs = conn.cursor()
    curs.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
