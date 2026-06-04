import flet as ft

class LoginView:
    def __init__(self, controller):
        self.controller = controller
    
    def build(self):
        title = ft.Text(
            "Sistema de Gestión de Calificaciones",
            size=32,
            weight="bold",
        )
        
        self.username_field = ft.TextField(label="Usuario", width=300)
        self.password_field = ft.TextField(
            label="Contraseña",
            width=300,
            password=True,
            can_reveal_password=True
        )
        
        def on_login(e):
            self.controller.handle_login(
                self.username_field.value,
                self.password_field.value
            )
        
        def on_register(e):
            self.controller.show_register()
        
        login_btn = ft.ElevatedButton("Iniciar Sesión", on_click=on_login, width=300)
        register_btn = ft.TextButton("¿No tienes cuenta? Regístrate aquí", on_click=on_register)
        
        login_card = ft.Container(
            content=ft.Column(
                [title, ft.Divider(height=20), self.username_field, 
                 self.password_field, login_btn, register_btn],
                horizontal_alignment="center",
                spacing=15
            ),
            padding=30,
            width=400,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10)
        )
        
        self.controller.app.clear_and_add(
            ft.Row([login_card], alignment="center", vertical_alignment="center")
        )