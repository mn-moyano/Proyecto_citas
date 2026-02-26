import sqlite3

def obtener_conexion():
    conn = sqlite3.connect("clinica.db")
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla_productos():
    conn = obtener_conexion()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()