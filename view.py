from flask import Flask ,jsonify, request
from main import app, con

@app.route('/livros', methods=['GET'])
def livros():
    try:
        cur = con.cursor()
        cur.execute("SELECT id_livros, titulo, autor, ano_publicacao FROM livros")
        livros = cur.fetchall()
        livros_list = []
        for livro in livros:
            livros_list.append({
                'id_livros': livro[0],
                'titulo': livro[1],
                'autor': livro[2],
                'ano_publicacao': livro[3]
            })
        return jsonify(mensagem='Lista de Livros', livros=livros_list)
    except Exception as e:
        return jsonify(mensagem=f'Erro ao buscar livros: {e}'), 500
    finally:
        cur.close









@app.route('/adicionar_livros', methods=['POST'])
def adicionar_livros():
    try:
        dados = request.get_json()
        titulo = dados.get('titulo')
        autor = dados.get('autor')
        ano_publicacao = dados.get('ano_publicacao')
        cur = con.cursor()
        cur.execute("select 1 from livros where titulo = ?" , (titulo,))
        if cur.fetchone():
            return jsonify({"error=Livro já existe!"}), 400
        cur.execute("insert into livros (titulo, autor, ano_publicacao) values (?, ?, ?)", (titulo, autor, ano_publicacao))
        con.commit()
        return jsonify({
            'mensagem': 'Livro adicionado com sucesso!',
            'livro ': {
                'titulo': titulo,
                'autor': autor,
                'ano_publicacao': ano_publicacao
            }
        }), 201
    except Exception as e:
        return jsonify(mensagem=f'Erro ao adicionar livro: {e}'), 500
    finally:
        cur.close()