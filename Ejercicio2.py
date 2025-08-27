# Verificación de contraseña - Python

STORED_PASSWORD = "Secreto123"  # contraseña almacenada

def verificar_contrasena(entrada, almacenada=STORED_PASSWORD):
    # Comparamos ignorando mayúsculas/minúsculas y espacios extra
    return entrada.strip().lower() == almacenada.strip().lower()

def main():
    intento = input("Escribe la contraseña: ")
    if verificar_contrasena(intento):
        print("Contraseñas coinciden.")
    else:
        print("Contraseñas NO coinciden.")

if __name__ == "__main__":
    main()
