# Quiz 26/09/2025 - Sistema de gestión de inventarios.

## Autor  
**Andrés Sebastián Coral Vallejo.** 

---

## ACLARACIÓN IMPORTANTE:

Una disculpa por mi ausencia el día de hoy, me encontraba en revisión de un hemograma en el Dispensario Norte de Sanidad Militar.
A pesar de eso me encontraba al tanto de la clase y del grupo de Teams, por lo que aquí está mi entrega.
Agradezco mucho su comprensión, le deseo un excelente día.

---

### El programa tiene la capacidad de:
- Mostrar: cantidad, precio por ítem y el precio total.
- CRUD (Create, Read, Update, Delete)

Podría decirse que el programa consta de 4 capas principales:  
- **Modelo (`Product`)** → Encargado de definir la estructura de datos.  
- **Lógica (`Inventory`)** → Que maneja el inventario y operaciones CRUD.  
- **Interfaz (`main` + funciones UI)** → Que permite la interacción con el usuario.  
- **Utilidades (`IO` + helpers)** → Para dar validaciones y formato. 

---

## Estructura del código.

### 1. **Clase `Product`**
Representa un producto de la tienda.  
Atributos principales:  
- `id`: identificador único de 4 dígitos (`0001`, `0002`, …).  
- `name`: nombre del producto.  
- `quantity`: cantidad en inventario.  
- `pricePerItem`: precio unitario.  

Incluye el método `totalPrice()` para calcular el valor total de ese producto (`cantidad × precio unitario`).  

---

### 2. **Clase `Inventory`**
Administra la lista de productos y las operaciones CRUD:  

- `addProduct()`: añade un nuevo producto con ID automático.  
- `listProducts()`: devuelve la lista completa de productos.  
- `findById()`: busca un producto por su ID.  
- `updateProduct()`: permite modificar nombre, cantidad o precio de un producto.  
- `deleteProduct()`: elimina un producto existente.  
- `totalInventoryValue()`: calcula el valor total del inventario.  
- `count()`: muestra cuántos productos hay registrados.  

---

### 3. **Objeto `IO`**
Maneja la entrada de datos del usuario con validaciones:  
- `readNonEmptyString()`: asegura que el texto no esté vacío.  
- `readInt()`: lee enteros con validación de rangos.  
- `readBigDecimal()`: lee valores decimales, útil para precios.  
- `pauseEnter()`: pausa la ejecución hasta presionar *Enter*.  

---

### 4. **Función `main()`**
Contiene el menú interactivo de la aplicación:  

Opciones disponibles:  
1. Listar productos  
2. Añadir producto  
3. Actualizar producto  
4. Eliminar producto  
5. Mostrar resumen y totales  
6. Salir   

---

### 5. **Funciones de interfaz (UI)**
Cada opción del menú llama a una función que implementa la interacción:  
- `listProductsUI()`: imprime en formato tabla todos los productos.  
- `addProductUI()`: guía al usuario para registrar un nuevo producto.  
- `updateProductUI()`: permite modificar datos de un producto existente.  
- `deleteProductUI()`: confirma y elimina un producto del inventario.  
- `showTotalsUI()`: muestra un resumen con totales y valores acumulados.  

---

### 6. **Helpers**
- `formatMoney()`: da formato uniforme a precios (`2 decimales`).  
- `shorten()`: acorta nombres largos para que encajen en la tabla.  




