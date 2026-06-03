from models.database import Database

class GradeModel:
    @staticmethod
    def get_calificaciones(usuario_id: int, semestre: int) -> list:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            cursor.execute("""
                SELECT c.*, m.nombre as materia_nombre 
                FROM calificaciones c
                JOIN materias m ON c.materia_id = m.id
                WHERE c.usuario_id = %s AND c.semestre = %s
            """, (usuario_id, semestre))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    @staticmethod
    def save_calificacion(usuario_id: int, materia_id: int, semestre: int, 
                          unidad1: float, unidad2: float, unidad3: float) -> tuple:
        db = Database()
        cursor = db.get_cursor()
        
        try:
            promedio = round((unidad1 + unidad2 + unidad3) / 3, 2)
            
            cursor.execute("""
                SELECT id FROM calificaciones 
                WHERE usuario_id = %s AND materia_id = %s AND semestre = %s
            """, (usuario_id, materia_id, semestre))
            
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE calificaciones 
                    SET unidad1 = %s, unidad2 = %s, unidad3 = %s, promedio = %s
                    WHERE usuario_id = %s AND materia_id = %s AND semestre = %s
                """, (unidad1, unidad2, unidad3, promedio, usuario_id, materia_id, semestre))
            else:
                cursor.execute("""
                    INSERT INTO calificaciones 
                    (usuario_id, materia_id, semestre, unidad1, unidad2, unidad3, promedio)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (usuario_id, materia_id, semestre, unidad1, unidad2, unidad3, promedio))
            
            db.commit()
            return True, "Calificación guardada exitosamente"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
        finally:
            cursor.close()
    
    @staticmethod
    def get_promedio_general(usuario_id: int, semestre: int = None) -> float:
        db = Database()
        cursor = db.get_cursor(dictionary=False)
        
        try:
            if semestre:
                query = """
                    SELECT AVG(promedio) as promedio 
                    FROM calificaciones 
                    WHERE usuario_id = %s AND semestre = %s
                """
                cursor.execute(query, (usuario_id, semestre))
            else:
                query = "SELECT AVG(promedio) as promedio FROM calificaciones WHERE usuario_id = %s"
                cursor.execute(query, (usuario_id,))
            
            result = cursor.fetchone()
            return round(result[0], 2) if result and result[0] else 0.0
        finally:
            cursor.close()