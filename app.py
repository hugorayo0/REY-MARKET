import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import db_helper
import hashlib
import os

app = Flask(__name__)
application = app

app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def inicio():
    return render_template("index.html")

# ───────────────── HISTORIAL ─────────────────
@app.route("/historial")
def historial():
    if not session.get('id_usuario'):
        return redirect(url_for('login'))

    conexion, cursor = db_helper.get_db()

    cursor.execute(
        """
        SELECT 
            p.id_pedido,
            p.fecha_pedido,
            p.precio_total,
            p.estado,
            COUNT(pp.id_producto) AS num_productos
        FROM pedidos p
        LEFT JOIN productos_pedidos pp ON p.id_pedido = pp.id_pedido
        WHERE p.id_usuario = %s
        GROUP BY p.id_pedido
        ORDER BY p.fecha_pedido DESC
        LIMIT 5
        """,
        (session['id_usuario'],)
    )

    pedidos = cursor.fetchall()

    historial = []
    for pedido in pedidos:
        cursor.execute(
            """
            SELECT 
                pr.nombre, 
                pr.url_imagen, 
                pp.cantidad,
                pr.precio_unidad,
                d.descuento,
                CASE 
                    WHEN d.descuento IS NOT NULL 
                    THEN ROUND(pr.precio_unidad * (1 - d.descuento / 100), 2)
                    ELSE pr.precio_unidad
                END AS precio_final
            FROM productos_pedidos pp
            JOIN productos pr ON pp.id_producto = pr.id_producto
            LEFT JOIN descuentos d ON pr.id_descuento = d.id_descuento
            WHERE pp.id_pedido = %s
            """,
            (pedido['id_pedido'],)
        )
        items = cursor.fetchall()
        historial.append({
            'id_pedido':    pedido['id_pedido'],
            'fecha_pedido': pedido['fecha_pedido'],
            'precio_total': pedido['precio_total'],
            'estado':       pedido['estado'],
            'items':        items
        })

    cursor.close()
    conexion.close()

    return render_template("historial.html", historial=historial)


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

    cursor.execute("SELECT * FROM categorias;")
    categorias = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos,
        categorias=categorias
    )


@app.route("/Cuenta")
def cuenta():
    return render_template("cuenta.html")


@app.route("/Contacto", methods=['GET', 'POST'])
def contacto():
    mensaje_ok = False
    error = None

    if request.method == 'POST':
        nombre  = request.form.get('nombre', '').strip()
        email   = request.form.get('email', '').strip()
        mensaje = request.form.get('mensaje', '').strip()

        try:
            msg = MIMEMultipart()
            msg['From']    = 'damibonye@gmail.com'
            msg['To']      = 'damibonye@gmail.com'
            msg['Subject'] = f'Contacto web - {nombre}'
            msg.attach(MIMEText(
                f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}",
                'plain'
            ))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
                servidor.login(
                    'damibonye@gmail.com',
                    os.environ.get('EMAIL_PASSWORD')
                )
                servidor.sendmail(
                    'damibonye@gmail.com',
                    ['damibonye@gmail.com'],
                    msg.as_string()
                )
            mensaje_ok = True

        except Exception as e:
            print("ERROR AL ENVIAR CORREO:", e)
            error = "No se pudo enviar el mensaje. Inténtalo más tarde."

    return render_template("contacto.html", mensaje_ok=mensaje_ok, error=error)



# ───────────────── CARRITO ─────────────────

@app.route("/carrito")
def carrito():

    carrito_session = session.get('carrito', [])

    productos_carrito = []

    subtotal = 0

    conexion, cursor = db_helper.get_db()

    for item in carrito_session:

        cursor.execute("""
            SELECT *
            FROM vista_productos
            WHERE id_producto = %s
        """, (item['id'],))

        producto = cursor.fetchone()

        if not producto:
            continue

        precio = float(producto['precio_unidad'])

        if (
            producto['descuento']
            and producto['estado'] == 'activo'
        ):
            precio = precio * (
                1 - float(producto['descuento']) / 100
            )

        precio = round(precio, 2)

        subtotal_producto = precio * item['cantidad']

        subtotal += subtotal_producto

        productos_carrito.append({
            'id': producto['id_producto'],
            'nombre': producto['nombre'],
            'precio': precio,
            'cantidad': item['cantidad']
        })

    envio = 0 if subtotal >= 30 else 3.99
    total = subtotal + envio

    direcciones = []

    if session.get('id_usuario'):

        cursor.execute(
            "SELECT * FROM direcciones WHERE id_usuario = %s",
            (session['id_usuario'],)
        )

        direcciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "carrito.html",
        carrito=productos_carrito,
        subtotal=subtotal,
        envio=envio,
        total=total,
        direcciones=direcciones
    )


