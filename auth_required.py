from functools import wraps
from flask import Flask, request,jsonify
import requests

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el token desde la cookie (o header)
        token = request.cookies.get('authToken') 
        if not token:
            return jsonify({'success': False, 'message': 'Acceso no autorizado, token no encontrado'}), 401
        
        # Llamar al Lambda para validar el token
        lambda_response = requests.post('https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/validate-token', json={'token': token})
        
        if lambda_response.status_code == 200:
            # Si el token es válido, proceder con la ejecución de la función
            return f(*args, **kwargs)
        else:
            # Si el token es inválido, retornar un error
            return jsonify({'success': False, 'message': 'Token inválido o expirado'}), 401
    
    return decorated_function