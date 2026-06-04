import flet as ft

class DashboardView:
    def __init__(self, controller):
        self.controller = controller
        self.grades_container = None
        self.promedio_text = None
        self.semestre_dropdown = None
    
    def build(self):
        user = self.controller.app.get_user()
        
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"Bienvenido, {user['nombre_completo']}", size=24, weight="bold"),
                            ft.Text(f"Especialidad: {user['especialidad_nombre']}", size=16),
                        ],
                        spacing=5
                    ),
                    ft.TextButton("Cerrar Sesión", on_click=lambda e: self.controller.logout())
                ],
                alignment="spaceBetween"
            ),
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10
        )
        
        self.semestre_dropdown = ft.Dropdown(
            label="Semestre",
            width=200,
            value=str(self.controller.get_current_semester()),
            options=[ft.dropdown.Option(str(i), f"{i}° Semestre") for i in range(1, 7)]
        )
        self.semestre_dropdown.on_change = self.on_semester_change
        
        self.grades_container = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO, height=500)
        self.promedio_text = ft.Text(size=20, weight="bold")
        
        self.refresh_grades()
        
        self.controller.app.clear_and_add(
            header,
            ft.Divider(height=20),
            ft.Row([ft.Text("Gestión de Calificaciones", size=24, weight="bold"), self.semestre_dropdown],
                   alignment="spaceBetween"),
            ft.Divider(height=10),
            self.promedio_text,
            ft.Divider(height=10),
            self.grades_container
        )
    
    def on_semester_change(self, e):
        self.controller.change_semester(int(self.semestre_dropdown.value))
    
    def refresh_grades(self):
        self.grades_container.controls.clear()
        
        materias = self.controller.get_materias()
        calificaciones = self.controller.get_calificaciones()
        calificaciones_dict = {c['materia_id']: c for c in calificaciones}
        
        if not materias:
            self.grades_container.controls.append(
                ft.Text("No hay materias registradas para este semestre", size=16, color=ft.colors.GREY_400)
            )
            self.update_promedios()
            return
        
        for materia in materias:
            calif = calificaciones_dict.get(materia['id'])
            
            u1_field = ft.TextField(
                label="Unidad 1", width=120,
                value=str(calif['unidad1']) if calif and calif['unidad1'] else "",
            )
            u2_field = ft.TextField(
                label="Unidad 2", width=120,
                value=str(calif['unidad2']) if calif and calif['unidad2'] else "",
            )
            u3_field = ft.TextField(
                label="Unidad 3", width=120,
                value=str(calif['unidad3']) if calif and calif['unidad3'] else "",
            )
            
            promedio_text = ft.Text("", size=16, weight="bold")
            estado_text = ft.Text("", size=14, weight="bold")
            
            if calif:
                promedio_val = (calif['unidad1'] + calif['unidad2'] + calif['unidad3']) / 3
                promedio_text.value = f"Promedio: {promedio_val:.2f}"
                estado_text.value = "✅ Aprobado" if promedio_val >= 6 else "❌ Reprobado"
                estado_text.color = ft.colors.GREEN if promedio_val >= 6 else ft.colors.RED
            
            def make_save_handler(materia_id, u1, u2, u3, prom_text, estado_text_ref):
                def save(e):
                    try:
                        if not u1.value or not u2.value or not u3.value:
                            self.controller.app.show_snackbar("Todos los campos son obligatorios", True)
                            return
                        
                        val1 = float(u1.value)
                        val2 = float(u2.value)
                        val3 = float(u3.value)
                        
                        if not all(0 <= v <= 10 for v in [val1, val2, val3]):
                            self.controller.app.show_snackbar("Las calificaciones deben estar entre 0 y 10", True)
                            return
                        
                        success, message = self.controller.save_calificacion(materia_id, val1, val2, val3)
                        
                        if success:
                            promedio = (val1 + val2 + val3) / 3
                            prom_text.value = f"Promedio: {promedio:.2f}"
                            
                            if promedio >= 6:
                                estado_text_ref.value = "✅ Aprobado"
                                estado_text_ref.color = ft.colors.GREEN
                            else:
                                estado_text_ref.value = "❌ Reprobado"
                                estado_text_ref.color = ft.colors.RED
                            
                            self.update_promedios()
                            self.controller.app.show_snackbar(message, False)
                        else:
                            self.controller.app.show_snackbar(message, True)
                        
                        self.controller.app.page.update()
                        
                    except ValueError:
                        self.controller.app.show_snackbar("Las calificaciones deben ser números válidos", True)
                
                return save
            
            save_btn = ft.ElevatedButton(
                "Guardar",
                on_click=make_save_handler(materia['id'], u1_field, u2_field, u3_field, promedio_text, estado_text)
            )
            
            materia_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(materia['nombre'], size=18, weight="bold"),
                            ft.Divider(),
                            ft.Row([u1_field, u2_field, u3_field, save_btn, promedio_text, estado_text],
                                   alignment="start", spacing=20, wrap=True)
                        ],
                        spacing=10
                    ),
                    padding=15
                )
            )
            
            self.grades_container.controls.append(materia_card)
        
        self.update_promedios()
        self.controller.app.page.update()
    
    def update_promedios(self):
        semestre_prom, general_prom = self.controller.get_promedios()
        semester = self.controller.get_current_semester()
        self.promedio_text.value = f"Promedio del {semester}° Semestre: {semestre_prom:.2f}  |  Promedio General Acumulado: {general_prom:.2f}"