@app.route("/carrito/agregar", methods=['POST'])
def agregar_carrito():

    data = request.get_json()

    id_producto = int(data['id'])

    carrito = session.get('carrito', [])

    encontrado = False

    for item in carrito:
        if item['id'] == id_producto:
            item['cantidad'] += 1
            encontrado = True
            break

    if not encontrado:
        carrito.append({
            'id': id_producto,
            'cantidad': 1
        })

    session['carrito'] = carrito
    session.modified = True

    total_items = sum(i['cantidad'] for i in carrito)

    return jsonify({
        'ok': True,
        'total_items': total_items
    })


@app.route("/carrito/sumar/<int:id>")
def sumar_carrito(id):

    carrito = session.get('carrito', [])

    for item in carrito:
        if item['id'] == id:
            item['cantidad'] += 1
            break

    session['carrito'] = carrito
    session.modified = True

    return redirect(url_for('carrito'))


@app.route("/carrito/restar/<int:id>")
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


@app.route("/carrito/eliminar/<int:id>")
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
    
    conexion, cursor = db_helper.get_db()
    
    subtotal = 0
    
    for item in carrito:
    
        cursor.execute("""
            SELECT *
            FROM vista_productos
            WHERE id_producto = %s
        """, (item['id'],))
    
        producto = cursor.fetchone()
    
        if not producto:
            continue
    
        precio = float(producto['precio_unidad'])
    
        if (
            producto['descuento']
            and producto['estado'] == 'activo'
        ):
            precio = precio * (
                1 - float(producto['descuento']) / 100
            )
    
        subtotal += precio * item['cantidad']
    
    if not carrito:
        return redirect(url_for('productos'))

    

    envio = 0 if subtotal >= 30 else 3.99
    total = subtotal + envio

    conexion, cursor = db_helper.get_db()

    cursor.execute(
        "SELECT * FROM direcciones WHERE id_usuario = %s",
        (session['id_usuario'],)
    )

    direcciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    if request.method == 'POST':

        # ─── EDITAR DIRECCIÓN ───

        id_direccion_editar = request.form.get('id_direccion_editar')

        if id_direccion_editar:

            conexion, cursor = db_helper.get_db()

            try:
                cursor.execute(
                    """
                    UPDATE direcciones
                    SET 
                        nombre_entrega=%s,
                        calle_entrega=%s,
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
                        request.form.get('nombre_entrega', '').strip(),
                        request.form.get('calle_entrega', '').strip(),
                        request.form.get('portal_entrega', '').strip(),
                        request.form.get('piso_entrega', '').strip(),
                        request.form.get('puerta_entrega', '').strip(),
                        request.form.get('localidad_entrega', '').strip(),
                        request.form.get('provincia_entrega', '').strip(),
                        request.form.get('cp_entrega', '').strip(),
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
        
        if id_direccion == 'temporal':
            id_direccion = None
        
        direccion_temporal = session.get('direccion_temporal')

        if id_direccion or direccion_temporal:

            conexion, cursor = db_helper.get_db()

            try:
                cursor.execute(
                    """
                    INSERT INTO pedidos (id_usuario, precio_total, fecha_pedido, estado)
                    VALUES (%s, %s, NOW(), 'pendiente')
                    """,
                    (session['id_usuario'], total)
                )
                conexion.commit()

                id_pedido = cursor.lastrowid

                for item in carrito:
                    cursor.execute(
                        """
                        INSERT INTO productos_pedidos (id_pedido, id_producto, cantidad)
                        VALUES (%s, %s, %s)
                        """,
                        (id_pedido, int(item['id']), int(item['cantidad']))
                    )
                conexion.commit()

                session['carrito'] = []
                session.modified = True
                session['ultimo_pedido'] = id_pedido
                session['pedido_completado'] = True
                session.pop('direccion_temporal', None)
                return redirect(url_for('pago'))

            except Exception as e:
                print("ERROR DETALLADO:", e)
                conexion.rollback()
                return redirect(url_for('carrito'))

            finally:
                cursor.close()
                conexion.close()

        # ─── NUEVA DIRECCIÓN ───

        nombre_entrega = request.form.get('Nombre', '').strip()
        calle = request.form.get('calle_entrega', '').strip()
        portal = request.form.get('portal_entrega', '').strip()
        piso = request.form.get('piso_entrega', '').strip()
        puerta = request.form.get('puerta_entrega', '').strip()
        localidad = request.form.get('localidad_entrega', '').strip()
        provincia = request.form.get('provincia_entrega', '').strip()
        cp = request.form.get('cp_entrega', '').strip()
        informacion = request.form.get('info_opcional_entrega', '').strip()
        guardar = request.form.get('guardar_direccion')

        if not all([calle, portal, piso, puerta, localidad, provincia, cp]):
            return redirect(url_for('carrito'))

        conexion, cursor = db_helper.get_db()

        try:
            if guardar:
                cursor.execute(
                    """
                    INSERT INTO direcciones (id_usuario, nombre_entrega, calle_entrega, portal_entrega,
                        piso_entrega, puerta_entrega, localidad_entrega, provincia_entrega, cp_entrega, info_opcional_entrega)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (session['id_usuario'], nombre_entrega, calle, portal, piso, puerta, localidad, provincia, cp, informacion)
                )
                conexion.commit()

            cursor.execute(
                """
                INSERT INTO pedidos (id_usuario, precio_total, fecha_pedido, estado)
                VALUES (%s, %s, NOW(), 'pendiente')
                """,
                (session['id_usuario'], total)
            )
            conexion.commit()

            id_pedido = cursor.lastrowid

            for item in carrito:
                cursor.execute(
                    """
                    INSERT INTO productos_pedidos (id_pedido, id_producto, cantidad)
                    VALUES (%s, %s, %s)
                    """,
                    (id_pedido, int(item['id']), int(item['cantidad']))
                )
            conexion.commit()

            session['carrito'] = []
            session.modified = True
            session['ultimo_pedido'] = id_pedido
            session['pedido_completado'] = True
            session.pop('direccion_temporal', None)
            return redirect(url_for('pago'))

        except Exception as e:
            print("ERROR DETALLADO:", e)
            conexion.rollback()

            return redirect(url_for('carrito'))

        finally:
            cursor.close()
            conexion.close()

    return redirect(url_for('carrito'))

