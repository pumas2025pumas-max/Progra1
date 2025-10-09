# KIWILLET - Plan de implementación

## 1. Objetivo del proyecto
Desarrollar una billetera virtual de consola en Python que permita administrar usuarios, tarjetas, servicios y movimientos de dinero utilizando exclusivamente estructuras de datos simples (listas y diccionarios) y archivos planos (JSON/CSV). El sistema debe cumplir con los requerimientos funcionales y técnicos definidos por la cátedra para la segunda etapa del proyecto.

## 2. Alcance y supuestos
- **Interfaz**: aplicación de consola sin uso de librerías externas ni frameworks gráficos.
- **Persistencia**: almacenamiento mediante archivos JSON (credenciales) y CSV (registros de tarjetas, servicios, movimientos y reportes). No se emplean bases de datos ni servicios externos.
- **Usuarios**: autenticación básica con nombre de usuario y contraseña almacenados en archivo JSON encriptado simple (hash/obfuscación).
- **Moneda**: se trabaja con una única moneda (pesos ARS) y no se contemplan cotizaciones.
- **Sesiones**: un solo usuario logueado a la vez. No se maneja concurrencia.

## 3. Estructuras de datos previstas
- `usuarios`: lista de diccionarios con campos `usuario`, `password_hash`, `saldo_disponible`.
- `tarjetas`: lista de diccionarios asociados al usuario activo con `id`, `tipo`, `entidad`, `numero_enmascarado`, `vencimiento`, `cvc_encriptado`.
- `servicios`: lista de diccionarios con `id`, `nombre`, `categoria` (luz, gas, internet, etc.) y `monto`.
- `movimientos`: lista de diccionarios con `fecha`, `tipo` (pago, recarga, transferencia), `descripcion`, `monto`, `saldo_resultante`.
- `log_bitacora`: lista de entradas con `timestamp`, `accion`, `detalle` para auditoría básica.

## 4. Módulos y responsabilidades
1. **Inicio (`main.py`)**
   - Cargar archivos de datos.
   - Presentar menú principal e invocar acciones.
2. **Gestión de usuarios (`usuarios.py`)**
   - Alta de usuarios (validar duplicados).
   - Inicio de sesión y cierre.
   - Modificación de contraseña y control de saldo.
3. **Tarjetas (`tarjetas.py`)**
   - Alta, consulta y eliminación de tarjetas.
   - Registro de pagos con tarjeta (descarga automática del saldo disponible).
4. **Servicios (`servicios.py`)**
   - Listado y registro de servicios habituales.
   - Pagos de servicios y almacenamiento en `movimientos`.
5. **Movimientos y reportes (`movimientos.py`)**
   - Registrar ingresos, pagos y transferencias.
   - Generar estadísticas diarias (saldo promedio, mayor/menor saldo).
   - Exportar reportes CSV y resumen diario.
6. **Utilitarios (`io_archivos.py`, `seguridad.py`, `logger.py`)**
   - Lectura/escritura de JSON y CSV.
   - Hash/validación de contraseñas.
   - Registro de bitácora en archivo `.log` con fecha y hora.

## 5. Flujo general del programa
1. Mostrar pantalla de bienvenida y menú principal.
2. Permitir crear usuario nuevo o iniciar sesión existente.
3. Tras autenticación, mostrar menú principal con opciones:
   1. Gestión de tarjetas
   2. Pago de servicios
   3. Modificar cuenta (contraseña, alias, saldo inicial)
   4. Transferencias y recargas
   5. Consultar reportes y estadísticas
   6. Salir
4. Cada opción invoca funciones específicas, actualiza estructuras y persiste cambios.
5. Al salir, guardar archivos actualizados y registrar la acción en la bitácora.

## 6. Gestión de archivos
- `usuarios.json`: credenciales y saldo inicial cifrado mediante hash.
- `tarjetas_<usuario>.csv`: tarjetas activas del usuario logueado.
- `servicios.csv`: catálogo base de servicios disponibles.
- `movimientos_<usuario>.csv`: histórico de operaciones.
- `bitacora.log`: registro de todas las acciones con marca temporal.
- `estadisticas_<fecha>.csv`: resumen diario generado al cierre de sesión.

## 7. Manejo de errores y validaciones
- Validar entradas de usuario (tipos, rangos, formatos).
- Controlar que no existan operaciones con saldo insuficiente.
- Evitar duplicados en tarjetas y servicios asociados al usuario.
- Capturar excepciones de lectura/escritura de archivos y registrar en la bitácora.
- Reintentar operaciones críticas o notificar al usuario de manera clara.

## 8. Seguridad básica
- Almacenar contraseñas con hash (por ejemplo `hashlib.sha256`).
- Enmascarar datos sensibles de tarjetas al mostrarlos (últimos 4 dígitos).
- Registrar intentos fallidos de login.
- Bloquear temporalmente el usuario tras N intentos incorrectos.

## 9. Estadísticas y reportes
- Calcular saldo mínimo, máximo y promedio por día.
- Identificar mayor ingreso y mayor gasto del período.
- Generar tabla resumen y exportar a CSV para análisis en Excel.
- Incluir resumen en consola al finalizar la sesión.

## 10. Plan de pruebas
- **Pruebas unitarias básicas**: funciones de validación y cálculos.
- **Pruebas manuales**:
  - Alta y login de usuario.
  - Registro de tarjetas, pagos y recargas.
  - Validación de saldo insuficiente.
  - Generación de reportes.
  - Revisión de bitácora.

## 11. Cronograma sugerido
1. Configurar estructura del proyecto y archivos base.
2. Implementar gestión de usuarios y persistencia JSON.
3. Desarrollar módulos de tarjetas y servicios con operaciones básicas.
4. Añadir registro de movimientos y reportes.
5. Integrar logging y manejo de errores.
6. Ejecutar pruebas y preparar documentación final.

## 12. Entregables
- Código fuente en repositorio Git con historial limpio.
- Archivos JSON/CSV de prueba.
- Bitácora `.log` con eventos relevantes.
- Documentación (README + memoria en DOCX basada en este plan).
- Capturas o registros de ejecución (opcional para la presentación).
