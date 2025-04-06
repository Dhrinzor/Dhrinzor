import sqlite3
import logging
from pages.authentication.utils.KeyManager import KeyManager  # Asumimos que este módulo contiene KeyManager
from datetime import datetime

class InventoryDB:
    def __init__(self):
        self.conn = sqlite3.connect("DB/data_hub.db") 
        self.key_manager = KeyManager()  # Crear instancia de KeyManager 
        self.encryption_key = self.key_manager.encryption_key  # Obtener la clave de encriptación 
        self.decryption_key = self.key_manager.decryption_key  # Obtener la clave de desencriptación 
        self.setup_logging()  # Configurar el sistema de registro
        self.create_tables()

    def setup_logging(self):
        """Configurar el sistema de logs"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def connect(self):
        """Permitir el uso de la conexión en diferentes hilos"""
        return sqlite3.connect("DB/data_hub.db", check_same_thread=False)
    
    def encrypt_value(self, value):
        """Encriptar valores sensibles"""
        if value == "DEPÓSITO":
            return value
        return ''.join(self.encryption_key.get(char, char) for char in str(value))
    
    def decrypt_value(self, value):
        """Desencriptar valores sensibles"""
        if value is None:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return ''.join(self.decryption_key.get(value[i:i+5], value[i:i+5]) for i in range(0, len(value), 5))
    
    def sanitize_table_name(self, name):
        if not isinstance(name, str):
            name = str(name)  # Convertir a cadena si no lo es
        return ''.join(c for c in name if c.isalnum() or c == '_')

    def create_tables(self):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Crear tabla de almacen
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

                logging.info("Tablas principales creadas exitosamente.")
                conn.commit()

        except sqlite3.OperationalError as e:
            logging.error(f"Error operacional al crear tablas: {e}")
        except Exception as e:
            logging.error(f"Otro error ocurrió al crear tablas: {e}")
        
    def create_dynamic_table(self, table_name, schema):
        """Crear tablas dinámicas reutilizando código"""
        try:
            table_name = self.sanitize_table_name(table_name)  # Validar nombre
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
                logging.info(f"Tabla dinámica creada: {table_name}")
                conn.commit()
        except sqlite3.OperationalError as e:
            logging.error(f"Error operacional al crear tabla dinámica: {e}")
        except Exception as e:
            logging.error(f"Otro error ocurrió al crear tabla dinámica: {e}")

    def create_inventory_table_for_cafe(self, cafe_id):
        """Crear inventario para cada cafetería"""
        table_name = f"cafe_{self.sanitize_table_name(cafe_id)}_inventory"
        schema = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            precio_costo REAL,
            precio_venta REAL,
            cantidad INTEGER,
            fecha TEXT,
            beneficios REAL,
            disponibilidad BOOL
        """
        self.create_dynamic_table(table_name, schema)

    def crear_almacen_establecimiento(self, establecimiento):
        """Crear tablas relacionadas con el almacén del establecimiento"""
        table_name = f"Almacen_{self.sanitize_table_name(establecimiento)}"
        table_name_venta = f"productos_a_vender_{self.sanitize_table_name(establecimiento)}"
        table_name_vendidos = f"productos_vendidos_{self.sanitize_table_name(establecimiento)}"

        schema_almacen = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            cantidad INTEGER,
            precio_costo REAL,
            precio_venta REAL,
            fecha TEXT
        """
        schema_venta = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Producto_vender TEXT,
            cantidad INTEGER,
            precio REAL,
            fecha TEXT DEFAULT (datetime('now','localtime'))
        """
        schema_vendidos = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Producto_vendido TEXT,
            cantidad_vendida INTEGER,
            precio REAL,
            fecha TEXT DEFAULT (datetime('now','localtime')),
            vendedor TEXT
        """

        self.create_dynamic_table(table_name, schema_almacen)
        self.create_dynamic_table(table_name_venta, schema_venta)
        self.create_dynamic_table(table_name_vendidos, schema_vendidos)

################INSERT##################################################################################################
    def insert_almacen_item(self, producto, precio_costo, cantidad, fecha, importe, deposito, inventario_almacen):
        # Formatear los valores numéricos a dos decimales
        precio_costo = round(float(precio_costo), 2)
        importe = round(float(importe), 2)
        
        encrypted_producto = self.encrypt_value(producto)
        encrypted_precio_costo = self.encrypt_value(str(precio_costo))
        encrypted_cantidad = self.encrypt_value(str(cantidad))
        encrypted_fecha = self.encrypt_value(fecha)
        encrypted_importe = self.encrypt_value(str(importe))
        encrypted_deposito = self.encrypt_value(str(deposito))
        encrypted_inventario_almacen = self.encrypt_value(str(inventario_almacen))
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO almacen (producto, precio_costo, cantidad, fecha, importe, deposito, inventario_almacen) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (encrypted_producto, encrypted_precio_costo, encrypted_cantidad, encrypted_fecha, encrypted_importe, encrypted_deposito, encrypted_inventario_almacen))
            
            # Omitir la inserción en productos_existentes si el producto es "DEPÓSITO"
            if producto.lower() == "depósito":
                conn.commit()
                return
            
            # Verificar si el producto ya existe en la tabla productos_existentes
            cursor.execute("SELECT id, precio_costo, cantidad FROM productos_existentes WHERE producto = ?", (encrypted_producto,))
            existing_product = cursor.fetchone()

            if existing_product:
                # Actualizar el producto en la tabla productos_existentes
                existing_id = existing_product[0]
                existing_precio_costo = float(self.decrypt_value(existing_product[1]))
                existing_cantidad = int(self.decrypt_value(existing_product[2]))

                new_cantidad = existing_cantidad + int(cantidad)
                new_precio_costo = ((existing_precio_costo * existing_cantidad) + (float(precio_costo) * int(cantidad))) / new_cantidad
                new_precio_costo = round(new_precio_costo, 2)  # Formatear a dos decimales

                encrypted_new_precio_costo = self.encrypt_value(str(new_precio_costo))
                encrypted_new_cantidad = self.encrypt_value(str(new_cantidad))
                cursor.execute("""
                UPDATE productos_existentes 
                SET precio_costo = ?, cantidad = ?, fecha = ? 
                WHERE id = ?
                """, (encrypted_new_precio_costo, encrypted_new_cantidad, encrypted_fecha, existing_id))
            else:
                # Insertar un nuevo registro en la tabla productos_existentes
                cursor.execute("""
                INSERT INTO productos_existentes (producto, precio_costo, cantidad, fecha) 
                VALUES (?, ?, ?, ?)
                """, (encrypted_producto, encrypted_precio_costo, encrypted_cantidad, encrypted_fecha))

            conn.commit()
    
    def insert_category(self, start_range, end_range):
        encrypted_start = self.encrypt_value(start_range)
        encrypted_end = self.encrypt_value(end_range)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO category_table (start_range, end_range) VALUES (?, ?)", (encrypted_start, encrypted_end))
            conn.commit()
    
    def create_new_cafe(self, cafe_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            # Encriptar el nombre de la cafetería
            encrypted_name = self.encrypt_value(cafe_name)
            # Insertar nueva cafetería
            cursor.execute("INSERT INTO cafeterias (cafe_name) VALUES (?)", (encrypted_name,))
            cafe_id = cursor.lastrowid  # Obtener el ID de la nueva cafetería
            conn.commit()
        return cafe_id
    
    def insert_transferencia_cafe(self, cafe_id, producto_nombre, precio_costo, precio_venta, cantidad):
        table_name = f"cafe_{cafe_id}_inventory"
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        beneficios = round((precio_venta - precio_costo) * cantidad, 2)  # Redondear a dos decimales
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {table_name} (producto, precio_costo, precio_venta, cantidad, fecha, beneficios, disponibilidad)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.encrypt_value(producto_nombre), self.encrypt_value(precio_costo), self.encrypt_value(precio_venta), self.encrypt_value(cantidad), self.encrypt_value(fecha), self.encrypt_value(beneficios), True))
            conn.commit()

    def insert_transferencia_exitosa(self, cafe_nombre, cafe_id):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transferencia = f"TRANSFERENCIA REALIZADA HACIA LA CAFETERIA: {cafe_nombre} "
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transferencias_exitosas (fecha, transferencia, cafe_id)
                VALUES (?, ?, ?)
            """, (self.encrypt_value(fecha), self.encrypt_value(transferencia), cafe_id))
            conn.commit()

