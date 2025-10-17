import kotlin.math.*

/**
 * Operador de extensión personalizado para repetición de cadenas
 * Facilita la creación de separadores visuales en la interfaz
 */
private operator fun String.times(repeticiones: Int) = repeat(repeticiones)

/**
 * Clase base para operaciones matemáticas fundamentales.
 * Proporciona funcionalidades básicas de aritmética, gestión de memoria 
 * y seguimiento del historial de operaciones realizadas.
 */
open class MaquinaCalculadoraBasica {

    // Sistema de almacenamiento temporal para valores
    private var registroMemoria: Double = 0.0

    // Registro cronológico de todas las operaciones ejecutadas
    private val registroHistorial: MutableList<String> = mutableListOf()

    /**
     * Propiedad que controla la cantidad de decimales mostrados en los resultados.
     * Se valida automáticamente para asegurar un valor mínimo de 10 decimales.
     */
    var nivelPrecision: Int = 10
        set(nuevoValor) {
            field = if (nuevoValor > 0) nuevoValor else 10
        }

    /**
     * Operaciones de suma para números enteros.
     * Implementación directa sin registro histórico por ser operación básica.
     */
    open fun efectuarSuma(primerOperando: Int, segundoOperando: Int): Int = primerOperando + segundoOperando

    /**
     * Operaciones de suma para números de punto flotante.
     * Incluye registro automático en el historial de operaciones.
     */
    open fun efectuarSuma(primerOperando: Double, segundoOperando: Double): Double {
        val valorResultado = primerOperando + segundoOperando
        almacenarOperacion("$primerOperando + $segundoOperando = $valorResultado")
        return valorResultado
    }

    /**
     * Operaciones de resta para números enteros.
     * Versión simplificada sin registro histórico.
     */
    open fun efectuarResta(primerOperando: Int, segundoOperando: Int): Int = primerOperando - segundoOperando

    /**
     * Operaciones de resta para números de punto flotante.
     * Almacena automáticamente la operación en el historial.
     */
    open fun efectuarResta(primerOperando: Double, segundoOperando: Double): Double {
        val valorResultado = primerOperando - segundoOperando
        almacenarOperacion("$primerOperando - $segundoOperando = $valorResultado")
        return valorResultado
    }

    /**
     * Operaciones de multiplicación para números enteros.
     * Implementación básica sin seguimiento histórico.
     */
    open fun efectuarMultiplicacion(primerOperando: Int, segundoOperando: Int): Int = primerOperando * segundoOperando

    /**
     * Operaciones de multiplicación para números de punto flotante.
     * Registra la operación realizada en el historial del sistema.
     */
    open fun efectuarMultiplicacion(primerOperando: Double, segundoOperando: Double): Double {
        val valorResultado = primerOperando * segundoOperando
        almacenarOperacion("$primerOperando * $segundoOperando = $valorResultado")
        return valorResultado
    }

    /**
     * División de números enteros con conversión automática a punto flotante.
     * Incluye validación para prevenir división por cero.
     */
    open fun efectuarDivision(primerOperando: Int, segundoOperando: Int): Double {
        if (segundoOperando == 0) throw ErrorDivisionCero()
        return primerOperando.toDouble() / segundoOperando.toDouble()
    }

    /**
     * División de números de punto flotante con validación de precisión.
     * Utiliza tolerancia numérica para detectar divisores prácticamente nulos.
     */
    open fun efectuarDivision(primerOperando: Double, segundoOperando: Double): Double {
        if (abs(segundoOperando) < 1e-10) throw ErrorDivisionCero()
        val valorResultado = primerOperando / segundoOperando
        almacenarOperacion("$primerOperando / $segundoOperando = $valorResultado")
        return valorResultado
    }

    /**
     * Almacena un valor numérico en el registro de memoria del sistema.
     * Proporciona confirmación visual del almacenamiento exitoso.
     */
    fun almacenarEnMemoria(valorAGuardar: Double) {
        registroMemoria = valorAGuardar
        almacenarOperacion("Memoria almacenada: $valorAGuardar")
        println("💾 Valor $valorAGuardar guardado en memoria")
    }

    /**
     * Recupera el valor actualmente almacenado en la memoria del sistema.
     * Registra la operación de recuperación en el historial.
     */
    fun recuperarDeMemoria(): Double {
        almacenarOperacion("Memoria recuperada: $registroMemoria")
        println("📤 Valor recuperado de memoria: $registroMemoria")
        return registroMemoria
    }

    /**
     * Incrementa el valor de memoria sumando el valor proporcionado.
     * Útil para acumular resultados en cálculos iterativos.
     */
    fun incrementarMemoria(valorIncremento: Double) {
        registroMemoria += valorIncremento
        almacenarOperacion("M+ $valorIncremento, Memoria actual: $registroMemoria")
        println("➕ Memoria + $valorIncremento = $registroMemoria")
    }

    /**
     * Decrementa el valor de memoria restando el valor proporcionado.
     * Complementa la funcionalidad de incremento para operaciones complejas.
     */
    fun decrementarMemoria(valorDecremento: Double) {
        registroMemoria -= valorDecremento
        almacenarOperacion("M- $valorDecremento, Memoria actual: $registroMemoria")
        println("➖ Memoria - $valorDecremento = $registroMemoria")
    }

    /**
     * Reinicia el registro de memoria estableciendo su valor en cero.
     * Proporciona confirmación visual de la operación de limpieza.
     */
    fun reiniciarMemoria() {
        registroMemoria = 0.0
        almacenarOperacion("Memoria reiniciada")
        println("🗑️ Memoria reiniciada")
    }

    /**
     * Método protegido para el registro interno de operaciones.
     * Mantiene automáticamente el historial limitado a 100 entradas.
     */
    protected fun almacenarOperacion(descripcionOperacion: String) {
        registroHistorial.add("${java.time.LocalDateTime.now()}: $descripcionOperacion")
        if (registroHistorial.size > 100) {
            registroHistorial.removeFirst()
        }
    }

    /**
     * Presenta el historial de operaciones en formato tabular.
     * Muestra las últimas 10 operaciones para evitar sobrecarga visual.
     */
    fun presentarHistorial() {
        println("\n📋 HISTORIAL DE OPERACIONES:")
        println("=" * 40)
        if (registroHistorial.isEmpty()) {
            println("No hay operaciones en el historial")
        } else {
            registroHistorial.takeLast(10).forEach { println(it) }
        }
    }

    /**
     * Elimina completamente el historial de operaciones.
     * Útil para iniciar sesiones de cálculo desde cero.
     */
    fun vaciarHistorial() {
        registroHistorial.clear()
        println("🧹 Historial vaciado")
    }

    /**
     * Formatea los resultados numéricos para presentación optimizada.
     * Distingue entre números enteros y decimales para mejor legibilidad.
     */
    open fun formatearSalida(valorResultado: Double): String {
        return if (valorResultado == floor(valorResultado)) {
            valorResultado.toInt().toString()
        } else {
            "%.${nivelPrecision}f".format(valorResultado).trimEnd('0').trimEnd('.')
        }
    }
}