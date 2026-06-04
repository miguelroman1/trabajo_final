import flet as ft
from models.user_model import UserModel

class RegisterView:
    def __init__(self, controller):
        self.controller = controller
    
    def build(self):
        especialidades = UserModel.get_especialidades()
        especialidad_options = [ft.dropdown.Option(str(e['id']), e['nombre']) for e in especialidades]
        
        self.nombre_field = ft.TextField(label="Nombre Completo", width=400)
        self.curp_field = ft.TextField(label="CURP", width=400)
        self.correo_field = ft.TextField(label="Correo Institucional", width=400)
        self.celular_field = ft.TextField(label="Celular", width=400)
        self.username_field = ft.TextField(label="Usuario", width=400)
        self.password_field = ft.TextField(label="Contraseña", width=400, password=True, can_reveal_password=True)
        self.confirm_password_field = ft.TextField(label="Confirmar Contraseña", width=400, password=True, can_reveal_password=True)
        self.especialidad_dropdown = ft.Dropdown(
            label="Especialidad",
            width=400,
            options=especialidad_options
        )
        
        def on_submit(e):
            form_data = {
                'nombre_completo': self.nombre_field.value,
                'curp': self.curp_field.value,
                'correo': self.correo_field.value,
                'celular': self.celular_field.value,
                'username': self.username_field.value,
                'password': self.password_field.value,
                'confirm_password': self.confirm_password_field.value,
                'especialidad_id': self.especialidad_dropdown.value
            }
            self.controller.handle_register(form_data)
        
        def on_back(e):
            self.controller.show_login()
        
        form_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registro de Alumno", size=28, weight="bold", color=ft.Colors.BLUE),
                    ft.Divider(height=20),
                    self.nombre_field,
                    self.curp_field,
                    self.correo_field,
                    self.celular_field,
                    self.username_field,
                    self.password_field,
                    self.confirm_password_field,
                    self.especialidad_dropdown,
                    ft.Row(
                        [ft.ElevatedButton("Registrarse", on_click=on_submit),
                         ft.TextButton("Volver", on_click=on_back)],
                        alignment="center",
                        spacing=20
                    ),
                ],
                spacing=15,
                horizontal_alignment="center",
                scroll=ft.ScrollMode.AUTO
            ),
            width=500,
            height=600,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.GREY_400)
        )
        
        self.controller.app.clear_and_add(
            ft.Row([form_container], alignment="center", vertical_alignment="center")
        )