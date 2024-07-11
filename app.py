from flask import Flask, render_template, request, redirect, url_for, send_from_directory


import os

import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    miResultado = cursor.fetchall()

    insertarObjetos = [] 
    nombreDeColumnas = [columna[0] for columna in cursor.description]
    
    for unRegistro in miResultado:
        insertarObjetos.append(dict(zip(nombreDeColumnas, unRegistro)))

        cursor.close()




    return render_template('index.html', data=insertarObjetos)

@app.route('/user', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    email = request.form['email']
    cel = request.form['cel']
    pinturas = request.form['pinturas']
    color = request.form['color']

    if nombre and apellido and dni and email and cel and pinturas and color:
        cursor = db.database.cursor()
        sql = "INSERT INTO usuarios (nombre, apellido, dni, email, cel, pinturas, color) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (nombre, apellido, dni, email, cel, pinturas, color)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/editar/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    email = request.form['email']
    cel = request.form['cel']
    pinturas = request.form['pinturas']
    color = request.form['color']

    if nombre and apellido and dni and email and cel and pinturas and color:
        cursor = db.database.cursor()
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, dni = %s, email = %s, cel = %s, pinturas = %s, color = %s WHERE id = %s"
        data = (nombre, apellido, dni, email, cel, pinturas, color, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.run(debug=True, port=4000)

