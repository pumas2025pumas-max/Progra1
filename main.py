"""Programa sencillo de billetera virtual."""

import datetime

import helpers


def pausar():
    input("Presione ENTER para continuar...")


def mostrar_menu():
    print("\n===== KIWILLET =====")
    print("1. Ver saldo")
    print("2. Ingresar dinero")
    print("3. Gestionar tarjetas")
    print("4. Pagar servicio")
    print("5. Ver movimientos")
    print("6. Cambiar contraseña")
    print("7. Salir")
    return input("Opción: ").strip()


def mostrar_menu_tarjetas():
    print("\n--- Tarjetas ---")
    print("1. Listar tarjetas")
    print("2. Agregar tarjeta")
    print("3. Eliminar tarjeta")
    print("4. Volver")
    return input("Opción: ").strip()


def iniciar_sesion(usuarios):
    while True:
        print("\n1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Salir")
        opcion = input("Seleccione: ").strip()
        if opcion == "1":
            nombre = input("Usuario: ").strip()
            clave = input("Contraseña: ").strip()
            datos = usuarios.get(nombre)
            if datos and datos.get("clave") == clave:
                print("Bienvenido", nombre)
                return nombre
            print("Datos incorrectos.")
        elif opcion == "2":
            nombre = input("Nuevo usuario: ").strip()
            if not nombre:
                print("Ingrese un nombre válido.")
                continue
            if nombre in usuarios:
                print("El usuario ya existe.")
                continue
            clave = input("Contraseña: ").strip()
            usuarios[nombre] = {"clave": clave, "saldo": 0.0}
            helpers.guardar_usuarios(usuarios)
            print("Usuario creado. Ingrese nuevamente para continuar.")
        elif opcion == "3":
            return None
        else:
            print("Opción inválida.")


def mostrar_tarjetas(tarjetas_usuario):
    if not tarjetas_usuario:
        print("No hay tarjetas cargadas.")
        return
    for tarjeta in tarjetas_usuario:
        alias = tarjeta.get("alias", "")
        numero = helpers.mascara_tarjeta(tarjeta.get("numero", ""))
        tipo = tarjeta.get("tipo", "")
        vencimiento = tarjeta.get("vencimiento", "")
        print(f"Alias: {alias} | Número: {numero} | Tipo: {tipo} | Vence: {vencimiento}")


def flujo_tarjetas(tarjetas, usuario):
    while True:
        opcion = mostrar_menu_tarjetas()
        tarjetas_usuario = helpers.obtener_tarjetas_usuario(tarjetas, usuario)
        if opcion == "1":
            mostrar_tarjetas(tarjetas_usuario)
            pausar()
        elif opcion == "2":
            alias = input("Alias de la tarjeta: ").strip()
            numero = input("Número: ").strip()
            tipo = input("Tipo: ").strip()
            vencimiento = input("Vencimiento (MM/AA): ").strip()
            if helpers.agregar_tarjeta(tarjetas, usuario, alias, numero, tipo, vencimiento):
                print("Tarjeta agregada.")
            else:
                print("Ya existe una tarjeta con ese alias.")
            pausar()
        elif opcion == "3":
            alias = input("Alias a eliminar: ").strip()
            if helpers.eliminar_tarjeta(tarjetas, usuario, alias):
                print("Tarjeta eliminada.")
            else:
                print("No se encontró la tarjeta.")
            pausar()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")


def ingresar_dinero(usuarios, movimientos, usuario):
    monto = input("Monto a ingresar: ").strip()
    try:
        valor = float(monto)
    except ValueError:
        print("Monto inválido.")
        return
    if valor <= 0:
        print("El monto debe ser positivo.")
        return
    usuarios[usuario]["saldo"] += valor
    helpers.guardar_usuarios(usuarios)
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    saldo_actual = helpers.formatear_monto(usuarios[usuario]["saldo"])
    helpers.registrar_movimiento(
        movimientos,
        usuario,
        fecha,
        "Ingreso de dinero",
        helpers.formatear_monto(valor),
        saldo_actual,
    )
    print("Saldo actualizado:", saldo_actual)


