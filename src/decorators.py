from typing import Callable
from flask import session, flash, redirect, url_for,current_app,request,jsonify
import functools
import os
from src import app

def requires_admin(f: Callable) -> Callable:
    print(os.environ.get('ADMIN'))
    @functools.wraps(f)
    def decorated_function(*args,**kwargs):
        try:
            print(session['username'])
        except KeyError:
            flash('Necesitas estar logueado y con las credenciales correspondientes','info')
            return redirect(url_for('users.login'))
        if session['username'] != os.environ.get('ADMIN'):
            flash('Necesitas ser el administrador para ingresar aqui','danger')
            return redirect(url_for('users.login'))
        return f(*args,**kwargs)
    return decorated_function

api_pass = ''
def protected(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == app.config.get('ADMIN', '') and auth.password == api_pass:
            return f(*args, **kwargs)
        return jsonify({"message": "Authentication failed, capo"}), 401
    return decorated_function

