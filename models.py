from database import db
import uuid
import sys
from datetime import datetime
from flask_login import UserMixin

def current_time():
    return datetime.now().strftime('%Y-%m-%d')


class Empresa(UserMixin, db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    correo = db.Column(db.String, unique=True, nullable=False)
    contrasena = db.Column(db.String, nullable=False)
    telefono = db.Column(db.String, nullable=False)
    ruc = db.Column(db.String, nullable=False, unique=True)
    nombre_empresa = db.Column(db.String, nullable=False)
    razon_social = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)

    # Relación con Empleo
    empleos = db.relationship('Empleo', back_populates='empresa')

    def serialize(self):
        return {
            'id': self.id,
            'correo': self.correo,
            'telefono': self.telefono,
            'ruc': self.ruc,
            'nombre_empresa': self.nombre_empresa,
            'razon_social': self.razon_social,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __init__(self, correo, contrasena, telefono, ruc, nombre_empresa, razon_social):
        self.correo = correo
        self.contrasena = contrasena
        self.telefono = telefono
        self.ruc = ruc
        self.nombre_empresa = nombre_empresa
        self.razon_social = razon_social

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            empresa_created_id = self.empresa_id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return empresa_created_id


class Empleo(db.Model):
    __tablename__ = 'empleos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    nombre = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.String, default=current_time)
    fecha_final_postulacion = db.Column(db.String, nullable=False)
    ubicacion = db.Column(db.String, nullable=False)
    salario = db.Column(db.String, nullable=False)  # Puede contener texto, por ejemplo, "A convenir"
    vacantes = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    funciones = db.Column(db.Text, nullable=False)
    beneficios = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text, nullable=False)
    tipo_contrato = db.Column(db.String, nullable=False)  # Ej: "Indefinido", "Temporal"
    modalidad_asistencia = db.Column(db.String, nullable=False)  # Ej: "Presencial", "Remoto"
    empresa_id = db.Column(db.String(36), db.ForeignKey('empresas.id'), nullable=False)

    # Relación con Empresa
    empresa = db.relationship('Empresa', back_populates='empleos')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_creacion': self.fecha_creacion,
            'fecha_final_postulacion': self.fecha_final_postulacion,
            'ubicacion': self.ubicacion,
            'salario': self.salario,
            'vacantes': self.vacantes,
            'descripcion': self.descripcion,
            'funciones': self.funciones,
            'beneficios': self.beneficios,
            'requisitos': self.requisitos,
            'tipo_contrato': self.tipo_contrato,
            'modalidad_asistencia': self.modalidad_asistencia,
            'empresa_id': self.empresa_id
        }

