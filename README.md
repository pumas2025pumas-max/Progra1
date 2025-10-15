# Kiwillet (versión simple)

Este proyecto implementa una billetera virtual muy sencilla para consola. El foco está en practicar el manejo de estructuras de datos básicas (listas y diccionarios) y el uso de archivos de texto como almacenamiento.

## Archivos utilizados
- `main.py`: contiene el programa principal con los menús y el flujo de la aplicación.
- `helpers.py`: módulo único con funciones de apoyo para leer y guardar información en archivos.
- `usuarios.txt`: cada línea guarda `usuario;contraseña;saldo`.
- `tarjetas.txt`: líneas con `usuario;alias;numero;tipo;vencimiento`.
- `movimientos.txt`: historial de operaciones en formato `usuario;fecha;concepto;monto;saldo`.
- `servicios.txt`: listado de servicios disponibles (`codigo;nombre;monto`). Si el archivo no existe se crea automáticamente con tres ejemplos.

## Cómo ejecutar
1. Asegurate de tener Python 3 instalado.
2. Desde la carpeta del proyecto corré:
   ```bash
   python main.py
   ```
3. El programa permite crear un usuario, iniciar sesión, cargar tarjetas, ingresar dinero, pagar servicios y consultar movimientos.

## Notas
- Todos los datos se guardan en los archivos `.txt` dentro de la carpeta del proyecto.
- Los montos se muestran con dos decimales y no se utilizan librerías externas.
- El objetivo es mantener el código claro y fácil de seguir, sin características avanzadas.
