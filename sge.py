"""
Sistema de Gestión de Estudiantes (SGE) básico
Aplicación por consola en Python 3.10+ (usa match/case, equivalente a switch).

Funcionalidades: agregar estudiantes, mostrarlos (ascendente/descendente),
buscarlos por ID y salir del sistema.
"""

CAPACIDAD_MAXIMA = 50          # Límite para no crecer sin control (requisito de la guía)
NOTA_MINIMA = 0.0              # Escala colombiana de 0.0 a 5.0
NOTA_MAXIMA = 5.0


# ---------------------------------------------------------------------------
# Unidades de código reutilizables (entrada validada)
# ---------------------------------------------------------------------------
def leer_entero(mensaje, minimo, maximo):
    """Repite la lectura hasta recibir un entero dentro de [minimo, maximo].
    Se usa while con try/except porque no sabemos cuántos intentos fallidos habrá."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:                      # El usuario escribió texto, no un número
            print("  [!] Entrada inválida: escribe solo números enteros.")
            continue
        if valor < minimo or valor > maximo:    # Decisión simple: rango permitido
            print(f"  [!] El valor debe estar entre {minimo} y {maximo}.")
        else:
            return valor


def leer_decimal(mensaje, minimo, maximo):
    """Igual que leer_entero, pero para números con decimales (acepta coma o punto)."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("  [!] Entrada inválida: escribe un número (ej. 4.2).")
            continue
        if valor < minimo or valor > maximo:
            print(f"  [!] La nota debe estar entre {minimo} y {maximo}.")
        else:
            return valor


def leer_texto(mensaje):
    """Evita cadenas vacías: un estudiante sin nombre no tiene sentido."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("  [!] Este campo no puede quedar vacío.")


# ---------------------------------------------------------------------------
# Operaciones del sistema
# ---------------------------------------------------------------------------
def mostrar_menu():
    print("\n===== SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE) =====")
    print("1. Agregar estudiante")
    print("2. Mostrar estudiantes")
    print("3. Buscar estudiante por ID")
    print("4. Salir")


def buscar_posicion_por_id(estudiantes, id_buscado):
    """Búsqueda lineal. Devuelve la posición en la lista o -1 si no existe.
    Complejidad O(n): en el peor caso recorre todos los registros."""
    for posicion in range(len(estudiantes)):
        if estudiantes[posicion]["id"] == id_buscado:
            return posicion
    return -1


def mostrar_estudiante(estudiante):
    """Imprime un solo registro (reutilizada por 'Mostrar' y por 'Buscar')."""
    print(f"  ID: {estudiante['id']:<8} Nombre: {estudiante['nombre']:<22} "
          f"Programa: {estudiante['programa']:<20} Nota: {estudiante['nota']:.1f}")


def agregar_estudiante(estudiantes, total_estudiantes):
    """Agrega un estudiante y devuelve el nuevo conteo total."""
    if total_estudiantes < CAPACIDAD_MAXIMA:                    # Decisión: ¿hay espacio?
        id_nuevo = leer_entero("  ID (número entero positivo): ", 1, 999999999)
        if buscar_posicion_por_id(estudiantes, id_nuevo) == -1:  # Decisión ANIDADA: ¿ID libre?
            nombre = leer_texto("  Nombre completo: ")
            programa = leer_texto("  Programa académico: ")
            nota = leer_decimal("  Nota promedio (0.0 - 5.0): ", NOTA_MINIMA, NOTA_MAXIMA)
            estudiantes.append({"id": id_nuevo, "nombre": nombre,
                                "programa": programa, "nota": nota})
            total_estudiantes += 1                              # Variable de CONTEO
            print(f"  [OK] Estudiante agregado. Total registrados: {total_estudiantes}")
        else:
            print("  [!] Ya existe un estudiante con ese ID. Operación cancelada.")
    else:
        print("  [!] Capacidad máxima alcanzada. No se pueden agregar más estudiantes.")
    return total_estudiantes


def mostrar_estudiantes(estudiantes, total_estudiantes):
    """Muestra la lista en orden ascendente o descendente y el promedio general."""
    if total_estudiantes == 0:
        print("  [i] No hay estudiantes registrados todavía.")
        return

    print("  1. Orden de registro (ascendente)")
    print("  2. Orden inverso (descendente)")
    orden = leer_entero("  Elige el orden: ", 1, 2)

    print(f"\n  --- Lista de estudiantes ({total_estudiantes}) ---")
    if orden == 1:
        for posicion in range(0, total_estudiantes):           # Iteración ASCENDENTE
            mostrar_estudiante(estudiantes[posicion])
    else:
        for posicion in range(total_estudiantes - 1, -1, -1):  # Iteración DESCENDENTE
            mostrar_estudiante(estudiantes[posicion])

    suma_notas = 0.0                                          # Variable de SUMATORIA
    for estudiante in estudiantes:
        suma_notas += estudiante["nota"]
    print(f"  Promedio general del grupo: {suma_notas / total_estudiantes:.2f}")


def buscar_estudiante(estudiantes):
    """Busca por ID e informa si fue encontrado o no."""
    if len(estudiantes) == 0:
        print("  [i] No hay estudiantes registrados todavía.")
        return
    id_buscado = leer_entero("  ID a buscar: ", 1, 999999999)
    posicion = buscar_posicion_por_id(estudiantes, id_buscado)
    if posicion != -1:                                         # Decisión simple: ¿encontrado?
        print("  [OK] Estudiante encontrado:")
        mostrar_estudiante(estudiantes[posicion])
    else:
        print(f"  [X] No existe ningún estudiante con el ID {id_buscado}.")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    estudiantes = []            # Lista que almacena los registros (estructura de datos)
    total_estudiantes = 0       # Variable de CONTEO
    bandera_salir = False       # BANDERA que controla el bucle principal

    while not bandera_salir:    # Repetición condicionada al comienzo
        mostrar_menu()
        opcion = leer_entero("Selecciona una opción (1-4): ", 1, 4)

        match opcion:           # Decisión múltiple (equivalente a switch)
            case 1:
                total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
            case 2:
                mostrar_estudiantes(estudiantes, total_estudiantes)
            case 3:
                buscar_estudiante(estudiantes)
            case 4:
                bandera_salir = True
                print("\nSaliendo del sistema. ¡Hasta pronto!")


if __name__ == "__main__":
    main()
