from functools import wraps
from flask import Flask, request,jsonify, redirect, url_for
import requests

import json
from functools import wraps
from flask import request, redirect, url_for

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el token desde las cookies
        token = request.cookies.get('authToken')
        if not token:
            print("No hay token en las cookies. Redirigiendo al login.")
            return redirect(url_for('views.login'))

        # Llamar al Lambda para validar el token
        lambda_response = requests.post(
            'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/validate-token',
            json={'token': token}
        )
        
        if lambda_response.status_code == 200:
            try:
                # Decodificar la respuesta completa
                response_data = lambda_response.json()
                
                # Decodificar el campo 'body' que está como string
                body = json.loads(response_data.get('body', '{}'))
                
                if body.get('success'):
                    # Token válido, actualizar el token
                    new_token = body.get('token')
                    kwargs['token'] = new_token
                    return f(*args, **kwargs)
                else:
                    print("Token inválido según Lambda. Redirigiendo al login.")
                    return redirect(url_for('views.login'))
            except Exception as e:
                print(f"Error al procesar la respuesta del Lambda: {e}")
                return redirect(url_for('views.login'))
        else:
            print("Error en la validación del token. Redirigiendo al login.")
            return redirect(url_for('views.login'))
    
    return decorated_function

