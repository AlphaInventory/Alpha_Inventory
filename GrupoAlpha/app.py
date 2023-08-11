import os

from flask import Flask

from flask import render_template, request, redirect, session, flash

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

costo_total = 0

precio_total = 0

precio_total_articulos = 0

#SITIO
@app.route('/')
def index():
    return render_template('sitio/index.html')

@app.route('/', methods=['post'])
def index_entrar():

    correo_electronico=request.form['email']
    contrasena=request.form['password']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT id_usuario, correo_electronico, contrasena FROM `registro_usuario` WHERE correo_electronico = %s AND contrasena = %s", (correo_electronico, contrasena))
    registro_usuario=bdsql.fetchone()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE correo_electronico = %s", (correo_electronico))
    correo_electronicoR=bdsql.fetchall()

    if registro_usuario:
        session['logueado'] = True
        session['id_usuario'] = list(str(registro_usuario[0]))
        # return f"el id es {session['id_usuario']}"
        return redirect('/inicio_inventario')
    if not correo_electronicoR:
        flash("El correo electronico no esta registrado", 'error')
        return redirect('/')
    if not registro_usuario:
        flash("El correo electronico o la contraseña son incorrectos", 'warning')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/cerrar_sesion')
def index_salir():
    session.clear()
    return redirect('/')

@app.route('/inicio_inventario')
def inicio_inventario():

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
    
    return render_template('sitio/inicio_inventario.html', marcas=marcas, encargado_ventas=encargado_ventas,encargado_compras=encargado_compras)
    
