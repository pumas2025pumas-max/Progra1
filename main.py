"""Programa principal de la billetera virtual Kiwillet."""
from __future__ import annotations

from typing import Dict, List, Optional

from io_archivos import asegurar_estructura_directorios
from logger import registrar_evento
from movimientos import cargar_movimientos, generar_reporte, registrar_movimiento
from servicios import cargar_servicios, obtener_servicio
from tarjetas import agregar_tarjeta, cargar_tarjetas, eliminar_tarjeta, obtener_tarjeta
from usuarios import (
    Usuario,
    autenticar_usuario,
    cargar_usuarios,
    cambiar_contrasena,
    crear_usuario,
    actualizar_saldo,
)

usuarios_globales: Dict[str, Usuario] = {}

MENU_PRINCIPAL = """
====== KIWILLET ======
1. Gestionar tarjetas
2. Pagar servicios
3. Modificar cuenta
4. Ingresar dinero
5. Ver reportes
6. Salir
Seleccione una opción: """

MENU_TARJETAS = """
-- Tarjetas --
1. Listar tarjetas
2. Agregar tarjeta
3. Eliminar tarjeta
4. Volver
Seleccione una opción: """

MENU_REPORTES = """
-- Reportes --
1. Mostrar estadísticas en pantalla
2. Exportar reporte CSV
3. Volver
Seleccione una opción: """


def pausar() -> None:
    input("Presione ENTER para continuar...")


def solicitar_opcion(mensaje: str) -> str:
    return input(mensaje).strip()


def mostrar_tarjetas(tarjetas: List[Dict[str, str]]) -> None:
    if not tarjetas:
        print("No hay tarjetas registradas.")
        return
    print("Tarjetas registradas:")
    for tarjeta in tarjetas:
        numero = tarjeta.get("numero", "")
        numero_visible = "****" + numero[-4:] if len(numero) >= 4 else numero
        print(
            f"ID: {tarjeta.get('id','')} | Tipo: {tarjeta.get('tipo','')} | "
            f"Entidad: {tarjeta.get('entidad','')} | Número: {numero_visible} | "
            f"Vencimiento: {tarjeta.get('vencimiento','')}"
        )


def flujo_tarjetas(usuario: Usuario, tarjetas_usuario: List[Dict[str, str]]) -> None:
    while True:
        opcion = solicitar_opcion(MENU_TARJETAS)
        if opcion == "1":
            mostrar_tarjetas(tarjetas_usuario)
            pausar()
        elif opcion == "2":
            tarjeta_id = input("Ingrese ID de la tarjeta: ").strip()
            tipo = input("Tipo (crédito/débito): ").strip()
            entidad = input("Entidad emisora: ").strip()
            numero = input("Número (solo últimos dígitos visibles): ").strip()
            vencimiento = input("Vencimiento (MM/AA): ").strip()
            if agregar_tarjeta(usuario.nombre, tarjetas_usuario, {
                "id": tarjeta_id,
                "tipo": tipo,
                "entidad": entidad,
                "numero": numero,
                "vencimiento": vencimiento,
            }):
                print("Tarjeta agregada correctamente.")
            else:
                print("Ya existe una tarjeta con ese ID.")
            pausar()
        elif opcion == "3":
            tarjeta_id = input("Ingrese el ID de la tarjeta a eliminar: ").strip()
            if eliminar_tarjeta(usuario.nombre, tarjetas_usuario, tarjeta_id):
                print("Tarjeta eliminada.")
            else:
                print("No se encontró la tarjeta indicada.")
            pausar()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")


