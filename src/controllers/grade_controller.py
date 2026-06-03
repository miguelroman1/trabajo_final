import flet as ft
from models.subject_model import SubjectModel
from models.grade_model import GradeModel
from views.dashboard_view import DashboardView

class GradeController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.dashboard_view = DashboardView(self)
        self.current_semester = 1
    
    def show_dashboard(self):
        self.dashboard_view.build()
    
    def get_materias(self):
        user = self.app.get_user()
        if user:
            return SubjectModel.get_materias_por_semestre(
                user['especialidad_id'],
                self.current_semester
            )
        return []
    
    def get_calificaciones(self):
        user = self.app.get_user()
        if user:
            return GradeModel.get_calificaciones(
                user['id'],
                self.current_semester
            )
        return []
    
    def save_calificacion(self, materia_id: int, unidad1: float, 
                          unidad2: float, unidad3: float) -> tuple:
        user = self.app.get_user()
        if user:
            return GradeModel.save_calificacion(
                user['id'],
                materia_id,
                self.current_semester,
                unidad1, unidad2, unidad3
            )
        return False, "Usuario no autenticado"
    
    def get_promedios(self):
        user = self.app.get_user()
        if user:
            semestre_prom = GradeModel.get_promedio_general(
                user['id'],
                self.current_semester
            )
            general_prom = GradeModel.get_promedio_general(user['id'])
            return semestre_prom, general_prom
        return 0.0, 0.0
    
    def change_semester(self, semester: int):
        self.current_semester = semester
        self.dashboard_view.refresh_grades()
    
    def get_current_semester(self):
        return self.current_semester
    
    def logout(self):
        self.app.show_login()