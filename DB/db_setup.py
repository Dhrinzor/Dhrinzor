import sqlite3
import os

def initialize_database(db_name):
    # Asegurarse de que la carpeta "DB" exista
    db_folder = os.path.join(os.getcwd(), "DB")
    if not os.path.exists(db_folder):
        os.mkdir(db_folder)

    # Ruta del archivo de la base de datos
    db_path = os.path.join(db_folder, f"DB_{db_name}.db")

    # Crear conexión con SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear la tabla inicial para el negocio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS negocio (
            business_name TEXT NOT NULL
        )
    """)

    # Insertar el nombre del negocio en la tabla
    cursor.execute("""
        INSERT INTO negocio (business_name) VALUES (?)
    """, (db_name,))

    conn.commit()
    conn.close()
    print(f"Base de datos creada en: {db_path}")