def pagar_servicio(usuarios, tarjetas, servicios, movimientos, usuario):
    tarjetas_usuario = helpers.obtener_tarjetas_usuario(tarjetas, usuario)
    if not tarjetas_usuario:
        print("Debe registrar al menos una tarjeta.")
        return
    print("Tarjetas disponibles:")
    for tarjeta in tarjetas_usuario:
        print("-", tarjeta.get("alias", ""))
    alias = input("Seleccione tarjeta por alias: ").strip()
    tarjeta_elegida = None
    for tarjeta in tarjetas_usuario:
        if tarjeta.get("alias") == alias:
            tarjeta_elegida = tarjeta
            break
    if tarjeta_elegida is None:
        print("Tarjeta no encontrada.")
        return
    print("Servicios disponibles:")
    for servicio in servicios:
        codigo = servicio.get("codigo", "")
        nombre = servicio.get("nombre", "")
        monto = helpers.formatear_monto(servicio.get("monto", "0"))
        print(f"{codigo} - {nombre} ({monto})")
    codigo = input("Código del servicio: ").strip()
    servicio = helpers.buscar_servicio(servicios, codigo)
    if servicio is None:
        print("Servicio inexistente.")
        return
    monto_str = input("Monto a pagar (ENTER para sugerido): ").strip()
    if monto_str:
        try:
            monto = float(monto_str)
        except ValueError:
            print("Monto inválido.")
            return
    else:
        try:
            monto = float(servicio.get("monto", "0"))
        except ValueError:
            monto = 0.0
    saldo_actual = usuarios[usuario]["saldo"]
    if monto > saldo_actual:
        print("Saldo insuficiente.")
        return
    usuarios[usuario]["saldo"] = saldo_actual - monto
    helpers.guardar_usuarios(usuarios)
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    helpers.registrar_movimiento(
        movimientos,
        usuario,
        fecha,
        f"Pago {servicio.get('nombre', '')}",
        helpers.formatear_monto(monto),
        helpers.formatear_monto(usuarios[usuario]["saldo"]),
    )
    print("Pago realizado con la tarjeta", alias)
    print("Saldo actual:", helpers.formatear_monto(usuarios[usuario]["saldo"]))


def mostrar_movimientos(movimientos, usuario):
    lista = movimientos.get(usuario, [])
    if not lista:
        print("No hay movimientos registrados.")
        return
    for movimiento in lista:
        fecha = movimiento.get("fecha", "")
        concepto = movimiento.get("concepto", "")
        monto = movimiento.get("monto", "")
        saldo = movimiento.get("saldo", "")
        print(f"[{fecha}] {concepto} - {monto} (Saldo: {saldo})")


def cambiar_clave(usuarios, usuario):
    actual = input("Contraseña actual: ").strip()
    if usuarios[usuario]["clave"] != actual:
        print("Contraseña incorrecta.")
        return
    nueva = input("Nueva contraseña: ").strip()
    if not nueva:
        print("Debe ingresar una contraseña válida.")
        return
    usuarios[usuario]["clave"] = nueva
    helpers.guardar_usuarios(usuarios)
    print("Contraseña actualizada.")


def principal():
    helpers.inicializar_archivos()
    usuarios = helpers.leer_usuarios()
    tarjetas = helpers.leer_tarjetas()
    movimientos = helpers.leer_movimientos()
    servicios = helpers.leer_servicios()
    usuario = iniciar_sesion(usuarios)
    if usuario is None:
        print("Hasta luego.")
        return
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            saldo = helpers.formatear_monto(usuarios[usuario]["saldo"])
            print("Saldo disponible:", saldo)
            pausar()
        elif opcion == "2":
            ingresar_dinero(usuarios, movimientos, usuario)
            pausar()
        elif opcion == "3":
            flujo_tarjetas(tarjetas, usuario)
        elif opcion == "4":
            pagar_servicio(usuarios, tarjetas, servicios, movimientos, usuario)
            pausar()
        elif opcion == "5":
            mostrar_movimientos(movimientos, usuario)
            pausar()
        elif opcion == "6":
            cambiar_clave(usuarios, usuario)
            pausar()
        elif opcion == "7":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")
            pausar()


if __name__ == "__main__":
    principal()
