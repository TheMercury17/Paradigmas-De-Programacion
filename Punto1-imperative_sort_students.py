# Quicksort in-place (imperativo)
# Ordena la lista de (Nombre, Nota) por:
#  1) Nota descendente
#  2) Nombre ascendente si las notas empatan
# Usa exactamente la MISMA lista de 12 estudiantes que el archivo .hs

from typing import List, Tuple

Student = Tuple[str, int]

# -----------------------
# Datos por defecto (misma lista que en Haskell)
# -----------------------
example_students: List[Student] = [
    ("María",     92),
    ("Valentina", 92),
    ("Juan",      85),
    ("Carlos",    85),
    ("Sofía",     78),
    ("Diego",     74),
    ("Andrés",    68),
    ("Daniela",   68),
    ("Mateo",     55),
    ("Lucía",     55),
    ("Catalina",  40),
    ("Luis",      30),
]

# Función clave compuesta: (-score, name)
# - Negamos la nota para obtener orden descendente con una comparación normal.
# - El nombre queda tal cual para ordenar ascendentemente en caso de empate.

def key_fn(student: Student):
    return (-student[1], student[0])

# Implementación imperativa: quicksort in-place.
# Comentarios importantes:
# - Modifica la lista 'arr' directamente osea que la está mutando.
# - Devuelve la misma referencia por conveniencia.

def imperative_quicksort(arr: List[Student]) -> List[Student]:
    def partition(a, low, high):
        # Elegimos pivote en la posición media
        pivot = key_fn(a[(low + high) // 2])
        i, j = low, high
        # Avanzamos i hasta encontrar elemento >= pivot
        # Retrocedemos j hasta encontrar elemento <= pivot
        while i <= j:
            while key_fn(a[i]) < pivot:
                i += 1
            while key_fn(a[j]) > pivot:
                j -= 1
            if i <= j:
                # swap
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        return i, j

    def _qsort(a, low, high):
        if low >= high:
            return
        i, j = partition(a, low, high)
        if low < j:
            _qsort(a, low, j)
        if i < high:
            _qsort(a, i, high)

    if len(arr) <= 1:
        return arr
    _qsort(arr, 0, len(arr) - 1)
    return arr

# Pequeña utilidad declarativa para comparar
def declarative_sort(students: List[Student]) -> List[Student]:
    # Versión declrativa en Python que no muta: devuelve nueva lista ordenada
    return sorted(students, key=lambda s: (-s[1], s[0]))

# -----------------------
# Ejecución de ejemplo 
# -----------------------
if __name__ == "__main__":
    print("Lista original de estudiantes (ejemplo):")
    for s in example_students:
        print(s)

    # 1) Usar la versión imperativa (quicksort in-place)
    arr_imp = list(example_students)  # copia para no mutar el original
    imperative_quicksort(arr_imp)
    print("\nResultado (imperativo, quicksort in-place):")
    for s in arr_imp:
        print(s)

    # 2) Usar la versión declarativa (sorted) para verificar igualdad de resultados
    arr_dec = declarative_sort(example_students)
    print("\nResultado (declarativo, sorted):")
    for s in arr_dec:
        print(s)

    # Comprobación rápida: ambos resultados deberían ser idénticos
    assert arr_imp == arr_dec, "ERROR: los resultados imperativo y declarativo no coinciden"
    print("\nVerificación: los dos métodos producen el mismo orden")
