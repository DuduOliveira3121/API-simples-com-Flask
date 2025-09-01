from flask import Flask, jsonify, make_response, request

Usuarios = [
    {"id": 1, "nome": "Alice Ferreira", "email": "alice.ferreira@example.com"},
    {"id": 2, "nome": "Bruno Souza", "email": "bruno.souza@example.com"},
    {"id": 3, "nome": "Carla Mendes", "email": "carla.mendes@example.com"},
    {"id": 4, "nome": "Diego Santos", "email": "diego.santos@example.com"},
    {"id": 5, "nome": "Fernanda Lima", "email": "fernanda.lima@example.com"}
]

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/users', methods=['GET'])
def get_users():
    return make_response(jsonify(Usuarios))

@app.route('/users', methods=['POST'])
def create_users():
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
    user = next((u for u in Usuarios if u.get('id') == user_id), None)
    if user:
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"error": "Usuário não encontrado"}), 404)
    
@app.route('/users/<int:user_id>', methods=['PUT'])
def uptade_specific_users(user_id):
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
    global Usuarios
    user = next((u for u in Usuarios if u.get('id') == user_id), None)
    if user:
        Usuarios = [u for u in Usuarios if u.get('id') != user_id]
        return make_response(jsonify({"message": f"O Usuário {user_id} foi excluído"}), 200)
    else:
        return make_response(jsonify({"error": "Usuário não encontrado"}), 404)


app.run(debug = True)