@app.route('/inicio_inventario/marcas/bd', methods=['post'])
def inicio_inventario_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s,%s)")

    datos_marcas=(codigo_marca, nombre_marca,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/inicio_inventario')

@app.route('/inicio_inventario/encVentas/bd', methods=['post'])
def inicio_inventario_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`, `id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas,nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/inicio_inventario')

@app.route('/inicio_inventario/encCompras/bd', methods=['post'])
def inicio_inventario_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/inicio_inventario')

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

@app.route('/movimientosdiario')
def movimiento_diario():

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

    global costo_total
    global precio_total

    return render_template ('sitio/movimientosdiario.html', ventas=ventas, compras=compras, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, costo_total=costo_total, precio_total=precio_total)

@app.route('/movimientosdiario/marcas/bd', methods=['post'])
def movimientosdiario_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/movimientosdiario')

@app.route('/movimientosdiario/encVentas/bd', methods=['post'])
def movimientosdiario_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/movimientosdiario')

@app.route('/movimientosdiario/encCompras/bd', methods=['post'])
def movimientosdiario_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/movimientosdiario')

@app.route('/movimientosdiario/eliminar_cuenta/bd', methods=['post'])
def movimientosdiario_eliminar_cuenta_bd():

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

@app.route('/movimientoporarticulo')
def movimiento_articulo():

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

    return render_template ('sitio/movimientoporarticulo.html', ventas=ventas, compras=compras, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

@app.route('/movimientoporarticulo/marcas/bd', methods=['post'])
def movimientoporarticulo_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/movimientosdiario')

@app.route('/movimientoporarticulo/encVentas/bd', methods=['post'])
def movimientoporarticulo_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/movimientosdiario')

@app.route('/movimientoporarticulo/encCompras/bd', methods=['post'])
def movimientoporarticulo_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/movimientosdiario')

@app.route('/movimientoporarticulo/eliminar_cuenta/bd', methods=['post'])
def movimientoporarticulo_eliminar_cuenta_bd():

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

@app.route('/listadodearticulos')
def costo_inventario():

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

    global precio_total_articulos

    return render_template ('sitio/listadodearticulos.html', articulos=articulos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, precio_total_articulos=precio_total_articulos)

@app.route('/listadodearticulos/marcas/bd', methods=['post'])
def listadodearticulos_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/listadodearticulos')

@app.route('/listadodearticulos/encVentas/bd', methods=['post'])
def listadodearticulos_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/listadodearticulos')

@app.route('/listadodearticulos/encCompras/bd', methods=['post'])
def listadodearticulos_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/listadodearticulos')

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

    return render_template('sitio/listadodeprecios.html', articulos=precios, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

@app.route('/listadodeprecios/marcas/bd', methods=['post'])
def listadodeprecios_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/listadodeprecios')

@app.route('/listadodeprecios/encVentas/bd', methods=['post'])
def listadodeprecios_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/listadodeprecios')

@app.route('/listadodeprecios/encCompras/bd', methods=['post'])
def listadodeprecios_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/listadodeprecios')

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

    global costo_total

    return render_template('sitio/listadodecompras.html', compras=compras, suplidores=suplidores, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, costo_total=costo_total)

@app.route('/listadodecompras/marcas/bd', methods=['post'])
def listadodecompras_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/listadodecompras')

@app.route('/listadodecompras/encVentas/bd', methods=['post'])
def listadodecompras_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/listadodecompras')

@app.route('/listadodecompras/encCompras/bd', methods=['post'])
def listadodecompras_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/listadodecompras')

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

    global precio_total

    return render_template('sitio/listadodeventas.html', ventas=ventas, clientes=clientes, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras, precio_total=precio_total)

@app.route('/listadodeventas/marcas/bd', methods=['post'])
def listadodeventas_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/listadodeventas')

@app.route('/listadodeventas/encVentas/bd', methods=['post'])
def listadodeventas_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/listadodeventas')

@app.route('/listadodeventas/encCompras/bd', methods=['post'])
def listadodeventas_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/listadodeventas')

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
    
    return render_template('sitio/listadodeclientes.html', clientes=clientes, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

@app.route('/listadodeclientes/marcas/bd', methods=['post'])
def listadodeclientes_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca,session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/listadodeclientes')

@app.route('/listadodeclientes/encVentas/bd', methods=['post'])
def listadodeclientes_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/listadodeclientes')

@app.route('/listadodeclientes/encCompras/bd', methods=['post'])
def listadodeclientes_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/listadodeclientes')

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

    return render_template('sitio/listadodesuplidores.html', suplidores=suplidores, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

@app.route('/listadodesuplidores/marcas/bd', methods=['post'])
def listadodesuplidores_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/listadodesuplidores')

@app.route('/listadodesuplidores/encVentas/bd', methods=['post'])
def listadodesuplidores_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/listadodesuplidores')

@app.route('/listadodesuplidores/encCompras/bd', methods=['post'])
def listadodesuplidores_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/listadodesuplidores')

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

@app.route('/perfil/marcas/bd', methods=['post'])
def perfil_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/perfil')

@app.route('/perfil/encVentas/bd', methods=['post'])
def perfil_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/perfil')

@app.route('/perfil/encCompras/bd', methods=['post'])
def perfil_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras,)
    bd.commit()

    return redirect('/perfil')

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

@app.route('/terminosycondiciones/marcas/bd', methods=['post'])
def terminosycondiciones_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/terminosycondiciones')

@app.route('/terminosycondiciones/encVentas/bd', methods=['post'])
def terminosycondiciones_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/terminosycondiciones')

@app.route('/terminosycondiciones/encCompras/bd', methods=['post'])
def terminosycondiciones_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/terminosycondiciones')

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

@app.route('/registrate')
def registrate():
    
    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario`")
    registro_usuario=bdsql.fetchall()

    return render_template('admin/registrate.html', registro_usuario=registro_usuario)

@app.route('/registrate/bd', methods=['post'])
def registro_usuario():

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
        return redirect('/registrate')
    if contrasena == contrasena_:
        session['contrasena_iguales'] = True

        sql= ("INSERT INTO `registro_usuario` (`id_usuario`,`nombre`,`apellido`,`direccion`,`telefono`,`correo_electronico`,`contrasena`) VALUES (NULL, %s, %s, %s, %s, %s, %s);")

        datos=(nombre, apellido, direccion, telefono, correo_electronico, contrasena)

        bd=mysql.connect()
        bdsql=bd.cursor()
        bdsql.execute(sql, datos)
        bd.commit()
        return redirect('/metododepago')
    if contrasena != contrasena_:
        flash("Las contraseñas no coinciden")
        return redirect('/registrate')
    else:
        return redirect('/registrate')

@app.route('/registrate/olvidastetucontrasena/bd', methods=['post'])
def olvidaste_contrasena_bd():

    recipients=request.form['correo']

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT correo_electronico FROM `registro_usuario` WHERE correo_electronico=%s",(recipients))
    olvidaste_contrasena=bdsql.fetchall()
    
    if olvidaste_contrasena:
        session['registrado'] = recipients
        msg = Message('AlphaInventory.SRL', sender = 'grupoalpha.infotep@gmail.com', recipients=[recipients])
        msg.html = "Hola,<br>¡Hubo una solicitud para cambiar su contraseña!<br>Si no realizó esta solicitud, ignore este correo electrónico.<br>De lo contrario, ingrese a este enlace para cambiar su contraseña: <a href='http://127.0.0.1:5000/recuperarcontrasena' target='blank'>Enlace</a>"
        mail.send(msg)

        return redirect('/')
    else:
        return redirect('/registrate')
    
@app.route('/metododepago')
def metodo_pago():

    if not 'contrasena_iguales' in session:
        return redirect('/registrate')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `metodo_pago`")
    metodo_pago=bdsql.fetchall()

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario`")
    registro_usuario=bdsql.fetchall()

    return render_template('admin/metododepago.html', metodo_pago=metodo_pago, registro_usuario=registro_usuario)

@app.route('/metododepago/bd', methods=['post'])
def metodo_pago_bd():
    
    numero_tarjeta=request.form['inputNumero']
    nombre_tarjeta=request.form['inputNombre']
    mes=request.form['selectMes']
    año=request.form['selectYear']
    cvv=request.form['inputCCV']
    id_usuario=request.form['id_usuario']

    sql_met_pag= ("INSERT INTO `metodo_pago` (`id_metodo_pago`,`numero_tarjeta`,`nombre_tarjeta`,`mes`,`año`,`cvv`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s);")

    datos_metodo_pago=(numero_tarjeta, nombre_tarjeta, mes, año, cvv, id_usuario)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_met_pag, datos_metodo_pago)
    bd.commit()

    return redirect('/')

@app.route('/recuperarcontrasena')
def recuperar_contrasena():

    if not 'registrado' in session:
        return redirect('/olvidastetucontrasena')

    bdsql=mysql.connect().cursor()
    bdsql.execute("SELECT * FROM `registro_usuario`")
    recuperar_contrasena=bdsql.fetchall()

    return render_template('admin/recuperarcontrasena.html', recuperar_contrasena=recuperar_contrasena)

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

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE registro_usuario SET contrasena = %s WHERE id=%s",(contrasena, id))
    bd.commit()

    return redirect('/')

@app.route('/registrodearticulos')
def registro_articulos():

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

    return render_template('admin/registrodearticulos.html', articulos=articulos, marcas=marcas, encargado_ventas=encargado_ventas, encargado_compras=encargado_compras)

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
    cantidad=request.form['cant']
    margen_beneficio=request.form['margen']
    unidad_medida=request.form['medida']

    total_articulos = int(cantidad)*int(precio)

    global precio_total_articulos
    precio_total_articulos =  total_articulos + precio_total_articulos

    sql_articulos=('INSERT INTO `articulos` (`id_articulo`,`codigo`,`descripcion`,`talla`,`marca`,`referencia`,`ubicacion`,`costo`,`precio`,`itbis`,`cantidad`,`margen_beneficio`,`unidad_medida`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    datos_articulos=(codigo,descripcion,talla,marca,referencia,ubicacion,costo,precio,itbis,cantidad,margen_beneficio,unidad_medida, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_articulos, datos_articulos)
    bd.commit()

    return redirect('/registrodearticulos')

@app.route('/registrodearticulos/marcas/bd', methods=['post'])
def registrodearticulos_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/registrodearticulos')

@app.route('/registrodearticulos/encVentas/bd', methods=['post'])
def registrodearticulos_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/registrodearticulos')

@app.route('/registrodearticulos/encCompras/bd', methods=['post'])
def registrodearticulos_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/registrodearticulos')

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

@app.route('/registrodeclientes/bd', methods=['post'])
def registro_clientes_bd():

    codigo=request.form['codigo']
    nombre=request.form['nom']
    direccion=request.form['dir']
    cuidad=request.form['ciudad']
    telefono=request.form['tel']
    cedula=request.form['cedula']
    email=request.form['email']
    rnc=request.form['rnc']
    descuentos=request.form['descuento']

    sql_clientes=('INSERT INTO `clientes` (`id_cliente`,`codigo`,`nombre`,`direccion`,`ciudad`,`telefono`,`cedula`,`email`,`rnc`,`descuentos`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    datos_clientes=(codigo,nombre,direccion,cuidad,telefono,cedula,email,rnc,descuentos, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_clientes, datos_clientes)
    bd.commit()

    return redirect('/registrodeclientes')

@app.route('/registrodeclientes/marcas/bd', methods=['post'])
def registrodeclientes_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/registrodeclientes')

@app.route('/registrodeclientes/encVentas/bd', methods=['post'])
def registrodeclientes_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/registrodeclientes')

@app.route('/registrodeclientes/encCompras/bd', methods=['post'])
def registrodeclientes_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/registrodeclientes')

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

    sql_suplidores= ("INSERT INTO `suplidores` (`id_suplidor`,`codigo`,`nombre`,`direccion`,`ciudad`,`telefono`,`limite_credito`,`condiciones`,`rnc`,`descuentos`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    datos_suplidores=(codigo,nombre,direccion,ciudad,telefono,limite_credito,condiciones,rnc,descuentos, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_suplidores, datos_suplidores)
    bd.commit()

    return redirect('/registrodesuplidores')

@app.route('/registrodesuplidores/marcas/bd', methods=['post'])
def registrodesuplidores_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/registrodesuplidores')

@app.route('/registrodesuplidores/encVentas/bd', methods=['post'])
def registrodesuplidores_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/registrodesuplidores')

@app.route('/registrodesuplidores/encCompras/bd', methods=['post'])
def registrodesuplidores_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/registrodesuplidores')

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

@app.route('/compras/bd', methods=['post'])
def compras_registro_bd():

    numero_facturaC=request.form['fact']
    fecha_compra=request.form['date']
    encargado_compra=request.form['Encargado']
    suplidor=request.form['suplidores']
    codigo=request.form['codigo']
    cantidad=request.form['cantidad']
    itbis=request.form['itbis']
    costo=request.form['costo']

    tiempo=datetime.now()
    horaCompra=tiempo.strftime('%H:%M:%S')

    total_compra=int(cantidad)*int(costo)

    global costo_total
    costo_total = total_compra + costo_total

    sql=("INSERT INTO `compras`(`id_compra`,`numero_facturaC`,`horaCompra`,`fecha_compra`,`encargado_compra`,`suplidor`,`codigo`,`cantidad`,`itbis`,`costo`,`total_compra`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    datos=(numero_facturaC,horaCompra,fecha_compra,encargado_compra,suplidor,codigo,cantidad,itbis,costo,total_compra, session['id_usuario'])
    
    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql,datos)
    bd.commit()

    return redirect('/compras')

@app.route('/compras/marcas/bd', methods=['post'])
def compras_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/compras')

@app.route('/compras/encVentas/bd', methods=['post'])
def compras_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/compras')

@app.route('/compras/encCompras/bd', methods=['post'])
def compras_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/compras')

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

@app.route('/ventas/bd', methods=['post'])
def ventas_registro_bd():

    numero_facturaV=request.form['fact']
    fecha_venta=request.form['date']
    encargado_venta=request.form['Encargado']
    cliente=request.form['cliente']
    codigo=request.form['codigo']
    cantidad=request.form['cantidad']
    itbis=request.form['itbis']
    precio=request.form['precio']

    tiempo=datetime.now()
    horaVenta=tiempo.strftime('%H:%M:%S')

    total_venta=int(cantidad)*int(precio)

    global precio_total
    precio_total = total_venta + precio_total

    sql=("INSERT INTO `ventas`(`id_venta`,`numero_facturaV`,`horaVenta`,`fecha_venta`,`encargado_venta`,`cliente`,`codigo`,`cantidad`,`itbis`,`precio`,`total_venta`,`id_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    datos=(numero_facturaV,horaVenta,fecha_venta,encargado_venta,cliente,codigo,cantidad,itbis,precio,total_venta, session['id_usuario'])
    
    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql,datos)
    bd.commit()

    return redirect('/ventas')

@app.route('/ventas/marcas/bd', methods=['post'])
def ventas_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`) VALUES (NULL, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/ventas')

@app.route('/ventas/encVentas/bd', methods=['post'])
def ventas_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/ventas')

@app.route('/ventas/encCompras/bd', methods=['post'])
def ventas_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/ventas')

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

@app.route('/respaldos/eliminar/bd', methods=['post'])
def respaldos_eliminar_bd():

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `respaldos` WHERE id_respaldo=%s",(session['id_usuario']))
    respaldos=bdsql.fetchall()
    bd.commit()
    print(respaldos)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("DELETE FROM `respaldos` WHERE id_respaldo=%s",(session['id_usuario']))
    bd.commit()

    return redirect('/respaldos')

@app.route('/respaldos/marcas/bd', methods=['post'])
def respaldos_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/respaldos')

@app.route('/respaldos/encVentas/bd', methods=['post'])
def respaldos_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/respaldos')

@app.route('/respaldos/encCompras/bd', methods=['post'])
def respaldos_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/respaldos')

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

@app.route('/perfileditar/bd', methods=['post'])
def perfil_bd():

    correo_electronico=request.form['email']
    direccion=request.form['dir']
    telefono=request.form['tel']

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("SELECT * FROM `registro_usuario` WHERE id_usuario=%s",(session['id_usuario']))
    backup=bdsql.fetchall()
    bd.commit()
    print(backup)

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute("UPDATE registro_usuario SET direccion = %s, telefono = %s, correo_electronico = %s WHERE id_usuario=%s",(direccion, telefono, correo_electronico, session['id_usuario']))
    bd.commit()
    
    return redirect('/inicio_inventario')

@app.route('/perfileditar/marcas/bd', methods=['post'])
def perfileditar_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/perfileditar')

@app.route('/perfileditar/encVentas/bd', methods=['post'])
def perfileditar_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/perfileditar')

@app.route('/perfileditar/encCompras/bd', methods=['post'])
def perfileditar_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/perfileditar')

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

@app.route('/cambiarcontrasena/marcas/bd', methods=['post'])
def cambiarcontrasena_marcas_bd():

    codigo_marca=request.form['codigo_marca']
    nombre_marca=request.form['nombre_marca']

    sql_marcas= ("INSERT INTO `marcas` (`id_marca`,`codigo_marca`,`nombre_marca`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_marcas=(codigo_marca, nombre_marca, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_marcas, datos_marcas)
    bd.commit()    

    return redirect('/cambiarcontrasena')

@app.route('/cambiarcontrasena/encVentas/bd', methods=['post'])
def cambiarcontrasena_enc_ventas_bd():

    codigo_enc_ventas=request.form['codigo_enc_ventas']
    nombre_enc_ventas=request.form['nombre_enc_ventas']

    sql_enc_ventas= ("INSERT INTO `encargados_ven` (`id_encargadoV`,`codigo_encargadoV`,`nombre_encargadoV`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_ventas=(codigo_enc_ventas, nombre_enc_ventas, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_ventas, datos_enc_ventas)
    bd.commit()

    return redirect('/cambiarcontrasena')

@app.route('/cambiarcontrasena/encCompras/bd', methods=['post'])
def cambiarcontrasena_enc_compras_bd():

    codigo_enc_compras=request.form['codigo_enc_compras']
    nombre_enc_compras=request.form['nombre_enc_compras']

    sql_enc_compras= ("INSERT INTO `encargados_com` (`id_encargadoC`,`codigo_encargadoC`,`nombre_encargadoC`,`id_usuario`) VALUES (NULL, %s, %s, %s)")

    datos_enc_compras=(codigo_enc_compras, nombre_enc_compras, session['id_usuario'])

    bd=mysql.connect()
    bdsql=bd.cursor()
    bdsql.execute(sql_enc_compras, datos_enc_compras)
    bd.commit()

    return redirect('/cambiarcontrasena')

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
    app.run(debug=True)