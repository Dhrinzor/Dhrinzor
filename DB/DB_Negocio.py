import sqlite3
import os


class DBNegocio:
    def __init__(self, db_path):
        # Define la ruta de la base de datos (debe proporcionarse un archivo existente)
        self.db_path = db_path
        self.verify_database_exists()

    def verify_database_exists(self):
        """
        Asegúrate de que el archivo de la base de datos exista.
        """
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"La base de datos '{self.db_path}' no existe. Por favor, mueva el archivo a la carpeta correcta antes de proceder.")

    def connect(self):
        """
        Conecta a la base de datos especificada.
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

    def setup_negocio_tables(self):
        """
        Configura las tablas específicas del modo 'Empresa' en la base de datos existente.
        """
        try:
            conn = self.connect()
            if not conn:
                return
            cursor = conn.cursor()

            # Crear las tablas específicas del modo negocio
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS almacen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT NOT NULL,
                    precio_costo REAL,
                    cantidad INTEGER,
                    fecha TEXT,
                    importe REAL,
                    deposito REAL,
                    inventario_almacen REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cafeterias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cafe_name TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS category_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_range TEXT NOT NULL,
                    end_range TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos_existentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT NOT NULL,
                    precio_costo REAL,
                    cantidad INTEGER,
                    fecha TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transferencias_exitosas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    transferencia TEXT,
                    cafe_id INTEGER
                )
            """)

            # Confirmar los cambios en la base de datos
            conn.commit()
            print(f"Tablas del modo negocio configuradas exitosamente en '{self.db_path}'.")
        except sqlite3.Error as e:
            print(f"Error al configurar las tablas del modo negocio en '{self.db_path}': {e}")
        finally:
            if conn:
                conn.close()