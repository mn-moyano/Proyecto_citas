# Importamos Flask y render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from form import ProductoForm
from inventario.bd import init_db, get_db_connection
from inventario.inventario import Inventario
import os
# Creamos la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'

#Crear tabla al iniciar
init_db()
inventario = Inventario()
inventario.cargar_desde_db()

# Ruta principal → ahora renderiza index.html
@app.route("/")
def inicio():
    return render_template("index.html")

# Página Acerca de
@app.route("/about")
def about():
    return render_template("about.html")

# Página de Pacientes
@app.route("/pacientes")
def pacientes():
    return render_template("pacientes.html")

# Página de Citas
@app.route("/citas")
def citas():
    return render_template("citas.html")

# Página de Facturación
@app.route("/facturas")
def facturas():
    return render_template("facturas.html")

#Ruta para listar productos
@app.route('/productos')
def productos_listar():
    inventario.cargar_desde_db()
    productos = list(inventario.productos.values())
    return render_template('productos.html', productos=productos)

#Nuevo producto
@app.route("/productos/nuevo", methods=['GET', 'POST'])
def producto_nuevo():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        inventario.agregar_producto(nombre, descripcion, cantidad, precio)
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('productos_listar'))
    return render_template('producto_form.html', form=form)


#Ruta para editar producto
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    producto = inventario.productos.get(id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos_listar'))
    
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        cantidad = int(form.cantidad.data)
        precio = float(form.precio.data)
        inventario.actualizar_producto(id, nombre, descripcion, cantidad, precio)
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('productos_listar'))
    return render_template('producto_form.html', form=form, producto=producto)

#Ruta para eliminar producto
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def producto_eliminar(id):
    inventario.eliminar_producto(id)
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos_listar'))

def listar_productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return productos

#Ruta clientes
@app.route('/clientes')
def clientes():
    return 'Aquí puedes ver nuestros clientes'

#Ruta formulario
@app.route('/formulario')
def formulario():
    return 'producto_form.html'

# Ejecutar aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)