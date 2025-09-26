import java.math.BigDecimal
import java.math.RoundingMode
import kotlin.system.exitProcess

// ----------------------
// Modelo: Producto
// ----------------------
data class Product(
    val id: String,               
    var name: String,
    var quantity: Int,
    var pricePerItem: BigDecimal
) {
    fun totalPrice(): BigDecimal {
        return pricePerItem.multiply(BigDecimal.valueOf(quantity.toLong()))
            .setScale(2, RoundingMode.HALF_UP)
    }
}

// ----------------------
// Inventario (lógica OO)
// ----------------------
class Inventory {
    private val items = mutableListOf<Product>()
    private var nextId = 1

    // Generador de ID tipo 0001, 0002...
    private fun generateId(): String {
        return String.format("%04d", nextId++)
    }

    // CREATE
    fun addProduct(name: String, quantity: Int, pricePerItem: BigDecimal): Product {
        val p = Product(
            id = generateId(),
            name = name,
            quantity = quantity,
            pricePerItem = pricePerItem.setScale(2, RoundingMode.HALF_UP)
        )
        items.add(p)
        return p
    }

    // READ (listar todos)
    fun listProducts(): List<Product> = items.toList()

    // READ (buscar por id)
    fun findById(id: String): Product? = items.find { it.id == id }

    // UPDATE
    fun updateProduct(id: String, newName: String?, newQuantity: Int?, newPrice: BigDecimal?): Boolean {
        val p = findById(id) ?: return false
        newName?.let { p.name = it }
        newQuantity?.let { p.quantity = it }
        newPrice?.let { p.pricePerItem = it.setScale(2, RoundingMode.HALF_UP) }
        return true
    }

    // DELETE
    fun deleteProduct(id: String): Boolean {
        val p = findById(id) ?: return false
        return items.remove(p)
    }

    // Valor total
    fun totalInventoryValue(): BigDecimal {
        return items.fold(BigDecimal.ZERO) { acc, prod -> acc + prod.totalPrice() }
            .setScale(2, RoundingMode.HALF_UP)
    }

    // Contador
    fun count(): Int = items.size
}

// ----------------------
// Utilidades de I/O
// ----------------------
object IO {
    private fun readTrimmedLine(prompt: String): String {
        print(prompt)
        val line = readLine()
        return line?.trim() ?: ""
    }

    fun readNonEmptyString(prompt: String): String {
        while (true) {
            val s = readTrimmedLine(prompt)
            if (s.isNotEmpty()) return s
            println("Entrada vacía — por favor ingresa un valor.")
        }
    }

    fun readInt(prompt: String, min: Int? = null, max: Int? = null): Int {
        while (true) {
            val s = readTrimmedLine(prompt)
            try {
                val v = s.toInt()
                if (min != null && v < min) {
                    println("El valor debe ser >= $min.")
                    continue
                }
                if (max != null && v > max) {
                    println("El valor debe ser <= $max.")
                    continue
                }
                return v
            } catch (e: Exception) {
                println("Entrada inválida. Ingresa un número entero.")
            }
        }
    }

    fun readBigDecimal(prompt: String, min: BigDecimal? = null): BigDecimal {
        while (true) {
            val s = readTrimmedLine(prompt).replace(",", ".")
            try {
                val bd = BigDecimal(s).setScale(2, RoundingMode.HALF_UP)
                if (min != null && bd < min) {
                    println("El valor debe ser >= $min.")
                    continue
                }
                return bd
            } catch (e: Exception) {
                println("Entrada inválida. Ingresa un número (ej: 12.50).")
            }
        }
    }

    fun pauseEnter() {
        print("\nPresiona Enter para volver al menú...")
        readLine()
    }
}

// ----------------------
// Interfaz de usuario (menú)
// ----------------------
fun main() {
    val inventory = Inventory()

    // Datos de ejemplo
    inventory.addProduct("Cargador USB-C 65W", 20, BigDecimal("29.99"))
    inventory.addProduct("Auriculares Bluetooth", 15, BigDecimal("79.50"))
    inventory.addProduct("SSD 1TB", 8, BigDecimal("109.00"))

    while (true) {
        println("\n=== SISTEMA DE INVENTARIO — TIENDA DE ELECTRÓNICA ===")
        println("Items en inventario: ${inventory.count()} | Valor total: \$${inventory.totalInventoryValue()}")
        println()
        println("1) Listar productos")
        println("2) Añadir producto")
        println("3) Actualizar producto")
        println("4) Eliminar producto")
        println("5) Mostrar resumen y totales")
        println("6) Salir")
        print("Selecciona una opción (1-6): ")

        when (readLine()?.trim()) {
            "1" -> listProductsUI(inventory)
            "2" -> addProductUI(inventory)
            "3" -> updateProductUI(inventory)
            "4" -> deleteProductUI(inventory)
            "5" -> showTotalsUI(inventory)
            "6" -> {
                println("Saliendo... ¡Hasta luego!")
                exitProcess(0)
            }
            else -> println("Opción inválida. Intenta de nuevo.")
        }
    }
}

// ----------------------
// Funciones UI
// ----------------------
fun listProductsUI(inv: Inventory) {
    println("\n--- LISTADO DE PRODUCTOS ---")
    val list = inv.listProducts()
    if (list.isEmpty()) {
        println("Inventario vacío.")
    } else {
        println(String.format("%-6s %-25s %8s %12s %12s", "ID", "Nombre", "Cantidad", "Precio/unid.", "Precio total"))
        println("-".repeat(70))
        for (p in list) {
            println(String.format("%-6s %-25s %8d %12s %12s",
                p.id, shorten(p.name, 25), p.quantity, formatMoney(p.pricePerItem), formatMoney(p.totalPrice())))
        }
    }
    IO.pauseEnter()
}

