import sqlite3
import threading
from pages.authentication.utils.KeyManager import KeyManager

class UserDB:
    def __init__(self):
        self.db_path = "DB/data_hub.db"
        self.key_manager = KeyManager()  # Crear instancia de KeyManager 
        self.encryption_key = self.key_manager.encryption_key  # Obtener la clave de encriptación 
        self.decryption_key = self.key_manager.decryption_key  # Obtener la clave de desencriptación 
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def encrypt_value(self, value):
        if value == "DEPÓSITO":
            return value
        return ''.join(self.encryption_key.get(char, char) for char in str(value))
    
    def decrypt_value(self, value):
        if value is None:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return ''.join(self.decryption_key.get(value[i:i+5], value[i:i+5]) for i in range(0, len(value), 5))
   
    def create_tables(self):
        with self.connect() as conn:
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
            )""")
            conn.execute("""
            INSERT OR IGNORE INTO users (Enombre, Eusuario, Econtraseña, rol) VALUES
            ('Administrador', 'fH}yc98&-`7z+DnsAN#63teZB', 
            'wRyw[adj2MmkJa6AFdB_adj2MA",!F+tq}8GbBFmmA7b"33pEAAFdB_QwEVu&v3s|AFdB_bEMEIk2&K,mkJa6pl.@K7z+Dnk2&K,tZn$Qh.Q^Au=Fj5b.E/X', 'Administrador')
            """)

    def user_exists(self, Eusuario):
        encrypted_user = self.encrypt_value(Eusuario)
        with self.connect() as conn:
            result = conn.execute("""
            SELECT 1 FROM users WHERE Eusuario = ?
            """, (encrypted_user,)).fetchone()
            return result is not None

    def signup(self, Enombre, Eusuario, Econtraseña, rol, establecimiento=None, telefono=None):
        encrypted_password = self.encrypt_value(Econtraseña)
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO users (Enombre, Eusuario, Econtraseña, rol, establecimiento, telefono)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.encrypt_value(Enombre), self.encrypt_value(Eusuario), encrypted_password, self.encrypt_value(rol), self.encrypt_value(establecimiento), self.encrypt_value(telefono)))

    def password_auth(self, Econtraseña):
        encrypted_password = self.encrypt_value(Econtraseña)
        with self.connect() as conn:
            pass_auth = conn.execute("""
            SELECT * FROM users WHERE Econtraseña = ?
            """, (encrypted_password,)).fetchone()
            return pass_auth is not None

    def login(self, Eusuario, Econtraseña):
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
        with self.connect() as conn:
            conn.execute("INSERT INTO login_history (username) VALUES (?)", (self.encrypt_value(username),))

    def get_last_login_user(self):
        with self.connect() as conn:
            result = conn.execute("SELECT username FROM login_history ORDER BY login_time DESC LIMIT 1").fetchone()
        return self.decrypt_value(result[0]) if result else None

    def update_password(self, username, new_password):
        encrypted_password = self.encrypt_value(new_password)
        with self.connect() as conn:
            conn.execute("""
            UPDATE users SET Econtraseña = ? WHERE Eusuario = ?
            """, (encrypted_password, self.encrypt_value(username)))

    # En la clase UserDB
    def add_user(self, nombre, usuario, contrasena, rol, establecimiento, telefono):
        encrypted_user = self.encrypt_value(usuario)
        encrypted_password = self.encrypt_value(contrasena)
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO users (Enombre, Eusuario, Econtraseña, rol, establecimiento, telefono) VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, encrypted_user, encrypted_password, rol, establecimiento, telefono))
            conn.commit()

    def get_establecimientos(self):
        with self.connect() as conn:
            cursor = conn.execute("""
            SELECT cafe_name FROM cafeterias
            """)
            encrypted_establecimientos = [row[0] for row in cursor.fetchall()]
            return [self.decrypt_value(est) for est in encrypted_establecimientos]

    def get_usuarios(self):
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