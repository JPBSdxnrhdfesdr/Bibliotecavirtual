from hashlib import algorithms_available

from flask import Flask, jsonify, request
from flask_bcrypt import generate_password_hash
from main import app, con

import threading

import smtplib
from email.mime.text import MIMEtext

import sqlite3

import jwt
import datetime
SECRET_KEY = 'senha_secreta'

@app.route('/livro', methods=['GET'])
def livro():
    try:
        cur = con.cursor()
        cur.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros")
        livros = cur.fetchall():

livros_list = []
for livro in livros:
    livros_list.append({
        'ID_LIVRO': livro[0],
        'titulo': livro[1],
        'autor': livro[2],
        'ano_publicacao': livro[3]
})
return jsonify(
mensagem='Lista de livros',
livros=livros_list
), 200

except Exception as e:
    return jsonify(
    mensagem=f'Erro ao consultar banco de dados: {e}'
    ), 500

def gerar_token(id_usuario):
    payload = {'id_usuario': id_usuario},
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutos=10)
                  }






    token = jwt.encode(playload, senha_secreta, algorithm='HS256')

    return token

def remover _bearer(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]
    else:
        return token

@app.route('/criar_livro', methods=['POST']))
def criar_livro():
try:
    dados = request.get_json()

titulo = dados.get('titulo')
autor = dados.get('autor')
ano_publicacao = dados.get('ano_publicacao')

if not all([titulo, autor, ano_publicacao]):
    return jsonify({'erro': 'Todos os campos são obrigatórios'}), 401
oken = remover_bearer(token)


try:
    payload = jwt.decode(oken, senha_secreta, algorithms=['HS256'])
except jwt.ExpiredSignatureError:
    return jsonify({'message': 'token invalido'}), 401
except jwt.InvalidTokenError:
    return jsonify({'message': 'token invalido'}), 401

cur = con.cursor()

# Verifica se já existe
cur.execute(
"SELECT 1 FROM livro WHERE titulo = %s",
(titulo,)
)
if cur.fetchone():
    return jsonify({'erro': 'Livro já cadastrado'}), 400

# Insere o livro
cur.execute(
"""
INSERT INTO livros (titulo, autor, ano_publicacao)
VALUES (, , ,)
""",
(titulo, autor, ano_publicacao)
)

con.commit()

return jsonify({
 'mensagem': 'Livro cadastrado com sucesso'
 }), 201

except Exception as e:(
    con.rollback())
return jsonify({
'mensagem': f'Erro ao cadastrar livro: {e}'
}), 500


@app.route('/editar_livros/<int:id>', methods=['PUT'])
def editar_livros(id):

cur = con.cursor()
cur.execute("""select id_livro, titulo, autor, ano_publicacao
from livros
where id_livro = ?""", (id))
tem_livro = cur.fetchone()
if not tem_livro:
    cur.close()
    return jsonify({"error": "livro não encontrado"})


data = request.get_json()
TITULO = data.get("titulo")
AUTOR = data.get("autor")
ANO_PUBLICACAO = data.get("ano_publicacao")


cur.execute(""" update livros set titulos = ?, autor = ?, ano_publicacao = ? """, (titulo, autor, ano_publicacao, id))

con.commit()

cur.close()


return jsonify({"message": "livro atualizado com sucesso",
                "livro": {
                    'ID_LIVRO' : ID_LIVRO,
                    'TITULO' : TITULO,
                    'AUTOR' : AUTOR,
                    'ANO_PUBLICACAO' : ANO_PUBLICACAO
                }
                })


@app.route('/deletar_livros/<int:id>', methods=['DELETE'])
def deletar_livros(id):
    cur = con.cursor()
    cur.execute('select 1 from LIVROS where ID_LIVROS = ?', (id,))
    if cur.fetchone():
        cur.close()
        return jsonify({'error': "livro nao encontrado"}), 404

    cur.execute("delete from livros where id_livro = ?", (id,))
    cur.commit()
    cur.close()

    return jsonify({"message": "livro deletado com sucesso",
    'ID_LIVROS' : id} )



@app.route('/cadastro_user', methods=['GET', 'POST'])
def cadastro_user():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT 1 FROM USUARIOS WHERE usuarios.EMAIL = ?', (email,))
        if cursor.fetchone():
            flash('Esse email já está cadastrado')
            return redirect(url_for('index'))
        senha_cripto = generate_password_hash(senha)
        cursor.execute("INSERT INTO USUARIOS(nome, email, senha) VALUES(?, ?, ?)",
                       (nome, email, senha_cripto))

        con.commit()
    finally:
        cursor.close()
    flash('O Usuário Foi Cadastrado Com Sucesso!')
    return redirect(url_for('index'))

@app.route('/relatorio')
def relatorio():
    cursor = con.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicado FROM livros")
    livros = cursor.fetchall()
    cursor.close()


app= Flask(__name__)
app.run(debug=True)






