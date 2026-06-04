# Sistema de Gestión de Estudiantes

def buscar_estudiante(legajo, lista_estudiantes):
    """Busca un estudiante por su legajo y devuelve su índice o -1 si no existe."""
    for i in range(len(lista_estudiantes)):
        if lista_estudiantes[i]["legajo"] == legajo:
            return i
    return -1

def calcular_promedio(lista_notas):
    """Calcula el promedio de una lista de números."""
    if not lista_notas:
        return 0.0
    return sum(lista_notas) / len(lista_notas)

def registrar_nuevo_estudiante(lista_estudiantes):
    print("\n--- Registro de Nuevo Estudiante ---")
    try:
        legajo = int(input("Ingrese el número de legajo (único): "))
        
        # Validar que el legajo para que no se repita
        if buscar_estudiante(legajo, lista_estudiantes) != -1:
            print("Error: El legajo ya se encuentra registrado.")
            return

        nombre = input("Ingrese el nombre completo: ")
        
        nuevo_estudiante = {
            "nombre": nombre,
            "legajo": legajo,
            "calificaciones": [],
            "promedio": 0.0
        }
        
        lista_estudiantes.append(nuevo_estudiante)
        print(f"Estudiante {nombre} registrado con éxito.")
    except ValueError:
        print("Error: El legajo debe ser un número entero.")

def registrar_nota(lista_estudiantes):
    if not lista_estudiantes:
        print("\nNo hay estudiantes registrados.")
        return

    print("\nEstudiantes registrados:")
    for est in lista_estudiantes:
        print(f"Legajo: {est['legajo']} - Nombre: {est['nombre']}")

    try:
        legajo = int(input("\nIngrese el legajo del estudiante: "))
        indice = buscar_estudiante(legajo, lista_estudiantes)
        
        if indice == -1:
            print("Error: Estudiante no encontrado.")
            return

        nota = float(input("Ingrese la calificación (0-10): "))
        if 0 <= nota <= 10:
            lista_estudiantes[indice]["calificaciones"].append(nota)
            # Recalcular promedio automáticamente
            nuevo_prom = calcular_promedio(lista_estudiantes[indice]["calificaciones"])
            lista_estudiantes[indice]["promedio"] = nuevo_prom
            print("Calificación registrada correctamente.")
        else:
            print("Error: La nota debe estar entre 0 y 10.")
    except ValueError:
        print("Error: Entrada inválida.")

def gestionar_cola_consultas(lista_estudiantes, cola_consultas, opcion):
    if opcion == 3: # Agregar a la cola
        try:
            legajo = int(input("\nIngrese el legajo para la consulta: "))
            if buscar_estudiante(legajo, lista_estudiantes) != -1:
                cola_consultas.append(legajo)
                print("Estudiante agregado a la cola de espera.")
            else:
                print("Error: El legajo no existe.")
        except ValueError:
            print("Error: Legajo inválido.")
            
    elif opcion == 4: # Atender consulta (FIFO)
        if not cola_consultas:
            print("\nLa cola de consultas está vacía.")
        else:
            legajo_atendido = cola_consultas.pop(0) # FIFO: saca el primero
            idx = buscar_estudiante(legajo_atendido, lista_estudiantes)
            est = lista_estudiantes[idx]
            print("\n--- Atendiendo Consulta ---")
            print(f"Nombre: {est['nombre']}")
            print(f"Legajo: {est['legajo']}")
            print(f"Promedio actual: {est['promedio']:.2f}")

def mostrar_estudiantes(lista_estudiantes):
    if not lista_estudiantes:
        print("\nNo hay estudiantes para mostrar.")
        return

    # Ordenar por promedio de mayor a menor usando una función lambda
    lista_ordenada = sorted(lista_estudiantes, key=lambda x: x["promedio"], reverse=True)
    
    print("\n--- Lista de Estudiantes (Ordenada por Promedio) ---")
    for e in lista_ordenada:
        cant_notas = len(e["calificaciones"])
        print(f"Nombre: {e['nombre']} | Legajo: {e['legajo']} | Notas: {cant_notas} | Promedio: {e['promedio']:.2f}")

def mostrar_estadisticas(lista_estudiantes, cola_consultas):
    if not lista_estudiantes:
        print("\nNo hay datos suficientes para generar estadísticas.")
        return

    total_estudiantes = len(lista_estudiantes)
    # Promedio de todos los promedios
    suma_promedios = sum(e["promedio"] for e in lista_estudiantes)
    promedio_general = suma_promedios / total_estudiantes
    
    mejor = max(lista_estudiantes, key=lambda x: x["promedio"])
    peor = min(lista_estudiantes, key=lambda x: x["promedio"])
    
    print("\n--- Estadísticas Generales ---")
    print(f"Total registrados: {total_estudiantes}")
    print(f"Promedio general de la materia: {promedio_general:.2f}")
    print(f"Mejor promedio: {mejor['nombre']} ({mejor['promedio']:.2f})")
    print(f"Peor promedio: {peor['nombre']} ({peor['promedio']:.2f})")
    print(f"Estudiantes esperando consulta: {len(cola_consultas)}")

def menu_principal():
    estudiantes = []
    cola_consultas = []
    
    while True:
        print("\n--- MENÚ DE GESTIÓN ACADÉMICA ---")
        print("1. Registrar nuevo estudiante")
        print("2. Registrar calificación")
        print("3. Agregar a cola de consultas")
        print("4. Atender siguiente consulta")
        print("5. Ver todos los estudiantes")
        print("6. Ver estadísticas generales")
        print("7. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_nuevo_estudiante(estudiantes)
        elif opcion == "2":
            registrar_nota(estudiantes)
        elif opcion == "3":
            gestionar_cola_consultas(estudiantes, cola_consultas, 3)
        elif opcion == "4":
            gestionar_cola_consultas(estudiantes, cola_consultas, 4)
        elif opcion == "5":
            mostrar_estudiantes(estudiantes)
        elif opcion == "6":
            mostrar_estadisticas(estudiantes, cola_consultas)
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_principal()