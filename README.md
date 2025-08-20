# Taller de Haskell: Sistema de Gestión de Inventario  

Este proyecto implementa un **sistema de inventario interactivo en Haskell**, con el objetivo de resolver un problema de negocio de manera práctica y didáctica.  

El programa permite **gestionar productos**, **aplicar descuentos**, **consultar resúmenes**, y **modificar el inventario** en una interfaz basada en consola.  

---

## Autor  
**Andrés Sebastián Coral Vallejo**  


---

## Funcionalidades principales  

El sistema soporta las siguientes operaciones:  

1. **Agregar producto** → Permite registrar un nuevo producto con nombre, precio y cantidad.  
2. **Actualizar cantidad** → Modifica la cantidad de un producto ya existente.  
3. **Eliminar producto** → Borra un producto del inventario.  
4. **Mostrar resumen** → Calcula el total de productos en stock y el valor total del inventario.  
5. **Buscar producto** → Consulta precio y cantidad de un producto específico.  
6. **Aplicar descuento general** → Aplica un porcentaje de descuento a todos los productos del inventario.  
7. **Mostrar inventario completo** → Lista todos los productos con su respectiva información.  
8. **Aplicar descuento a un producto específico** → Permite asignar un descuento solo a un producto.  
9. **Salir del sistema**  

##  Notas importantes  

- El sistema **ignora mayúsculas y minúsculas** al comparar nombres de productos.  
- Los precios se actualizan automáticamente cuando se aplican descuentos.  
- Se incluye una función para limpiar la consola (`clearScreen`) que funciona en Windows, Linux y Mac.
   Consulté como a traves de: https://stackoverflow.com/questions/2472391/how-do-i-clear-the-terminal-screen-in-haskell

