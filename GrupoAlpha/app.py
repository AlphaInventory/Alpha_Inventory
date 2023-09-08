from flask import Flask, render_template, request, redirect, session, flash

from flaskext.mysql import MySQL

from datetime import datetime

from flask_mail import Mail, Message

app=Flask(__name__)

mail = Mail(app)

app.secret_key="grupoalpha"

mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='alphainventory'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'grupoalpha.infotep@gmail.com'
app.config['MAIL_PASSWORD'] = 'qmasvsogjgbpavqz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql.init_app(app)

diariosCompra_filtro = 0
diariosVenta_filtro = 0
mArticuloCompras_filtro = 0
mArticuloVentas_filtro = 0
articulo_filtro = 0
precio_filtro = 0
compra_filtro = 0
venta_filtro = 0
cliente_filtro = 0
suplidor_filtro = 0

#SITIO
@app.route('/')
def index():
    return render_template('sitio/index.html')

# INDEX-INICIO DE SESION
@app.route('/', methods=['post'])
def index_inicio_sesion():

    correo_electronico=request.form['email']
    contrasena=request.form['password']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT id_usuario, correo_electronico, contrasena FROM `registro_usuario` WHERE correo_electronico = %s AND contrasena = %s", (correo_electronico, contrasena))
    registro_usuario=bdsql.fetchone()

    if not registro_usuario:
        flash("El correo electronico o la contraseña son incorrectos")
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT correo_electronico FROM `metodo_pago` WHERE correo_electronico=%s", (correo_electronico))
    usuarioM=bdsql.fetchall()

    if not usuarioM:
        return redirect('/metododepago')
    if registro_usuario:
        session['logueado'] = True
        session['id_usuario'] = list(str(registro_usuario[0]))
        return redirect('/inicio_inventario')
    else:
        return redirect('/')
    
# CERRAR SESION
@app.route('/cerrar_sesion')
def index_salir():
    session.clear()
    return redirect('/')

# INICIO INVENTARIO
@app.route('/inicio_inventario')
def inicio_inventario():

    if not 'logueado' in session:
        return redirect('/')
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    usuario=bdsql.fetchone()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()
    
    return render_template('sitio/inicio_inventario.html', usuario=usuario, marcas=marcas, encargado_ventas=encargado_ventas,encargado_compras=encargado_compras)

# INICIO INVENTARIO - CREADOR DE MARCAS 
@app.route('/inicio_inventario/marcas/bd', methods=['post'])
def inicio_inventario_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s,%s)")

    datos_marcas=(codigo_marca, nombre_marca,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/inicio_inventario')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/inicio_inventario')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/inicio_inventario')

# INICIO INVENTARIO - CREADOR ENCARGADO DE VENTAS
@app.route('/inicio_inventario/encVentas/bd', methods=['post'])
def inicio_inventario_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`, `id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas,nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/inicio_inventario')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/inicio_inventario')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/inicio_inventario')

# INICIO INVENTARIO - CREADOR DE ENCARGADO DE COMPRAS
@app.route('/inicio_inventario/encCompras/bd', methods=['post'])
def inicio_inventario_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/inicio_inventario')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/inicio_inventario')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/inicio_inventario')

# INICIO INVENTARIO - ELIMINAR CUENTA
@app.route('/inicio_inventario/eliminar_cuenta/bd', methods=['post'])
def inicio_inventario_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# MOVIMIENTOS DIARIO | COMPRAS 
@app.route('/movimientosdiariocompras')
def movimiento_diariocompras():

    if not 'logueado' in session:
        return redirect('/')   

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*costo) FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    costo_total=bdsql.fetchone()

    costo_total = costo_total[0]

    return render_template ('sitio/movimientosdiariocompras.html', compras=compras, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, costo_total=costo_total, diariosCompra_filtro=diariosCompra_filtro)

# MOVIMIENTOS DIARIO | COMPRAS - (FILTRO)
@app.route('/movimientosdiariocompras/filtrobd', methods=['post'])
def movimientosdiariocompras_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/movimientosdiariocompras')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    diariosCompras_filtro=bdsql.fetchall()

    global diariosCompra_filtro
    diariosCompra_filtro = diariosCompras_filtro

    return redirect('/movimientosdiariocompras')

# MOOVIMIENTOS DIARIO | COMPRAS - (REINICIAR FILTRO)
@app.route('/movimientosdiariocompras', methods=['get','post'])
def movimientosdiariocompras_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*costo) FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    costo_total=bdsql.fetchone()

    costo_total = costo_total[0]

    return render_template('sitio/movimientosdiariocompras.html', compras=compras, costo_total=costo_total)

# MOVIMIENTOS DIARIO | COMPRAS - CREADOR MARCAS
@app.route('/movimientosdiariocompras/marcas/bd', methods=['post'])
def movimientosdiariocompras_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/movimientosdiariocompras')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/movimientosdiariocompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/movimientosdiariocompras')

# MOVIMIENTOS DIARIO | COMPRAS - CREADOR ENCARGADO DE VENTAS
@app.route('/movimientosdiariocompras/encVentas/bd', methods=['post'])
def movimientosdiariocompras_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/movimientosdiariocompras')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/movimientosdiariocompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/movimientosdiariocompras')

# MOVIMIENTOS DIARIO | COMPRA - CREADOR ENCARGADO DE COMPRAS
@app.route('/movimientosdiariocompras/encCompras/bd', methods=['post'])
def movimientosdiariocompras_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/movimientosdiariocompras')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/movimientosdiariocompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/movimientosdiariocompras')

# MOVIMIENTOS DIARIO | COMPRAS - ELIMINAR CUENTA
@app.route('/movimientosdiariocompras/eliminar_cuenta/bd', methods=['post'])
def movimientosdiariocompras_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# MOVIMIENTOS DIARIO | VENTAS
@app.route('/movimientosdiarioventas')
def movimiento_diarioventas():

    if not 'logueado' in session:
        return redirect('/')   

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*costo) FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    costo_total=bdsql.fetchone()

    costo_total = costo_total[0]

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*precio) FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    precio_total=bdsql.fetchone()

    precio_total = precio_total[0]

    return render_template ('sitio/movimientosdiarioventas.html', ventas=ventas, compras=compras, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, costo_total=costo_total, precio_total=precio_total, diariosVenta_filtro=diariosVenta_filtro)

# MOVIMIENTOS DIARIO | VENTAS - (FILTRO)
@app.route('/movimientosdiarioventas/filtrobd', methods=['post'])
def movimientosdiarioventas_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/movimientosdiarioventas')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    diariosVentas_filtro=bdsql.fetchall()

    global diariosVenta_filtro
    diariosVenta_filtro = diariosVentas_filtro

    return redirect('/movimientosdiarioventas')

# MOVIMIENTOS DIARIO | VENTAS (REINICIAR FILTRO)
@app.route('/movimientosdiarioventas', methods=['get','post'])
def movimientosdiarioventas_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*precio) FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    precio_total=bdsql.fetchone()

    precio_total = precio_total[0]

    return render_template('sitio/movimientosdiarioventas.html', ventas=ventas, precio_total=precio_total)

# MOVIMIENTOS DIARIO | VENTA - CREADOR MARCAS
@app.route('/movimientosdiarioventas/marcas/bd', methods=['post'])
def movimientosdiarioventas_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/movimientosdiarioventas')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/movimientosdiarioventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/movimientosdiarioventas')

# MOVIMIENTOS DIARIO | VENTAS - CREADOR ENCARGADO DE VENTAS
@app.route('/movimientosdiarioventas/encVentas/bd', methods=['post'])
def movimientosdiarioventas_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/movimientosdiarioventas')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/movimientosdiarioventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/movimientosdiarioventas')

# MOVIMIENTOS DIARIO | VENTAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/movimientosdiarioventas/encCompras/bd', methods=['post'])
def movimientosdiarioventas_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/movimientosdiarioventas')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/movimientosdiarioventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/movimientosdiarioventas')

# MOVIMIENTOS DIARIO | VENTAS - ELIMINAR CUENTA
@app.route('/movimientosdiarioventas/eliminar_cuenta/bd', methods=['post'])
def movimientosdiarioventas_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# MOVIMEINTO POR ARTICULO | COMPRAS
@app.route('/movimientoporarticulocompras')
def movimiento_articulo_compras():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template ('sitio/movimientoporarticulocompras.html', compras=compras, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, mArticuloCompras_filtro=mArticuloCompras_filtro)

# MOVIMEINTO POR ARTICULO | COMPRAS - (FILTRO)
@app.route('/movimientoporarticulocompras/filtrobd', methods=['post'])
def movimientoporarticulocompras_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/movimientoporarticulocompras')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    mArticulosCompras_filtro=bdsql.fetchall()

    global mArticuloCompras_filtro
    mArticuloCompras_filtro = mArticulosCompras_filtro

    return redirect('/movimientoporarticulocompras')

# MOVIMEINTO POR ARTICULO | COMPRAS - (REINICIAR FILTRO)
@app.route('/movimientoporarticulocompras', methods=['get','post'])
def movimientoporarticulocompras_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    return render_template('sitio/movimientoporarticulocompras.html', compras=compras)

# MOVIMEINTO POR ARTICULO | COMPRAS - CREADOR MARCAS
@app.route('/movimientoporarticulocompras/marcas/bd', methods=['post'])
def movimientoporarticulocompras_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/movimientoporarticulocompras')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/movimientoporarticulocompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/movimientoporarticulocompras')

