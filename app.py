from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import mysql.connector
import db_helper
import hashlib
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")




@app.route("/")
def inicio():
    return redirect(url_for("Pagina_Principal"))

@app.route("/Pagina_Principal")
def Pagina_Principal():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_usuario = request.form.get('email','').strip()
        pwd_hash = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()[:200]
        
        conexion, cursor = db_helper.get_db()

        SQL = ""

        cursor.execute(SQL, [correo_usuario])

        usuario = cursor.fetchone()

        if usuario is not None and pwd_hash == usuario["contraseña"]:
            session["id_usuario"] = usuario["id_usuario"]
            session["tipo_usuario"] = usuario["tipo_usuario"] # Nos sirve para saber que la persona que esta accediendo es cliente o administrador(el Rol del usuario)
            session["correo"] = usuario["correo"]   
            return redirect(url_for("productos"))
        
    return render_template("login.html")
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template("registro.html")
    nombre  = request.form.get('Nombre', '').strip()
    apellido1 = request.form.get('Apellido1', '').strip()
    apellido2 = request.form.get('Apellido2', '').strip()   # minúscula, igual que el HTML
    email  = request.form.get('email', '').strip()
    password  = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    if not nombre or not email or not apellido1 or not apellido2 or not password:
        return render_template('registro.html', error='Rellena todos los campos obligatorios')
    if password != password2:
        return render_template('registro.html', error='Las contraseñas no coinciden')

    pwd_hash = hashlib.sha256(password.encode()).hexdigest()

    conexion, cursor = db_helper.get_db()
    cursor.execute("SELECT id_usuario FROM USUARIO WHERE email = %s", (email,))
    if cursor.fetchone():
        return render_template('registro.html', error='Ese email ya está en uso.')


    cursor.execute(
       
        "INSERT INTO usuarios (nombre, apellido1, apellido2, email, contraseña) "
        "VALUES (%s, %s, %s, %s, %s)",
        (nombre, apellido1, apellido2, email, pwd_hash)
        
    )
    conexion.commit()
    return redirect(url_for("login"))
    
@app.route("/productos", methods=['GET', 'POST'])
def productos():

    conexion, cursor = db_helper.get_db()

    SQL = f"""
        SELECT * FROM vista_productos;
    """

    cursor.execute(SQL)
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()
    
    return render_template("productos.html", productos=productos)

@app.route("/ofertas")
def ofertas():
    return render_template("ofertas.html")

@app.route("/Cuenta")
def cuenta():
    return render_template("cuenta.html")

@app.route("/Contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/carrito")
def carrito():
    carrito = session.get('carrito', [])
    subtotal = sum(i['precio'] * i['cantidad'] for i in carrito)
    envio = 0 if subtotal >= 30 else 3.99
    total = subtotal + envio
    return render_template("carrito.html", carrito=carrito, subtotal=subtotal, envio=envio, total=total)

@app.route("/carrito/agregar", methods=['POST'])
def agregar_carrito():
    from flask import jsonify
    data = request.get_json()
    nombre = data['nombre']
    precio = data['precio']

    carrito = session.get('carrito', [])

    for item in carrito:
        if item['nombre'] == nombre:
            item['cantidad'] += 1
            break
    else:
        carrito.append({'id': nombre, 'nombre': nombre, 'precio': precio, 'cantidad': 1})

    session['carrito'] = carrito
    session.modified = True

    # Esto suma UNIDADES, no líneas
    total_items = sum(i['cantidad'] for i in carrito)
    return jsonify({'ok': True, 'total_items': total_items})

@app.route("/carrito/sumar/<id>")
def sumar_carrito(id):
    carrito = session.get('carrito', [])
    for item in carrito:
        if item['id'] == id:
            item['cantidad'] += 1
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('carrito'))

@app.route("/carrito/restar/<id>")
def restar_carrito(id):
    carrito = session.get('carrito', [])
    for item in carrito:
        if item['id'] == id:
            item['cantidad'] -= 1
            if item['cantidad'] <= 0:
                carrito.remove(item)
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('carrito'))

@app.route("/carrito/eliminar/<id>")
def eliminar_carrito(id):
    carrito = session.get('carrito', [])
    session['carrito'] = [i for i in carrito if i['id'] != id]
    session.modified = True
    return redirect(url_for('carrito'))
    
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.context_processor
def inject_carrito():
    carrito = session.get('carrito', [])
    total_items = sum(i['cantidad'] for i in carrito)
    return dict(total_items_carrito=total_items)

if __name__ == "__main__":
    app.run(debug=True)