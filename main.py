from mysql.connector import connect, Error
from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


# Configuração do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/swagger.yaml'    # Caminho do arquivo de configuração do Swagger
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Gestão de alunos'}
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.yaml')
def swagger_yaml():
    return send_from_directory('.', 'swagger.yaml')


# Função para conectar ao banco de dados MySQL
def conectar():
    conexao = connect(
        host='localhost',
        user='root',
        password='mysql1234',
        database='escola',
        auth_plugin='mysql_native_password'
    )
    return conexao


# Rota para adicionar um aluno
@app.route('/alunos/novo', methods=['POST'])
def inserir_aluno():
    cursor = None
    conexao = None
    data = request.json
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
        INSERT INTO alunos (nome, nascimento, notas_primeiro_semestre, notas_segundo_semestre, nome_professor, 
        numero_sala) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (data['nome'], data['nascimento'], data['notas_primeiro_semestre'], data['notas_segundo_semestre'],
              data['nome_professor'], data['numero_sala'])
                       )
        conexao.commit()
        return jsonify({'message': 'Aluno inserido com Sucesso!'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# Rota para listar todos os alunos
@app.route('/alunos/lista', methods=['GET'])
def ler_aluno():
    cursor = None
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM alunos')
        resultados = cursor.fetchall()
        alunos = [{'id': aluno[0],
                   'nome': aluno[1],
                   'nascimento': aluno[2],
                   'notas_primeiro_semestre': aluno[3],
                   'notas_segundo_semestre': aluno[4],
                   'nome_professor': aluno[5],
                   'numero_sala': aluno[6]}
                  for aluno in resultados]
        return jsonify(alunos), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# Rota para atualizar informações de um aluno
@app.route('/alunos/update/<id>', methods=['PUT'])
def atualizar_aluno(id):
    data = request.json
    cursor = None
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
        UPDATE alunos
        SET nome = %s, nascimento = %s, notas_primeiro_semestre = %s, notas_segundo_semestre = %s, nome_professor = %s, 
            numero_sala = %s
        WHERE id = %s
        ''', (data['nome'], data['nascimento'], data['notas_primeiro_semestre'],
              data['notas_segundo_semestre'], data['nome_professor'],
              data['numero_sala'], id))
        conexao.commit()
        return jsonify({'message': 'Aluno atualizado com Sucesso!'}), 200
    except Error as e:
        print(f'Erro ao inserir aluno: {e}')
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f'Erro desconhecido: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# Rota para excluir um aluno
@app.route('/alunos/delete/<id>', methods=['DELETE'])
def excluir_aluno(id):
    cursor = None
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM alunos WHERE id = %s', (id,))
        conexao.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': f'Aluno com o ID {id} excluído com Sucesso'}), 200
        else:
            return jsonify({'error': 'Aluno não encontrado.'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conexao:
            conexao.close()
        if cursor:
            cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
