import flet as ft
from models.user_model import UserModel

class ProfileView:
    def __init__(self, controller):
        self.controller = controller
        self.edit_mode = False
        
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
        self.nombre_field = ft.TextField(label="Nombre Completo", value=user.get('nombre_completo', ''), width=400, read_only=True)
        self.curp_field = ft.TextField(label="CURP", value=user.get('curp', ''), width=400, read_only=True)
        self.matricula_field = ft.TextField(label="Matrícula", value=user.get('matricula', user.get('username', '')), width=400, read_only=True)
        self.correo_field = ft.TextField(label="Correo Institucional", value=user.get('correo', ''), width=400, read_only=True)
        self.celular_field = ft.TextField(label="Celular", value=user.get('celular', ''), width=400, read_only=True)
        self.especialidad_field = ft.TextField(label="Especialidad", value=user.get('especialidad_nombre', ''), width=400, read_only=True)
        self.username_field = ft.TextField(label="Usuario", value=user.get('username', ''), width=400, read_only=True)
        
        self.nueva_password_field = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, width=400, visible=False)
        self.confirm_password_field = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, width=400, visible=False)
        
        # Foto de perfil
        self.foto_container = ft.Container(
            width=120, height=120,
            bgcolor=ft.colors.BLUE_100,
            border_radius=60,
            content=ft.Icon(ft.icons.PERSON, size=60, color=ft.colors.BLUE_700),
        )
        
        self.edit_btn = ft.ElevatedButton("Editar Perfil", on_click=self.toggle_edit, icon=ft.icons.EDIT)
        self.save_btn = ft.ElevatedButton("Guardar Cambios", on_click=self.save_profile, icon=ft.icons.SAVE, visible=False)
        self.cancel_btn = ft.OutlinedButton("Cancelar", on_click=self.toggle_edit, visible=False)
        self.change_password_btn = ft.TextButton("Cambiar Contraseña", on_click=self.toggle_password_fields, visible=False)
        
        header = ft.Row(
            [
                self.foto_container,
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
        
        # Column con SCROLL y centrado horizontal
        all_content = ft.Column(
            [
                ft.Text("Mi Perfil", size=28, weight="bold", color=ft.colors.BLUE_700),
                ft.Divider(height=20),
                header,
                ft.Divider(height=20),
                self.nombre_field,
                self.curp_field,
                self.matricula_field,
                self.correo_field,
                self.celular_field,
                self.especialidad_field,
                self.username_field,
                ft.Divider(height=20),
                self.nueva_password_field,
                self.confirm_password_field,
                ft.Row([self.edit_btn, self.save_btn, self.cancel_btn, self.change_password_btn],
                       spacing=20),
                ft.Divider(height=20),
                ft.ElevatedButton("Regresar al Dashboard", on_click=lambda e: self.controller.app.show_dashboard(),
                                  icon=ft.icons.ARROW_BACK, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, width=300),
                ft.Container(height=30),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment="center",
        )
        
        # Contenedor principal - centrado usando una Row
        centered_container = ft.Row(
            [all_content],
            alignment="center",
            vertical_alignment="center",
            expand=True,
        )
        
        self.controller.app.clear_and_add(centered_container)
    
    def toggle_edit(self, e):
        self.edit_mode = not self.edit_mode
        read_only = not self.edit_mode
        self.nombre_field.read_only = read_only
        self.curp_field.read_only = read_only
        self.matricula_field.read_only = read_only
        self.correo_field.read_only = read_only
        self.celular_field.read_only = read_only
        
        self.edit_btn.visible = not self.edit_mode
        self.save_btn.visible = self.edit_mode
        self.cancel_btn.visible = self.edit_mode
        self.change_password_btn.visible = self.edit_mode
        
        if not self.edit_mode:
            self.nueva_password_field.visible = False
            self.confirm_password_field.visible = False
            self.nueva_password_field.value = ""
            self.confirm_password_field.value = ""
        
        self.controller.app.page.update()
    
    def toggle_password_fields(self, e):
        visible = not self.nueva_password_field.visible
        self.nueva_password_field.visible = visible
        self.confirm_password_field.visible = visible
        if not visible:
            self.nueva_password_field.value = ""
            self.confirm_password_field.value = ""
        self.controller.app.page.update()
    
    def save_profile(self, e):
        user = self.controller.app.get_user()
        
        new_password = None
        if self.nueva_password_field.value:
            if self.nueva_password_field.value != self.confirm_password_field.value:
                self.controller.app.show_snackbar("Las contraseñas no coinciden", True)
                return
            if len(self.nueva_password_field.value) < 6:
                self.controller.app.show_snackbar("La contraseña debe tener al menos 6 caracteres", True)
                return
            new_password = self.nueva_password_field.value
        
        update_data = {
            'nombre_completo': self.nombre_field.value,
            'curp': self.curp_field.value.upper(),
            'matricula': self.matricula_field.value,
            'correo': self.correo_field.value,
            'celular': self.celular_field.value
        }
        
        success, message = UserModel.update_profile(user['id'], update_data, new_password)
        
        if success:
            updated_user = UserModel.get_user_by_id(user['id'])
            if updated_user:
                self.controller.app.set_user(updated_user)
            self.controller.app.show_snackbar(message, False)
            self.toggle_edit(None)
        else:
            self.controller.app.show_snackbar(message, True)
        
        self.controller.app.page.update()