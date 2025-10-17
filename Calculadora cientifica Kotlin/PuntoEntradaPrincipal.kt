/**
 * Punto de entrada principal del Sistema de Calculadora Científica Avanzada.
 * Inicializa el sistema de interfaz de usuario y maneja errores críticos
 * que puedan ocurrir durante la inicialización del programa.
 */

/**
 * Función principal que inicia la ejecución del sistema completo.
 * Incluye manejo robusto de excepciones para garantizar estabilidad.
 */
fun main() {
    try {
        // Inicialización del sistema de interfaz de usuario
        val sistemaInterfaz = SistemaInterfazUsuario()

        // Ejecución del bucle principal interactivo
        sistemaInterfaz.ejecutarSistemaInteractivo()

    } catch (excepcionCritica: Exception) {
        println("💥 Error crítico durante la inicialización: ${excepcionCritica.message}")
        excepcionCritica.printStackTrace()
    }
}