# # MOVIMEINTO POR ARTICULO | COMPRAS - CREADOR ENCARGADO DE VENTAS
@app.route('/movimientoporarticulocompras/encVentas/bd', methods=['post'])
def movimientoporarticulocompras_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/movimientoporarticulocompras')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/movimientoporarticulocompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/movimientoporarticulocompras')

# MOVIMEINTO POR ARTICULO | COMPRAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/movimientoporarticulocompras/encCompras/bd', methods=['post'])
def movimientoporarticulocompras_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/movimientoporarticulocompras')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/movimientoporarticulocompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/movimientoporarticulocompras')

# MOVIMEINTO POR ARTICULO | COMPRAS - ELIMINAR CUENTA
@app.route('/movimientoporarticulocompras/eliminar_cuenta/bd', methods=['post'])
def movimientoporarticulocompras_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# MOVIMEINTO POR ARTICULO | VENTAS
@app.route('/movimientoporarticuloventas')
def movimiento_articulo_ventas():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template ('sitio/movimientoporarticuloventas.html', ventas=ventas, compras=compras, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, mArticuloVentas_filtro=mArticuloVentas_filtro)

# MOVIMEINTO POR ARTICULO | VENTAS - (FILTRO)
@app.route('/movimientoporarticuloventas/filtrobd', methods=['post'])
def movimientoporarticuloventas_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/movimientoporarticuloventas')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    mArticulosVenta_filtro=bdsql.fetchall()

    global mArticuloVentas_filtro
    mArticuloVentas_filtro = mArticulosVenta_filtro

    return redirect('/movimientoporarticuloventas')

# MOVIMEINTO POR ARTICULO | VENTAS - (REINICIAR FILTRO)
@app.route('/movimientoporarticuloventas', methods=['get','post'])
def movimientoporarticuloventas_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    return render_template('sitio/movimientoporarticuloventas.html', ventas=ventas)

# MOVIMEINTO POR ARTICULO | VENTAS - CREADOR MARCAS
@app.route('/movimientoporarticuloventas/marcas/bd', methods=['post'])
def movimientoporarticuloventas_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/movimientoporarticuloventas')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/movimientoporarticuloventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/movimientoporarticuloventas')

# MOVIMEINTO POR ARTICULO | VENTAS - CREADOR ENCARGADO DE VENTAS
@app.route('/movimientoporarticuloventas/encVentas/bd', methods=['post'])
def movimientoporarticuloventas_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/movimientoporarticuloventas')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/movimientoporarticuloventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/movimientoporarticuloventas')

# MOVIMEINTO POR ARTICULO | VENTAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/movimientoporarticulo/encCompras/bd', methods=['post'])
def movimientoporarticuloventas_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/movimientoporarticuloventas')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/movimientoporarticuloventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/movimientoporarticuloventas')

# MOVIMEINTO POR ARTICULO | VENTAS - ELIMINAR CUENTA
@app.route('/movimientoporarticuloventas/eliminar_cuenta/bd', methods=['post'])
def movimientoporarticuloventas_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# LISTADO DE ARTICULOS
@app.route('/listadodearticulos')
def listadodearticulos():

    if not 'logueado' in session:
        return redirect('/')
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    articulos=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*precio) FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    precio_total_articulos=bdsql.fetchone()

    precio_total_articulos = (precio_total_articulos[0])

    global articulo_filtro

    return render_template('sitio/listadodearticulos.html', articulos=articulos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, precio_total_articulos=precio_total_articulos, articulo_filtro=articulo_filtro)

# LISTADO DE ARTICULOS - (FILTRO)
@app.route('/listadodearticulos/filtrobd', methods=['post'])
def listado_articulos_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/listadodearticulos')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    articulos_filtro=bdsql.fetchall()

    global articulo_filtro
    articulo_filtro =articulos_filtro

    return redirect('/listadodearticulos')

# LISTADO DE ARTICULOS - (REINICIAR FILTRO)
@app.route('/listadodearticulos', methods=['get','post'])
def listadodearticulos_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    articulos=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*precio) FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    precio_total_articulos=bdsql.fetchone()

    precio_total_articulos = (precio_total_articulos[0])

    return render_template('sitio/listadodearticulos.html', articulos=articulos, precio_total_articulos=precio_total_articulos)

# LISTADO DE ARTICULOS - CREADOR MARCAS
@app.route('/listadodearticulos/marcas/bd', methods=['post'])
def listadodearticulos_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/listadodearticulos')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/listadodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/listadodearticulos')

# LISTADO DE ARTICULOS - CREADOR ENCARGADO DE VENTAS
@app.route('/listadodearticulos/encVentas/bd', methods=['post'])
def listadodearticulos_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/listadodearticulos')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/listadodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/listadodearticulos')

# LISTADO DE ARTICULOS - CREADOR ENCARGADO DE COMPRAS
@app.route('/listadodearticulos/encCompras/bd', methods=['post'])
def listadodearticulos_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/listadodearticulos')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/listadodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/listadodearticulos')
    
# LISTADO DE ARTICULOS - ELIMINAR ARTICULO    
@app.route('/listadodearticulos/eliminar/bd', methods=['post'])
def listadodearticulos_eliminar_bd():

    id_articulo=request.form['id_articulo']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_articulo=%s",(id_articulo))
    articulos=bdsql.fetchall()
    bd.commit()
    print(articulos)

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT cantidad FROM `articulos` WHERE id_articulo=%s",(id_articulo))
    cantidad=bdsql.fetchone()

    cantidad = cantidad[0]

    if cantidad != 0:
        flash("No puedes eliminar este articulos porque todavia hay disponibles")
        return redirect('/listadodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute("DELETE FROM `articulos` WHERE id_articulo=%s",(id_articulo))
        bd.commit()

        return redirect('/listadodearticulos')

# LISTADO DE ARTICULOS - ELIMINAR CUENTA
@app.route('/listadodearticulos/eliminar_cuenta/bd', methods=['post'])
def listadodearticulos_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# LISTADO DE PRECIOS
@app.route('/listadodeprecios')
def listado_precios():

    if not 'logueado' in session:
        return redirect('/')
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    precios=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    global precio_filtro

    return render_template('sitio/listadodeprecios.html', articulos=precios, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, precio_filtro=precio_filtro)

# LISTADO DE PRECIOS - (FILTRO)
@app.route('/listadodeprecios/filtrobd', methods=['post'])
def listado_precios_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/listadodeprecios')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    precios_filtro=bdsql.fetchall()

    global precio_filtro
    precio_filtro =precios_filtro

    return redirect('/listadodeprecios')

# LISTADO DE PRECIOS - (REINICIAR FILTRO)
@app.route('/listadodeprecios', methods=['get','post'])
def listadodeprecios_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    articulos=bdsql.fetchall()

    return render_template('sitio/listadodeprecios.html', articulos=articulos)

# LISTADO DE PRECIOS - CREADOR MARCAS
@app.route('/listadodeprecios/marcas/bd', methods=['post'])
def listadodeprecios_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/listadodeprecios')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/listadodeprecios')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/listadodeprecios')

# LISTADO DE PRECIOS - CREADOR ENCARGADO DE VENTAS
@app.route('/listadodeprecios/encVentas/bd', methods=['post'])
def listadodeprecios_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/listadodeprecios')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/listadodeprecios')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/listadodeprecios')

# LISTADO DE PRECIOS - CREADOR ENCARGADO DE COMPRAS
@app.route('/listadodeprecios/encCompras/bd', methods=['post'])
def listadodeprecios_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/listadodeprecios')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/listadodeprecios')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/listadodeprecios')

# LISTADO DE PRECIOS - ELIMINAR CUENTA
@app.route('/listadodeprecios/eliminar_cuenta/bd', methods=['post'])
def listadodeprecios_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# LISTADO DE COMPRAS
@app.route('/listadodecompras')
def listado_compras():

    if not 'logueado' in session:
        return redirect('/')
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_usuario=%s",(session['id_usuario']))
    suplidores=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*costo) FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    costo_total=bdsql.fetchone()

    costo_total = costo_total[0]

    global compra_filtro

    return render_template('sitio/listadodecompras.html', compras=compras, suplidores=suplidores, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, costo_total=costo_total, compra_filtro=compra_filtro)

# LISTADO DE COMPRAS - (FILTRO)
@app.route('/listadodecompras/filtrobd', methods=['post'])
def listado_compras_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/listadodecompras')
    else:
        bdsql=mysql.connect().cursor()
        bdsql.execute("SELECT * FROM `compras` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
        compras_filtro=bdsql.fetchall()

        global compra_filtro
        compra_filtro = compras_filtro

        return redirect('/listadodecompras')

# LISTADO DE COMPRAS - (REINICIAR FILTRO)
@app.route('/listadodecompras', methods=['get','post'])
def listadodecompras_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*costo) FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    costo_total=bdsql.fetchone()

    costo_total = costo_total[0]

    return render_template('sitio/listadodecompras.html', compras=compras, costo_total=costo_total)

# LISTADO DE COMPRAS - CREADOR MARCAS
@app.route('/listadodecompras/marcas/bd', methods=['post'])
def listadodecompras_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/listadodecompras')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/listadodecompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/listadodecompras')

# LISTADO DE COMPRAS - CREADOR ENCARGADO DE VENTAS
@app.route('/listadodecompras/encVentas/bd', methods=['post'])
def listadodecompras_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/listadodecompras')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/listadodecompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/listadodecompras')

# LISTADO DE COMPRAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/listadodecompras/encCompras/bd', methods=['post'])
def listadodecompras_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/listadodecompras')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/listadodecompras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/listadodecompras')

