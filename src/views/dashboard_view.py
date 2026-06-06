import flet as ft

class DashboardView:
    def __init__(self, controller):
        self.controller = controller
        self.grades_container = None
        self.promedio_text = None
        self.semestre_dropdown = None
    
    def build(self):
        user = self.controller.app.get_user()
        
        # AppBar
        self.controller.app.page.appbar = ft.AppBar(
            title=ft.Text(f"Control Escolar - {user['nombre_completo']}", size=18),
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            toolbar_height=50,
            actions=[
                ft.IconButton(icon=ft.icons.ADD_CIRCLE, on_click=self.mostrar_dialogo_agregar, icon_size=20, tooltip="Agregar Materia"),
                ft.IconButton(icon=ft.icons.PERSON, on_click=lambda e: self.controller.app.show_profile(), icon_size=20),
                ft.IconButton(icon=ft.icons.EXIT_TO_APP, on_click=lambda e: self.controller.logout(), icon_size=20),
            ]
        )
        
        # Header
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"{user['nombre_completo']}", size=16, weight="bold"),
                    ft.Text(f"{user['especialidad_nombre']}", size=13),
                ],
                spacing=3
            ),
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border_radius=8
        )
        
        self.semestre_dropdown = ft.Dropdown(
            label="Semestre",
            width=180,
            value=str(self.controller.get_current_semester()),
            options=[ft.dropdown.Option(str(i), f"{i}° Semestre") for i in range(1, 7)]
        )
        self.semestre_dropdown.on_change = self.on_semester_change
        
        self.grades_container = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        self.promedio_text = ft.Text(size=16, weight="bold")
        
        self.refresh_grades()
        
        main_layout = ft.Column(
            [
                header,
                ft.Divider(height=10),
                ft.Row(
                    [ft.Text("Gestión de Calificaciones", size=20, weight="bold"), self.semestre_dropdown],
                    alignment="spaceBetween"
                ),
                ft.Divider(height=8),
                self.promedio_text,
                ft.Divider(height=10),
                self.grades_container,
            ],
            spacing=8,
            expand=True,
        )
        
        container = ft.Container(content=main_layout, padding=20, expand=True)
        self.controller.app.clear_and_add(container)
    
    def mostrar_dialogo_agregar(self, e):
        nombre_field = ft.TextField(label="Nombre de la materia", width=300)
        
        def agregar_click(e):
            nombre = nombre_field.value.strip()
            if not nombre:
                self.controller.app.show_snackbar("Ingrese el nombre de la materia", True)
                return
            
            success, message = self.controller.agregar_materia(nombre)
            if success:
                self.controller.app.show_snackbar(message, False)
                self.refresh_grades()
                dialog.open = False
            else:
                self.controller.app.show_snackbar(message, True)
            
            self.controller.app.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Agregar Nueva Materia"),
            content=nombre_field,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton("Agregar", on_click=agregar_click),
            ],
            actions_alignment="end",
        )
        
        self.controller.app.page.dialog = dialog
        dialog.open = True
        self.controller.app.page.update()
    
    def mostrar_dialogo_eliminar(self, materia_id: int, materia_nombre: str):
        def eliminar_click(e):
            success, message = self.controller.eliminar_materia(materia_id)
            if success:
                self.controller.app.show_snackbar(message, False)
                self.refresh_grades()
                dialog.open = False
            else:
                self.controller.app.show_snackbar(message, True)
            
            self.controller.app.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Eliminar Materia"),
            content=ft.Text(f"¿Eliminar la materia '{materia_nombre}'?\nSe eliminarán también todas sus calificaciones."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton("Eliminar", on_click=eliminar_click, bgcolor=ft.colors.RED, color=ft.colors.WHITE),
            ],
            actions_alignment="end",
        )
        
        self.controller.app.page.dialog = dialog
        dialog.open = True
        self.controller.app.page.update()
    
    def on_semester_change(self, e):
        self.controller.change_semester(int(self.semestre_dropdown.value))
    
    def calcular_promedio(self, unidad1, unidad2, unidad3):
        """Calcula el promedio solo con las unidades que tienen nota"""
        notas = []
        if unidad1 is not None and unidad1 != "" and unidad1 != 0:
            notas.append(float(unidad1))
        if unidad2 is not None and unidad2 != "" and unidad2 != 0:
            notas.append(float(unidad2))
        if unidad3 is not None and unidad3 != "" and unidad3 != 0:
            notas.append(float(unidad3))
        
        if len(notas) == 0:
            return 0.0
        return sum(notas) / len(notas)
    
    def refresh_grades(self):
        self.grades_container.controls.clear()
        
        materias = self.controller.get_materias()
        calificaciones = self.controller.get_calificaciones()
        calificaciones_dict = {c['materia_id']: c for c in calificaciones}
        
        if not materias:
            self.grades_container.controls.append(
                ft.Text("No hay materias registradas para este semestre", size=14, color=ft.colors.GREY_400)
            )
            self.update_promedios()
            return
        
        for materia in materias:
            calif = calificaciones_dict.get(materia['id'])
            
            u1_value = str(calif['unidad1']) if calif and calif['unidad1'] and calif['unidad1'] != 0 else ""
            u2_value = str(calif['unidad2']) if calif and calif['unidad2'] and calif['unidad2'] != 0 else ""
            u3_value = str(calif['unidad3']) if calif and calif['unidad3'] and calif['unidad3'] != 0 else ""
            
            u1_field = ft.TextField(
                label="Unidad 1", width=100, height=45,
                value=u1_value,
                text_size=13, text_align=ft.TextAlign.CENTER
            )
            u2_field = ft.TextField(
                label="Unidad 2", width=100, height=45,
                value=u2_value,
                text_size=13, text_align=ft.TextAlign.CENTER
            )
            u3_field = ft.TextField(
                label="Unidad 3", width=100, height=45,
                value=u3_value,
                text_size=13, text_align=ft.TextAlign.CENTER
            )
            
            promedio_text = ft.Text("", size=14, weight="bold")
            estado_text = ft.Text("", size=16)
            
            if calif:
                # Usar la función calcular_promedio
                notas = []
                if calif['unidad1'] and calif['unidad1'] != 0:
                    notas.append(calif['unidad1'])
                if calif['unidad2'] and calif['unidad2'] != 0:
                    notas.append(calif['unidad2'])
                if calif['unidad3'] and calif['unidad3'] != 0:
                    notas.append(calif['unidad3'])
                
                if len(notas) > 0:
                    promedio_val = sum(notas) / len(notas)
                    promedio_text.value = f"Prom: {promedio_val:.2f}"
                    estado_text.value = "✅ Aprobado" if promedio_val >= 6 else "❌ Reprobado"
                    estado_text.color = ft.colors.GREEN if promedio_val >= 6 else ft.colors.RED
            
            def make_save_handler(mid, u1, u2, u3, prom_txt, estado_txt):
                def save(e):
                    try:
                        # Obtener valores (pueden estar vacíos)
                        v1 = float(u1.value) if u1.value and u1.value.strip() else None
                        v2 = float(u2.value) if u2.value and u2.value.strip() else None
                        v3 = float(u3.value) if u3.value and u3.value.strip() else None
                        
                        # Validar que al menos una unidad tenga nota
                        if v1 is None and v2 is None and v3 is None:
                            self.controller.app.show_snackbar("Ingrese al menos una calificación", True)
                            return
                        
                        # Validar rango de notas (solo las que tienen valor)
                        for v in [v1, v2, v3]:
                            if v is not None and not (0 <= v <= 10):
                                self.controller.app.show_snackbar("Las calificaciones deben estar entre 0 y 10", True)
                                return
                        
                        # Guardar calificaciones
                        success, msg = self.controller.save_calificacion(mid, v1 if v1 is not None else 0, 
                                                                          v2 if v2 is not None else 0, 
                                                                          v3 if v3 is not None else 0)
                        
                        if success:
                            # Calcular promedio solo con las notas existentes
                            notas = [n for n in [v1, v2, v3] if n is not None]
                            if notas:
                                prom = sum(notas) / len(notas)
                                prom_txt.value = f"Prom: {prom:.2f}"
                                estado_txt.value = "✅ Aprobado" if prom >= 6 else "❌ Reprobado"
                                estado_txt.color = ft.colors.GREEN if prom >= 6 else ft.colors.RED
                            
                            self.update_promedios()
                            self.controller.app.show_snackbar(msg, False)
                        else:
                            self.controller.app.show_snackbar(msg, True)
                        
                        self.controller.app.page.update()
                    except ValueError:
                        self.controller.app.show_snackbar("Ingrese números válidos", True)
                return save
            
            save_btn = ft.ElevatedButton(
                "Guardar",
                on_click=make_save_handler(materia['id'], u1_field, u2_field, u3_field, promedio_text, estado_text),
                height=45, width=100
            )
            
            eliminar_btn = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED,
                icon_size=20,
                tooltip="Eliminar materia",
                on_click=lambda e, mid=materia['id'], mnom=materia['nombre']: self.mostrar_dialogo_eliminar(mid, mnom)
            )
            
            materia_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [ft.Text(materia['nombre'], size=16, weight="bold", expand=True), eliminar_btn],
                                alignment="spaceBetween"
                            ),
                            ft.Divider(height=5),
                            ft.Row([u1_field, u2_field, u3_field, save_btn, promedio_text, estado_text],
                                   alignment="start", spacing=15, wrap=True)
                        ],
                        spacing=10
                    ),
                    padding=15
                ),
                elevation=3
            )
            
            self.grades_container.controls.append(materia_card)
        
        self.update_promedios()
        self.controller.app.page.update()
    
    def update_promedios(self):
        semestre_prom, general_prom = self.controller.get_promedios()
        semester = self.controller.get_current_semester()
        self.promedio_text.value = f"📊 Promedio {semester}° Semestre: {semestre_prom:.2f}  |  📈 Promedio General: {general_prom:.2f}"