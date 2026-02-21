# Importamos Flask y render_template
from flask import Flask, render_template
import os

# Creamos la aplicación
app = Flask(__name__)

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

# Ejecutar aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)