fun addProductUI(inv: Inventory) {
    println("\n--- AÑADIR PRODUCTO ---")
    val name = IO.readNonEmptyString("Nombre del producto: ")
    val qty = IO.readInt("Cantidad (>= 0): ", min = 0)
    val price = IO.readBigDecimal("Precio por unidad (ej: 39.90): ", min = BigDecimal.ZERO)
    val added = inv.addProduct(name, qty, price)
    println("\nProducto añadido con éxito:")
    println("ID: ${added.id}")
    println("Nombre: ${added.name}")
    println("Cantidad: ${added.quantity}")
    println("Precio/unidad: \$${formatMoney(added.pricePerItem)}")
    println("Precio total: \$${formatMoney(added.totalPrice())}")
    IO.pauseEnter()
}

fun updateProductUI(inv: Inventory) {
    println("\n--- ACTUALIZAR PRODUCTO ---")
    val id = IO.readNonEmptyString("Ingresa el ID del producto a actualizar: ")
    val p = inv.findById(id)
    if (p == null) {
        println("No se encontró producto con ID = $id")
        IO.pauseEnter()
        return
    }

    println("Producto encontrado: ${p.name} (Cantidad: ${p.quantity}, Precio: \$${formatMoney(p.pricePerItem)})")
    println("Deja vacío si no deseas modificar un campo.")

    print("Nuevo nombre [${p.name}]: ")
    val newNameRaw = readLine()?.trim()
    val newName = if (newNameRaw.isNullOrEmpty()) null else newNameRaw

    var newQty: Int? = null
    while (true) {
        print("Nueva cantidad [${p.quantity}]: ")
        val raw = readLine()?.trim()
        if (raw.isNullOrEmpty()) break
        try {
            val v = raw.toInt()
            if (v < 0) {
                println("La cantidad debe ser >= 0.")
                continue
            }
            newQty = v
            break
        } catch (e: Exception) {
            println("Entrada inválida. Ingresa un número entero.")
        }
    }

    var newPrice: BigDecimal? = null
    while (true) {
        print("Nuevo precio/unidad [${formatMoney(p.pricePerItem)}]: ")
        val raw = readLine()?.trim()
        if (raw.isNullOrEmpty()) break
        try {
            val bd = BigDecimal(raw.replace(",", ".")).setScale(2, RoundingMode.HALF_UP)
            if (bd < BigDecimal.ZERO) {
                println("El precio debe ser >= 0.")
                continue
            }
            newPrice = bd
            break
        } catch (e: Exception) {
            println("Entrada inválida. Usa formato numérico (ej: 49.90).")
        }
    }

    val ok = inv.updateProduct(id, newName, newQty, newPrice)
    if (ok) {
        println("Producto actualizado correctamente.")
        val updated = inv.findById(id)!!
        println("-> ${updated.name} | Cantidad: ${updated.quantity} | Precio/unidad: \$${formatMoney(updated.pricePerItem)} | Total: \$${formatMoney(updated.totalPrice())}")
    } else {
        println("Error al actualizar el producto.")
    }
    IO.pauseEnter()
}

fun deleteProductUI(inv: Inventory) {
    println("\n--- ELIMINAR PRODUCTO ---")
    val id = IO.readNonEmptyString("Ingresa el ID del producto a eliminar: ")
    val p = inv.findById(id)
    if (p == null) {
        println("No se encontró producto con ID = $id")
        IO.pauseEnter()
        return
    }

    println("Producto: ${p.name} | Cantidad: ${p.quantity} | Precio total: \$${formatMoney(p.totalPrice())}")
    print("¿Confirmas eliminación? (s/N): ")
    val confirm = readLine()?.trim()?.lowercase()
    if (confirm == "s" || confirm == "si") {
        val deleted = inv.deleteProduct(id)
        if (deleted) println("Producto eliminado.") else println("No se pudo eliminar el producto.")
    } else {
        println("Eliminación cancelada.")
    }
    IO.pauseEnter()
}

fun showTotalsUI(inv: Inventory) {
    println("\n--- RESUMEN Y TOTALES ---")
    val list = inv.listProducts()
    if (list.isEmpty()) {
        println("Inventario vacío.")
    } else {
        var grandTotal = BigDecimal.ZERO
        println(String.format("%-25s %8s %12s %12s", "Nombre", "Cantidad", "Precio/unid.", "Precio total"))
        println("-".repeat(70))
        for (p in list) {
            println(String.format("%-25s %8d %12s %12s",
                shorten(p.name, 25), p.quantity, formatMoney(p.pricePerItem), formatMoney(p.totalPrice())))
            grandTotal += p.totalPrice()
        }
        println("-".repeat(70))
        println(String.format("%-25s %8s %12s %12s", "TOTAL INVENTARIO", "", "", formatMoney(grandTotal)))
    }
    IO.pauseEnter()
}

// ----------------------
// Helpers
// ----------------------
fun formatMoney(bd: BigDecimal): String = bd.setScale(2, RoundingMode.HALF_UP).toPlainString()

fun shorten(s: String, maxLen: Int): String {
    return if (s.length <= maxLen) s else s.substring(0, maxLen - 3) + "..."
}

