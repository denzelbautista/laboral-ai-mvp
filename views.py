# views.py
import json

import requests
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

# Crea un Blueprint llamado 'views'
views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    return render_template("index.html")


@views_bp.route("/empleos_listar")
def shop():
    response = requests.post(
        "https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/listartodos",
        json={},
    )

    if response.status_code == 200:

        body = response.json().get("body")
        if body:
            empleos = json.loads(body)

        else:
            empleos = []
    else:
        empleos = []
        print("Error en la API:", response.status_code)

    return render_template("shop.html", empleos=empleos)


@views_bp.route("/contact")
def contact():
    return render_template("contact.html")


@views_bp.route("/comprar")
def sell():
    return render_template("comprar.html")


@views_bp.route("/carrito")
def carrito():
    return render_template("carrito.html")


@views_bp.route("/register")
def register():
    return render_template("register.html")


@views_bp.route("/login")
def login():
    return render_template("login.html")


@views_bp.route("/detallesproducto")
def detallesproducto():
    product_id = request.args.get("id")
    return render_template("detallesproducto.html", product_id=product_id)


@views_bp.route("/editarproducto")
def editarproducto():
    product_id = request.args.get("id")
    return render_template("editarproducto.html", product_id=product_id)


@views_bp.route("/registroproducto")
def registroproducto():
    return render_template("registroproducto.html")


@views_bp.route("/misproductos")
def misproductos():
    return render_template("misproductos.html")


@views_bp.route("/profile")
def profile():
    return render_template("profile.html")


@views_bp.route("/dashboard")

def dashboard():
    token = request.cookies.get('authToken')
    print("dash", token)
    if not token:
        return redirect(url_for('views.login'))

    headers = {'Authorization': f'Bearer {token}'}
    api_url = "https://7yvvp7f7s5.execute-api.us-east-1.amazonaws.com/prod/empresa/detalles"
    response = requests.get(api_url, headers=headers)

    if response.status_code != 200 or not response.json().get('success'):
        return redirect(url_for('views.login'))

    user_data = response.json().get('data', {})
    nombre = user_data.get('empresa_datos', {}).get('nombre', 'Usuario')

    iniciales = ''.join([n[0].upper() for n in nombre.split() if n])[:2]

    return render_template('dashboard_base.html', iniciales=iniciales, nombre=nombre)



@views_bp.route("/detallesempleo")
def detallesempleo():
    return render_template("detallesempleo.html")