###############GET###########################################################################################
    def get_producto_id_by_nombre(self, nombre):
        with self.connect() as conn:
            cursor = conn.cursor()
            # Encripta el nombre antes de realizar la consulta
            encrypted_nombre =nombre #self.encrypt_value(nombre)
            cursor.execute("SELECT id FROM productos WHERE nombre = ?", (encrypted_nombre,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
    
    def get_all_almacen(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                id,
                producto,
                precio_costo,
                cantidad,
                fecha,
                importe,
                deposito,
                inventario_almacen
            FROM almacen
            """)
            rows = cursor.fetchall()
            data = []
            for row in rows:
                producto = self.decrypt_value(row[1])
                precio_costo = self.convert_to_float(self.decrypt_value(row[2]))
                cantidad = self.convert_to_int(self.decrypt_value(row[3]))
                fecha = self.decrypt_value(row[4])
                importe = self.convert_to_float(self.decrypt_value(row[5]))
                deposito = self.convert_to_float(self.decrypt_value(row[6]))
                inventario_almacen = self.convert_to_float(self.decrypt_value(row[7]))
                
                data.append({
                    "id": row[0],
                    "Producto": producto,
                    "Precio": precio_costo,
                    "Cantidad": cantidad,
                    "Fecha": fecha,
                    "Importe": importe,
                    "Deposito": deposito,
                    "Inventario Almacén": inventario_almacen,
                })
            return data
    
    def convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return 0.0
    
    def convert_to_int(self, value):
        try:
            return int(value)
        except ValueError:
            return 0

        def convert_to_float(self, value):
            try:
                return float(value)
            except ValueError:
                return 0.0

        def convert_to_int(self, value):
            try:
                return int(value)
            except ValueError:
                return 0

###############################
    def get_all_categories(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, start_range, end_range FROM category_table")
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    "id": row[0],
                    "start_range": self.decrypt_value(row[1]),
                    "end_range": self.decrypt_value(row[2])
                })
            return result
    
    def get_all_categories_sorted(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, start_range, end_range FROM category_table ORDER BY start_range ASC")
            rows = cursor.fetchall()
            result = []
            for row in rows:
                decrypted_start = self.decrypt_value(row[1])
                decrypted_end = self.decrypt_value(row[2])
                result.append({
                    "id": row[0],
                    "start_range": decrypted_start,
                    "end_range": decrypted_end
                })
            return result
 
 ############################################################################################################   
    def get_all_cafeterias(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, cafe_name FROM cafeterias")
            cafes = cursor.fetchall()
            # Desencriptar los datos
            return [{
                "id": self.decrypt_value(cafe[0]),
                "nombre": self.decrypt_value(cafe[1])
            } for cafe in cafes]

    def get_cafe_by_name(self, cafe_name):
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cafeterias WHERE cafe_name = ?", (self.encrypt_value(cafe_name),))
            return cursor.fetchone()
  
    def get_cafe_name_by_id(self, cafe_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cafe_name FROM cafeterias WHERE id = ?", (cafe_id,))
            result = cursor.fetchone()
            return self.decrypt_value(result[0]) if result else None

    def get_cafe_id_by_name(self, cafe_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cafeterias WHERE cafe_name = ?", (self.encrypt_value(cafe_name),))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
       
    def get_all_productos_existentes(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT producto, precio_costo, cantidad, fecha FROM productos_existentes")
            productos = cursor.fetchall()
            return [{
                "producto": self.decrypt_value(prod[0]), 
                "precio_costo": float(self.decrypt_value(prod[1])), 
                "cantidad": int(self.decrypt_value(prod[2])), 
                "fecha": self.decrypt_value(prod[3])
            } for prod in productos]

    def get_all_transferencias_exitosas(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT transferencia, fecha, cafe_id FROM transferencias_exitosas ORDER BY id DESC")
            rows = cursor.fetchall()
            transferencias = []
            for row in rows:
                transferencias.append({
                    "transferencia": self.decrypt_value(row[0]),
                    "fecha": self.decrypt_value(row[1]),
                    "cafe_id": row[2]  # Assuming cafe_id is not encrypted
                })
            return transferencias

    def get_all_transferencias_exitosas_cafe(self, cafe_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT transferencia, fecha FROM transferencias_exitosas WHERE cafe_id = ?", (cafe_id,))
            rows = cursor.fetchall()
            transferencias = []
            for row in rows:
                transferencias.append({
                    "transferencia": self.decrypt_value(row[0]),
                    "fecha": self.decrypt_value(row[1])
                })
            return transferencias

    def get_all_inventario_cafe(self, cafe_id):
        table_name = f"cafe_{cafe_id}_inventory"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT producto, precio_costo, precio_venta, cantidad, fecha, beneficios FROM {table_name}")
            rows = cursor.fetchall()
            inventario = []
            for row in rows:
                inventario.append({
                    "producto": self.decrypt_value(row[0]),
                    "precio_costo": float(self.decrypt_value(row[1])),
                    "precio_venta": float(self.decrypt_value(row[2])),
                    "cantidad": int(self.decrypt_value(row[3])),
                    "fecha": self.decrypt_value(row[4]),
                    "beneficios": row[5]
                })
            return inventario
   
 ################################################################################################################
    def get_transferencias_disponibles(self, cafe_id):
        table_name = f"cafe_{cafe_id}_inventory"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, producto, precio_costo, precio_venta, cantidad, fecha, disponibilidad FROM {table_name} WHERE disponibilidad = ?", (True,))
            rows = cursor.fetchall()
            transferencias = []
            for row in rows:
                transferencias.append({
                    "id": row[0],
                    "producto": self.decrypt_value(row[1]),
                    "precio_costo": float(self.decrypt_value(row[2])),
                    "precio_venta": float(self.decrypt_value(row[3])),
                    "cantidad": int(self.decrypt_value(row[4])),
                    "fecha": self.decrypt_value(row[5]),
                    "disponibilidad": bool(row[6])
                })
            return transferencias
    
    def get_all_inventario_almacen_establecimiento(self, establecimiento):
        table_name = f"Almacen_{establecimiento.replace(' ', '_')}"

        # Crear la tabla si no existe
        schema = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            cantidad INTEGER,
            precio_costo REAL,
            precio_venta REAL,
            fecha TEXT
        """
        self.create_dynamic_table(table_name, schema)

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT producto, cantidad, precio_costo, precio_venta, fecha FROM {table_name}")
            rows = cursor.fetchall()

            inventario = []
            for row in rows:
                inventario.append({
                    "producto": self.decrypt_value(row[0]),
                    "cantidad": int(self.decrypt_value(row[1])),
                    "precio_costo": float(self.decrypt_value(row[2])),
                    "precio_venta": float(self.decrypt_value(row[3])),
                    "fecha": self.decrypt_value(row[4])
                })
            return inventario

    def get_inventario_transferencia(self, cafe_id, transferencia):
        table_name = f"cafe_{cafe_id}_inventory"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT producto, precio_costo, precio_venta, cantidad, fecha, beneficios
                FROM {table_name}
                WHERE producto = ?
            """, (self.encrypt_value(transferencia),))
            inventario = cursor.fetchall()
        print(f"Inventario transferido: {inventario}")  # Depuración para verificar el inventario transferido
        return [{"producto": self.decrypt_value(row[0]), "precio_costo": row[1], "precio_venta": row[2], "cantidad": row[3], "fecha": self.decrypt_value(row[4]), "beneficios": row[5]} for row in inventario]

    def get_inventario_cafe(self, cafe_id, fecha):
        table_name = f"cafe_{cafe_id}_inventory"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT producto, precio_costo, precio_venta, cantidad, beneficios, fecha FROM {table_name} WHERE fecha = ?", (self.encrypt_value(fecha),))
            rows = cursor.fetchall()
            inventario = []
            for row in rows:
                inventario.append({
                    "producto": self.decrypt_value(row[0]),
                    "precio_costo": float(self.decrypt_value(row[1])),
                    "precio_venta": float(self.decrypt_value(row[2])),
                    "cantidad": int(self.decrypt_value(row[3])),
                    "beneficios": float(self.decrypt_value(row[4])),
                    "fecha": self.decrypt_value(row[5])
                })
            return inventario

##############UPDATE########################################################################################
    def update_almacen_item(self, id, producto, precio_costo, cantidad, fecha, importe, deposito, inventario_almacen):
        encrypted_producto = self.encrypt_value(producto)
        encrypted_precio_costo = self.encrypt_value(str(precio_costo))
        encrypted_cantidad = self.encrypt_value(str(cantidad))
        encrypted_fecha = self.encrypt_value(fecha)
        encrypted_importe = self.encrypt_value(str(importe))
        encrypted_deposito = self.encrypt_value(str(deposito))
        encrypted_inventario_almacen = self.encrypt_value(str(inventario_almacen))
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE almacen SET 
                producto = ?, 
                precio_costo = ?, 
                cantidad = ?, 
                fecha = ?, 
                importe = ?, 
                deposito = ?, 
                inventario_almacen = ? 
            WHERE id = ?
            """, (encrypted_producto, encrypted_precio_costo, encrypted_cantidad, encrypted_fecha, encrypted_importe, encrypted_deposito, encrypted_inventario_almacen, id))
            conn.commit()

    def update_category(self, category_id, new_start_range, new_end_range):
        encrypted_start = self.encrypt_value(new_start_range)
        encrypted_end = self.encrypt_value(new_end_range)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE category_table SET start_range = ?, end_range = ? WHERE id = ?", (encrypted_start, encrypted_end, category_id))
            conn.commit()
    
    def update_producto_cantidad(self, producto_nombre, nueva_cantidad):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos_existentes
                SET cantidad = ?
                WHERE producto = ?
            """, (self.encrypt_value(nueva_cantidad), self.encrypt_value(producto_nombre)))
            conn.commit()

    def actualizar_disponibilidad(self, cafe_id, transferencia_id, disponibilidad):
        table_name = f"cafe_{cafe_id}_inventory"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table_name} SET disponibilidad = ? WHERE id = ?", (disponibilidad, transferencia_id))
            conn.commit()

############DELETE########################################################################################
    def delete_category(self, category_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM category_table WHERE id = ?", (category_id,))
            conn.commit()

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cafeterias WHERE id = ?", (cafeteria_id,))
            cursor.execute("DELETE FROM inventario_cafeterias WHERE cafeteria_id = ?", (cafeteria_id,))
            conn.commit()

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conn.commit()
    
    def delete_almacen_item(self, id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM almacen WHERE id = ?", (id,))
            conn.commit()
    
    def delete_producto(self, producto_nombre):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM productos_existentes
                WHERE producto = ?
            """, (self.encrypt_value(producto_nombre),))
            conn.commit()

#############EXISTS#####################################################################################
    def is_category_duplicate(self, start_range, end_range):
        encrypted_start = self.encrypt_value(start_range)
        encrypted_end = self.encrypt_value(end_range)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM category_table WHERE start_range = ? AND end_range = ?", (encrypted_start, encrypted_end))
            count = cursor.fetchone()[0]
            return count > 0
    
    def table_exists(self, table_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            result = cursor.fetchone()
            return result is not None
    
    def producto_in_almacen(self, producto_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM almacen WHERE producto_id = ?", (producto_id,))
            count = cursor.fetchone()[0]
            return count > 0

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM inventario_cafeterias WHERE producto_id = ? AND cafeteria_id = ?", (producto_id, cafeteria_id))
            count = cursor.fetchone()[0]
            return count > 0
    
    def producto_exists(self, producto_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos WHERE id = ?", (producto_id,))
            count = cursor.fetchone()[0]
            return count > 0

####################################################################################################   
    def aceptar_transferencia(self, cafe_id, producto):
        table_name = f"cafe_{cafe_id}_inventory"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {table_name}
                SET disponibilidad = ?
                WHERE producto = ?
            """, (False, self.encrypt_value(producto)))
            conn.commit()

    def get_product_by_name(self, table_name, producto):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM {table_name} WHERE producto = ?
            """, (self.encrypt_value(producto),))
            row = cursor.fetchone()
            if row:
                return [self.decrypt_value(col) for col in row]
            return None

    def update_product_in_almacen(self, table_name, producto, cantidad, precio_costo, precio_venta):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {table_name}
                SET cantidad = cantidad + ?,
                    precio_costo = (precio_costo + ?) / 2,
                    precio_venta = (precio_venta + ?) / 2
                WHERE producto = ?
            """, (self.encrypt_value(cantidad), self.encrypt_value(precio_costo), self.encrypt_value(precio_venta), self.encrypt_value(producto)))
            conn.commit()

    def insert_product_in_almacen(self, table_name, producto, cantidad, precio_costo, precio_venta, fecha):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {table_name} (producto, cantidad, precio_costo, precio_venta, fecha)
                VALUES (?, ?, ?, ?, ?)
            """, (self.encrypt_value(producto), self.encrypt_value(cantidad), self.encrypt_value(precio_costo), self.encrypt_value(precio_venta), self.encrypt_value(fecha)))
            conn.commit()

    def update_transferencia_disponibilidad(self, transferencia_id, disponibilidad):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transferencias
                SET disponibilidad = ?
                WHERE id = ?
            """, (self.encrypt_value(disponibilidad), transferencia_id))
            conn.commit()

##########################################################################################################################    
    def obtener_producto_vendido(self, tabla, producto):
        query = f"SELECT * FROM {tabla} WHERE Producto_vender = ?"
        params = (self.encrypt_value(producto),)

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return [self.decrypt_value(col) for col in row]
            return None

    def obtener_todos_productos_a_vender(self, tabla):
        query = f"SELECT Producto_vender, cantidad, precio FROM {tabla}"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            productos = cursor.fetchall()
            return [[self.decrypt_value(prod[0]), self.decrypt_value(prod[1]), self.decrypt_value(prod[2])] for prod in productos]
    
    def obtener_cantidad(self,tabla,producto):
        query = f"SELECT  cantidad FROM {tabla}"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            productos = cursor.fetchall()
            return [self.decrypt_value(prod[0]) for prod in productos]
        
    def insert_producto_vendido(self, tabla, producto_vendido):
        query = f"INSERT INTO {tabla} (Producto_vender, cantidad, precio, fecha) VALUES (?, ?, ?, ?)"
        params = (self.encrypt_value(producto_vendido['Producto_vender']), self.encrypt_value(producto_vendido['cantidad']), self.encrypt_value(producto_vendido['precio']), self.encrypt_value(producto_vendido['fecha']))

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def actualizar_producto_vendido(self, tabla, producto, nueva_cantidad):
        try:
            query = f"UPDATE {tabla} SET cantidad = ? WHERE Producto_vender = ?"
            params = (self.encrypt_value(nueva_cantidad), self.encrypt_value(producto))

            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()

            # Verificar que la actualización fue exitosa
            cursor.execute(f"SELECT cantidad FROM {tabla} WHERE Producto_vender = ?", (self.encrypt_value(producto),))
            cantidad_actualizada = cursor.fetchone()
            if cantidad_actualizada:
                print(f"Cantidad actualizada en la BD para {producto}: {self.decrypt_value(cantidad_actualizada[0])}")
            else:
                print(f"Error: No se encontró el producto {producto} tras la actualización.")
        except Exception as ex:
            print(f"Error al actualizar producto vendido: {ex}")
    
    def eliminar_producto_de_venta(self, tabla, producto):
        query = f"DELETE FROM {tabla} WHERE Producto_vender = ?"
        params = (self.encrypt_value(producto),)

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def actualizar_cantidad_producto(self, tabla, producto, cantidad):
        query = f"UPDATE {tabla} SET cantidad = ? WHERE producto = ?"
        params = (self.encrypt_value(cantidad), self.encrypt_value(producto))

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def eliminar_producto(self, tabla, producto):
        query = f"DELETE FROM {tabla} WHERE producto = ?"
        params = (self.encrypt_value(producto),)

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
    
    def confirmar_pago(self,table_name_vendidos,productos_vendidos,usuario,table_name_almacen,table_name_venta):
        with self.connect() as conn:
            cursor = conn.cursor()
            for producto in productos_vendidos:
                cursor.execute(f"""
                    INSERT INTO {table_name_vendidos} (Producto_vendido, cantidad_vendida, precio, fecha, vendedor)
                    VALUES (?, ?, ?, datetime('now','localtime'), ?)
                """, (self.encrypt_value(producto[0]), self.encrypt_value(producto[1]), self.encrypt_value(producto[2]), self.encrypt_value(usuario)))

                # cursor.execute(f"""
                #     UPDATE {table_name_almacen}
                #     SET cantidad = ?
                #     WHERE producto = ?
                # """, (self.encrypt_value(producto[1]), self.encrypt_value(producto[0])))

            cursor.execute(f"DELETE FROM {table_name_venta}")
            conn.commit()