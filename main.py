import os
from lista_tareas import ListaDeTareas
from tarea import Tarea


# ── Utilidades de consola ─────────────────────────────────────────────────────

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def linea(char="─", largo=50):
    print(char * largo)


def titulo(texto):
    limpiar()
    linea("═")
    print(f"  📋  {texto}")
    linea("═")
    print()


def pausar():
    input("\n  Presiona Enter para continuar...")


def pedir_prioridad() -> str:
    print("  Prioridad: (1) Alta  (2) Media  (3) Baja")
    opciones = {"1": "alta", "2": "media", "3": "baja"}
    while True:
        eleccion = input("  Opción [1-3]: ").strip()
        if eleccion in opciones:
            return opciones[eleccion]
        print("  ⚠️  Opción inválida.")


# ── Acciones del menú ─────────────────────────────────────────────────────────

def mostrar_tareas(lista: ListaDeTareas):
    titulo("Lista de Tareas")

    print("  Mostrar: (1) Todas  (2) Pendientes  (3) Completadas")
    filtros = {"1": "todas", "2": "pendientes", "3": "completadas"}
    eleccion = input("  Opción [1-3, Enter=todas]: ").strip() or "1"
    filtro = filtros.get(eleccion, "todas")

    tareas = lista.listar(filtro)
    print()
    linea()

    if not tareas:
        print("  No hay tareas para mostrar.")
    else:
        for t in tareas:
            print(f"  {t}")

    linea()
    pausar()


def agregar_tarea(lista: ListaDeTareas):
    titulo("Agregar Nueva Tarea")

    titulo_tarea = input("  Título: ").strip()
    if not titulo_tarea:
        print("  ⚠️  El título no puede estar vacío.")
        pausar()
        return

    descripcion = input("  Descripción (opcional): ").strip()
    prioridad = pedir_prioridad()

    tarea = lista.agregar(titulo_tarea, descripcion, prioridad)
    print(f"\n  ✅ Tarea #{tarea.id} '{tarea.titulo}' agregada exitosamente.")
    pausar()


def completar_tarea(lista: ListaDeTareas):
    titulo("Completar Tarea")

    pendientes = lista.listar("pendientes")
    if not pendientes:
        print("  No hay tareas pendientes.")
        pausar()
        return

    for t in pendientes:
        print(f"  {t}")

    print()
    try:
        id_tarea = int(input("  ID de la tarea a completar: ").strip())
        if lista.completar(id_tarea):
            print(f"\n  ✅ Tarea #{id_tarea} marcada como completada.")
        else:
            print(f"\n  ⚠️  No se encontró la tarea #{id_tarea}.")
    except ValueError:
        print("  ⚠️  Ingresa un número válido.")

    pausar()


def eliminar_tarea(lista: ListaDeTareas):
    titulo("Eliminar Tarea")

    tareas = lista.listar()
    if not tareas:
        print("  No hay tareas.")
        pausar()
        return

    for t in tareas:
        print(f"  {t}")

    print()
    try:
        id_tarea = int(input("  ID de la tarea a eliminar: ").strip())
        tarea = lista.detalle(id_tarea)
        if not tarea:
            print(f"\n  ⚠️  No se encontró la tarea #{id_tarea}.")
            pausar()
            return

        confirmar = input(f"  ¿Eliminar '{tarea.titulo}'? (s/n): ").strip().lower()
        if confirmar == "s":
            lista.eliminar(id_tarea)
            print(f"\n  🗑️  Tarea #{id_tarea} eliminada.")
        else:
            print("  Cancelado.")
    except ValueError:
        print("  ⚠️  Ingresa un número válido.")

    pausar()


def editar_tarea(lista: ListaDeTareas):
    titulo("Editar Tarea")

    tareas = lista.listar()
    if not tareas:
        print("  No hay tareas.")
        pausar()
        return

    for t in tareas:
        print(f"  {t}")

    print()
    try:
        id_tarea = int(input("  ID de la tarea a editar: ").strip())
        tarea = lista.detalle(id_tarea)
        if not tarea:
            print(f"\n  ⚠️  No se encontró la tarea #{id_tarea}.")
            pausar()
            return

        print(f"\n  Editando: '{tarea.titulo}' (Enter para mantener el valor actual)")
        nuevo_titulo = input(f"  Título [{tarea.titulo}]: ").strip() or tarea.titulo
        nueva_desc = input(f"  Descripción [{tarea.descripcion}]: ").strip()
        if nueva_desc == "":
            nueva_desc = tarea.descripcion

        print(f"  Prioridad actual: {tarea.prioridad}")
        cambiar = input("  ¿Cambiar prioridad? (s/n): ").strip().lower()
        nueva_prioridad = pedir_prioridad() if cambiar == "s" else tarea.prioridad

        lista.editar(id_tarea, nuevo_titulo, nueva_desc, nueva_prioridad)
        print(f"\n  ✅ Tarea #{id_tarea} actualizada.")
    except ValueError:
        print("  ⚠️  Ingresa un número válido.")

    pausar()


def ver_estadisticas(lista: ListaDeTareas):
    titulo("Estadísticas")

    stats = lista.estadisticas()
    total = stats["total"]
    completadas = stats["completadas"]
    pendientes = stats["pendientes"]
    porcentaje = (completadas / total * 100) if total > 0 else 0

    barra = int(porcentaje / 5)
    progreso = "█" * barra + "░" * (20 - barra)

    linea()
    print(f"  Total de tareas   : {total}")
    print(f"  ✔  Completadas    : {completadas}")
    print(f"  ○  Pendientes     : {pendientes}")
    print(f"\n  Progreso: [{progreso}] {porcentaje:.0f}%")
    linea()
    print("\n  Pendientes por prioridad:")
    print(f"  🔴 Alta   : {stats['por_prioridad']['alta']}")
    print(f"  🟡 Media  : {stats['por_prioridad']['media']}")
    print(f"  🟢 Baja   : {stats['por_prioridad']['baja']}")
    linea()

    pausar()


# ── Menú principal ────────────────────────────────────────────────────────────

def menu():
    lista = ListaDeTareas()

    while True:
        titulo("Gestor de Tareas")
        stats = lista.estadisticas()
        print(f"  Tareas: {stats['total']} total  |  {stats['pendientes']} pendientes  |  {stats['completadas']} completadas\n")
        linea()
        print("  1.  Ver tareas")
        print("  2.  Agregar tarea")
        print("  3.  Completar tarea")
        print("  4.  Editar tarea")
        print("  5.  Eliminar tarea")
        print("  6.  Ver estadísticas")
        print("  0.  Salir")
        linea()

        opcion = input("  Elige una opción: ").strip()

        acciones = {
            "1": mostrar_tareas,
            "2": agregar_tarea,
            "3": completar_tarea,
            "4": editar_tarea,
            "5": eliminar_tarea,
            "6": ver_estadisticas,
        }

        if opcion == "0":
            limpiar()
            print("\n  👋 ¡Hasta luego!\n")
            break
        elif opcion in acciones:
            acciones[opcion](lista)
        else:
            print("  ⚠️  Opción inválida.")
            pausar()


if __name__ == "__main__":
    menu()