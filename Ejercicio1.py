# Verificador de edad legal - Python
def mayor_de_edad(edad):
    return edad >= 18

def main():
    entrada = input("Ingresa tu edad: ").strip()
    try:
        edad = int(entrada)
        if edad < 0:
            print("Edad inválida: no puede ser negativa.")
            return
    except ValueError:
        print("Entrada inválida: por favor ingresa un número entero.")
        return

    if mayor_de_edad(edad):
        print("Eres mayor de edad.")
    else:
        print("Eres menor de edad.")

if __name__ == "__main__":
    main()