# LISTADO DE COMPRAS - ELIMINAR CUENTA
@app.route('/listadodecompras/eliminar_cuenta/bd', methods=['post'])
def listadodecompras_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# LISTADO DE VENTAS
@app.route('/listadodeventas')
def listado_ventas():

    if not 'logueado' in session:
        return redirect('/')
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_usuario=%s",(session['id_usuario']))
    clientes=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*precio) FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    precio_total=bdsql.fetchone()

    precio_total = precio_total[0]

    global venta_filtro

    return render_template('sitio/listadodeventas.html', ventas=ventas, clientes=clientes, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, precio_total=precio_total, venta_filtro=venta_filtro)

# LISTADO DE VENTAS - (FILTRO)
@app.route('/listadodeventas/filtrobd', methods=['post'])
def listado_ventas_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/listadodeventas')
    else:
        bdsql=mysql.connect().cursor()
        bdsql.execute("SELECT * FROM `ventas` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
        ventas_filtro=bdsql.fetchall()

        global venta_filtro
        venta_filtro =ventas_filtro

        return redirect('/listadodeventas')

# LISTADO DE VENTAS - (REINICIAR FILTRO)
@app.route('/listadodeventas', methods=['get','post'])
def listadodeventas_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT SUM(cantidad*precio) FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    precio_total=bdsql.fetchone()

    precio_total = precio_total[0]

    return render_template('sitio/listadodeventas.html', ventas=ventas, precio_total=precio_total)

# LISTADO DE VENTAS - CREADOR MARCAS
@app.route('/listadodeventas/marcas/bd', methods=['post'])
def listadodeventas_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/registrodearticulos')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/registrodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/listadodeventas')

# LISTADO DE VENTAS - CREADOR ENCARGADO DE VENTAS
@app.route('/listadodeventas/encVentas/bd', methods=['post'])
def listadodeventas_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/listadodeventas')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/listadodeventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/listadodeventas')

# LISTADO DE VENTAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/listadodeventas/encCompras/bd', methods=['post'])
def listadodeventas_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/listadodeventas')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/listadodeventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/listadodeventas')

# LISTADO DE VENTAS - ELIMINAR CUENTA
@app.route('/listadodeventas/eliminar_cuenta/bd', methods=['post'])
def listadodeventas_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# LISTADO DE CLIENTES
@app.route('/listadodeclientes')
def listado_clientes():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_usuario=%s",(session['id_usuario']))
    clientes=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    global cliente_filtro
    
    return render_template('sitio/listadodeclientes.html', clientes=clientes, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, cliente_filtro=compra_filtro)

# LISTADO DE CLIENTES - (FILTRO)
@app.route('/listadodeclientes/filtrobd', methods=['post'])
def listado_clientes_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/listadodeclientes')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    clientes_filtro=bdsql.fetchall()

    global cliente_filtro
    cliente_filtro = clientes_filtro

    return redirect('/listadodeclientes')

# LISTADO DE CLIENTES - (REINICIAR FILTRO)
@app.route('/listadodeclientes', methods=['get','post'])
def listadodeclientes_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_usuario=%s",(session['id_usuario']))
    clientes=bdsql.fetchall()

    return render_template('sitio/listadodeclientes.html', clientes=clientes)

# LISTADO DE CLIENTES - CREADOR MARCAS
@app.route('/listadodeclientes/marcas/bd', methods=['post'])
def listadodeclientes_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/listadodeclientes')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/listadodeclientes')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/listadodeclientes')

# LISTADO DE CLIENTES - CREADOR ENCARGADO DE VENTAS
@app.route('/listadodeclientes/encVentas/bd', methods=['post'])
def listadodeclientes_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/listadodeclientes')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/listadodeclientes')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/listadodeclientes')

# LISTADO DE CLIENTES - CREADOR ENCARGADO DE COMPRAS
@app.route('/listadodeclientes/encCompras/bd', methods=['post'])
def listadodeclientes_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/listadodeclientes')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/listadodeclientes')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/listadodeclientes')

# LISTADO DE CLIENTES - ELIMINAR CLIENTE
@app.route('/listadodeclientes/eliminar/bd', methods=['post'])
def listadodeclientes_eliminar_bd():

    id_cliente=request.form['id_cliente']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_cliente=%s",(id_cliente))
    clientes=bdsql.fetchall()
    bd.commit()
    print(clientes)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `clientes` WHERE id_cliente=%s",(id_cliente))
    bd.commit()

    return redirect('/listadodeclientes')

# LISTADO DE CLIENTES - ELIMINAR CUENTA
@app.route('/listadodeclientes/eliminar_cuenta/bd', methods=['post'])
def listadodeclientes_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# LISTADO DE SUPLIDORES
@app.route('/listadodesuplidores')
def listado_suplidores():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_usuario=%s",(session['id_usuario']))
    suplidores=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    global suplidor_filtro

    return render_template('sitio/listadodesuplidores.html', suplidores=suplidores, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, suplidor_filtro=suplidor_filtro)

# LISTADO DE SUPLIDORES - (FILTRO)
@app.route('/listadodesuplidores/filtrobd', methods=['post'])
def listado_suplidores_filtrobd():

    codigo_desde=request.form['des-codigo']
    codigo_hasta=request.form['has-codigo']

    if (codigo_desde and codigo_hasta) == "":
        return redirect('/listadodesuplidores')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE codigo BETWEEN {0} AND {1}".format(codigo_desde, codigo_hasta))
    suplidores_filtro=bdsql.fetchall()

    global suplidor_filtro
    suplidor_filtro =suplidores_filtro

    return redirect('/listadodesuplidores')

# LISTADO DE SUPLIDORES - (REINICIAR FILTRO)
@app.route('/listadodesuplidores', methods=['get','post'])
def listadodesuplidores_reiniciar():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_usuario=%s",(session['id_usuario']))
    suplidores=bdsql.fetchall()

    return render_template('sitio/listadodesuplidores.html', suplidores=suplidores)

# LISTADO DE SUPLIDORES - CREADOR MARCAS
@app.route('/listadodesuplidores/marcas/bd', methods=['post'])
def listadodesuplidores_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/listadodesuplidores')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/listadodesuplidores')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/listadodesuplidores')

# LISTADO DE SUPLIDORES - CREADOR ENCARGADO DE VENTAS
@app.route('/listadodesuplidores/encVentas/bd', methods=['post'])
def listadodesuplidores_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/listadodesuplidores')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/listadodesuplidores')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/listadodesuplidores')

# LISTADO DE SUPLIDORES - CREADOR ENCARGADO DE COMPRAS
@app.route('/listadodesuplidores/encCompras/bd', methods=['post'])
def listadodesuplidores_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/listadodesuplidores')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/listadodesuplidores')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/listadodesuplidores')

# LISTADO DE SUPLIDORES - ELIMINAR SUPLIDOR
@app.route('/listadodesuplidores/eliminar/bd', methods=['post'])
def listadodesuplidores_eliminar_bd():

    id_suplidor=request.form['id_suplidor']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_suplidor=%s",(id_suplidor))
    suplidores=bdsql.fetchall()
    bd.commit()
    print(suplidores)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `suplidores` WHERE id_suplidor=%s",(id_suplidor))
    bd.commit()

    return redirect('/listadodesuplidores')

# LISTADO DE SUPLIDORES - ELIMINAR CUENTA
@app.route('/listadodesuplidores/eliminar_cuenta/bd', methods=['post'])
def listadodesuplidores_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# PERFIL
@app.route('/perfil')
def perfil():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    perfil=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template('sitio/perfil.html', perfil=perfil, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# PERFIL - CREADOR MARCAS
@app.route('/perfil/marcas/bd', methods=['post'])
def perfil_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/perfil')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/perfil')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/perfil')

# PERFIL - CREADOR ENCARGADO DE VENTAS
@app.route('/perfil/encVentas/bd', methods=['post'])
def perfil_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/perfil')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/perfil')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/perfil')

# PERFIL - CREADOR ENCARGADO DE COMPRAS
@app.route('/perfil/encCompras/bd', methods=['post'])
def perfil_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/perfil')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/perfil')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/perfil')

# PERFIL - ELIMINAR CUENTA
@app.route('/perfil/eliminar_cuenta/bd', methods=['post'])
def perfil_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# TERMINOS Y CONDICIONES
@app.route('/terminosycondiciones')
def terminos_condiciones():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template ('sitio/terminosycondiciones.html', marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# TERMINOS Y CONDICIONES - CREADOR MARCAS
@app.route('/terminosycondiciones/marcas/bd', methods=['post'])
def terminosycondiciones_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/terminosycondiciones')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/terminosycondiciones')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/terminosycondiciones')

# TERMINOS Y CONDICIONES - CREADOR ENCARGADO DE VENTAS
@app.route('/terminosycondiciones/encVentas/bd', methods=['post'])
def terminosycondiciones_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/terminosycondiciones')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/terminosycondiciones')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/terminosycondiciones')

# TERMINOS Y CONDICIONES - CREADOR ENCARGADO DE COMPRAS
@app.route('/terminosycondiciones/encCompras/bd', methods=['post'])
def terminosycondiciones_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/terminosycondiciones')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/terminosycondiciones')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/terminosycondiciones')

# TERMINOS Y CONDICIONES - ELIMINAR CUENTA
@app.route('/terminosycondiciones/eliminar_cuenta/bd', methods=['post'])
def terminosycondiciones_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

#ADMIN
@app.route('/admin/')
def admin():

    if not 'logueado' in session:
        return redirect('/')
    return render_template('/admin/')

