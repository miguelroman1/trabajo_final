import flet as ft
from models.user_model import UserModel
from utils.validators import Validators

class ProfileView:
    def __init__(self, controller):
        self.controller = controller
        
    def build(self):
        user = self.controller.app.get_user()
        if not user:
            self.controller.app.show_login()
            return
        
        # AppBar
        self.controller.app.page.appbar = ft.AppBar(
            title=ft.Text("Mi Perfil"),
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: self.controller.app.show_dashboard()
            ),
        )
        
        # Campos
        nombre_field = ft.TextField(label="Nombre Completo", value=user.get('nombre_completo', ''), width=400, read_only=False)
        curp_field = ft.TextField(label="CURP", value=user.get('curp', ''), width=400, read_only=False)
        matricula_field = ft.TextField(label="Matrícula", value=user.get('matricula', 'No registrada'), width=400, read_only=True)
        correo_field = ft.TextField(label="Correo Institucional", value=user.get('correo', ''), width=400, read_only=False)
        celular_field = ft.TextField(label="Celular", value=user.get('celular', ''), width=400, read_only=False, helper_text="10-15 dígitos, ej: 6562222258")
        especialidad_field = ft.TextField(label="Especialidad", value=user.get('especialidad_nombre', ''), width=400, read_only=True)
        username_field = ft.TextField(label="Usuario", value=user.get('username', ''), width=400, read_only=False)
        
        # Campos de contraseña
        nueva_password_field = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, width=400)
        confirm_password_field = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, width=400)
        
        # Foto de perfil
        foto_container = ft.Container(
            width=120, height=120,
            bgcolor=ft.colors.BLUE_100,
            border_radius=60,
            content=ft.Icon(ft.icons.PERSON, size=60, color=ft.colors.BLUE_700),
        )
        
        def guardar_cambios(e):
            # Validar campos obligatorios
            if not nombre_field.value:
                self.controller.app.show_snackbar("El nombre completo es obligatorio", True)
                return
            
            if not correo_field.value:
                self.controller.app.show_snackbar("El correo es obligatorio", True)
                return
            
            if not username_field.value:
                self.controller.app.show_snackbar("El usuario es obligatorio", True)
                return
            
            # Validar celular si se ingresó
            celular = celular_field.value.strip() if celular_field.value else ""
            if celular and not Validators.validate_phone(celular):
                self.controller.app.show_snackbar("Celular inválido. Use 10-15 dígitos, ej: 6562222258", True)
                return
            
            # Validar contraseña nueva si se ingresó
            new_password = None
            if nueva_password_field.value:
                if nueva_password_field.value != confirm_password_field.value:
                    self.controller.app.show_snackbar("Las contraseñas no coinciden", True)
                    return
                if len(nueva_password_field.value) < 6:
                    self.controller.app.show_snackbar("La contraseña debe tener al menos 6 caracteres", True)
                    return
                new_password = nueva_password_field.value
            
            # Preparar datos a actualizar
            update_data = {
                'nombre_completo': nombre_field.value,
                'curp': curp_field.value.upper(),
                'correo': correo_field.value,
                'celular': celular,
                'username': username_field.value
            }
            
            success, message = UserModel.update_profile(user['id'], update_data, new_password)
            
            if success:
                updated_user = UserModel.get_user_by_id(user['id'])
                if updated_user:
                    self.controller.app.set_user(updated_user)
                self.controller.app.show_snackbar(message, False)
                nueva_password_field.value = ""
                confirm_password_field.value = ""
            else:
                self.controller.app.show_snackbar(message, True)
            
            self.controller.app.page.update()
        
        header = ft.Row(
            [
                foto_container,
                ft.Column(
                    [
                        ft.Text(user.get('nombre_completo', ''), size=24, weight="bold"),
                        ft.Text(f"@{user.get('username', '')}", size=16, color=ft.colors.GREY_600),
                        ft.Text(f"Matrícula: {user.get('matricula', user.get('username', ''))}", size=14, color=ft.colors.GREY_500),
                    ]
                )
            ],
            vertical_alignment="center",
            spacing=30
        )
        
        all_content = ft.Column(
            [
                ft.Text("Mi Perfil", size=28, weight="bold", color=ft.colors.BLUE_700),
                ft.Divider(height=20),
                header,
                ft.Divider(height=20),
                nombre_field,
                curp_field,
                matricula_field,
                correo_field,
                celular_field,
                especialidad_field,
                username_field,
                ft.Divider(height=20),
                ft.Text("Cambiar Contraseña", size=18, weight="bold"),
                nueva_password_field,
                confirm_password_field,
                ft.Divider(height=20),
                ft.Row(
                    [
                        ft.ElevatedButton("Guardar Cambios", on_click=guardar_cambios, icon=ft.icons.SAVE),
                        ft.ElevatedButton("Regresar", on_click=lambda e: self.controller.app.show_dashboard(), icon=ft.icons.ARROW_BACK),
                    ],
                    spacing=20,
                    alignment="center"
                ),
                ft.Container(height=30),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment="center",
        )
        
        centered_container = ft.Row(
            [all_content],
            alignment="center",
            vertical_alignment="center",
            expand=True,
        )
        
        self.controller.app.clear_and_add(centered_container)