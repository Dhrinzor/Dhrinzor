import os
import shutil
import sqlite3

def initialize_database(business_name):
    """
    Inicializa la base de datos para el negocio proporcionado.
    Mueve archivos .db al disco C:\MagicCorp\DB y configura el archivo DB_{business_name}.db con las tablas requeridas.
    """
    magiccorp_path = os.path.join("C:\\", "MagicCorp")
    db_dest_path = os.path.join(magiccorp_path, "DB")

    # Asegurar que las carpetas de destino existan
    if not os.path.exists(magiccorp_path):
        os.mkdir(magiccorp_path)
    if not os.path.exists(db_dest_path):
        os.mkdir(db_dest_path)

    # Ruta de origen de la carpeta DB local
    source_folder = os.path.join(os.getcwd(), "DB")
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"No se encontró la carpeta de origen: {source_folder}")

    # Mover archivos .db al destino
    db_files = [f for f in os.listdir(source_folder) if f.endswith(".db")]
    if not db_files:
        raise FileNotFoundError("No se encontraron archivos .db en la carpeta de origen.")

    for file in db_files:
        src_path = os.path.join(source_folder, file)
        dest_path = os.path.join(db_dest_path, file)
        shutil.move(src_path, dest_path)
        print(f"Archivo movido: {file} -> {dest_path}")

    # Trabajar con el archivo específico DB_{business_name}.db
    business_db_path = os.path.join(db_dest_path, f"DB_{business_name}.db")
    if not os.path.exists(business_db_path):
        # Crear el archivo si no existe
        open(business_db_path, "w").close()
        print(f"Archivo de base de datos creado: {business_db_path}")

    conn = sqlite3.connect(business_db_path)
    cursor = conn.cursor()

    # Crear las tablas específicas para el negocio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS negocio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO negocio (nombre) VALUES (?)
    """, (business_name,))
    conn.commit()
    conn.close()

    print(f"Base de datos configurada correctamente para el negocio: {business_name}")