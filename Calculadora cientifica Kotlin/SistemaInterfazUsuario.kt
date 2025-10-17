/**
 * Sistema de interfaz de usuario para la calculadora científica avanzada.
 * Proporciona una interfaz de línea de comandos interactiva con capacidades
 * de procesamiento de expresiones, gestión de memoria y configuración del sistema.
 */
class SistemaInterfazUsuario {

    // Instancia del motor de cálculo científico para procesamiento de operaciones
    private val motorCalculoAvanzado = SistemCalculoCientifico()

    /**
     * Método principal que inicializa y ejecuta el bucle interactivo del sistema.
     * Presenta la interfaz de bienvenida y procesa comandos hasta que el usuario termine la sesión.
     */
    fun ejecutarSistemaInteractivo() {
        // Presentación del banner de bienvenida del sistema
        presentarBannerInicial()
        mostrarInformacionAyuda()

        // Bucle principal de interacción con el usuario
        while (true) {
            try {
                print("\n🧮 SistemaCalculadora> ")
                val entradaUsuario = readLine()?.trim() ?: continue

                // Procesamiento de comandos mediante estructura condicional
                when {
                    entradaUsuario.isEmpty() -> continue
                    entradaUsuario == "ayuda" || entradaUsuario == "help" -> mostrarInformacionAyuda()
                    entradaUsuario == "salir" || entradaUsuario == "exit" -> break
                    entradaUsuario == "historial" -> motorCalculoAvanzado.presentarHistorial()
                    entradaUsuario == "limpiar" -> motorCalculoAvanzado.vaciarHistorial()
                    entradaUsuario.startsWith("precision ") -> modificarNivelPrecision(entradaUsuario)
                    entradaUsuario.startsWith("modo ") -> alterarSistemaMedicionAngular(entradaUsuario)
                    entradaUsuario == "memoria" || entradaUsuario == "mr" -> exhibirResultado(motorCalculoAvanzado.recuperarDeMemoria())
                    entradaUsuario.startsWith("ms ") -> ejecutarAlmacenamientoMemoria(entradaUsuario)
                    entradaUsuario.startsWith("m+ ") -> ejecutarIncrementoMemoria(entradaUsuario)
                    entradaUsuario.startsWith("m- ") -> ejecutarDecrementoMemoria(entradaUsuario)
                    entradaUsuario == "mc" -> motorCalculoAvanzado.reiniciarMemoria()
                    entradaUsuario == "estado" -> presentarEstadoSistema()
                    else -> procesarExpresionMatematica(entradaUsuario)
                }

            } catch (excepcionCalculadora: ErrorSistemaCalculadora) {
                println("⚠️ ${excepcionCalculadora.message}")
            } catch (excepcionGenerica: Exception) {
                println("💥 Error inesperado: ${excepcionGenerica.message}")
            }
        }

        println("\n👋 ¡Hasta la vista, calculadora!")
    }

    /**
     * Presenta el banner inicial decorativo del sistema.
     * Utiliza caracteres Unicode para crear una interfaz visualmente atractiva.
     */
    private fun presentarBannerInicial() {
        println("""

╔════════════════════════════════════════════════╗
║         SISTEMA CALCULADORA CIENTÍFICA         ║
║            Arquitectura Orientada              ║
║              a Objetos (AOO)                   ║
╚════════════════════════════════════════════════╝

        """.trimIndent())
    }

    /**
     * Muestra la información completa de ayuda y comandos disponibles.
     * Organiza los comandos por categorías para facilitar la navegación.
     */
    private fun mostrarInformacionAyuda() {
        println("""

╔═══════════════════════════════════════════════════════════════════════╗
║                           COMANDOS DISPONIBLES                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║ • Expresiones: 2 + 3 * 4, sqrt(16), sin(30), log(100)               ║
║ • Memoria: ms <valor>, mr, m+ <valor>, m- <valor>, mc                 ║
║ • Configuración: precision <número>, modo <radianes|grados>           ║
║ • Utilidades: historial, limpiar, estado, ayuda, salir               ║
╚═══════════════════════════════════════════════════════════════════════╝

        """.trimIndent())
    }