# REGISTRO USUARIO
@app.route('/registro_usuario')
def registro_usuario():
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario`")
    registro_usuario=bdsql.fetchall()

    return render_template('admin/registrousuario.html', registro_usuario=registro_usuario)

# REGISTRO USUARIO - BASE DE DATOS
@app.route('/registro_usuario/bd', methods=['post'])
def registro_usuario_bd():

    nombre=request.form['nom']
    apellido=request.form['ape']
    direccion=request.form['dir']
    telefono=request.form['tel']
    correo_electronico=request.form['email']
    contrasena=request.form['password']
    contrasena_=request.form['password-']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE correo_electronico = %s",(correo_electronico))
    registro_usuario=bdsql.fetchall()

    if registro_usuario:
        flash("Correo electronico registrado")
        return redirect('/registro_usuario')
    if contrasena != contrasena_:
        flash("Las contraseñas no coinciden")
        return redirect('/registro_usuario')
    if contrasena == contrasena_:
        session['contrasena_iguales'] = True

        sql= ("INSERT INTO `registro_usuario` (`id_usuario`,`nombre`,`apellido`,`direccion`,`telefono`,`correo_electronico`,`contrasena`) VALUES (NULL, %s, %s, %s, %s, %s, %s);")

        datos=(nombre, apellido, direccion, telefono, correo_electronico, contrasena)

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql, datos)
        bd.commit()
        return redirect('/metododepago')
    else:
        return redirect('/registro_usuario')

# REGISTRO USUARIO | OLVIDASTE TU CONTRASEÑA - BASE DE DATOS
@app.route('/registro_usuario/olvidastetucontrasena/bd', methods=['post'])
def olvidaste_contrasena_bd():

    recipients=request.form['correo']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT correo_electronico FROM `registro_usuario` WHERE correo_electronico=%s",(recipients))
    olvidaste_contrasena=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre FROM `registro_usuario` WHERE correo_electronico=%s",(recipients))
    usuario=bdsql.fetchone()

    usuarios = usuario[0]
    
    if olvidaste_contrasena:
        session['registrado'] = recipients
        msg = Message('AlphaInventory', sender = 'grupoalpha.infotep@gmail.com', recipients=[recipients])
        msg.html = "Hola {0},<br>¡Hubo una solicitud para cambiar su contraseña!<br>Si no realizó esta solicitud, ignore este correo electrónico.<br>De lo contrario, ingrese a este enlace para cambiar su contraseña: <a href='http://127.0.0.1:5000/recuperarcontrasena' target='blank'>Enlace</a>".format(usuarios)
        mail.send(msg)

        return redirect('/')
    else:
        return redirect('/registro_usuario')
    
# METODO DE PAGO 
@app.route('/metododepago')
def metodo_pago():

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `metodo_pago`")
    metodo_pago=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario`")
    registro_usuario=bdsql.fetchall()

    return render_template('admin/metododepago.html', metodo_pago=metodo_pago, registro_usuario=registro_usuario)

# METODO DE PAGO - BASE DE DATOS
@app.route('/metododepago/bd', methods=['post'])
def metodo_pago_bd():
    
    numero_tarjeta=request.form['inputNumero']
    nombre_tarjeta=request.form['inputNombre']
    correo_electronico=request.form['email']
    mes=request.form['selectMes']
    año=request.form['selectYear']
    cvv=request.form['inputCCV']
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT id_usuario FROM `registro_usuario` WHERE correo_electronico=%s",(correo_electronico))
    id_usuario=bdsql.fetchall()
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT correo_electronico FROM `registro_usuario` WHERE correo_electronico=%s",(correo_electronico))
    correo_electronicoV=bdsql.fetchall()

    if not correo_electronicoV:
        flash("El correo electronico no esta registrado")
        return redirect('/metododepago')
    else:
        sql_met_pag= ("INSERT INTO `metodo_pago` (`id_metodo_pago`,`numero_tarjeta`,`nombre_tarjeta`,`correo_electronico`,`mes`,`año`,`cvv`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);")

        datos_metodo_pago=(numero_tarjeta, nombre_tarjeta, correo_electronico, mes, año, cvv, id_usuario)

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_met_pag, datos_metodo_pago)
        bd.commit()

        return redirect('/')

# RECUPERAR CONTRASEÑA
@app.route('/recuperarcontrasena')
def recuperar_contrasena():

    # if not 'registrado' in session:
    #     return redirect('/')

    # bdsql=mysql.connect().cursor()
    # bdsql.execute("SELECT * FROM `registro_usuario` WHERE correo_electronico=%s",(session['registrado']))
    # recuperar_contrasena=bdsql.fetchall()

    return render_template('admin/recuperarcontrasena.html')

# RECUPERAR CONTRASEÑA - BASE DE DATOS
@app.route('/recuperarcontrasena/bd', methods=['post'])
def recuperar_contrasena_bd():
    
    id=request.form['id_registro']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT contrasena FROM `registro_usuario` WHERE id_usuario=%s",(id))
    recuperar_contrasena=bdsql.fetchall()
    bd.commit()
    print(recuperar_contrasena)

    contrasena=request.form['password']
    contrasena_=request.form['password-']

    if contrasena != contrasena_:
        flash("Las contrasenas no coinciden")
        return redirect('/recuperarcontrasena')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute("UPDATE registro_usuario SET contrasena = %s WHERE id_usuario=%s",(contrasena, id))
        bd.commit()

        return redirect('/')

# REGISTRO DE ARTICULOS
@app.route('/registrodearticulos')
def registro_articulos():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    articulos=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s GROUP BY nombre_marca",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template('admin/registrodearticulos.html', articulos=articulos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# REGISTRO DE ARTICULOS - BASE DE DATOS
@app.route('/registrodearticulos/bd', methods=['post'])
def registro_articulos_bd():

    codigo=request.form['codigo']
    descripcion=request.form['descripcion']
    talla=request.form['size']
    marca=request.form['marca']
    referencia=request.form['ref']
    ubicacion=request.form['direccion']
    costo=request.form['costo']
    precio=request.form['precio']
    itbis=request.form['itbis']
    cantidad=0
    margen_beneficio= round(((int(precio) - int(costo)) / int(precio)) * 100)
    unidad_medida=request.form['medida']
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT codigo FROM `articulos` WHERE codigo=%s AND id_usuario=%s",(codigo, session['id_usuario']))
    codigosA=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND id_usuario=%s",(marca, session['id_usuario']))
    marcasM=bdsql.fetchall()

    if codigosA:
        flash("Este codigo de articulo esta registrado")
        return redirect('/registrodearticulos')
    if not marcasM:
        flash("Este marca no esta registrada verifique en el buscador las marcas creadas")
        return redirect('/registrodearticulos')
    if costo > precio:
        flash("El costo no puede ser mayor al precio")
        return redirect('/registrodearticulos')
    if itbis != ("18" or "16" or "0"):
        flash("Debe seleccionar el itbis")
        return redirect('/registrodearticulos')
    else:
        sql_articulos=('INSERT INTO `articulos` (`id_articulo`,`codigo`,`descripcion`,`talla`,`marca`,`referencia`,`ubicacion`,`costo`,`precio`,`itbis`,`cantidad`,`margen_beneficio`,`unidad_medida`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

        datos_articulos=(codigo,descripcion,talla,marca,referencia,ubicacion,costo,precio,itbis,cantidad,margen_beneficio,unidad_medida, session['id_usuario'])

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_articulos, datos_articulos)
        bd.commit()

        return redirect('/registrodearticulos')

# REGISTRO DE ARTICULOS - CREADOR MARCAS
@app.route('/registrodearticulos/marcas/bd', methods=['post'])
def registrodearticulos_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/registrodearticulos')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/registrodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/registrodearticulos')

# REGISTRO DE ARTICULOS - CREADOR ENCARGADO DE VENTAS
@app.route('/registrodearticulos/encVentas/bd', methods=['post'])
def registrodearticulos_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/registrodearticulos')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/registrodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/registrodearticulos')

# REGISTRO DE ARTICULOS - CREADOR ENCARGADO DE COMPRAS
@app.route('/registrodearticulos/encCompras/bd', methods=['post'])
def registrodearticulos_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/registrodearticulos')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/registrodearticulos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/registrodearticulos')

# REGISTRO DE ARTICULOS - ELIMINAR MARCA
@app.route('/registrodearticulos/marcas/eliminar/bd', methods=['post'])
def registrodearticulos_marcas_eliminar_bd():

    id_marca=request.form['id_marca']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_marca=%s AND id_usuario=%s",(id_marca, session['id_usuario']))
    marcas=bdsql.fetchall()
    bd.commit()
    print(marcas)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `marcas` WHERE id_marca=%s",(id_marca))
    bd.commit()

    return redirect('/registrodearticulos')

# REGISTRO DE ARTICULOS - ELIMINAR CUENTA
@app.route('/registrodearticulos/eliminar_cuenta/bd', methods=['post'])
def regitrodearticulos_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# EDITAR ARTICULO
@app.route('/editararticulo/<int:id>')
def editar_articulo(id):

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_articulo=%s",(id))
    articulos=bdsql.fetchall()
    bd.commit()

    return render_template('admin/editararticulo.html', articulos=articulos)

