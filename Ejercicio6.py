# Asignación grupal - Python

def asignar_grupo(nombre, genero):
    if not nombre or not nombre.strip():
        return "Entrada inválida: el nombre no puede estar vacío."
    nombre = nombre.strip()
    primera = nombre[0].upper()
    if not primera.isalpha():
        return "Entrada inválida: el nombre debe comenzar con una letra."

    genero_norm = genero.strip().lower()
    # Masculino
    if genero_norm.startswith("m"):
        if "A" <= primera <= "M":
            return f"{nombre}: Grupo A (Deportes)"
        else:
            return f"{nombre}: Grupo B (Ciencias)"
    # Femenino
    elif genero_norm.startswith("f"):
        if "A" <= primera <= "M":
            return f"{nombre}: Grupo C (Arte)"
        else:
            return f"{nombre}: Grupo D (Matemáticas)"
    else:
        return "Debe ingresar un género válido"

def main():
    nombre = input("Ingresa tu nombre: ")
    genero = input("Ingresa tu género (M/F): ")
    resultado = asignar_grupo(nombre, genero)
    print(resultado)

if __name__ == "__main__":
    main()
