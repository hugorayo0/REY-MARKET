from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import mysql.connector
import db_helper
import hashlib
import os

app = Flask(__name__)
application = app

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def inicio():
    return redirect(url_for("Pagina_Principal"))


@app.route("/Pagina_Principal")
def Pagina_Principal():
    return render_template("index.html")


# ───────────────── LOGIN ─────────────────

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        correo_usuario = request.form.get('email', '').strip()
        pwd_hash = hashlib.sha256(
            request.form.get('password', '').encode()
        ).hexdigest()

        conexion, cursor = db_helper.get_db()

        cursor.execute(
            """
            SELECT id_usuario, nombre, correo, contraseña, tipo_usuario
            FROM usuarios
            WHERE correo = %s
            """,
            [correo_usuario]
        )

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario is not None and pwd_hash == usuario["contraseña"]:

            session["id_usuario"] = usuario["id_usuario"]
            session["tipo_usuario"] = usuario["tipo_usuario"]
            session["correo"] = usuario["correo"]
            session["nombre"] = usuario["nombre"]
            session["es_admin"] = (
                usuario["tipo_usuario"] == "administrador"
            )

            return redirect(url_for("productos"))

        return render_template(
            "login.html",
            error="Correo o contraseña incorrectos"
        )

    return render_template("login.html")


# ───────────────── REGISTRO ─────────────────

