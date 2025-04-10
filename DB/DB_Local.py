import sqlite3
import logging
import os


class DBLocal:
    def __init__(self, business_name, db_directory=None):
        """
        Inicializa la clase con el archivo de base de datos existente en el formato DB_(nombre del negocio).db.
        :param business_name: Nombre del negocio utilizado para construir la ruta del archivo de base de datos.
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

    def create_tables(self):
        """
        Crea las tablas requeridas para el modo Local en la base de datos existente.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Crear tabla de cafeterías
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS cafeterias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cafe_name TEXT NOT NULL
                )
                """)

                # Insertar cafetería predeterminada si no existe
                cursor.execute("""
                INSERT INTO cafeterias (id, cafe_name)
                SELECT 1, 'default'
                WHERE NOT EXISTS (SELECT 1 FROM cafeterias WHERE id = 1)
                """)

                # Crear tabla categories con columnas start_range y end_range
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS category_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_range TEXT NOT NULL,
                    end_range TEXT NOT NULL
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
                
                # Crear tabla de productos existentes
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos_existentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT,
                    precio_costo REAL,
                    cantidad INTEGER,
                    fecha TEXT
                )
                """)

                # Crear tabla de transferencias exitosas
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS transferencias_exitosas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    transferencia TEXT,
                    cafe_id INTEGER
                )
                """)

                # Crear tabla de transferencias recibidas
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS transferencias_recibidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    transferencia TEXT,
                    cafe_id INTEGER,
                    fecha_transferencia TEXT DEFAULT (datetime('now','localtime'))
                )
                """)

                logging.info("Tablas principales creadas exitosamente.")
                conn.commit()

        except sqlite3.OperationalError as e:
            logging.error(f"Error operacional al crear tablas: {e}")
        except Exception as e:
            logging.error(f"Otro error ocurrió al crear tablas: {e}")

    def create_dynamic_table(self, table_name, schema):
        """Crear tablas dinámicas reutilizando código."""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
                logging.info(f"Tabla dinámica creada: {table_name}")
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error al crear tabla dinámica: {e}")
        except Exception as e:
            logging.error(f"Otro error ocurrió al crear tabla dinámica: {e}")