# EDITAR ARTICULO - BASE DE DATOS
@app.route('/editararticulo/bd/<int:id>', methods=['post'])
def editar_articulo_bd(id):

    codigo=request.form['codigo']
    descripcion=request.form['descripcion']
    talla=request.form['size']
    marca=request.form['marca']
    referencia=request.form['ref']
    ubicacion=request.form['direccion']
    costo=request.form['costo']
    precio=request.form['precio']
    itbis=request.form['itbis']
    margen_beneficio=request.form['margen']
    unidad_medida=request.form['medida']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_articulo=%s",(id))
    articulos=bdsql.fetchall()
    bd.commit()
    print(articulos)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE articulos SET codigo = %s, descripcion = %s, talla = %s, marca = %s, referencia = %s, ubicacion = %s, costo = %s, precio = %s, itbis = %s, margen_beneficio = %s, unidad_medida = %s WHERE id_articulo=%s",(codigo, descripcion, talla, marca, referencia, ubicacion, costo, precio, itbis, margen_beneficio, unidad_medida, id))
    bd.commit()

    return redirect('/listadodearticulos')

# REGISTRO DE CLIENTES
@app.route('/registrodeclientes')
def registro_clientes():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_usuario=%s",(session['id_usuario']))
    clientes=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template('admin/registrodeclientes.html', clientes=clientes, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# REGISTRO DE CLIENTES - BASE DE DATOS
@app.route('/registrodeclientes/bd', methods=['post'])
def registro_clientes_bd():

    codigo=request.form['codigo']
    nombre=request.form['nom']
    direccion=request.form['dir']
    ciudad=request.form['ciudad']
    telefono=request.form['tel']
    cedula=request.form['cedula']
    email=request.form['email']
    rnc=request.form['rnc']
    descuentos=request.form['descuento']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT codigo FROM `clientes` WHERE codigo=%s AND id_usuario=%s",(codigo, session['id_usuario']))
    codigoC=bdsql.fetchall()

    if codigoC:
        flash("Este codigo de cliente esta registrado")
        return redirect('/registrodeclientes')
    else:
        sql_clientes=('INSERT INTO `clientes` (`id_cliente`,`codigo`,`nombre`,`direccion`,`ciudad`,`telefono`,`cedula`,`email`,`rnc`,`descuentos`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

        datos_clientes=(codigo,nombre,direccion,ciudad,telefono,cedula,email,rnc,descuentos, session['id_usuario'])

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_clientes, datos_clientes)
        bd.commit()

        return redirect('/registrodeclientes')

# REGISTRO DE CLIENTES - CREADOR MARCAS
@app.route('/registrodeclientes/marcas/bd', methods=['post'])
def registrodeclientes_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/registrodeclientes')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/registrodeclientes')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/registrodeclientes')

# REGISTRO DE CLIENTES - CREADOR ENCARGADO DE VENTAS
@app.route('/registrodeclientes/encVentas/bd', methods=['post'])
def registrodeclientes_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/registrodeclientes')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/registrodeclientes')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/registrodeclientes')

# REGISTRO DE CLIENTES - CREADOR EMCARGADO DE COMPRAS
@app.route('/registrodeclientes/encCompras/bd', methods=['post'])
def registrodeclientes_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/registrodeclientes')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/registrodeclientes')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/registrodeclientes')

# REGISTRO DE CLIENTES - ELIMINAR CUENTA
@app.route('/registrodeclientes/eliminar_cuenta/bd', methods=['post'])
def registrodeclientes_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# EDITAR CLIENTE
@app.route('/editarcliente/<int:id>')
def editar_cliente(id):

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_cliente=%s",(id))
    clientes=bdsql.fetchall()
    bd.commit()

    return render_template('admin/editarcliente.html', clientes=clientes)

# EDITAR CLIENTE - BASE DE DATOS
@app.route('/editarcliente/bd/<int:id>', methods=['post'])
def editar_cliente_bd(id):

    codigo=request.form['codigo']
    nombre=request.form['nom']
    direccion=request.form['dir']
    ciudad=request.form['ciudad']
    telefono=request.form['tel']
    cedula=request.form['cedula']
    email=request.form['email']
    rnc=request.form['rnc']
    descuentos=request.form['descuento']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_cliente=%s",(id))
    clientes=bdsql.fetchall()
    bd.commit()
    print(clientes)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE clientes SET codigo = %s, nombre = %s, direccion = %s, ciudad = %s, telefono = %s, cedula = %s, email = %s, rnc = %s, descuentos = %s WHERE id_cliente=%s",(codigo, nombre, direccion, ciudad, telefono, cedula, email, rnc, descuentos, id))
    bd.commit()

    return redirect('/listadodeclientes')

# REGISTRO DE SUPLIDORES
@app.route('/registrodesuplidores')
def registro_suplidores():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_usuario=%s",(session['id_usuario']))
    suplidores=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template('admin/registrodesuplidores.html', suplidores=suplidores, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# REGISTRO DE SUPLIDORES - BASE DE DATOS
@app.route('/registrodesuplidores/bd', methods=['post'])
def registro_suplidores_bd():

    codigo=request.form['codigo']
    nombre=request.form['nom']
    direccion=request.form['dir']
    ciudad=request.form['ciudad']
    telefono=request.form['tel']
    limite_credito=request.form['limite']
    condiciones=request.form['condiciones']
    rnc=request.form['rnc']
    descuentos=request.form['descuento']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT codigo FROM `suplidores` WHERE codigo=%s AND id_usuario=%s",(codigo, session['id_usuario']))
    codigoS=bdsql.fetchall()

    if codigoS:
        flash("Este codigo de suplidor esta registrado")
        return redirect('/registrodesuplidores')
    else:
        sql_suplidores=("INSERT INTO `suplidores` (`id_suplidor`,`codigo`,`nombre`,`direccion`,`ciudad`,`telefono`,`limite_credito`,`condiciones`,`rnc`,`descuentos`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        datos_suplidores=(codigo,nombre,direccion,ciudad,telefono,limite_credito,condiciones,rnc,descuentos, session['id_usuario'])

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_suplidores, datos_suplidores)
        bd.commit()

        return redirect('/registrodesuplidores')

# REGISTRO DE SUPLIDORES - CREADOR MARCAS
@app.route('/registrodesuplidores/marcas/bd', methods=['post'])
def registrodesuplidores_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/registrodesuplidores')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/registrodesuplidores')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/registrodesuplidores')

# REGISTRO DE SUPLIDORES - CREADOR ENCARGADO DE VENTAS
@app.route('/registrodesuplidores/encVentas/bd', methods=['post'])
def registrodesuplidores_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/registrodesuplidores')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/registrodesuplidores')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/registrodesuplidores')

# REGISTRO DE SUPLIDORES - CREADOR ENCARGADO DE COMPRAS
@app.route('/registrodesuplidores/encCompras/bd', methods=['post'])
def registrodesuplidores_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/registrodesuplidores')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/registrodesuplidores')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/registrodesuplidores')

# REGISTRO DE SUPLIDORES - ELIMINAR CUENTA
@app.route('/registrodesuplidores/eliminar_cuenta/bd', methods=['post'])
def registrodesuplidores_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# EDITAR SUPLIDOR
@app.route('/editarsuplidor/<int:id>')
def editar_suplidor(id):

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_suplidor=%s",(id))
    suplidores=bdsql.fetchall()
    bd.commit()

    return render_template('admin/editarsuplidor.html', suplidores=suplidores)

# EDITAR SUPLIDOR - BASE DE DATOS
@app.route('/editarsuplidor/bd/<int:id>', methods=['post'])
def editar_suplidor_bd(id):

    codigo=request.form['codigo']
    nombre=request.form['nom']
    direccion=request.form['dir']
    ciudad=request.form['ciudad']
    telefono=request.form['tel']
    limite_credito=request.form['limite']
    condiciones=request.form['condiciones']
    rnc=request.form['rnc']
    descuentos=request.form['descuento']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_suplidor=%s",(id))
    suplidores=bdsql.fetchall()
    bd.commit()
    print(suplidores)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE suplidores SET codigo = %s, nombre = %s, direccion = %s, ciudad = %s, telefono = %s, limite_credito = %s, condiciones = %s, rnc = %s, descuentos = %s WHERE id_suplidor=%s",(codigo, nombre, direccion, ciudad, telefono, limite_credito, condiciones, rnc, descuentos, id))
    bd.commit()

    return redirect('/listadodesuplidores')

