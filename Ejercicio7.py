# Evaluación de los empleados - Python

def evaluar_puntuacion(puntuacion):
    """
    Recibe una puntuación (0-100) y devuelve una tupla (nivel, recompensa).
    Niveles / Recompensas por defecto:
      90-100 : "Excelente" -> 1000.0
      75-89  : "Muy bueno"  ->  500.0
      60-74  : "Aceptable"  ->  200.0
      0-59   : "Necesita mejorar" -> 0.0
    Lanza ValueError si la puntuación está fuera de 0..100.
    """
    if puntuacion < 0 or puntuacion > 100:
        raise ValueError("La puntuación debe estar entre 0 y 100.")
    if puntuacion >= 90:
        return ("Excelente", 1000.0)
    elif puntuacion >= 75:
        return ("Muy bueno", 500.0)
    elif puntuacion >= 60:
        return ("Aceptable", 200.0)
    else:
        return ("Necesita mejorar", 0.0)

def main():
    try:
        entrada = input("Ingresa la puntuación del empleado (0-100): ").strip()
        score = float(entrada)
    except ValueError:
        print("Entrada inválida: por favor ingresa un número entre 0 y 100.")
        return

    try:
        nivel, recompensa = evaluar_puntuacion(score)
    except ValueError as e:
        print("Error:", e)
        return

    print(f"Nivel de rendimiento: {nivel}")
    print(f"Recompensa monetaria: ${recompensa:.2f}")

if __name__ == "__main__":
    main()