# Para añadir nueva direccion
@app.route('/direccion/nueva', methods=['POST'])
def nueva_direccion():

    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    nombre = request.form['nombre_entrega']
    calle = request.form['calle_entrega']
    portal = request.form['portal_entrega']
    piso = request.form['piso_entrega']
    puerta = request.form['puerta_entrega']
    localidad = request.form['localidad_entrega']
    provincia = request.form['provincia_entrega']
    cp = request.form['cp_entrega']
    info = request.form.get('info_opcional_entrega')

    guardar = request.form.get('guardar_direccion')

    if guardar:

        conexion, cursor = db_helper.get_db()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO direcciones (
                id_usuario,
                nombre_entrega,
                calle_entrega,
                portal_entrega,
                piso_entrega,
                puerta_entrega,
                localidad_entrega,
                provincia_entrega,
                cp_entrega,
                info_opcional_entrega
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session['id_usuario'],
            nombre,
            calle,
            portal,
            piso,
            puerta,
            localidad,
            provincia,
            cp,
            info
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

    else:

        session['direccion_temporal'] = {
            'nombre': nombre,
            'calle': calle,
            'portal': portal,
            'piso': piso,
            'puerta': puerta,
            'localidad': localidad,
            'provincia': provincia,
            'cp': cp,
            'info': info
        }

    return redirect(url_for('carrito'))

# Para editar una direccion
@app.route('/direccion/editar', methods=['POST'])
def editar_direccion():

    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    id_direccion = request.form['id_direccion_editar']

    conexion, cursor = db_helper.get_db()

    try:
        cursor.execute("""
            UPDATE direcciones
            SET
                nombre_entrega=%s,
                calle_entrega=%s,
                portal_entrega=%s,
                piso_entrega=%s,
                puerta_entrega=%s,
                localidad_entrega=%s,
                provincia_entrega=%s,
                cp_entrega=%s,
                info_opcional_entrega=%s
            WHERE id_direccion=%s
            AND id_usuario=%s
        """, (
            request.form['nombre_entrega'],
            request.form['calle_entrega'],
            request.form['portal_entrega'],
            request.form['piso_entrega'],
            request.form['puerta_entrega'],
            request.form['localidad_entrega'],
            request.form['provincia_entrega'],
            request.form['cp_entrega'],
            request.form.get('info_opcional_entrega'),
            id_direccion,
            session['id_usuario']
        ))
        conexion.commit()

    except Exception as e:
        print("ERROR AL EDITAR DIRECCIÓN:", e)
        conexion.rollback()

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('carrito'))

