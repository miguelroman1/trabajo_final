Proyecto Control Escolar - Unidad 3
Este repositorio contiene el sistema de Control Escolar, una aplicación de escritorio/web robusta desarrollada en Python utilizando Flet para la interfaz gráfica y MySQL como sistema de gestión de bases de datos.

📋 Descripción de los Componentes del Proyecto
A continuación se detalla el cumplimiento de cada uno de los criterios de evaluación establecidos en la rúbrica:

1. 🗄️ Base de Datos e Historial (20%)
Estructura Relacional: El sistema cuenta con un diseño de base de datos totalmente normalizado que garantiza la integridad de la información escolar. Incluye de forma obligatoria la tabla de Especialidades para clasificar correctamente el historial de los alumnos.

Script SQL: En la raíz del proyecto (o carpeta correspondiente) se adjunta el archivo .sql listo para su ejecución. Está optimizado y estructurado de manera que funciona correctamente a la primera, creando las tablas, llaves primarias, foráneas y registros iniciales sin errores.

2. 🛡️ Validación de Datos (20%)
Aplicación "A prueba de errores": El sistema cuenta con capas de validación robustas antes de procesar cualquier solicitud en la base de datos para evitar caídas de la aplicación (crashes).

Alertas del Sistema: Se implementaron componentes nativos de Flet (AlertDialog y SnackBar) para notificar al usuario de forma clara en los siguientes escenarios:

Campos obligatorios vacíos o datos faltantes.

Notas o calificaciones fuera del rango permitido (el sistema restringe estrictamente que los valores estén en el rango de 0 a 10).

3. 🧮 Lógica y Cálculos en Python (20%)
Toda la lógica de negocio está programada en Python de manera precisa y eficiente, cumpliendo con los siguientes requerimientos analíticos:

Promedio por Unidad: Cálculo exacto de las calificaciones parciales de los estudiantes.

Promedio por Materia: Consolidación de las notas de las unidades para obtener la calificación final de cada asignatura.

Promedio General Acumulado: Módulo automatizado que calcula el promedio global histórico de cada alumno a lo largo de su estancia escolar.

4. 🎨 Interfaz Flet y Login (15%)
El diseño de la interfaz de usuario (UI) se construyó priorizando la experiencia del usuario (UX) mediante vistas fluidas, reactivas y completamente funcionales:

Pantalla de Login: Sistema de acceso seguro para usuarios registrados.

Pantalla de Registro: Formulario validado para el alta de nuevos usuarios en el sistema.

Dashboard Principal: Panel de control intuitivo y estético que permite navegar fácilmente entre los diferentes módulos (Alumnos, Materias, Calificaciones, etc.).

5. 📄 Documentación (15%)
El desarrollo del proyecto está respaldado por un reporte formal adjunto que incluye:

Diagrama Entidad-Relación (DER): El modelado gráfico completo de la base de datos.

Evidencias del Sistema: Capturas de pantalla detalladas que demuestran el correcto funcionamiento de las validaciones, alertas y cálculos de la aplicación.

6. 📁 Estructura del Repositorio (10%)
Este repositorio se mantiene bajo las mejores prácticas de desarrollo de software:

Organización: Código limpio y ordenado en carpetas específicas según su función (arquitectura del proyecto).

Historial de Cambios: Uso riguroso de Git con commits frecuentes y mensajes descriptivos que explican el avance del desarrollo.

Código Listo: El código es completamente funcional y ejecutable siguiendo las instrucciones de este documento.

🚀 Instrucciones de Ejecución
(Opcional: Aquí pueden agregar los comandos rápidos para que su profesor lo corra, por ejemplo:)

Clonar el repositorio.

Importar el archivo .sql en su gestor de bases de datos.

Instalar dependencias: pip install flet mysql-connector-python

Ejecutar la aplicación: python main.py




Te extraño America vuelve a mis brazos ❤️ 