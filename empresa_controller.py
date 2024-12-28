# empresas_controller.py
from flask import Blueprint, abort, request, jsonify
import requests
from database import init_app, db
from config.local import config
from models import Empresa
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Crea un Blueprint llamado 'empresas'
empresas_bp = Blueprint('empresas', __name__)

# Crear una nueva empresa
@empresas_bp.route('/empresas', methods=['POST'])
def create_empresa():
    list_errors = []
    returned_code = 201
    try:
        data = request.json

        # Validar los campos requeridos
        for field in ['correo', 'contrasena', 'numero_contacto', 'ruc', 'nombre_empresa', 'razon_social']:
            if field not in data:
                list_errors.append(f'{field} es requerido')

        if 'correo' in data:
            correo = data['correo']
            if Empresa.query.filter_by(correo=correo).first():
                list_errors.append('El correo ya está registrado')

        if len(list_errors) > 0:
            print(list_errors)
            returned_code = 400
        else:
            # Crear una nueva empresa
            nueva_empresa = Empresa(
                correo=data['correo'],
                contrasena= data['contrasena'],
                telefono=data['numero_contacto'],
                ruc=data['ruc'],
                nombre_empresa=data['nombre_empresa'],
                razon_social=data['razon_social']
            )
            db.session.add(nueva_empresa)
            db.session.commit()

            # Loguear automáticamente
            login_user(nueva_empresa)

            return jsonify({
                'success': True,
                'message': 'Empresa registrada exitosamente'
            }), 201

    except Exception as e:
        print('Error: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': list_errors,
            'message': 'Error creando una nueva empresa'
        }), 400
    elif returned_code != 201:
        print(data)
        return jsonify({
            'success': False,
            'message': 'Error inesperado'
        }), 500



# Iniciar sesión
@empresas_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        if not correo or not contrasena:
            print(data)
            return jsonify({'success': False, 'message': 'Correo y contraseña son requeridos'}), 400

        empresa = Empresa.query.filter_by(correo=correo).first()

        if empresa and (empresa.contrasena == contrasena):
            login_user(empresa)
            return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

    except Exception as e:
        print('Error: ', e)
        return jsonify({'success': False, 'message': 'Error en el servidor'}), 500


# Cerrar sesión
@empresas_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'}), 200


# Obtener perfil de la empresa actual
@empresas_bp.route('/empresas', methods=['GET'])
@login_required
def get_current_empresa():
    empresa = current_user

    if not empresa:
        return jsonify({'error': 'Empresa no encontrada'}), 404

    return jsonify({
        'success': True,
        'empresa': {
            'empresa_id': empresa.empresa_id,
            'correo': empresa.correo,
            'telefono': empresa.telefono,
            'ruc': empresa.ruc,
            'nombre_empresa': empresa.nombre_empresa,
            'razon_social': empresa.razon_social
        }
    }), 200


# Actualizar información de la empresa
@empresas_bp.route('/empresas', methods=['PATCH'])
@login_required
def update_empresa():
    empresa = current_user
    if not empresa:
        return jsonify({'error': 'No autorizado para editar este perfil'}), 403

    data = request.form

    # Actualizar los campos editables
    empresa.telefono = data.get('telefono', empresa.telefono)
    empresa.nombre_empresa = data.get('nombre_empresa', empresa.nombre_empresa)
    empresa.razon_social = data.get('razon_social', empresa.razon_social)

    # Manejar la subida de la imagen de perfil (opcional)
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                data={'key': '2adc25aee373fb46c2d721f17defe3d4'},  # Reemplaza con tu clave de API de imgBB
                files={'image': file}
            )
            if response.status_code == 200:
                image_url = response.json()['data']['url']
                empresa.imagen_empresa = image_url
            else:
                return jsonify({'success': False, 'message': 'Error subiendo imagen a imgbb'}), 500

    try:
        db.session.commit()
        return jsonify({'message': 'Información actualizada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error actualizando información'}), 500


# Ruta protegida de ejemplo
@empresas_bp.route('/protected')
@login_required
def protected_route():
    return jsonify({'message': f'Hola, empresa {current_user.empresa_id}!'}), 200
