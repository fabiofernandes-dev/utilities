import requests
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

def verify_jwt_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obter o token do cabeçalho de autorização
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
            else:
                return jsonify({"message": "Invalid token format"}), 400
        else:
            return jsonify({"message": "Token is missing"}), 403

        # Enviar o token para o endpoint de verificação
        response = requests.post('http://teste.com/token_info', data={'token': token})
        if response.status_code != 200:
            # Token inválido ou erro ao verificar o token
            return jsonify({"message": "Token is invalid or expired"}), 403

        return f(*args, **kwargs)

    return decorated_function

@app.route('/some-route')
@verify_jwt_token
def some_route():
    return jsonify({"message": "This is a protected route"})

if __name__ == '__main__':
    app.run(debug=True)
