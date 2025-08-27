# Precios de Arcade - Python

def precio_boleto(edad):
    """Devuelve el precio del boleto según la edad.
    Lanza ValueError si la edad no es un entero no negativo."""
    if not isinstance(edad, int):
        raise ValueError("La edad debe ser un entero.")
    if edad < 0:
        raise ValueError("La edad no puede ser negativa.")
    if edad <= 3:
        return 0.0
    if edad <= 12:
        return 5.0
    if edad <= 17:
        return 7.0
    if edad <= 64:
        return 12.0
    return 8.0  # 65+

def main():
    try:
        entrada = input("Ingresa la edad del cliente: ").strip()
        edad = int(entrada)
    except ValueError:
        print("Entrada inválida: por favor ingresa un número entero no negativo.")
        return

    try:
        precio = precio_boleto(edad)
    except ValueError as e:
        print("Error:", e)
        return

    if precio == 0.0:
        print("Precio: Entrada gratuita.")
    else:
        print(f"Precio del boleto: ${precio:.2f}")

if __name__ == "__main__":
    main()