# ───────────────── PAGO ─────────────────

@app.route("/pago")
def pago():
    if not session.get('id_usuario'):
        return redirect(url_for('login'))
    if not session.pop('pedido_completado', False):
        return redirect(url_for('productos'))

    id_pedido = session.get('ultimo_pedido')

    return render_template("pago.html", id_pedido=id_pedido)


# ───────────────── DIRECCIONES ─────────────────
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
            "DELETE FROM productos WHERE id_producto = %s",
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


@app.route("/admin/producto/anadir", methods=['POST'])
def anadir_producto():

    if not session.get('es_admin'):
        return redirect(url_for('productos'))

    nombre    = request.form.get('nombre', '').strip()
    precio    = request.form.get('precio_unidad')
    unidad    = request.form.get('unidad_medida', '').strip()
    imagen    = request.form.get('url_imagen', '').strip()
    id_cat    = request.form.get('id_categoria')
    descuento = request.form.get('descuento') or None
    fecha_fin = request.form.get('fecha_fin') or None
    estado = request.form.get('estado')

    conexion, cursor = db_helper.get_db()

    try:
        id_descuento = None
        if descuento:
            cursor.execute(
                "INSERT INTO descuentos (descuento, tipo_descuento, fecha_fin) VALUES (%s, 'porcentaje', %s)",
                (descuento, fecha_fin)
            )
            conexion.commit()
            id_descuento = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO productos (nombre, precio_unidad, unidad_medida, url_imagen, id_categoria, id_descuento)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre, precio, unidad, imagen, id_cat, id_descuento)
        )
        conexion.commit()

    except Exception as e:
        print("ERROR AL ANADIR:", e)
        conexion.rollback()

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('productos'))


@app.route("/admin/producto/editar/<int:id>", methods=['POST'])
def editar_producto(id):

    if not session.get('es_admin'):
        return redirect(url_for('productos'))

    nombre    = request.form.get('nombre', '').strip()
    precio    = request.form.get('precio_unidad')
    unidad    = request.form.get('unidad_medida', '').strip()
    imagen    = request.form.get('url_imagen', '').strip()
    categoria = request.form.get('id_categoria')
    descuento = request.form.get('descuento', '').strip()
    fecha_fin = request.form.get('fecha_fin') or None
    estado = request.form.get('estado')

    conexion, cursor = db_helper.get_db()

    try:
        cursor.execute(
            "SELECT id_descuento FROM productos WHERE id_producto = %s", (id,)
        )
        row = cursor.fetchone()
        id_descuento_actual = row['id_descuento'] if row else None

        if descuento and int(descuento) > 0:
            if id_descuento_actual:
                cursor.execute(
                    "UPDATE descuentos SET descuento=%s, fecha_fin=%s, estado=%s WHERE id_descuento=%s",
                    (descuento, fecha_fin, estado, id_descuento_actual)
                )
            else:
                cursor.execute(
                    "INSERT INTO descuentos (descuento, tipo_descuento, fecha_fin) VALUES (%s, 'porcentaje', %s)",
                    (descuento, fecha_fin)
                )
                conexion.commit()
                id_descuento_actual = cursor.lastrowid

        cursor.execute(
            """
            UPDATE productos
            SET nombre=%s, precio_unidad=%s, unidad_medida=%s,
                url_imagen=%s, id_categoria=%s, id_descuento=%s
            WHERE id_producto=%s
            """,
            (nombre, precio, unidad, imagen, categoria, id_descuento_actual, id)
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