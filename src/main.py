import flet as ft
from controllers.app_controller import AppController

def main(page: ft.Page):
    app = AppController(page)
    app.run()

if __name__ == "__main__":
    ft.app(target=main)