from flask import Flask, request, jsonify
from database import init_app, db
from config.local import config
from flask import Flask
# flask-login
from flask_login import LoginManager, login_required, current_user
# end flask-login
from datetime import datetime
from models import Empresa, Empleo
from views import views_bp
from empresa_controller import empresas_bp

app = Flask(__name__)
init_app(app)

app.config['SECRET_KEY'] = config['SECRET_KEY']

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.login'

@login_manager.user_loader
def load_user(empresa_id):
    return Empresa.query.get(empresa_id)

# Para la web

app.register_blueprint(views_bp)
app.register_blueprint(empresas_bp)

# Ruta para publicar un empleo
@app.route('/publicar-empleo', methods=['POST'])
@login_required
def publicar_empleo():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        
        # Validar que todos los campos requeridos estén presentes
        required_fields = ['nombre', 'fecha_final_postulacion', 'ubicacion', 'salario', 'vacantes', 'descripcion', 
                           'funciones', 'beneficios', 'requisitos', 'tipo_contrato', 'modalidad_asistencia']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(data)
            return jsonify({
                "success": False,
                "message": f"Faltan los siguientes campos: {', '.join(missing_fields)}"
            }), 400

        # Crear el objeto Empleo con los datos proporcionados
        nuevo_empleo = Empleo(
            nombre=data['nombre'],
            fecha_creacion=datetime.now().isoformat(),
            fecha_final_postulacion=data['fecha_final_postulacion'],
            ubicacion=data['ubicacion'],
            salario=data['salario'],
            vacantes=data['vacantes'],
            descripcion=data['descripcion'],
            funciones=data['funciones'],
            beneficios=data['beneficios'],
            requisitos=data['requisitos'],
            tipo_contrato=data['tipo_contrato'],
            modalidad_asistencia=data['modalidad_asistencia'],
            empresa_id=current_user.id  # La empresa_id proviene del usuario logueado
        )

        # Insertar el nuevo empleo en la base de datos
        db.session.add(nuevo_empleo)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Empleo creado exitosamente",
            "empleo_id": nuevo_empleo.id
        }), 201

    except Exception as e:
        print(f"Error al publicar empleo: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Error interno del servidor"
        }), 500

# Ruta para editar un empleo
@app.route('/empleo/editar', methods=['PATCH'])
@login_required
def editar_empleo():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data_empleos = request.json
        data = data_empleos.get('empleo_datos')
        empleo_id = data_empleos.get('detalle_key')
        if not empleo_id:
            return jsonify({
                "success": False,
                "message": "El campo 'empleo_id' es obligatorio"
            }), 400

        # Buscar el empleo en la base de datos
        empleo = Empleo.query.filter_by(id=empleo_id, empresa_id=current_user.id).first()
        if not empleo:
            return jsonify({
                "success": False,
                "message": "Empleo no encontrado o no autorizado para editar"
            }), 404

        # Actualizar los campos que se proporcionaron en la solicitud
        editable_fields = ['nombre', 'ubicacion', 'salario', 'vacantes', 'descripcion', 
                           'fecha_final']
        for field in editable_fields:
            if field in data:
                setattr(empleo, field, data[field])

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Empleo actualizado exitosamente",
            "empleo_id": empleo.id
        }), 200

    except Exception as e:
        print(f"Error al editar empleo: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Error interno del servidor"
        }), 500

# Ruta para eliminar un empleo
@app.route('/empleo/eliminar', methods=['DELETE'])
@login_required
def eliminar_empleo():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        empleo_id = data.get('detalle_key')
        if not empleo_id:
            return jsonify({
                "success": False,
                "message": "El campo 'empleo_id' es obligatorio"
            }), 400

        # Buscar el empleo en la base de datos
        empleo = Empleo.query.filter_by(id=empleo_id, empresa_id=current_user.id).first()
        if not empleo:
            return jsonify({
                "success": False,
                "message": "Empleo no encontrado o no autorizado para eliminar"
            }), 404

        # Eliminar el empleo de la base de datos
        db.session.delete(empleo)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Empleo eliminado exitosamente"
        }), 200

    except Exception as e:
        print(f"Error al eliminar empleo: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Error interno del servidor"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)