# COMPRAS
@app.route('/compras')
def compras():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `compras` WHERE id_usuario=%s",(session['id_usuario']))
    compras=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `suplidores` WHERE id_usuario=%s",(session['id_usuario']))
    suplidores=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    articulos=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template ('admin/compras.html', compras=compras, suplidores=suplidores, articulos=articulos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# COMPRAS - BASE DE DATOS
@app.route('/compras/bd', methods=['post'])
def compras_registro_bd():

    tiempo=datetime.now()

    numero_facturaC=request.form['fact']
    horaCompra=tiempo.strftime('%H:%M:%S') 
    fecha_compra=request.form['date']
    encargado_compra=request.form['Encargado']
    suplidor=request.form['suplidores']
    codigo=request.form['codigo']
    cantidad=request.form['cantidad']
    itbis=request.form['itbis']
    costo=request.form['costo']
    codigo_=request.form['codigo_']
    cantidad_=request.form['cantidad_']
    itbis_=request.form['itbis_']
    costo_=request.form['costo_']
    codigo__=request.form['codigo__']
    cantidad__=request.form['cantidad__']
    itbis__=request.form['itbis__']
    costo__=request.form['costo__']
    codigo___=request.form['codigo___']
    cantidad___=request.form['cantidad___']
    itbis___=request.form['itbis___']
    costo___=request.form['costo___']
    codigo____=request.form['codigo____']
    cantidad____=request.form['cantidad____']
    itbis____=request.form['itbis____']
    costo____=request.form['costo____']
    codigo_____=request.form['codigo_____']
    cantidad_____=request.form['cantidad_____']
    itbis_____=request.form['itbis_____']
    costo_____=request.form['costo_____']
    codigo______=request.form['codigo______']
    cantidad______=request.form['cantidad______']
    itbis______=request.form['itbis______']
    costo______=request.form['costo______']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(f"SELECT * FROM `articulos` WHERE codigo={codigo}")
    articulos=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT itbis FROM `articulos` WHERE codigo=%s AND itbis=%s", (codigo, itbis))
    itbisA=bdsql.fetchone()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT costo FROM `articulos` WHERE codigo=%s AND costo=%s", (codigo, costo))
    costoA=bdsql.fetchone()
    bd.commit()

    bd=mysql.connect()
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre FROM `suplidores` WHERE nombre=%s AND id_usuario=%s",(suplidor, session['id_usuario']))
    suplidores=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(encargado_compra ,session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    if codigo and cantidad:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad, codigo))
        bd.commit()
        if codigo_ and cantidad_:
            bd=mysql.connect()
            bdsql=bd.cursor()
            bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad_, codigo_))
            bd.commit()
            if codigo__ and cantidad__:
                bd=mysql.connect()
                bdsql=bd.cursor()
                bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad__, codigo__))
                bd.commit()
                if codigo___ and cantidad___:
                    bd=mysql.connect()
                    bdsql=bd.cursor()
                    bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad___, codigo___))
                    bd.commit()
                    if codigo____ and cantidad____:
                        bd=mysql.connect()
                        bdsql=bd.cursor()
                        bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad____, codigo____))
                        bd.commit()
                        if codigo_____ and cantidad_____:
                            bd=mysql.connect()
                            bdsql=bd.cursor()
                            bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad_____, codigo_____))
                            bd.commit()
                            if codigo______ and cantidad______:
                                bd=mysql.connect()
                                bdsql=bd.cursor()
                                bdsql.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo={1}".format(cantidad______, codigo______))
                                bd.commit()

    if not suplidores:
        flash("Este suplidor no esta registrado verifique en el buscador de suplidores")
        return redirect('/compras')
    if not encargado_compras:
        flash("Este encargado de compras no esta registrado verifique en el buscador de encargado de compras")
        return redirect('/compras')
    if not articulos:
        flash("Este articulo no existe")
        return redirect('/compras')
    if not itbisA:
        flash("Este no es el itbis del articulo")
        return redirect('/compras')
    if not costoA:
        flash("Este no es el costo del articulo")
        return redirect('/compras')
    if codigo and cantidad and itbis and costo and codigo_ and cantidad_ and itbis_ and costo_ and codigo__ and cantidad__ and itbis__ and costo__ and codigo___ and cantidad___ and itbis___ and costo___ and codigo____ and cantidad____ and itbis____ and costo____ and codigo____ and cantidad_____ and itbis_____ and costo_____ and codigo______ and cantidad______ and itbis______ and costo______:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        total_compra_ = ((int(cantidad_)*int(costo_)) * int(itbis)) / 100
        total_compra__ = ((int(cantidad__)*int(costo__)) * int(itbis)) / 100
        total_compra___ = ((int(cantidad___)*int(costo___)) * int(itbis)) / 100
        total_compra____ = ((int(cantidad____)*int(costo____)) * int(itbis)) / 100
        total_compra_____ = ((int(cantidad_____)*int(costo_____)) * int(itbis)) / 100
        total_compra______ = ((int(cantidad______)*int(costo______)) * int(itbis)) / 100
        sql______= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos______= [
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_,cantidad_,itbis_,costo_, total_compra_, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo__,cantidad__,itbis__,costo__, total_compra__, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo___,cantidad___,itbis___,costo___, total_compra___, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo____,cantidad____,itbis____,costo____, total_compra____, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_____,cantidad_____,itbis_____,costo_____, total_compra_____, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo______,cantidad______,itbis______,costo______, total_compra______, session['id_usuario']) 
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql______,datos______)
        bd.commit()

        return redirect('/compras')
    if codigo and cantidad and itbis and costo and codigo_ and cantidad_ and itbis_ and costo_ and codigo__ and cantidad__ and itbis__ and costo__ and codigo___ and cantidad___ and itbis___ and costo___ and codigo____ and cantidad____ and itbis____ and costo____ and codigo____ and cantidad_____ and itbis_____ and costo_____:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        total_compra_ = ((int(cantidad_)*int(costo_)) * int(itbis)) / 100
        total_compra__ = ((int(cantidad__)*int(costo__)) * int(itbis)) / 100
        total_compra___ = ((int(cantidad___)*int(costo___)) * int(itbis)) / 100
        total_compra____ = ((int(cantidad____)*int(costo____)) * int(itbis)) / 100
        total_compra_____ = ((int(cantidad_____)*int(costo_____)) * int(itbis)) / 100
        sql_____= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_____= [
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_,cantidad_,itbis_,costo_, total_compra_, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo__,cantidad__,itbis__,costo__, total_compra__, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo___,cantidad___,itbis___,costo___, total_compra___, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo____,cantidad____,itbis____,costo____, total_compra____, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_____,cantidad_____,itbis_____,costo_____, total_compra_____, session['id_usuario']) 
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_____,datos_____)
        bd.commit()

        return redirect('/compras')
    if codigo and cantidad and itbis and costo and codigo_ and cantidad_ and itbis_ and costo_ and codigo__ and cantidad__ and itbis__ and costo__ and codigo___ and cantidad___ and itbis___ and costo___ and codigo____ and cantidad____ and itbis____ and costo____:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        total_compra_ = ((int(cantidad_)*int(costo_)) * int(itbis)) / 100
        total_compra__ = ((int(cantidad__)*int(costo__)) * int(itbis)) / 100
        total_compra___ = ((int(cantidad___)*int(costo___)) * int(itbis)) / 100
        total_compra____ = ((int(cantidad____)*int(costo____)) * int(itbis)) / 100
        sql_= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_,cantidad_,itbis_,costo_, total_compra_, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo__,cantidad__,itbis__,costo__, total_compra__, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo___,cantidad___,itbis___,costo___, total_compra___, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo____,cantidad____,itbis____,costo____, total_compra____, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/compras')
    if codigo and cantidad and itbis and costo and codigo_ and cantidad_ and itbis_ and costo_ and codigo__ and cantidad__ and itbis__ and costo__ and codigo___ and cantidad___ and itbis___ and costo___:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        total_compra_ = ((int(cantidad_)*int(costo_)) * int(itbis)) / 100
        total_compra__ = ((int(cantidad__)*int(costo__)) * int(itbis)) / 100
        total_compra___ = ((int(cantidad___)*int(costo___)) * int(itbis)) / 100
        sql_= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_,cantidad_,itbis_,costo_, total_compra_, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo__,cantidad__,itbis__,costo__, total_compra__, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo___,cantidad___,itbis___,costo___, total_compra___, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/compras')
    if codigo and cantidad and itbis and costo and codigo_ and cantidad_ and itbis_ and costo_ and codigo__ and cantidad__ and itbis__ and costo__:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        total_compra_ = ((int(cantidad_)*int(costo_)) * int(itbis)) / 100
        total_compra__ = ((int(cantidad__)*int(costo__)) * int(itbis)) / 100
        sql_= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_,cantidad_,itbis_,costo_, total_compra_, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo__,cantidad__,itbis__,costo__, total_compra__, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/compras')
    if codigo and cantidad and itbis and costo and codigo_ and cantidad_ and itbis_ and costo_:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        total_compra_ = ((int(cantidad_)*int(costo_)) * int(itbis)) / 100
        sql_= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario']),
            (numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo_,cantidad_,itbis_,costo_, total_compra_, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/compras')
    if codigo and cantidad and itbis and costo:
        total_compra = ((int(cantidad)*int(costo)) * int(itbis)) / 100
        sql= ("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos=(numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo, total_compra, session['id_usuario'])

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql,datos)
        bd.commit()

        return redirect('/compras')

# COMPRAS - CREADOR MARCAS
@app.route('/compras/marcas/bd', methods=['post'])
def compras_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/compras')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/compras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/compras')

# COMPRAS - CREADOR ENCARGADO DE VENTAS
@app.route('/compras/encVentas/bd', methods=['post'])
def compras_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/compras')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/compras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/compras')


# COMPRAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/compras/encCompras/bd', methods=['post'])
def compras_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/compras')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/compras')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/compras')

# COMPRAS - ELIMINAR ENCARGADO DE COMPRA
@app.route('/compras/encargadocompra/eliminar/bd', methods=['post'])
def compra_encargadocompra_eliminar_bd():

    id_encargadocompra=request.form['id_encargadocompra']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_encargadoC=%s AND id_usuario=%s",(id_encargadocompra, session['id_usuario']))
    encargados_com=bdsql.fetchall()
    bd.commit()
    print(encargados_com)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `encargados_com` WHERE id_encargadoC=%s",(id_encargadocompra))
    bd.commit()

    return redirect('/compras')

