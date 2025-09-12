from flask import Flask, jsonify, make_response, request
from flasgger import Swagger

Usuarios = [
    {"id": 1, "nome": "Alice Ferreira", "email": "alice.ferreira@example.com"},
    {"id": 2, "nome": "Bruno Souza", "email": "bruno.souza@example.com"},
    {"id": 3, "nome": "Carla Mendes", "email": "carla.mendes@example.com"},
    {"id": 4, "nome": "Diego Santos", "email": "diego.santos@example.com"},
    {"id": 5, "nome": "Fernanda Lima", "email": "fernanda.lima@example.com"}
]


app = Flask(__name__)

swagger = Swagger(app, template={
    "info": {
        "title": "Minha API Flask",
        "description": "Um exemplo de API usando Flask e Swagger",
        "version": "1.0.0"
    }
}, config={
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
})
app.config['JSON_SORT_KEYS'] = False

@app.route('/users', methods=['GET'])
def get_users():
    """
    Lista todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários cadastrados
        examples:
          application/json: [
            {"id": 1, "nome": "Alice Ferreira", "email": "alice.ferreira@example.com"},
            {"id": 2, "nome": "Bruno Souza", "email": "bruno.souza@example.com"}
          ]
    """
    return make_response(jsonify(Usuarios))

@app.route('/users', methods=['POST'])
def create_users():
    """
    Cria um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do novo usuário
        schema:
          type: object
          required:
            - nome
            - email
          properties:
            nome:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao.silva@example.com
    responses:
      201:
        description: Usuário criado com sucesso
        examples:
          application/json: {"id": 6, "nome": "João da Silva", "email": "joao.silva@example.com"}
      400:
        description: Dados inválidos
    """
    usuarios = request.json
    if "nome" not in usuarios or "email" not in usuarios:
        return make_response(jsonify({"error": "nome e email são obrigatórios"}), 400)

    lista_id = [u['id'] for u in Usuarios]
    current_id = max(lista_id) + 1 if lista_id else 1

    novo_usuario = {
    "id": current_id,
    "nome": usuarios["nome"],
    "email": usuarios["email"]
    }

    Usuarios.append(novo_usuario)
    
    return make_response(jsonify(novo_usuario), 201)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_specific_users(user_id):
    """
    Retorna um usuário específico
    ---
    tags:
      - Usuários
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
        example: 1
    responses:
      200:
        description: Usuário encontrado
        examples:
          application/json: {"id": 1, "nome": "Alice Ferreira", "email": "alice.ferreira@example.com"}
      404:
        description: Usuário não encontrado
    """

    user = next((u for u in Usuarios if u.get('id') == user_id), None)
    if user:
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"error": "Usuário não encontrado"}), 404)
    
@app.route('/users/<int:user_id>', methods=['PUT'])
def uptade_specific_users(user_id):
    """
    Atualiza dados de um usuário específico
    ---
    tags:
      - Usuários
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser atualizado
        example: 2
      - in: body
        name: body
        required: true
        description: Campos permitidos para atualização (nome e/ou email)
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Maria Oliveira
            email:
              type: string
              example: maria.oliveira@example.com
    responses:
      200:
        description: Usuário atualizado com sucesso
        examples:
          application/json: {"id": 2, "nome": "Maria Oliveira", "email": "maria.oliveira@example.com"}
      400:
        description: Campo não permitido ou inválido
      404:
        description: Usuário não encontrado
    """

    user = next((u for u in Usuarios if u.get('id') == user_id), None)
    if user:
        dados = request.get_json()
        permitidos = {"nome", "email"}

        filtrados = {k: v for k,v in dados.items() if k in permitidos}

        if not filtrados:
            return make_response(jsonify({"error": "Campo não permitido para alteração"}), 400)
        
        for chave, valor in filtrados.items():
            user[chave] = valor

        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"error": "Usuário não encontrado"}), 404)
    
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    """
    Exclui um usuário específico
    ---
    tags:
      - Usuários
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser excluído
        example: 3
    responses:
      200:
        description: Usuário excluído com sucesso
        examples:
          application/json: {"message": "O Usuário 3 foi excluído"}
      404:
        description: Usuário não encontrado
    """
    global Usuarios
    user = next((u for u in Usuarios if u.get('id') == user_id), None)
    if user:
        Usuarios = [u for u in Usuarios if u.get('id') != user_id]
        return make_response(jsonify({"message": f"O Usuário {user_id} foi excluído"}), 200)
    else:
        return make_response(jsonify({"error": "Usuário não encontrado"}), 404)

if __name__ == "__main__":
    app.run(debug = True)
