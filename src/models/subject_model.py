from models.database import Database

class SubjectModel:
    @staticmethod
    def get_materias_por_semestre(especialidad_id: int, semestre: int) -> list:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            cursor.execute("""
                SELECT id, nombre, semestre 
                FROM materias 
                WHERE especialidad_id = %s AND semestre = %s
                ORDER BY nombre
            """, (especialidad_id, semestre))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    @staticmethod
    def agregar_materia(nombre: str, semestre: int, especialidad_id: int) -> tuple:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            cursor.execute("""
                SELECT id FROM materias 
                WHERE nombre = %s AND semestre = %s AND especialidad_id = %s
            """, (nombre, semestre, especialidad_id))
            
            if cursor.fetchone():
                return False, "La materia ya existe en este semestre"
            
            cursor.execute("""
                INSERT INTO materias (nombre, semestre, especialidad_id)
                VALUES (%s, %s, %s)
            """, (nombre, semestre, especialidad_id))
            
            db.commit()
            return True, "Materia agregada exitosamente"
        except Exception as e:
            return False, f"Error al agregar: {str(e)}"
        finally:
            cursor.close()
    
    @staticmethod
    def eliminar_materia(materia_id: int) -> tuple:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            # Primero eliminar calificaciones asociadas
            cursor.execute("DELETE FROM calificaciones WHERE materia_id = %s", (materia_id,))
            # Luego eliminar la materia
            cursor.execute("DELETE FROM materias WHERE id = %s", (materia_id,))
            
            db.commit()
            return True, "Materia eliminada exitosamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
        finally:
            cursor.close()