    /**
     * Procesa y evalúa expresiones matemáticas ingresadas por el usuario.
     * Utiliza el motor de cálculo científico para la evaluación.
     */
    private fun procesarExpresionMatematica(cadenaExpresion: String) {
        val valorResultado = motorCalculoAvanzado.procesarExpresionMatematica(cadenaExpresion)
        exhibirResultado(valorResultado)
    }

    /**
     * Presenta el resultado de una operación en formato optimizado.
     * Utiliza el formateador del sistema para la representación numérica.
     */
    private fun exhibirResultado(valorResultado: Double) {
        val representacionFormateada = motorCalculoAvanzado.formatearSalida(valorResultado)
        println("✨ Resultado: $representacionFormateada")
    }

    /**
     * Modifica el nivel de precisión decimal del sistema.
     * Valida y aplica el nuevo valor de precisión especificado.
     */
    private fun modificarNivelPrecision(comandoEntrada: String) {
        try {
            val nuevaPrecision = comandoEntrada.split(" ")[1].toInt()
            motorCalculoAvanzado.nivelPrecision = nuevaPrecision
            println("🎯 Precisión establecida en $nuevaPrecision dígitos")
        } catch (excepcion: Exception) {
            println("❌ Formato inválido. Use: precision <número>")
        }
    }

    /**
     * Altera el sistema de medición angular entre radianes y grados.
     * Permite cambiar la interpretación de funciones trigonométricas.
     */
    private fun alterarSistemaMedicionAngular(comandoEntrada: String) {
        val nuevoSistema = comandoEntrada.split(" ")[1]
        motorCalculoAvanzado.sistemaMedicionAngular = nuevoSistema
        println("📐 Modo de ángulos: ${motorCalculoAvanzado.sistemaMedicionAngular}")
    }

    /**
     * Ejecuta el almacenamiento de un valor específico en la memoria del sistema.
     * Parsea el valor desde la entrada del usuario y lo guarda.
     */
    private fun ejecutarAlmacenamientoMemoria(comandoEntrada: String) {
        try {
            val valorAAlmacenar = comandoEntrada.split(" ")[1].toDouble()
            motorCalculoAvanzado.almacenarEnMemoria(valorAAlmacenar)
        } catch (excepcion: Exception) {
            println("❌ Formato inválido. Use: ms <valor>")
        }
    }

    /**
     * Ejecuta la operación de incremento sobre el valor de memoria actual.
     * Suma el valor especificado al contenido actual de la memoria.
     */
    private fun ejecutarIncrementoMemoria(comandoEntrada: String) {
        try {
            val valorIncremento = comandoEntrada.split(" ")[1].toDouble()
            motorCalculoAvanzado.incrementarMemoria(valorIncremento)
        } catch (excepcion: Exception) {
            println("❌ Formato inválido. Use: m+ <valor>")
        }
    }

    /**
     * Ejecuta la operación de decremento sobre el valor de memoria actual.
     * Resta el valor especificado del contenido actual de la memoria.
     */
    private fun ejecutarDecrementoMemoria(comandoEntrada: String) {
        try {
            val valorDecremento = comandoEntrada.split(" ")[1].toDouble()
            motorCalculoAvanzado.decrementarMemoria(valorDecremento)
        } catch (excepcion: Exception) {
            println("❌ Formato inválido. Use: m- <valor>")
        }
    }

    /**
     * Presenta el estado actual completo del sistema.
     * Incluye configuración de precisión, modo angular y contenido de memoria.
     */
    private fun presentarEstadoSistema() {
        println("""

╔═══════════════════════════════════════════════╗
║                 ESTADO SISTEMA                ║
╠═══════════════════════════════════════════════╣
║ Precisión: ${motorCalculoAvanzado.nivelPrecision} dígitos                        ║
║ Modo ángulos: ${motorCalculoAvanzado.sistemaMedicionAngular}                   ║
║ Memoria: ${motorCalculoAvanzado.formatearSalida(motorCalculoAvanzado.recuperarDeMemoria())}                          ║
╚═══════════════════════════════════════════════╝

        """.trimIndent())
    }
}