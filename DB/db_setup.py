import os
import sqlite3
from DB.KeyManager import KeyManager


class UserDB:
    def __init__(self):
        # Ruta de la carpeta MagicCorp y archivo de base de datos
        self.magiccorp_path = r"C:\MagicCorp"
        self.db_path = os.path.join(self.magiccorp_path, "DB")
        self.key_file_path = os.path.join(self.magiccorp_path, "key.txt")

        # Verificar si las carpetas necesarias existen
        if not os.path.exists(self.magiccorp_path):
            raise FileNotFoundError(f"La carpeta {self.magiccorp_path} no existe. Verifique la instalación.")
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"La carpeta {self.db_path} no existe. Verifique la instalación.")
        if not os.path.exists(self.key_file_path):
            raise FileNotFoundError(f"El archivo {self.key_file_path} no existe. Verifique la instalación.")

        # Obtener el nombre del negocio desde key.txt
        self.business_name = self.get_business_name_from_key()
        if not self.business_name:
            raise ValueError("No se encontró el nombre del negocio en key.txt. Verifique el archivo.")

        # Ruta específica del archivo de base de datos
        self.business_db_path = os.path.join(self.db_path, f"DB_{self.business_name}.db")

        # Inicializar KeyManager
        self.key_manager = KeyManager()
        self.encryption_key = self.key_manager.encryption_key
        self.decryption_key = self.key_manager.decryption_key

        # Crear tablas necesarias
        self.create_tables()

    def connect(self):
        """Conecta a la base de datos específica del negocio."""
        return sqlite3.connect(self.business_db_path, check_same_thread=False)

    def get_business_name_from_key(self):
        """Obtiene el nombre del negocio desde el archivo key.txt."""
        with open(self.key_file_path, "r", encoding="utf-8") as key_file:
            for line in key_file:
                if "Negocio:" in line:
                    return line.split(":")[1].strip()
        return None

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

    def create_tables(self):
        """Crea las tablas específicas necesarias para el negocio."""
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
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                Enombre TEXT NOT NULL,
                Eusuario TEXT NOT NULL UNIQUE,
                Econtraseña TEXT NOT NULL,
                rol TEXT NOT NULL,
                establecimiento TEXT,
                telefono TEXT
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.execute("""
            INSERT OR IGNORE INTO users (Enombre, Eusuario, Econtraseña, rol) VALUES
            ('Administrador', 'fH}yc98&-`7z+DnsAN#63teZB',
            'wRyw[adj2MmkJa6AFdB_adj2MA",!F+tq}8GbBFmmA7b"33pEAAFdB_QwEVu&v3s|AFdB_bEMEIk2&K,mkJa6pl.@K7z+Dnk2&K,tZn$Qh.Q^Au=Fj5b.E/X', 
            'Administrador')
            """)

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
                {
                    "id": row[0],
                    "Enombre": row[1],
                    "Eusuario": self.decrypt_value(row[2]),
                    "rol": row[3],
                    "establecimiento": self.decrypt_value(row[4]),
                    "telefono": row[5]
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
                {
                    "id": row[0], 
                    "Enombre": row[1], 
                    "Eusuario": self.decrypt_value(row[2])
                }
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