def seleccionar_tarjeta(usuario: Usuario, tarjetas_usuario: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    if not tarjetas_usuario:
        print("Debe registrar al menos una tarjeta antes de operar.")
        return None
    mostrar_tarjetas(tarjetas_usuario)
    tarjeta_id = input("Seleccione el ID de la tarjeta a utilizar: ").strip()
    tarjeta = obtener_tarjeta(tarjetas_usuario, tarjeta_id)
    if tarjeta is None:
        print("Tarjeta no encontrada.")
        return None
    return tarjeta


def flujo_pago_servicios(usuario: Usuario, tarjetas_usuario: List[Dict[str, str]], movimientos_usuario: List[Dict[str, str]], servicios: List[Dict[str, str]]) -> None:
    if not servicios:
        print("No hay servicios cargados.")
        return
    tarjeta = seleccionar_tarjeta(usuario, tarjetas_usuario)
    if tarjeta is None:
        pausar()
        return
    print("Servicios disponibles:")
    for servicio in servicios:
        print(
            f"ID: {servicio.get('id','')} | {servicio.get('nombre','')} - {servicio.get('categoria','')} | "
            f"Monto sugerido: ${servicio.get('monto','0')}"
        )
    servicio_id = input("Ingrese ID del servicio a pagar: ").strip()
    servicio = obtener_servicio(servicios, servicio_id)
    if servicio is None:
        print("Servicio no encontrado.")
        pausar()
        return
    monto = input("Ingrese monto a pagar (ENTER para monto sugerido): ").strip()
    monto_float = float(servicio.get("monto", "0")) if not monto else float(monto)
    if monto_float > usuario.saldo:
        print("Saldo insuficiente, realice una recarga.")
        pausar()
        return
    usuario.saldo -= monto_float
    registrar_movimiento(
        usuario.nombre,
        movimientos_usuario,
        "Pago servicio",
        servicio.get("nombre", "Servicio"),
        monto_float,
        usuario.saldo,
    )
    actualizar_saldo(usuarios_globales, usuario.nombre, usuario.saldo)
    registrar_evento("pago_servicio", f"{usuario.nombre}:{servicio.get('nombre','')}:{monto_float:.2f}")
    print(f"Pago registrado. Saldo restante: ${usuario.saldo:.2f}")
    pausar()


def flujo_cambio_password(usuario: Usuario) -> None:
    nueva = input("Ingrese la nueva contraseña: ").strip()
    if not nueva:
        print("La contraseña no puede ser vacía.")
        return
    if cambiar_contrasena(usuarios_globales, usuario.nombre, nueva):
        print("Contraseña actualizada.")
    else:
        print("No se pudo actualizar la contraseña.")


def flujo_ingreso_dinero(usuario: Usuario, movimientos_usuario: List[Dict[str, str]]) -> None:
    monto = input("Ingrese el monto a acreditar: ").strip()
    try:
        monto_float = float(monto)
    except ValueError:
        print("Monto inválido.")
        return
    if monto_float <= 0:
        print("El monto debe ser positivo.")
        return
    usuario.saldo += monto_float
    registrar_movimiento(
        usuario.nombre,
        movimientos_usuario,
        "Ingreso",
        "Carga de saldo",
        monto_float,
        usuario.saldo,
    )
    actualizar_saldo(usuarios_globales, usuario.nombre, usuario.saldo)
    registrar_evento("ingreso_saldo", f"{usuario.nombre}:{monto_float:.2f}")
    print(f"Saldo actualizado: ${usuario.saldo:.2f}")


def flujo_reportes(usuario: Usuario, movimientos_usuario: List[Dict[str, str]]) -> None:
    from movimientos import calcular_estadisticas

    while True:
        opcion = solicitar_opcion(MENU_REPORTES)
        if opcion == "1":
            estadisticas = calcular_estadisticas(movimientos_usuario)
            print("Estadísticas actuales:")
            for clave, valor in estadisticas.items():
                if isinstance(valor, float):
                    print(f"- {clave.replace('_', ' ').title()}: {valor:.2f}")
                else:
                    print(f"- {clave.replace('_', ' ').title()}: {valor}")
            pausar()
        elif opcion == "2":
            ruta = generar_reporte(usuario.nombre, movimientos_usuario)
            print(f"Reporte exportado en: {ruta}")
            pausar()
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")


def menu_principal(usuario: Usuario, servicios: List[Dict[str, str]]) -> None:
    tarjetas_usuario = cargar_tarjetas(usuario.nombre)
    movimientos_usuario = cargar_movimientos(usuario.nombre)
    registrar_evento("inicio_sesion", usuario.nombre)
    while True:
        opcion = solicitar_opcion(MENU_PRINCIPAL)
        if opcion == "1":
            flujo_tarjetas(usuario, tarjetas_usuario)
        elif opcion == "2":
            flujo_pago_servicios(usuario, tarjetas_usuario, movimientos_usuario, servicios)
        elif opcion == "3":
            flujo_cambio_password(usuario)
        elif opcion == "4":
            flujo_ingreso_dinero(usuario, movimientos_usuario)
        elif opcion == "5":
            flujo_reportes(usuario, movimientos_usuario)
        elif opcion == "6":
            registrar_evento("cierre_sesion", usuario.nombre)
            print("Hasta luego!")
            break
        else:
            print("Opción inválida.")


def flujo_inicio() -> None:
    while True:
        print("\n=== Bienvenido a Kiwillet ===")
        print("1. Crear usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            nombre = input("Ingrese nombre de usuario: ").strip()
            password = input("Ingrese contraseña: ").strip()
            if not nombre or not password:
                print("Los campos no pueden quedar vacíos.")
                continue
            if crear_usuario(usuarios_globales, nombre, password):
                print("Usuario creado. Ya puede iniciar sesión.")
            else:
                print("El usuario ya existe.")
        elif opcion == "2":
            nombre = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            usuario = autenticar_usuario(usuarios_globales, nombre, password)
            if usuario:
                servicios = cargar_servicios()
                menu_principal(usuario, servicios)
            else:
                print("Credenciales inválidas.")
        elif opcion == "3":
            print("Gracias por utilizar Kiwillet.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    asegurar_estructura_directorios()
    usuarios_globales = cargar_usuarios()
    try:
        flujo_inicio()
    except KeyboardInterrupt:
        print("\nSesión finalizada por el usuario.")