# COMPRAS - ELIMINAR CUENTA
@app.route('/compras/eliminar_cuenta/bd', methods=['post'])
def compras_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# VENTAS
@app.route('/ventas')
def ventas():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `ventas` WHERE id_usuario=%s",(session['id_usuario']))
    ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `clientes` WHERE id_usuario=%s",(session['id_usuario']))
    clientes=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE id_usuario=%s",(session['id_usuario']))
    articulos=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template ('admin/ventas.html', ventas=ventas, clientes=clientes, articulos=articulos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# VENTAS - BASE DE DATOS
@app.route('/ventas/bd', methods=['post'])
def ventas_registro_bd():

    tiempo=datetime.now()

    numero_facturaV=request.form['fact']
    horaVenta=tiempo.strftime('%H:%M:%S')
    fecha_venta=request.form['date']
    encargado_venta=request.form['Encargado']
    cliente=request.form['cliente']
    codigo=request.form['codigo']
    cantidad=request.form['cantidad']
    itbis=request.form['itbis']
    precio=request.form['precio']
    codigo_=request.form['codigo_']
    itbis_=request.form['itbis_']
    cantidad_=request.form['cantidad_']
    precio_=request.form['precio_']
    codigo__=request.form['codigo__']
    itbis__=request.form['itbis__']
    cantidad__=request.form['cantidad__']
    precio__=request.form['precio__']
    codigo___=request.form['codigo___']
    itbis___=request.form['itbis___']
    cantidad___=request.form['cantidad___']
    precio___=request.form['precio___']
    codigo____=request.form['codigo____']
    itbis____=request.form['itbis____']
    cantidad____=request.form['cantidad____']
    precio____=request.form['precio____']
    codigo_____=request.form['codigo_____']
    itbis_____=request.form['itbis_____']
    cantidad_____=request.form['cantidad_____']
    precio_____=request.form['precio_____']
    codigo______=request.form['codigo______']
    itbis______=request.form['itbis______']
    cantidad______=request.form['cantidad______']
    precio______=request.form['precio______']


    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `articulos` WHERE codigo=%s",(codigo))
    articulos=bdsql.fetchone()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT itbis FROM `articulos` WHERE codigo=%s AND itbis=%s", (codigo, itbis))
    itbisA=bdsql.fetchone()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT precio FROM `articulos` WHERE codigo=%s AND precio=%s", (codigo, precio))
    precioA=bdsql.fetchone()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT cantidad FROM `articulos` WHERE (cantidad = 0) AND codigo=%s",(codigo))
    cantidadC=bdsql.fetchone()
    bd.commit()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre FROM `clientes` WHERE nombre=%s AND id_usuario=%s",(cliente, session['id_usuario']))
    clientes=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND id_usuario=%s",(encargado_venta, session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    if codigo and cantidad:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad, codigo))
        bd.commit()
        if codigo_ and cantidad_:
            bd=mysql.connect()
            bdsql=bd.cursor()
            bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad_, codigo_))
            bd.commit()
            if codigo__ and cantidad__:
                bd=mysql.connect()
                bdsql=bd.cursor()
                bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad__, codigo__))
                bd.commit()
                if codigo___ and cantidad___:
                    bd=mysql.connect()
                    bdsql=bd.cursor()
                    bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad___, codigo___))
                    bd.commit()
                    if codigo____ and cantidad____:
                        bd=mysql.connect()
                        bdsql=bd.cursor()
                        bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad____, codigo____))
                        bd.commit()
                        if codigo_____ and cantidad_____:
                            bd=mysql.connect()
                            bdsql=bd.cursor()
                            bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad_____, codigo_____))
                            bd.commit()
                            if codigo______ and cantidad______:
                                bd=mysql.connect()
                                bdsql=bd.cursor()
                                bdsql.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo={1}".format(cantidad______, codigo______))
                                bd.commit()

    if not clientes:
        flash("Este cliente no esta registrado verifique el buscador de clientes")
        return redirect('/ventas')
    if not encargado_ventas:
        flash("Este encargado de ventas no esta registrado verifique el buscador de encargados de ventas")
        return redirect('/ventas')
    if not articulos:
        flash("Este articulo no existe")
        return redirect('/ventas')
    if cantidadC:
        flash("No hay suficientes articulos para esta venta")
        return redirect('/ventas')
    if not itbisA:
        flash("Este no es el itbis del articulo")
        return redirect('/ventas')
    if not precioA:
        flash("Este no es el precio del articulo")
        return redirect('/ventas')
    if codigo and cantidad and itbis and precio and codigo_ and cantidad_ and itbis_ and precio_ and codigo__ and cantidad__ and itbis__ and precio__ and codigo___ and cantidad___ and itbis___ and precio___ and codigo____ and cantidad____ and itbis____ and precio____ and codigo____ and cantidad_____ and itbis_____ and precio_____ and codigo______ and cantidad______ and itbis______ and precio______:
        total_venta = ((int(cantidad)*int(precio)) * int(itbis)) / 100
        total_venta_ = ((int(cantidad_)*int(precio_)) * int(itbis)) / 100
        total_venta__ = ((int(cantidad__)*int(precio__)) * int(itbis)) / 100
        total_venta___ = ((int(cantidad___)*int(precio___)) * int(itbis)) / 100
        total_venta____ = ((int(cantidad____)*int(precio____)) * int(itbis)) / 100
        total_venta_____ = ((int(cantidad_____)*int(precio_____)) * int(itbis)) / 100
        total_venta______ = ((int(cantidad______)*int(precio______)) * int(itbis)) / 100
        sql______= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos______= [
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_,cantidad_,itbis_,precio_, total_venta_, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo__,cantidad__,itbis__,precio__, total_venta__, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo___,cantidad___,itbis___,precio___, total_venta___, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo____,cantidad____,itbis____,precio____, total_venta____, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_____,cantidad_____,itbis_____,precio_____, total_venta_____, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo______,cantidad______,itbis______,precio______, total_venta______, session['id_usuario'])  
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql______,datos______)
        bd.commit()

        return redirect('/ventas')
    if codigo and cantidad and itbis and precio and codigo_ and cantidad_ and itbis_ and precio_ and codigo__ and cantidad__ and itbis__ and precio__ and codigo___ and cantidad___ and itbis___ and precio___ and codigo____ and cantidad____ and itbis____ and precio____ and codigo____ and cantidad_____ and itbis_____ and precio_____:
        total_venta = ((int(cantidad)*int(precio)) * int(itbis)) / 100
        total_venta_ = ((int(cantidad_)*int(precio_)) * int(itbis)) / 100
        total_venta__ = ((int(cantidad__)*int(precio__)) * int(itbis)) / 100
        total_venta___ = ((int(cantidad___)*int(precio___)) * int(itbis)) / 100
        total_venta____ = ((int(cantidad____)*int(precio____)) * int(itbis)) / 100
        total_venta_____ = ((int(cantidad_____)*int(precio_____)) * int(itbis)) / 100
        sql_____= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_____= [
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_,cantidad_,itbis_,precio_, total_venta_, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo__,cantidad__,itbis__,precio__, total_venta__, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo___,cantidad___,itbis___,precio___, total_venta___, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo____,cantidad____,itbis____,precio____, total_venta____, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_____,cantidad_____,itbis_____,precio_____, total_venta_____, session['id_usuario']) 
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_____,datos_____)
        bd.commit()

        return redirect('/ventas')
    if codigo and cantidad and itbis and precio and codigo_ and cantidad_ and itbis_ and precio_ and codigo__ and cantidad__ and itbis__ and precio__ and codigo___ and cantidad___ and itbis___ and precio___ and codigo____ and cantidad____ and itbis____ and precio____:
        total_venta = ((int(cantidad)*int(precio)) * int(itbis)) / 100
        total_venta_ = ((int(cantidad_)*int(precio_)) * int(itbis)) / 100
        total_venta__ = ((int(cantidad__)*int(precio__)) * int(itbis)) / 100
        total_venta___ = ((int(cantidad___)*int(precio___)) * int(itbis)) / 100
        total_venta____ = ((int(cantidad____)*int(precio____)) * int(itbis)) / 100
        sql_= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_,cantidad_,itbis_,precio_, total_venta_, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo__,cantidad__,itbis__,precio__, total_venta__, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo___,cantidad___,itbis___,precio___, total_venta___, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo____,cantidad____,itbis____,precio____, total_venta____, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/ventas')
    if codigo and cantidad and itbis and precio and codigo_ and cantidad_ and itbis_ and precio_ and codigo__ and cantidad__ and itbis__ and precio__ and codigo___ and cantidad___ and itbis___ and precio___:
        total_venta = ((int(cantidad)*int(precio)) * int(itbis)) / 100
        total_venta_ = ((int(cantidad_)*int(precio_)) * int(itbis)) / 100
        total_venta__ = ((int(cantidad__)*int(precio__)) * int(itbis)) / 100
        total_venta___ = ((int(cantidad___)*int(precio___)) * int(itbis)) / 100
        sql_= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_,cantidad_,itbis_,precio_, total_venta_, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo__,cantidad__,itbis__,precio__, total_venta__, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo___,cantidad___,itbis___,precio___, total_venta___, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/ventas')
    if codigo and cantidad and itbis and precio and codigo_ and cantidad_ and itbis_ and precio_ and codigo__ and cantidad__ and itbis__ and precio__:
        total_venta = ((int(cantidad)*int(precio)) * int(itbis)) / 100 
        total_venta_ = ((int(cantidad_)*int(precio_)) * int(itbis)) / 100
        total_venta__ = ((int(cantidad__)*int(precio__)) * int(itbis)) / 100
        sql_= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_,cantidad_,itbis_,precio_, total_venta_, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo__,cantidad__,itbis__,precio__, total_venta__, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/ventas')
    if codigo and cantidad and itbis and precio and codigo_ and cantidad_ and itbis_ and precio_:
        total_venta = ((int(cantidad)*int(precio)) * int(itbis)) / 100
        total_venta_ = ((int(cantidad_)*int(precio_)) * int(itbis)) / 100
        sql_= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos_= [
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario']),
            (numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo_,cantidad_,itbis_,precio_, total_venta_, session['id_usuario'])
        ]

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.executemany(sql_,datos_)
        bd.commit()

        return redirect('/ventas')
    if codigo and cantidad and itbis and precio:
        total_venta = ((int(precio) * int(cantidad)) * int(itbis)) / 100

        sql= ("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        datos=(numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio, total_venta, session['id_usuario'])

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql,datos)
        bd.commit()

        return redirect('/ventas')

