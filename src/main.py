import flet as ft
from controllers.app_controller import AppController

def main(page: ft.Page):
    page.title = "Sistema de Control Escolar"
    page.window_width = 1000
    page.window_height = 550
    page.window_resizable = True
    page.padding = 10
    
    app = AppController(page)
    app.run()

if __name__ == "__main__":
    ft.app(target=main)