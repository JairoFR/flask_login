import os
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuario import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")    
    return render_template("dashboard.html", sistema=nombre_sistema)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("index.html")

@app.route('/registrar', methods=['POST'])
def registrar():
    
    if not User.validar(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "usuario": request.form['usuario'],
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    resultado = User.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/")

    flash("Usuario creado correctamente", "success")
    return redirect('/')

@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = User.get_by_email(request.form['identificacion'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['usuario'] = usuario.nombre

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    flash("Vuelve pronto", "success")
    return redirect('/login')