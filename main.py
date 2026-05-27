import flet as ft
import mysql.connector
import hashlib
import re
from typing import Optional, Dict, List

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sistema_calificaciones'
}

class DatabaseManager:
    """Maneja todas las operaciones de la base de datos"""
    
    @staticmethod
    def get_connection():
        return mysql.connector.connect(**DB_CONFIG)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return DatabaseManager.hash_password(password) == hashed
    
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_curp(curp: str) -> bool:
        pattern = r'^[A-Z]{4}\d{6}[A-Z]{6}\d{2}$'
        return re.match(pattern, curp) is not None
    
    @staticmethod
    def register_user(user_data: Dict) -> tuple:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id FROM usuarios WHERE username = %s OR correo = %s OR matricula = %s",
                          (user_data['username'], user_data['correo'], user_data['matricula']))
            if cursor.fetchone():
                return False, "El usuario, correo o matrícula ya existe"
            
            query = """
                INSERT INTO usuarios 
                (nombre_completo, curp, matricula, correo, celular, foto_perfil, username, password, especialidad_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            hashed_password = DatabaseManager.hash_password(user_data['password'])
            cursor.execute(query, (
                user_data['nombre_completo'],
                user_data['curp'],
                user_data['matricula'],
                user_data['correo'],
                user_data['celular'],
                user_data.get('foto_perfil', ''),
                user_data['username'],
                hashed_password,
                user_data['especialidad_id']
            ))
            conn.commit()
            return True, "Usuario registrado exitosamente"
        except Exception as e:
            return False, f"Error al registrar: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def login_user(username: str, password: str) -> Optional[Dict]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT u.*, e.nombre as especialidad_nombre 
                FROM usuarios u
                JOIN especialidades e ON u.especialidad_id = e.id
                WHERE u.username = %s
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            if user and DatabaseManager.verify_password(password, user['password']):
                return user
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_materias_por_semestre(especialidad_id: int, semestre: int) -> List[Dict]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, nombre, semestre 
                FROM materias 
                WHERE especialidad_id = %s AND semestre = %s
                ORDER BY nombre
            """, (especialidad_id, semestre))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_calificaciones(usuario_id: int, semestre: int) -> List[Dict]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT c.*, m.nombre as materia_nombre 
                FROM calificaciones c
                JOIN materias m ON c.materia_id = m.id
                WHERE c.usuario_id = %s AND c.semestre = %s
            """, (usuario_id, semestre))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def save_calificacion(usuario_id: int, materia_id: int, semestre: int, 
                          unidad1: float, unidad2: float, unidad3: float) -> tuple:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        try:
            promedio = round((unidad1 + unidad2 + unidad3) / 3, 2)
            
            cursor.execute("""
                SELECT id FROM calificaciones 
                WHERE usuario_id = %s AND materia_id = %s AND semestre = %s
            """, (usuario_id, materia_id, semestre))
            
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE calificaciones 
                    SET unidad1 = %s, unidad2 = %s, unidad3 = %s, promedio = %s
                    WHERE usuario_id = %s AND materia_id = %s AND semestre = %s
                """, (unidad1, unidad2, unidad3, promedio, usuario_id, materia_id, semestre))
            else:
                cursor.execute("""
                    INSERT INTO calificaciones 
                    (usuario_id, materia_id, semestre, unidad1, unidad2, unidad3, promedio)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (usuario_id, materia_id, semestre, unidad1, unidad2, unidad3, promedio))
            
            conn.commit()
            return True, "Calificación guardada exitosamente"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_promedio_general(usuario_id: int, semestre: int = None) -> float:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        try:
            if semestre:
                query = """
                    SELECT AVG(promedio) as promedio 
                    FROM calificaciones 
                    WHERE usuario_id = %s AND semestre = %s
                """
                cursor.execute(query, (usuario_id, semestre))
            else:
                query = "SELECT AVG(promedio) as promedio FROM calificaciones WHERE usuario_id = %s"
                cursor.execute(query, (usuario_id,))
            
            result = cursor.fetchone()
            return round(result[0], 2) if result and result[0] else 0.0
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_especialidades() -> List[Dict]:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, nombre FROM especialidades ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

class GradeManagerApp:
    def __init__(self):
        self.current_user = None
        self.selected_semester = 1
        self.page = None
    
    def main(self, page: ft.Page):
        self.page = page
        page.title = "Sistema de Gestión de Calificaciones"
        page.padding = 20
        page.window_width = 1200
        page.window_height = 800
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        
        self.show_login()
    
    def show_snackbar(self, message: str, is_error: bool = False):
        """Muestra un mensaje temporal en la parte inferior"""
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED if is_error else ft.Colors.GREEN,
            open=True
        )
        self.page.overlay.append(snackbar)
        self.page.update()
    
    def show_login(self):
        """Muestra la pantalla de login"""
        self.page.controls.clear()
        
        title = ft.Text(
            "Sistema de Gestión de Calificaciones",
            size=32,
            weight="bold",
            color=ft.Colors.BLUE
        )
        
        username_field = ft.TextField(
            label="Usuario",
            width=300
        )
        
        password_field = ft.TextField(
            label="Contraseña",
            width=300,
            password=True,
            can_reveal_password=True
        )
        
        error_text = ft.Text("", color=ft.Colors.RED)
        
        def on_login(e):
            if not username_field.value or not password_field.value:
                error_text.value = "Todos los campos son obligatorios"
                self.page.update()
                return
            
            user = DatabaseManager.login_user(username_field.value, password_field.value)
            if user:
                self.current_user = user
                self.show_dashboard()
            else:
                error_text.value = "Usuario o contraseña incorrectos"
                self.page.update()
        
        def on_register(e):
            self.show_register()
        
        login_btn = ft.ElevatedButton(
            "Iniciar Sesión",
            on_click=on_login,
            width=300
        )
        
        register_btn = ft.TextButton(
            "¿No tienes cuenta? Regístrate aquí",
            on_click=on_register
        )
        
        login_card = ft.Container(
            content=ft.Column(
                [
                    title,
                    ft.Divider(height=20),
                    username_field,
                    password_field,
                    error_text,
                    login_btn,
                    register_btn,
                ],
                horizontal_alignment="center",
                spacing=15
            ),
            padding=30,
            width=400,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.GREY
            )
        )
        
        self.page.add(
            ft.Row(
                [login_card],
                alignment="center",
                vertical_alignment="center"
            )
        )
        self.page.update()
    
    def show_register(self):
        """Muestra la pantalla de registro con scroll"""
        self.page.controls.clear()
        
        error_text = ft.Text("", color=ft.Colors.RED)
        
        especialidades = DatabaseManager.get_especialidades()
        especialidad_options = [ft.dropdown.Option(str(e['id']), e['nombre']) for e in especialidades]
        
        nombre_field = ft.TextField(label="Nombre Completo", width=400)
        curp_field = ft.TextField(label="CURP", width=400)
        matricula_field = ft.TextField(label="Matrícula", width=400)
        correo_field = ft.TextField(label="Correo Institucional", width=400)
        celular_field = ft.TextField(label="Celular", width=400)
        username_field = ft.TextField(label="Usuario", width=400)
        password_field = ft.TextField(label="Contraseña", width=400, password=True)
        confirm_password_field = ft.TextField(label="Confirmar Contraseña", width=400, password=True)
        especialidad_dropdown = ft.Dropdown(
            label="Especialidad",
            width=400,
            options=especialidad_options
        )
        
        def on_submit(e):
            required_fields = [
                nombre_field, curp_field, matricula_field, 
                correo_field, username_field, password_field, 
                confirm_password_field, especialidad_dropdown
            ]
            
            for field in required_fields:
                if not field.value:
                    error_text.value = "Todos los campos son obligatorios"
                    self.page.update()
                    return
            
            if not DatabaseManager.validate_curp(curp_field.value.upper()):
                error_text.value = "CURP no válida (Formato: 4 letras, 6 números, 6 letras, 2 números)"
                self.page.update()
                return
            
            if not DatabaseManager.validate_email(correo_field.value):
                error_text.value = "Correo electrónico no válido"
                self.page.update()
                return
            
            if password_field.value != confirm_password_field.value:
                error_text.value = "Las contraseñas no coinciden"
                self.page.update()
                return
            
            if len(password_field.value) < 6:
                error_text.value = "La contraseña debe tener al menos 6 caracteres"
                self.page.update()
                return
            
            user_data = {
                'nombre_completo': nombre_field.value,
                'curp': curp_field.value.upper(),
                'matricula': matricula_field.value,
                'correo': correo_field.value,
                'celular': celular_field.value,
                'username': username_field.value,
                'password': password_field.value,
                'especialidad_id': int(especialidad_dropdown.value)
            }
            
            success, message = DatabaseManager.register_user(user_data)
            if success:
                self.show_snackbar(message, False)
                self.show_login()
            else:
                error_text.value = message
                self.page.update()
        
        def on_back(e):
            self.show_login()
        
        form_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registro de Alumno", size=28, weight="bold", color=ft.Colors.BLUE),
                    ft.Divider(height=20),
                    nombre_field,
                    curp_field,
                    matricula_field,
                    correo_field,
                    celular_field,
                    username_field,
                    password_field,
                    confirm_password_field,
                    especialidad_dropdown,
                    error_text,
                    ft.Row(
                        [
                            ft.ElevatedButton("Registrarse", on_click=on_submit),
                            ft.TextButton("Volver", on_click=on_back)
                        ],
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
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.GREY
            )
        )
        
        self.page.add(
            ft.Row(
                [form_container],
                alignment="center",
                vertical_alignment="center"
            )
        )
        self.page.update()
    
    def show_dashboard(self):
        """Muestra el panel principal"""
        self.page.controls.clear()
        
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"Bienvenido, {self.current_user['nombre_completo']}",
                                   size=24, weight="bold"),
                            ft.Text(f"Especialidad: {self.current_user['especialidad_nombre']}",
                                   size=16),
                            ft.Text(f"Matrícula: {self.current_user['matricula']}",
                                   size=14, color=ft.Colors.GREY)
                        ],
                        spacing=5
                    ),
                    ft.TextButton(
                        "Cerrar Sesión",
                        on_click=lambda e: self.show_login()
                    )
                ],
                alignment="spaceBetween"
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_BLUE_100,
            border_radius=10
        )
        
        semestre_dropdown = ft.Dropdown(
            label="Semestre",
            width=200,
            value=str(self.selected_semester),
            options=[ft.dropdown.Option(str(i), f"{i}° Semestre") for i in range(1, 7)]
        )
        
        grades_container = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO, height=500)
        promedio_general_text = ft.Text(size=20, weight="bold")
        
        def on_semester_change(e):
            self.selected_semester = int(semestre_dropdown.value)
            update_grades_view()
        
        semestre_dropdown.on_change = on_semester_change
        
        def update_grades_view():
            grades_container.controls.clear()
            
            materias = DatabaseManager.get_materias_por_semestre(
                self.current_user['especialidad_id'], 
                self.selected_semester
            )
            
            if not materias:
                grades_container.controls.append(
                    ft.Text("No hay materias registradas para este semestre", size=16, color=ft.Colors.GREY)
                )
                self.page.update()
                return
            
            calificaciones = DatabaseManager.get_calificaciones(
                self.current_user['id'], 
                self.selected_semester
            )
            
            calificaciones_dict = {c['materia_id']: c for c in calificaciones}
            
            for materia in materias:
                calif = calificaciones_dict.get(materia['id'])
                
                u1_field = ft.TextField(
                    label="Unidad 1",
                    width=120,
                    value=str(calif['unidad1']) if calif and calif['unidad1'] else "",
                )
                
                u2_field = ft.TextField(
                    label="Unidad 2",
                    width=120,
                    value=str(calif['unidad2']) if calif and calif['unidad2'] else "",
                )
                
                u3_field = ft.TextField(
                    label="Unidad 3",
                    width=120,
                    value=str(calif['unidad3']) if calif and calif['unidad3'] else "",
                )
                
                promedio_text = ft.Text("", size=16, weight="bold")
                estado_text = ft.Text("", size=14, weight="bold")
                
                def make_save_handler(materia_id, u1, u2, u3, prom_text, estado_text_ref):
                    def save(e):
                        try:
                            if not u1.value or not u2.value or not u3.value:
                                self.show_snackbar("Todos los campos son obligatorios", True)
                                return
                            
                            val1 = float(u1.value)
                            val2 = float(u2.value)
                            val3 = float(u3.value)
                            
                            if not all(0 <= v <= 10 for v in [val1, val2, val3]):
                                self.show_snackbar("Las calificaciones deben estar entre 0 y 10", True)
                                return
                            
                            success, message = DatabaseManager.save_calificacion(
                                self.current_user['id'],
                                materia_id,
                                self.selected_semester,
                                val1, val2, val3
                            )
                            
                            if success:
                                promedio = (val1 + val2 + val3) / 3
                                prom_text.value = f"Promedio: {promedio:.2f}"
                                
                                if promedio >= 6:
                                    estado_text_ref.value = "✅ Aprobado"
                                    estado_text_ref.color = ft.Colors.GREEN
                                else:
                                    estado_text_ref.value = "❌ Reprobado"
                                    estado_text_ref.color = ft.Colors.RED
                                
                                general_prom = DatabaseManager.get_promedio_general(
                                    self.current_user['id']
                                )
                                general_total_prom = DatabaseManager.get_promedio_general(
                                    self.current_user['id'], 
                                    self.selected_semester
                                )
                                promedio_general_text.value = f"Promedio del {self.selected_semester}° Semestre: {general_total_prom:.2f}  |  Promedio General Acumulado: {general_prom:.2f}"
                                
                                self.show_snackbar(message, False)
                            else:
                                self.show_snackbar(message, True)
                            
                            self.page.update()
                            
                        except ValueError:
                            self.show_snackbar("Las calificaciones deben ser números válidos", True)
                    
                    return save
                
                if calif:
                    promedio_val = (calif['unidad1'] + calif['unidad2'] + calif['unidad3']) / 3
                    promedio_text.value = f"Promedio: {promedio_val:.2f}"
                    
                    if promedio_val >= 6:
                        estado_text.value = "✅ Aprobado"
                        estado_text.color = ft.Colors.GREEN
                    else:
                        estado_text.value = "❌ Reprobado"
                        estado_text.color = ft.Colors.RED
                
                save_btn = ft.ElevatedButton(
                    "Guardar",
                    on_click=make_save_handler(materia['id'], u1_field, u2_field, u3_field, 
                                              promedio_text, estado_text)
                )
                
                materia_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(materia['nombre'], size=18, weight="bold"),
                                ft.Divider(),
                                ft.Row(
                                    [u1_field, u2_field, u3_field, save_btn, promedio_text, estado_text],
                                    alignment="start",
                                    spacing=20,
                                    wrap=True
                                )
                            ],
                            spacing=10
                        ),
                        padding=15
                    )
                )
                
                grades_container.controls.append(materia_card)
            
            general_prom = DatabaseManager.get_promedio_general(
                self.current_user['id'],
                self.selected_semester
            )
            general_total_prom = DatabaseManager.get_promedio_general(
                self.current_user['id']
            )
            
            promedio_general_text.value = f"Promedio del {self.selected_semester}° Semestre: {general_prom:.2f}  |  Promedio General Acumulado: {general_total_prom:.2f}"
            
            self.page.update()
        
        update_grades_view()
        
        self.page.add(
            header,
            ft.Divider(height=20),
            ft.Row(
                [ft.Text("Gestión de Calificaciones", size=24, weight="bold"),
                 semestre_dropdown],
                alignment="spaceBetween"
            ),
            ft.Divider(height=10),
            promedio_general_text,
            ft.Divider(height=10),
            grades_container
        )
        self.page.update()

if __name__ == "__main__":
    app = GradeManagerApp()
    ft.app(target=app.main)