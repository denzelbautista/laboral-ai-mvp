# views.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from models import Empleo, Empresa

# Crea un Blueprint llamado 'views'
views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def index():
    return render_template("index.html")

@views_bp.route("/register")
def register():
    return render_template("register.html")


@views_bp.route("/login")
def login():
    return render_template("login.html")

# Vista para listar todos los empleos
@views_bp.route("/empleos_listar")
def shop():
    try:
        empleos = Empleo.query.all()  # Obtenemos todos los empleos
        empleos_list = [
            {
                "id": empleo.id,
                "nombre_empleo": empleo.nombre,
                "descripcion": empleo.descripcion,
                "funciones": empleo.funciones,
                "requisitos": empleo.requisitos,
                "beneficios": empleo.beneficios,
                "ubicacion": empleo.ubicacion,
                "fecha_creacion": empleo.fecha_creacion,
                "vacantes": empleo.vacantes,
                "fecha_final": empleo.fecha_final_postulacion,
                "salario": empleo.salario,
                "id": empleo.id,  
                "empresa_id": empleo.empresa_id,
            }
            for empleo in empleos
        ]
        return render_template("shop.html", empleos=empleos_list)
    except Exception as e:
        print(f"Error al listar empleos: {e}")
        return redirect(url_for("views.error"))


# Vista para registro de producto
@views_bp.route("/registroproducto")
@login_required
def registroproducto():
    try:
        empresa_id = current_user.id  # Obtenemos el ID de la empresa del usuario logueado
        empresa = Empresa.query.filter_by(id=empresa_id).first()

        if not empresa:
            return redirect(url_for("views.login"))

        nombre = empresa.nombre_empresa
        iniciales = "".join([n[0].upper() for n in nombre.split() if n])[:2]
        return render_template("registroproducto.html", nombre=nombre, iniciales=iniciales)
    except Exception as e:
        print(f"Error al cargar registro producto: {e}")
        return redirect(url_for("views.error"))


# Vista para el dashboard
@views_bp.route("/dashboard")
@login_required
def dashboard():
    try:
        empresa_id = current_user.id  # Obtenemos el ID de la empresa del usuario logueado
        empresa = Empresa.query.filter_by(id=empresa_id).first()

        if not empresa:
            return redirect(url_for("views.login"))

        empleos = Empleo.query.filter_by(empresa_id=empresa_id).all()  # Filtramos los empleos por empresa_id

        empleos_list = [
            {
                "id": empleo.id,
                "nombre_empleo": empleo.nombre,
                "descripcion": empleo.descripcion,
                "ubicacion": empleo.ubicacion,
                "vacantes": empleo.vacantes,
                "fecha_final": empleo.fecha_final_postulacion,
                "salario": empleo.salario,
            }
            for empleo in empleos
        ]

        nombre = empresa.nombre_empresa
        iniciales = "".join([n[0].upper() for n in nombre.split() if n])[:2]
        return render_template("dashboard.html", nombre=nombre, iniciales=iniciales, empleos=empleos_list)
    except Exception as e:
        print(f"Error al cargar dashboard: {e}")
        return redirect(url_for("views.error"))


# ///////////////////////////////////
@views_bp.route("/carrito")
def carrito():
    return render_template("carrito.html")
