API de Usuários com Flask

Este projeto é uma API simples desenvolvida com o **Framework Flask** para gerenciar usuários.  
A API permite realizar operações básicas de **CRUD** (Create, Read, Update, Delete), sendo útil para estudos e testes de integração.

Endpoints Disponíveis

- **GET /users** → Retorna todos os usuários cadastrados.  
- **POST /users** → Cria um novo usuário (necessário informar `nome` e `email` no corpo da requisição).  
- **GET /users/<id>** → Retorna um usuário específico pelo seu `id`.  
- **PUT /users/<id>** → Atualiza informações de um usuário (campos aceitos: `nome` e `email`).  
- **DELETE /users/<id>** → Remove um usuário pelo seu `id`.  

Testes no Postman

Todos os endpoints foram **testados no Postman**, garantindo o funcionamento correto das requisições.  
Foi possível validar os seguintes pontos:
- Criação de novos usuários enviando JSON no corpo da requisição.  
- Validação de campos obrigatórios (`nome` e `email`).  
- Atualização e exclusão de usuários.  
- Tratamento de erros para IDs inexistentes ou requisições inválidas.  

Como Executar

1. Clone este repositório.  
2. Instale as dependências do Flask:  
   pip install flask
