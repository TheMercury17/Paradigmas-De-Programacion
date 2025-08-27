# Comprobador de elegibilidad de impuestos - Python

TAX_AGE = 18
TAX_MONTHLY_THRESHOLD = 2000.0

def necesita_pagar_impuestos(edad, ingreso_mensual,
                             edad_minima=TAX_AGE,
                             umbral_ingreso=TAX_MONTHLY_THRESHOLD):
    """
    Devuelve True si la persona debe pagar impuestos según:
      - edad >= edad_minima
      - ingreso_mensual >= umbral_ingreso
    """
    if edad < 0 or ingreso_mensual < 0:
        raise ValueError("Edad e ingreso deben ser no negativos.")
    return edad >= edad_minima and ingreso_mensual >= umbral_ingreso

def main():
    try:
        edad = int(input("Ingresa tu edad: ").strip())
        ingreso = float(input("Ingresa tu ingreso mensual: ").strip())
    except ValueError:
        print("Entrada inválida: por favor ingresa un número válido para edad e ingreso.")
        return

    try:
        obligado = necesita_pagar_impuestos(edad, ingreso)
    except ValueError as e:
        print("Error:", e)
        return

    if obligado:
        print("Según los criterios, debes pagar impuestos.")
    else:
        print("Según los criterios, NO debes pagar impuestos.")

if __name__ == "__main__":
    main()