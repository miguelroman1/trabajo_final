from models.database import Database
from utils.validators import Validators

class UserModel:
    @staticmethod
    def register(user_data: dict) -> tuple:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            # Verificar si usuario o correo ya existen
            cursor.execute(
                "SELECT id FROM usuarios WHERE username = %s OR correo = %s",
                (user_data['username'], user_data['correo'])
            )
            if cursor.fetchone():
                return False, "El usuario o correo ya existe"
            
            # Hash de contraseña
            hashed_password = Validators.hash_password(user_data['password'])
            
            # Insertar usuario
            query = """
                INSERT INTO usuarios 
                (nombre_completo, curp, correo, celular, foto_perfil, username, password, especialidad_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                user_data['nombre_completo'],
                user_data['curp'],
                user_data['correo'],
                user_data['celular'],
                user_data.get('foto_perfil', ''),
                user_data['username'],
                hashed_password,
                user_data['especialidad_id']
            ))
            db.commit()
            return True, "Usuario registrado exitosamente"
            
        except Exception as e:
            return False, f"Error al registrar: {str(e)}"
        finally:
            cursor.close()
    
    @staticmethod
    def login(username: str, password: str) -> dict:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            query = """
                SELECT u.*, e.nombre as especialidad_nombre 
                FROM usuarios u
                JOIN especialidades e ON u.especialidad_id = e.id
                WHERE u.username = %s
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            if user and Validators.verify_password(password, user['password']):
                return user
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_especialidades() -> list:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            cursor.execute("SELECT id, nombre FROM especialidades ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()
    
    @staticmethod
    def update_profile(user_id: int, update_data: dict, new_password: str = None) -> tuple:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            # Construir query dinámica
            fields = []
            values = []
            
            for key, value in update_data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if new_password:
                fields.append("password = %s")
                values.append(Validators.hash_password(new_password))
            
            if not fields:
                return True, "No hay cambios para guardar"
            
            values.append(user_id)
            query = f"UPDATE usuarios SET {', '.join(fields)} WHERE id = %s"
            
            cursor.execute(query, values)
            db.commit()
            
            return True, "Perfil actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
        finally:
            cursor.close()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> dict:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            query = """
                SELECT u.*, e.nombre as especialidad_nombre 
                FROM usuarios u
                JOIN especialidades e ON u.especialidad_id = e.id
                WHERE u.id = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()