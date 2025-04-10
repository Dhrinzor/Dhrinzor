import sqlite3
import os


class DBLocalIndependiente:
    def __init__(self, business_name, db_directory=None):
        """
        Inicializa la clase con el archivo de base de datos existente en el formato DB_(nombre del negocio).db.
        :param business_name: Nombre del negocio, utilizado para construir la ruta del archivo de base de datos.
        :param db_directory: Directorio donde se encuentra la base de datos.
        """
        db_directory = db_directory or os.path.join("C:\\", "MagicCorp", "DB")
        self.db_path = os.path.join(db_directory, f"DB_{business_name}.db")

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"No se encontró el archivo de base de datos: {self.db_path}")

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

    def setup_local_independent_tables(self):
        """Crea las tablas necesarias para el modo local independiente dentro de la base de datos existente."""
        try:
            conn = self.connect()
            if not conn:
                return
            cursor = conn.cursor()

            # Crear las tablas requeridas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS almacen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT,
                    cantidad INTEGER,
                    precio_costo REAL,
                    precio_venta REAL,
                    fecha TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS venta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Producto_vender TEXT,
                    cantidad INTEGER,
                    precio REAL,
                    fecha TEXT DEFAULT (datetime('now','localtime'))
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Producto_vendido TEXT,
                    cantidad_vendida INTEGER,
                    precio REAL,
                    fecha TEXT DEFAULT (datetime('now','localtime')),
                    vendedor TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT,
                    precio_costo REAL,
                    precio_venta REAL,
                    cantidad INTEGER,
                    fecha TEXT,
                    beneficios REAL,
                    disponibilidad BOOL
                )
            """)

            # Confirmar los cambios
            conn.commit()
            print("Tablas para el modo Local Independiente configuradas correctamente.")
        except sqlite3.Error as e:
            print(f"Error al configurar las tablas del modo Local Independiente: {e}")
        finally:
            if conn:
                conn.close()

    def insert_data(self, table_name, data):
        """
        Inserta datos en una tabla específica.
        :param table_name: Nombre de la tabla donde se insertarán los datos.
        :param data: Diccionario con los campos y valores a insertar.
        """
        try:
            conn = self.connect()
            if not conn:
                return

            # Construir la consulta de inserción dinámica
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data.values()])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            conn.execute(query, tuple(data.values()))
            conn.commit()
            print(f"Datos insertados correctamente en la tabla {table_name}.")
        except sqlite3.Error as e:
            print(f"Error al insertar datos en la tabla {table_name}: {e}")
        finally:
            if conn:
                conn.close()

    def fetch_data(self, table_name):
        """
        Recupera todos los datos de una tabla.
        :param table_name: Nombre de la tabla.
        :return: Lista de registros.
        """
        try:
            conn = self.connect()
            if not conn:
                return []

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error al recuperar datos de la tabla {table_name}: {e}")
            return []
        finally:
            if conn:
                conn.close()