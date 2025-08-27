# Verificador par o impar - Python

def es_par(n):
    return n % 2 == 0

def main():
    entrada = input("Ingresa un número entero: ").strip()
    try:
        n = int(entrada)
    except ValueError:
        print("Entrada inválida: por favor ingresa un número entero.")
        return

    if es_par(n):
        print(f"{n} es par.")
    else:
        print(f"{n} es impar.")

if __name__ == "__main__":
    main()