@app.route("/registro", methods=['GET', 'POST'])
def registro():

    if request.method == 'GET':
        return render_template("registro.html")

    nombre = request.form.get('Nombre', '').strip()
    apellido1 = request.form.get('Apellido1', '').strip()
    apellido2 = request.form.get('Apellido2', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    if not nombre or not email or not apellido1 or not apellido2 or not password:
        return render_template(
            'registro.html',
            error='Rellena todos los campos obligatorios'
        )

    if password != password2:
        return render_template(
            'registro.html',
            error='Las contraseñas no coinciden'
        )

    pwd_hash = hashlib.sha256(password.encode()).hexdigest()

    conexion, cursor = db_helper.get_db()

    try:

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE correo = %s",
            (email,)
        )

        if cursor.fetchone():
            return render_template(
                'registro.html',
                error='Ese email ya está en uso.'
            )

        cursor.execute(
            """
            INSERT INTO usuarios
            (nombre, apellido1, apellido2, correo, contraseña)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre, apellido1, apellido2, email, pwd_hash)
        )

        conexion.commit()

    except Exception as e:

        print("ERROR AL INSERTAR:", e)
        conexion.rollback()

        return render_template(
            'registro.html',
            error=f'Error: {e}'
        )

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ───────────────── PRODUCTOS ─────────────────

@app.route("/productos", methods=['GET', 'POST'])
def productos():

    conexion, cursor = db_helper.get_db()

    cursor.execute("SELECT * FROM vista_productos;")

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


@app.route("/ofertas")
def ofertas():
    return render_template("ofertas.html")


@app.route("/Cuenta")
def cuenta():
    return render_template("cuenta.html")


@app.route("/Contacto")
def contacto():
    return render_template("contacto.html")


# ───────────────── CARRITO ─────────────────

@app.route("/carrito")
def carrito():

    carrito = session.get('carrito', [])

    subtotal = sum(
        float(i['precio']) * int(i['cantidad'])
        for i in carrito
    )

    envio = 0 if subtotal >= 30 else 3.99

    total = subtotal + envio

    direcciones = []

    if session.get('id_usuario'):

        conexion, cursor = db_helper.get_db()

        cursor.execute(
            """
            SELECT *
            FROM direcciones
            WHERE id_usuario = %s
            """,
            (session['id_usuario'],)
        )

        direcciones = cursor.fetchall()

        cursor.close()
        conexion.close()

    return render_template(
        "carrito.html",
        carrito=carrito,
        subtotal=subtotal,
        envio=envio,
        total=total,
        direcciones=direcciones
    )


@app.route("/carrito/agregar", methods=['POST'])
def agregar_carrito():

    data = request.get_json()

    id = data['id']
    nombre = data['nombre']
    precio = data['precio']

    carrito = session.get('carrito', [])

    for item in carrito:

        if item['id'] == id:
            item['cantidad'] += 1
            break

    else:

        carrito.append({
            'id': id,
            'nombre': nombre,
            'precio': precio,
            'cantidad': 1
        })

    session['carrito'] = carrito
    session.modified = True

    total_items = sum(i['cantidad'] for i in carrito)

    return jsonify({
        'ok': True,
        'total_items': total_items
    })


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

    session['carrito'] = [
        i for i in carrito if i['id'] != id
    ]

    session.modified = True

    return redirect(url_for('carrito'))


# ───────────────── CHECKOUT ─────────────────

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():

    if session.get("id_usuario") is None:
        return redirect(url_for("login"))

    carrito = session.get('carrito', [])

    if not carrito:
        return redirect(url_for('productos'))

    subtotal = sum(
        float(i['precio']) * int(i['cantidad'])
        for i in carrito
    )

    envio = 0 if subtotal >= 30 else 3.99
    total = subtotal + envio

    conexion, cursor = db_helper.get_db()

    cursor.execute(
        """
        SELECT *
        FROM direcciones
        WHERE id_usuario = %s
        """,
        (session['id_usuario'],)
    )

    direcciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    if request.method == 'POST':

        # ─── EDITAR DIRECCIÓN ───

        id_direccion_editar = request.form.get(
            'id_direccion_editar'
        )

        if id_direccion_editar:

            calle = request.form.get(
                'calle_entrega', ''
            ).strip()

            portal = request.form.get(
                'portal_entrega', ''
            ).strip()

            piso = request.form.get(
                'piso_entrega', ''
            ).strip()

            puerta = request.form.get(
                'puerta_entrega', ''
            ).strip()

            localidad = request.form.get(
                'localidad_entrega', ''
            ).strip()

            provincia = request.form.get(
                'provincia_entrega', ''
            ).strip()

            cp = request.form.get(
                'cp_entrega', ''
            ).strip()

            conexion, cursor = db_helper.get_db()

            try:

                cursor.execute(
                    """
                    UPDATE direcciones
                    SET calle_entrega=%s,
                        portal_entrega=%s,
                        piso_entrega=%s,
                        puerta_entrega=%s,
                        localidad_entrega=%s,
                        provincia_entrega=%s,
                        cp_entrega=%s
                    WHERE id_direccion=%s
                    AND id_usuario=%s
                    """,
                    (
                        calle,
                        portal,
                        piso,
                        puerta,
                        localidad,
                        provincia,
                        cp,
                        id_direccion_editar,
                        session['id_usuario']
                    )
                )

                conexion.commit()

            except Exception as e:

                print("ERROR AL EDITAR DIRECCIÓN:", e)
                conexion.rollback()

            finally:

                cursor.close()
                conexion.close()

            return redirect(url_for('carrito'))

        # ─── USAR DIRECCIÓN GUARDADA ───

        id_direccion = request.form.get('id_direccion')

        if id_direccion:

            conexion, cursor = db_helper.get_db()

            try:

                cursor.execute(
                    """
                    CALL insertar_pedido(%s, %s, @id_pedido)
                    """,
                    (session['id_usuario'], total)
                )

                conexion.commit()

                cursor.execute(
                    "SELECT @id_pedido AS id_pedido"
                )

                id_pedido = cursor.fetchone()['id_pedido']

                for item in carrito:

                    cursor.execute(
                        """
                        CALL insertar_producto_pedido(%s, %s)
                        """,
                        (id_pedido, item['id'])
                    )

                conexion.commit()

                session['carrito'] = []
                session.modified = True

                return redirect(url_for('pago'))

            except Exception as e:

                print("ERROR DETALLADO:", e)

                conexion.rollback()

                return redirect(url_for('carrito'))

            finally:

                cursor.close()
                conexion.close()

        # ─── NUEVA DIRECCIÓN ───

        nombre_entrega = request.form.get(
            'Nombre', ''
        ).strip()

        calle = request.form.get(
            'calle_entrega', ''
        ).strip()

        portal = request.form.get(
            'portal_entrega', ''
        ).strip()

        piso = request.form.get(
            'piso_entrega', ''
        ).strip()

        puerta = request.form.get(
            'puerta_entrega', ''
        ).strip()

        localidad = request.form.get(
            'localidad_entrega', ''
        ).strip()

        provincia = request.form.get(
            'provincia_entrega', ''
        ).strip()

        cp = request.form.get(
            'cp_entrega', ''
        ).strip()

        informacion = request.form.get(
            'info_opcional_entrega', ''
        ).strip()

        guardar = request.form.get(
            'guardar_direccion'
        )

        if not all([
            calle,
            portal,
            piso,
            puerta,
            localidad,
            provincia,
            cp
        ]):

            return render_template(
                "checkout.html",
                carrito=carrito,
                subtotal=subtotal,
                envio=envio,
                total=total,
                direcciones=direcciones,
                error="Por favor, rellena todos los campos obligatorios."
            )

        conexion, cursor = db_helper.get_db()

        try:

            if guardar:

                cursor.execute(
                    """
                    CALL insertar_direccion(
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        session['id_usuario'],
                        nombre_entrega,
                        calle,
                        portal,
                        piso,
                        puerta,
                        localidad,
                        provincia,
                        cp,
                        informacion
                    )
                )

                conexion.commit()

            cursor.execute(
                """
                CALL insertar_pedido(%s, %s, @id_pedido)
                """,
                (session['id_usuario'], total)
            )

            conexion.commit()

            cursor.execute(
                "SELECT @id_pedido AS id_pedido"
            )

            id_pedido = cursor.fetchone()['id_pedido']

            for item in carrito:

                cursor.execute(
                    """
                    CALL insertar_producto_pedido(%s, %s)
                    """,
                    (id_pedido, item['id'])
                )

            conexion.commit()

            session['carrito'] = []
            session.modified = True

            return redirect(url_for('pago'))

        except Exception as e:

            print("ERROR DETALLADO:", e)

            conexion.rollback()

            return render_template(
                "checkout.html",
                carrito=carrito,
                subtotal=subtotal,
                envio=envio,
                total=total,
                direcciones=direcciones,
                error=f"Error: {e}"
            )

        finally:

            cursor.close()
            conexion.close()

    return render_template(
        "checkout.html",
        carrito=carrito,
        subtotal=subtotal,
        envio=envio,
        total=total,
        direcciones=direcciones
    )


