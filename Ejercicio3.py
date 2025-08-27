# Calculadora de división - Python

def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None  # señalamos que hubo división por cero

def main():
    try:
        x = float(input("Ingresa el primer número (numerador): ").strip())
        y = float(input("Ingresa el segundo número (divisor): ").strip())
    except ValueError:
        print("Entrada inválida: por favor ingresa números válidos.")
        return

    resultado = dividir(x, y)
    if resultado is None:
        print("Error: división por cero.")
    else:
        print(f"Resultado: {resultado}")

if __name__ == "__main__":
    main()
