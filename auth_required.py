import json
from functools import wraps
from flask import request, redirect, url_for, make_response
import requests

# URL del Lambda para validar el token
LAMBDA_VALIDATE_TOKEN_URL = 'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/validate-token'

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el token desde las cookies
        token = request.cookies.get('authToken')
        if not token:
            print("[Auth] No hay token en las cookies. Redirigiendo al login.")
            return redirect(url_for('views.login'))

        try:
            # Llamar al Lambda para validar el token
            lambda_response = requests.post(
                LAMBDA_VALIDATE_TOKEN_URL,
                json={"body": json.dumps({"token": token})},  # Empaquetar el token como string JSON dentro del campo "body"
                timeout=5  # Limitar el tiempo de espera para evitar bloqueos
            )

            # Procesar la respuesta del Lambda
            if lambda_response.status_code == 200:
                response_data = lambda_response.json()
                
                # Deserializar el campo 'body' (que es una cadena JSON)
                body = json.loads(response_data.get('body', '{}'))  # Decodificar el campo 'body'

                if body.get('success'):
                    new_token = body.get('token')

                    if new_token:
                        kwargs['token'] = new_token
                        response.set_cookie('authToken', new_token, httponly=True)
                        return f(*args, **kwargs)

                    else:
                        kwargs['token'] = token
                        return f(*args, **kwargs)
                else:
                    print("[Auth] Token inválido según Lambda. Redirigiendo al login.")
            else:
                print(f"[Auth] Error en Lambda: {lambda_response.status_code} {lambda_response.text}")

        
        except Exception as e:
            print("Response de lambda en exception de [Auth] ", body)
            print(f"[Auth] Error al conectar con Lambda: {e}")
            
            # Eliminar la cookie si el token no es válido o hay errores
            response = make_response(redirect(url_for('views.login')))
            response.delete_cookie('authToken')
            return response
    
    return decorated_function
