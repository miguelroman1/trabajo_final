import flet as ft
from controllers.auth_controller import AuthController
from controllers.grade_controller import GradeController

class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = None
        self.auth_controller = AuthController(self)
        self.grade_controller = GradeController(self)
        self._setup_page()
    
    def _setup_page(self):
        self.page.title = "Sistema de Gestión de Calificaciones"
        self.page.padding = 20
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"
    
    def run(self):
        self.show_login()
    
    def show_login(self):
        self.auth_controller.show_login()
    
    def show_register(self):
        self.auth_controller.show_register()
    
    def show_dashboard(self):
        self.grade_controller.show_dashboard()
    
    def show_snackbar(self, message: str, is_error: bool = False):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.RED if is_error else ft.colors.GREEN,
            open=True
        )
        self.page.overlay.append(snackbar)
        self.page.update()
    
    def set_user(self, user):
        self.current_user = user
    
    def get_user(self):
        return self.current_user
    
    def clear_and_add(self, *controls):
        self.page.controls.clear()
        self.page.add(*controls)
        self.page.update()
    
    def logout(self):
        self.set_user(None)
        self.show_login()