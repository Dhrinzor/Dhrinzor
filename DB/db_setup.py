import os
import sqlite3


class BusinessDB:
    def __init__(self, db_path, business_name):
        self.db_path = db_path
        self.business_name = business_name

        # Asegurarse de que la carpeta de destino exista
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)  # Crea la carpeta y cualquier subcarpeta necesaria
            print(f"Carpeta creada: {self.db_path}")

        # Ruta específica del archivo de base de datos
        self.business_db_path = os.path.join(self.db_path, f"DB_{self.business_name}.db")

        # Crear el archivo de base de datos si no existe
        if not os.path.exists(self.business_db_path):
            open(self.business_db_path, "w").close()
            print(f"Archivo de base de datos creado: {self.business_db_path}")

        # Crear la tabla negocio
        self.create_business_table()

    def connect(self):
        """Conecta a la base de datos específica del negocio."""
        return sqlite3.connect(self.business_db_path, check_same_thread=False)

    def create_business_table(self):
        """Crea la tabla `negocio` en la base de datos."""
        with self.connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS negocio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
            """)
            conn.execute("""
            INSERT OR IGNORE INTO negocio (nombre) VALUES (?)
            """, (self.business_name,))
            print(f"Tabla `negocio` creada y configurada para el negocio: {self.business_name}")
            
from DB.KeyManager import KeyManager
class UserDB:
    def __init__(self, business_db_path):
        """Inicializa la clase UserDB con la ruta de la base de datos."""
        self.business_db_path = business_db_path

        # Asegurarse de que la carpeta y el archivo de base de datos existen
        self._prepare_database()

        # Inicializar KeyManager
        self.key_manager = KeyManager()
        self.encryption_key = self.key_manager.encryption_key
        self.decryption_key = self.key_manager.decryption_key

        # Crear las tablas relacionadas con usuarios
        self.create_user_tables()

    def _prepare_database(self):
        """Crea la carpeta y el archivo de base de datos si no existen."""
        # Asegurarse de que la carpeta para la base de datos exista
        folder_path = os.path.dirname(self.business_db_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Carpeta creada: {folder_path}")

        # Crear el archivo de base de datos si no existe
        if not os.path.exists(self.business_db_path):
            open(self.business_db_path, "w").close()
            print(f"Archivo de base de datos creado: {self.business_db_path}")

    def connect(self):
        """Conecta a la base de datos."""
        if not os.path.exists(self.business_db_path):
            raise FileNotFoundError(f"El archivo de base de datos no existe: {self.business_db_path}")
        return sqlite3.connect(self.business_db_path, check_same_thread=False)

    def encrypt_value(self, value):
        """Encripta valores usando la clave de encriptación."""
        if value == "DEPÓSITO":
            return value
        return ''.join(self.encryption_key.get(char, char) for char in str(value))

    def decrypt_value(self, value):
        """Desencripta valores usando la clave de desencriptación."""
        if value is None:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return ''.join(self.decryption_key.get(value[i:i + 5], value[i:i + 5]) for i in range(0, len(value), 5))


    def create_user_tables(self):
        """Crea las tablas relacionadas con usuarios."""
        with self.connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,Enombre TEXT NOT NULL, Eusuario TEXT NOT NULL UNIQUE,Econtraseña TEXT NOT NULL,
                rol TEXT NOT NULL,establecimiento TEXT,telefono TEXT
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS login_history (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL,login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.execute("""
            INSERT OR IGNORE INTO users (Enombre, Eusuario, Econtraseña, rol) VALUES
            ('Administrador', 'fH}yc98&-`7z+DnsAN#63teZB',
            'wRyw[adj2MmkJa6AFdB_adj2MA",!F+tq}8GbBFmmA7b"33pEAAFdB_QwEVu&v3s|AFdB_bEMEIk2&K,mkJa6pl.@K7z+Dnk2&K,tZn$Qh.Q^Au=Fj5b.E/X', 
            'Administrador')
            """)
            print("Tablas `users` y `login_history` creadas y configuradas.")            

    # Métodos relacionados con usuarios permanecen igual: signup, login, etc.
    def user_exists(self, Eusuario):
        """Verifica si un usuario existe en la base de datos."""
        encrypted_user = self.encrypt_value(Eusuario)
        with self.connect() as conn:
            result = conn.execute("""
            SELECT 1 FROM users WHERE Eusuario = ?
            """, (encrypted_user,)).fetchone()
            return result is not None

    def signup(self, Enombre, Eusuario, Econtraseña, rol, establecimiento=None, telefono=None):
        """Registra un nuevo usuario en la base de datos."""
        encrypted_password = self.encrypt_value(Econtraseña)
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO users (Enombre, Eusuario, Econtraseña, rol, establecimiento, telefono)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.encrypt_value(Enombre), self.encrypt_value(Eusuario), encrypted_password, self.encrypt_value(rol), self.encrypt_value(establecimiento), self.encrypt_value(telefono)))

    def login(self, Eusuario, Econtraseña):
        """Verifica las credenciales de un usuario."""
        encrypted_user = self.encrypt_value(Eusuario)
        encrypted_password = self.encrypt_value(Econtraseña)
        with self.connect() as conn:
            user = conn.execute("""
            SELECT * FROM users WHERE Eusuario = ? AND Econtraseña = ?
            """, (encrypted_user, encrypted_password)).fetchone()
            return user is not None
    def password_exists(self, password):
        encrypted_password = self.encrypt_value(password)
        with self.connect() as conn:
            result = conn.execute("""
            SELECT 1 FROM users WHERE Econtraseña = ?
            """, (encrypted_password,)).fetchone()
        return result is not None
    
    def insert_login_history(self, username):
        """Inserta un registro en el historial de inicio de sesión."""
        with self.connect() as conn:
            conn.execute("INSERT INTO login_history (username) VALUES (?)", (self.encrypt_value(username),))

    def get_last_login_user(self):
        """Obtiene el último usuario que inició sesión."""
        with self.connect() as conn:
            result = conn.execute("SELECT username FROM login_history ORDER BY login_time DESC LIMIT 1").fetchone()
        return self.decrypt_value(result[0]) if result else None

    def update_password(self, username, new_password):
        """Actualiza la contraseña de un usuario."""
        encrypted_password = self.encrypt_value(new_password)
        with self.connect() as conn:
            conn.execute("""
            UPDATE users SET Econtraseña = ? WHERE Eusuario = ?
            """, (encrypted_password, self.encrypt_value(username)))

    def delete_user(self, id_usuario):
        """Elimina un usuario por ID."""
        with self.connect() as conn:
            conn.execute("""
            DELETE FROM users WHERE id = ?
            """, (id_usuario,))
            conn.commit()

    def update_user(self, id_usuario, nombre, usuario, rol, establecimiento, telefono):
        """Actualiza la información de un usuario."""
        encrypted_user = self.encrypt_value(usuario)
        encrypted_establecimiento = self.encrypt_value(establecimiento)
        with self.connect() as conn:
            conn.execute("""
            UPDATE users SET Enombre = ?, Eusuario = ?, rol = ?, establecimiento = ?, telefono = ? WHERE id = ?
            """, (nombre, encrypted_user, rol, encrypted_establecimiento, telefono, id_usuario))
            conn.commit()

    def get_usuarios(self):
        """Obtiene todos los usuarios en la base de datos."""
        with self.connect() as conn:
            cursor = conn.execute("""
            SELECT id, Enombre, Eusuario, rol, establecimiento, telefono FROM users
            """)
            return [
                { "id": row[0],"Enombre": row[1], "Eusuario": self.decrypt_value(row[2]),"rol": row[3], "establecimiento": self.decrypt_value(row[4]),"telefono": row[5]
                }
                for row in cursor.fetchall()
            ]

    def delete_user(self, id_usuario):
        with self.connect() as conn:
            conn.execute("""
            DELETE FROM users WHERE id = ?
            """, (id_usuario,))
            conn.commit()

    def update_user(self, id_usuario, nombre, usuario, rol, establecimiento, telefono):
        encrypted_user = self.encrypt_value(usuario)
        encrypted_establecimiento = self.encrypt_value(establecimiento)
        with self.connect() as conn:
            conn.execute("""
            UPDATE users SET Enombre = ?, Eusuario = ?, rol = ?, establecimiento = ?, telefono = ? WHERE id = ?
            """, (nombre, encrypted_user, rol, encrypted_establecimiento, telefono, id_usuario))
            conn.commit()

    def get_password_user(self):
        with self.connect() as conn:
            cursor = conn.execute("""
            SELECT id, Enombre, Eusuario FROM users
            """)
            return [
                {"id": row[0],  "Enombre": row[1], "Eusuario": self.decrypt_value(row[2])}
                for row in cursor.fetchall()
            ]

    def get_user_role(self, usuario):
        with self.connect() as conn:
            cursor = conn.execute("SELECT rol FROM users WHERE Eusuario = ?", (self.encrypt_value(usuario),))
            result = cursor.fetchone()
            return self.decrypt_value(result[0]) if result else None

    def get_user_local(self, usuario):
        with self.connect() as conn:
            cursor = conn.execute("SELECT establecimiento FROM users WHERE Eusuario = ?", (self.encrypt_value(usuario),))
            result = cursor.fetchone()
            return self.decrypt_value(result[0]) if result else None