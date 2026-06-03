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