# VENTAS - CREADOR MARCAS
@app.route('/ventas/marcas/bd', methods=['post'])
def ventas_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`) VALUES (NULL, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/ventas')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/ventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/ventas')

# VENTAS - CREADOR ENCARGADO DE VENTAS
@app.route('/ventas/encVentas/bd', methods=['post'])
def ventas_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/ventas')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/ventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/ventas')

# VENTAS - CREADOR ENCARGADO DE COMPRAS
@app.route('/ventas/encCompras/bd', methods=['post'])
def ventas_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/ventas')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/ventas')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/ventas')

# VENTAS - ELIMINAR ENCARGADO DE VENTA
@app.route('/ventas/encargadoventa/eliminar/bd', methods=['post'])
def compra_encargadoventa_eliminar_bd():

    id_encargadoventa=request.form['id_encargadoventa']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_encargadoV=%s AND id_usuario=%s",(id_encargadoventa, session['id_usuario']))
    encargados_ven=bdsql.fetchall()
    bd.commit()
    print(encargados_ven)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `encargados_ven` WHERE id_encargadoV=%s",(id_encargadoventa))
    bd.commit()

    return redirect('/ventas')

# VENTAS - ELIMINAR CUENTA
@app.route('/ventas/eliminar_cuenta/bd', methods=['post'])
def ventas_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# RESPALADOS
@app.route('/respaldos')
def respaldos():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `respaldos` WHERE id_usuario=%s",(session['id_usuario']))
    respaldos=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template('admin/respaldos.html', respaldos=respaldos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# RESPALDOS - BASE DE DATOS
@app.route('/respaldos/bd', methods=['post'])
def respaldos_bd():

    fecha=datetime.now()
    fechaRespaldo=fecha.strftime('%Y-%m-%d')

    sql_respaldos= ("INSERT INTO `respaldos` (`id_respaldo`,`fecha_respaldo`,`id_usuario`) VALUES (NULL, %s, %s)")

    datos_respaldos=(fechaRespaldo, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_respaldos, datos_respaldos)
    bd.commit()

    return redirect('/respaldos')

# RESPALDOS - ELIMINAR RESPALDO
@app.route('/respaldos/eliminar/bd', methods=['post'])
def respaldos_eliminar_bd():

    id_respaldo=request.form['id_respaldo']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `respaldos` WHERE id_respaldo=%s",(id_respaldo))
    respaldos=bdsql.fetchall()
    bd.commit()
    print(respaldos)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `respaldos` WHERE id_respaldo=%s",(id_respaldo))
    bd.commit()

    return redirect('/respaldos')

# RESPALDOS - CREADOR MARCAS
@app.route('/respaldos/marcas/bd', methods=['post'])
def respaldos_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/respaldos')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/respaldos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/respaldos')

# RESPALDOS - CREADOR ENCARGADO DE VENTAS
@app.route('/respaldos/encVentas/bd', methods=['post'])
def respaldos_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/respaldos')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/respaldos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/respaldos')

# RESPALDOS - CREADOR ENCARGADO DE COMPRAS
@app.route('/respaldos/encCompras/bd', methods=['post'])
def respaldos_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/respaldos')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/respaldos')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/respaldos')

# RESPALDOS - ELIMINAR CUENTA
@app.route('/respaldos/eliminar_cuenta/bd', methods=['post'])
def respaldos_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# PERFIL EDITAR
@app.route('/perfileditar')
def perfil_editar():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    perfil=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()
    
    return render_template('admin/perfileditar.html', perfil=perfil, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# PERFIL EDITAR - BASE DE DATOS
@app.route('/perfileditar/bd', methods=['post'])
def perfil_bd():

    correo_electronico=request.form['email']
    direccion=request.form['dir']
    telefono=request.form['tel']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    perfil=bdsql.fetchall()
    bd.commit()
    print(perfil)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE registro_usuario SET direccion = %s, telefono = %s, correo_electronico = %s WHERE id_usuario=%s",(direccion, telefono, correo_electronico, session['id_usuario']))
    bd.commit()
    
    return redirect('/perfil')

# PERFIL EDITAR - CREADOR MARCAS
@app.route('/perfileditar/marcas/bd', methods=['post'])
def perfileditar_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/perfileditar')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/perfileditar')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/perfileditar')

# PERFIL EDITAR - CREADOR ENCARGADO DE VENTAS
@app.route('/perfileditar/encVentas/bd', methods=['post'])
def perfileditar_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/perfileditar')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/perfileditar')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/perfileditar')

# PERFIL EDITAR - CREADOR ENCARGADO DE COMPRAS
@app.route('/perfileditar/encCompras/bd', methods=['post'])
def perfileditar_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/perfileditar')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/perfileditar')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/perfileditar')

# PERFIL EDITAR - ELIMINAR CUENTA
@app.route('/perfileditar/eliminar_cuenta/bd', methods=['post'])
def perfileditar_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

# CAMBIAR CONTRASEÑA
@app.route('/cambiarcontrasena')
def cambiar_contrasena():

    if not 'logueado' in session:
        return redirect('/')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    cambiar_contrasena=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `marcas` WHERE id_usuario=%s",(session['id_usuario']))
    marcas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_ven` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_ventas=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `encargados_com` WHERE id_usuario=%s",(session['id_usuario']))
    encargado_compras=bdsql.fetchall()

    return render_template ('admin/cambiarcontrasena.html', cambiar_contrasena=cambiar_contrasena, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

# CAMBIAR CONTRASEÑA - BASE DE DATOS
@app.route('/cambiarcontrasena/bd', methods=['post'])
def cambiar_contrasena_bd():

    contrasena=request.form['password']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    cambiar_contrasena=bdsql.fetchall()
    bd.commit()
    print(cambiar_contrasena)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE registro_usuario SET contrasena = %s WHERE id_usuario=%s",(contrasena, session['id_usuario']))
    bd.commit()

    return redirect('/inicio_inventario')

# CAMBIAR CONTRASEÑA - CREADOR MARCAS
@app.route('/cambiarcontrasena/marcas/bd', methods=['post'])
def cambiarcontrasena_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_marca FROM `marcas` WHERE codigo_marca=%s AND  id_usuario=%s",(codigo_marca,session['id_usuario']))
    codigos_marcas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_marca FROM `marcas` WHERE nombre_marca=%s AND  id_usuario=%s",(nombre_marca,session['id_usuario']))
    nombres_marcas=bdsql.fetchall()
    bd.commit()

    if codigos_marcas:
        flash("Este codigo de marca ya esta registrado")
        return redirect('/cambiarcontrasena')
    if nombres_marcas:
        flash("Este nombre de marca ya esta registrado")
        return redirect('/cambiarcontrasena')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_marcas, datos_marcas)
        bd.commit()    

        return redirect('/cambiarcontrasena')

# CAMBIAR CONTRASEÑA - CREADOR ENCARGADO DE VENTAS
@app.route('/cambiarcontrasena/encVentas/bd', methods=['post'])
def cambiarcontrasena_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoV FROM `encargados_ven` WHERE codigo_encargadoV=%s AND  id_usuario=%s",(codigo_enc_ventas,session['id_usuario']))
    codigos_enc_ventas=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoV FROM `encargados_ven` WHERE nombre_encargadoV=%s AND  id_usuario=%s",(nombre_enc_ventas,session['id_usuario']))
    nombres_enc_ventas=bdsql.fetchall()
    bd.commit()

    if codigos_enc_ventas:
        flash("Este codigo de encargado de ventas ya esta registrado")
        return redirect('/cambiarcontrasena')
    if nombres_enc_ventas:
        flash("Este nombre de encargado de ventas ya esta registrado")
        return redirect('/cambiarcontrasena')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_ventas, datos_enc_ventas)
        bd.commit()

        return redirect('/cambiarcontrasena')

# CAMBIAR CONTRASEÑA - CREADOR ENCARGADO DE COMPRAS
@app.route('/cambiarcontrasena/encCompras/bd', methods=['post'])
def cambiarcontrasena_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT codigo_encargadoC FROM `encargados_com` WHERE codigo_encargadoC=%s AND id_usuario=%s",(codigo_enc_compras,session['id_usuario']))
    codigos_enc_compras=bdsql.fetchall()
    bd.commit()

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT nombre_encargadoC FROM `encargados_com` WHERE nombre_encargadoC=%s AND id_usuario=%s",(nombre_enc_compras,session['id_usuario']))
    nombres_enc_compras=bdsql.fetchall()
    bd.commit()

    if codigos_enc_compras:
        flash("Este codigo de encargado de compras ya esta registrado")
        return redirect('/cambiarcontrasena')
    if nombres_enc_compras:
        flash("Este nombre de encargado de compras ya esta registrado")
        return redirect('/cambiarcontrasena')
    else:
        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql_enc_compras, datos_enc_compras)
        bd.commit()

        return redirect('/cambiarcontrasena')

# CAMBIAR CONTRASEÑA - ELIMINAR CUENTA
@app.route('/cambiarcontrasena/eliminar_cuenta/bd', methods=['post'])
def cambiarcontrasena_eliminar_cuenta_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    eliminar_cuenta=bdsql.fetchall()
    bd.commit()
    print(eliminar_cuenta)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port="4000")