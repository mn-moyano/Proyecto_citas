# Importamos Flask y render_template
from flask import Flask, render_template
import os

#Importamos base de datos y modelo
from base_datos import obtener_conexion, crear_tabla_productos
from modelos import Producto

# Creamos la aplicación
app = Flask(__name__)

#Crear tabla al iniciar
crear_tabla_productos()

# Ruta principal → ahora renderiza index.html
@app.route("/")
def index():
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

#Inventario
@app.route("/inventario")
def inventario():
    conn = obtener_conexion()
    productos_db = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()

    #Diccionario
    inventario = {}
    for fila in productos_db:
        producto = Producto(
            fila["id"],
            fila["nombre"],
            fila["cantidad"],
            fila["precio"]
        )
        inventario[producto.id] = producto

    return render_template("inventario.html", inventario = inventario)

#Agregar producto
@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        conn = obtener_conexion()
        conn.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (nombre,cantidad, precio)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("inventario"))
    return render_template("agregar_producto.html")
# Ejecutar aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)