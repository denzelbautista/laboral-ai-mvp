from flask import Flask, request, jsonify , render_template , Request , redirect , url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from views import views_bp
import json
import requests
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Establece una clave secreta para la gestión de sesiones
app.register_blueprint(views_bp)

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
                print(body)
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
def publicar_empleo():
    try:
        # Obtener token desde la cookie HTTPOnly
        token = request.cookies.get('authToken')
        if not token:
            return jsonify({"success": False, "message": "Token no encontrado en cookies"}), 401

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
@login_required
def logout_user():
    # Cerrar la sesión usando Flask-Login
    logout_user()
    return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'}), 200

@app.route('/nuevo_empleo')
def create_empleo():
    return render_template('registroproducto.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Captura de datos del formulario
    empresa_id = request.form.get("empresa_id") #ahora con token será diferente
    empleo_datos = {
        "nombre_empleo": request.form.get("nombre_empleo"),
        "tipo_contrato": request.form.get("tipo_contrato"),
        "fecha_publicacion": request.form.get("fecha_publicacion"),
        "fecha_final": request.form.get("fecha_final"),
        "modalidad": request.form.get("modalidad"),
        "ubicacion": request.form.get("ubicacion"),
        "salario_min": int(request.form.get("salario_min")),
        "salario_max": int(request.form.get("salario_max")),
        "experiencia": request.form.get("experiencia"),
        "vacantes": int(request.form.get("vacantes")),
        "descripcion": request.form.get("descripcion"),
        "funciones": request.form.get("funciones").split(","),
        "requisitos": request.form.get("requisitos").split(","),
        "beneficios": request.form.get("beneficios").split(","),
        "nivel_estudios": request.form.get("nivel_estudios")
    }

    data = {
        "empresa_id": empresa_id,
        "empleo_datos": empleo_datos
    }

    # Enviar datos a la API externa
    api_url = "https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/crear"
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=data, headers=headers)

    # Mostrar la respuesta de la API
    if response.status_code == 200:
        return redirect(url_for('views.empleos_listar'))
    else:
        return jsonify({"status": "error", "message": "Error al enviar los datos", "details": response.text}), response.status_code


@app.route('/empleos', methods=['GET'])
def empleos():
    empresa_id = "c2bea60b-48b6-48c8-8b23-92e1f688a5b2"
    api_url = "https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/listarporempresa"
    headers = {"Content-Type": "application/json"}
    data = {"empresa_id": empresa_id}


    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        empleos_data = response.json().get('body', '[]')
        empleos = json.loads(empleos_data)
    else:
        empleos = []
    return render_template('dashboard.html', empleos=empleos)

if __name__ == '__main__':
    app.run(debug=True)

