
from flask import Flask, request, jsonify , render_template , Request , redirect , url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from views import views_bp
import json
import requests
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Establece una clave secreta para la gestión de sesiones
app.register_blueprint(views_bp)

from auth_required import auth_required

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.login'

# Estructuras de datos en memoria para reemplazar la base de datos
usuarios = {}
productos = {}
next_user_id = 1
next_product_id = 1

@login_manager.user_loader
def load_user(user_id):
    return usuarios.get(int(user_id))

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    required_fields = ['nombre', 'razon_social', 'RUC', 'correo', 'numero_contacto', 'contrasena']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    lambda_payload = {
        'correo_admin': data['correo'],
        'contrasena_admin': data['contrasena'],
        'ruc': data['RUC'],
        'razon_social': data['razon_social'],
        'empresa_datos': {
            'nombre': data['nombre'],
            'telefono': int(data['numero_contacto'])
        }
    }

    try:
        lambda_response = requests.post(
            'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/register',
            json=lambda_payload
        )
        lambda_result = lambda_response.json()

        if lambda_response.status_code == 200:
            body = json.loads(lambda_result['body'])
            if body.get('success'):
                token = body.get('token', None)

                # Configurar la respuesta con la cookie HTTPOnly
                response = jsonify({'success': True, 'message': 'Usuario registrado'})
                response.set_cookie(
                    'authToken', token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',  # Evita envíos CSRF
                    max_age=86400  # 24 horas
                )
                return response, 201
            else:
                return jsonify({'success': False, 'message': body.get('message', 'Error en registro')}), 400

        return jsonify({'success': False, 'message': 'Error en la respuesta de Lambda'}), lambda_response.status_code

    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al registrar usuario', 'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    required_fields = ['correo', 'contrasena']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    lambda_payload = {
        'correo_admin': data['correo'],
        'contrasena_proporcionada': data['contrasena']
    }

    try:
        lambda_response = requests.post(
            'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/login',
            json=lambda_payload
        )
        if lambda_response.status_code == 200:
            body = json.loads(lambda_response.json()['body'])
            if body.get('success'):
                token = body.get('token')
                print(token)
                # Configurar la respuesta con la cookie HTTPOnly
                response = jsonify({'success': True, 'message': 'Inicio de sesión exitoso'})
                response.set_cookie(
                    'authToken', token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=86400  # 24 horas
                )
                return response, 200
            else:
                return jsonify({'success': False, 'message': body.get('message', 'Credenciales incorrectas')}), 401

        return jsonify({'success': False, 'message': 'Error en la respuesta de Lambda'}), lambda_response.status_code

    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al iniciar sesión', 'error': str(e)}), 500


@app.route('/publicar-empleo', methods=['POST'])
@auth_required
def publicar_empleo(token):
    try:

        # Obtener datos del frontend
        data = request.json

        # Configurar el payload y los headers para Lambda
        lambda_payload = {
            "empleo_datos": data
        }
        lambda_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Reenviar la solicitud a la API Lambda
        lambda_response = requests.post(
            "https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/crear",
            json=lambda_payload,
            headers=lambda_headers
        )

        # Responder según la respuesta de Lambda
        if lambda_response.status_code == 200:
            return jsonify({"success": True, "message": "Empleo creado exitosamente"}), 200
        else:
            return jsonify({
                "success": False,
                "message": lambda_response.json().get("message", "Error en Lambda")
            }), lambda_response.status_code

    except Exception as e:
        print(f"Error en publicar_empleo: {e}")
        return jsonify({"success": False, "message": "Error interno del servidor"}), 500


@app.route('/api/logout', methods=['POST'])
@auth_required
def logout_user(): 
    pass # Esto se hará después

if __name__ == '__main__':
    app.run(debug=True)

