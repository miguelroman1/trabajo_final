import flet as ft
from models.user_model import UserModel
from utils.validators import Validators
from views.login_view import LoginView
from views.register_view import RegisterView

class AuthController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)
    
    def show_login(self):
        self.login_view.build()
    
    def show_register(self):
        self.register_view.build()
    
    def handle_login(self, username: str, password: str) -> bool:
        if not username or not password:
            self.app.show_snackbar("Todos los campos son obligatorios", True)
            return False
        
        user = UserModel.login(username, password)
        if user:
            self.app.set_user(user)
            self.app.show_dashboard()
            return True
        else:
            self.app.show_snackbar("Usuario o contraseña incorrectos", True)
            return False
    
    def handle_register(self, form_data: dict) -> bool:
        # Validar campos obligatorios
        required_fields = ['nombre_completo', 'curp', 'correo', 'username', 'password', 'confirm_password', 'especialidad_id']
        for field in required_fields:
            if not form_data.get(field):
                self.app.show_snackbar("Todos los campos son obligatorios", True)
                return False
        
        # Validar CURP
        if not Validators.validate_curp(form_data['curp'].upper()):
            self.app.show_snackbar("CURP no válida", True)
            return False
        
        # Validar email
        if not Validators.validate_email(form_data['correo']):
            self.app.show_snackbar("Correo electrónico no válido", True)
            return False
        
        # Validar contraseñas
        if form_data['password'] != form_data['confirm_password']:
            self.app.show_snackbar("Las contraseñas no coinciden", True)
            return False
        
        if len(form_data['password']) < 6:
            self.app.show_snackbar("La contraseña debe tener al menos 6 caracteres", True)
            return False
        
        # Preparar datos para registro
        user_data = {
            'nombre_completo': form_data['nombre_completo'],
            'curp': form_data['curp'].upper(),
            'correo': form_data['correo'],
            'celular': form_data.get('celular', ''),
            'username': form_data['username'],
            'password': form_data['password'],
            'especialidad_id': int(form_data['especialidad_id'])
        }
        
        success, message = UserModel.register(user_data)
        if success:
            self.app.show_snackbar(message, False)
            self.show_login()
            return True
        else:
            self.app.show_snackbar(message, True)
            return False
    
    def logout(self):
        self.app.set_user(None)
        self.show_login()