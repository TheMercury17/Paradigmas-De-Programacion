# Pedido de pizza - Python

VEG_MENU = ["Pimiento", "Champiñones", "Aceitunas", "Tomate", "Cebolla"]
NONVEG_MENU = ["Pepperoni", "Jamón", "Salchicha", "Bacon", "Anchoas"]

def mostrar_menu(menu):
    for i, item in enumerate(menu, start=1):
        print(f"{i}. {item}")

def obtener_eleccion_si_no(prompt):
    resp = input(prompt).strip().lower()
    if not resp:
        return None
    primera = resp[0]
    if primera in ("s", "y"):  # español/inglés: sí/yes
        return True
    if primera in ("n"):
        return False
    return None

def elegir_ingrediente(menu):
    mostrar_menu(menu)
    entrada = input("Elige el número del ingrediente adicional (o escribe el nombre): ").strip()
    # Intentamos interpretar como número
    if entrada.isdigit():
        idx = int(entrada) - 1
        if 0 <= idx < len(menu):
            return menu[idx]
        else:
            return None
    # si no es número, intentar matcheo por nombre (insensible a mayúsculas)
    nom = entrada.lower()
    for item in menu:
        if item.lower() == nom:
            return item
    return None

def main():
    print("¿Deseas una pizza vegetariana? (s/n)")
    es_veg = obtener_eleccion_si_no("> ")
    if es_veg is None:
        print("Entrada inválida. Responde 's' o 'n'.")
        return

    menu = VEG_MENU if es_veg else NONVEG_MENU
    tipo = "vegetariana" if es_veg else "no vegetariana"
    print(f"\nMenú para pizza {tipo}:")
    ing = elegir_ingrediente(menu)
    if ing is None:
        print("Selección inválida de ingrediente. Intenta de nuevo y elige un número o nombre válido.")
        return

    base = ["masa", "salsa de tomate", "queso"]
    descripcion = f"Pizza {tipo} con {', '.join(base)} y adicional: {ing}."
    print("\n--- Pedido confirmado ---")
    print(descripcion)
    print(f"(Vegetariana: {'Sí' if es_veg else 'No'})")

if __name__ == "__main__":
    main()