# ───────────────── PAGO ─────────────────

@app.route("/pago")
def pago():
    return render_template("pago.html")


# ───────────────── DIRECCIONES ─────────────────

@app.route("/direccion/editar/<int:id_direccion>", methods=['GET'])
def editar_direccion_form(id_direccion):

    if not session.get('id_usuario'):
        return redirect(url_for('login'))

    conexion, cursor = db_helper.get_db()

    cursor.execute(
        """
        SELECT *
        FROM direcciones
        WHERE id_direccion=%s
        AND id_usuario=%s
        """,
        (id_direccion, session['id_usuario'])
    )

    direccion = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not direccion:
        return redirect(url_for('carrito'))

    carrito = session.get('carrito', [])

    subtotal = sum(
        float(i['precio']) * int(i['cantidad'])
        for i in carrito
    )

    envio = 0 if subtotal >= 30 else 3.99
    total = subtotal + envio

    conexion, cursor = db_helper.get_db()

    cursor.execute(
        """
        SELECT *
        FROM direcciones
        WHERE id_usuario=%s
        """,
        (session['id_usuario'],)
    )

    direcciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "checkout.html",
        carrito=carrito,
        subtotal=subtotal,
        envio=envio,
        total=total,
        direcciones=direcciones,
        editar_direccion=direccion
    )


@app.route("/direccion/eliminar/<int:id_direccion>")
def eliminar_direccion(id_direccion):

    if not session.get('id_usuario'):
        return redirect(url_for('login'))

    conexion, cursor = db_helper.get_db()

    try:

        cursor.execute(
            """
            DELETE FROM direcciones
            WHERE id_direccion=%s
            AND id_usuario=%s
            """,
            (id_direccion, session['id_usuario'])
        )

        conexion.commit()

    except Exception as e:

        print("ERROR AL ELIMINAR DIRECCIÓN:", e)

        conexion.rollback()

    finally:

        cursor.close()
        conexion.close()

    return redirect(url_for('carrito'))


# ───────────────── ADMIN ─────────────────

@app.route("/admin/producto/eliminar/<int:id>", methods=['POST'])
def eliminar_producto(id):

    if not session.get('es_admin'):
        return redirect(url_for('productos'))

    conexion, cursor = db_helper.get_db()

    try:

        cursor.execute(
            """
            DELETE FROM productos
            WHERE id_producto = %s
            """,
            (id,)
        )

        conexion.commit()

    except Exception as e:

        print("ERROR AL ELIMINAR:", e)

        conexion.rollback()

    finally:

        cursor.close()
        conexion.close()

    return redirect(url_for('productos'))


@app.route("/admin/producto/editar/<int:id>", methods=['POST'])
def editar_producto(id):

    if not session.get('es_admin'):
        return redirect(url_for('productos'))

    nombre = request.form.get('nombre', '').strip()
    precio = request.form.get('precio_unidad')
    unidad = request.form.get('unidad_medida', '').strip()
    imagen = request.form.get('url_imagen', '').strip()

    conexion, cursor = db_helper.get_db()

    try:

        cursor.execute(
            """
            UPDATE productos
            SET nombre=%s,
                precio_unidad=%s,
                unidad_medida=%s,
                url_imagen=%s
            WHERE id_producto=%s
            """,
            (
                nombre,
                precio,
                unidad,
                imagen,
                id
            )
        )

        conexion.commit()

    except Exception as e:

        print("ERROR AL EDITAR:", e)

        conexion.rollback()

    finally:

        cursor.close()
        conexion.close()

    return redirect(url_for('productos'))


# ───────────────── CONTEXT ─────────────────

@app.context_processor
def inject_carrito():

    carrito = session.get('carrito', [])

    total_items = sum(
        i['cantidad'] for i in carrito
    )

    return dict(
        total_items_carrito=total_items
    )


# ───────────────── MAIN ─────────────────

if __name__ == "__main__":
    app.run(debug=True)