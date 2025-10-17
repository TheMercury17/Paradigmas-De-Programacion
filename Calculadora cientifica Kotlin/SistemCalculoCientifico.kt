import kotlin.math.*

/**
 * Extensión avanzada de la calculadora básica que incorpora funciones matemáticas
 * científicas y trigonométricas. Proporciona capacidades de cálculo profesional
 * con manejo de diferentes sistemas de medición angular.
 */
class SistemCalculoCientifico : MaquinaCalculadoraBasica() {

    // Control interno del sistema de medición angular utilizado
    private var utilizaRadianes: Boolean = true

    /**
     * Propiedad que gestiona el modo de interpretación de ángulos.
     * Permite alternar entre radianes y grados según las necesidades del cálculo.
     */
    var sistemaMedicionAngular: String
        get() = if (utilizaRadianes) "Radianes" else "Grados"
        set(nuevoSistema) {
            utilizaRadianes = nuevoSistema.lowercase() == "radianes" || nuevoSistema.lowercase() == "rad"
        }

    /**
     * Formateador especializado para resultados científicos.
     * Utiliza notación científica para números extremadamente grandes o pequeños.
     */
    override fun formatearSalida(valorResultado: Double): String {
        return when {
            abs(valorResultado) >= 1e6 || abs(valorResultado) <= 1e-6 && valorResultado != 0.0 ->
                "%.${nivelPrecision}e".format(valorResultado)
            else -> super.formatearSalida(valorResultado)
        }
    }

    /**
     * Calcula la función seno de un ángulo.
     * Convierte automáticamente entre grados y radianes según la configuración actual.
     */
    fun calcularSeno(valorAngular: Double): Double {
        val anguloEnRadianes = if (utilizaRadianes) valorAngular else Math.toRadians(valorAngular)
        val valorResultado = sin(anguloEnRadianes)
        almacenarOperacion("sin($valorAngular${if (utilizaRadianes) " rad" else "°"}) = $valorResultado")
        return valorResultado
    }

    /**
     * Calcula la función coseno de un ángulo.
     * Maneja automáticamente la conversión del sistema de medición angular.
     */
    fun calcularCoseno(valorAngular: Double): Double {
        val anguloEnRadianes = if (utilizaRadianes) valorAngular else Math.toRadians(valorAngular)
        val valorResultado = cos(anguloEnRadianes)
        almacenarOperacion("cos($valorAngular${if (utilizaRadianes) " rad" else "°"}) = $valorResultado")
        return valorResultado
    }

    /**
     * Calcula la función tangente con validación de singularidades.
     * Detecta y previene el cálculo en puntos donde la tangente es indefinida.
     */
    fun calcularTangente(valorAngular: Double): Double {
        val anguloEnRadianes = if (utilizaRadianes) valorAngular else Math.toRadians(valorAngular)
        val valorCoseno = cos(anguloEnRadianes)

        if (abs(valorCoseno) < 1e-10) {
            throw ErrorValorInvalido("Tangente indefinida para $valorAngular${if (utilizaRadianes) " radianes" else " grados"}")
        }

        val valorResultado = tan(anguloEnRadianes)
        almacenarOperacion("tan($valorAngular${if (utilizaRadianes) " rad" else "°"}) = $valorResultado")
        return valorResultado
    }

    /**
     * Realiza operaciones de exponenciación con validación de resultados.
     * Incluye verificación de valores indefinidos e infinitos.
     */
    fun calcularPotencia(valorBase: Double, valorExponente: Double): Double {
        try {
            val valorResultado = valorBase.pow(valorExponente)
            if (valorResultado.isNaN() || valorResultado.isInfinite()) {
                throw ErrorValorInvalido("Resultado indefinido para $valorBase^$valorExponente")
            }
            almacenarOperacion("$valorBase^$valorExponente = $valorResultado")
            return valorResultado
        } catch (excepcion: Exception) {
            throw ErrorValorInvalido("Error en cálculo de potencia: ${excepcion.message}")
        }
    }

    /**
     * Calcula la raíz cuadrada con validación de dominio.
     * Previene el cálculo de raíces de números negativos en el dominio real.
     */
    fun extraerRaizCuadrada(valorOperando: Double): Double {
        if (valorOperando < 0) {
            throw ErrorValorInvalido("No se puede calcular raíz cuadrada de número negativo")
        }
        val valorResultado = sqrt(valorOperando)
        almacenarOperacion("√$valorOperando = $valorResultado")
        return valorResultado
    }

    /**
     * Calcula logaritmo en base 10 con validación de dominio.
     * Asegura que el argumento sea estrictamente positivo.
     */
    fun calcularLogaritmoDecimal(valorOperando: Double): Double {
        if (valorOperando <= 0) {
            throw ErrorValorInvalido("El logaritmo solo acepta valores positivos")
        }
        val valorResultado = log10(valorOperando)
        almacenarOperacion("log₁₀($valorOperando) = $valorResultado")
        return valorResultado
    }

    /**
     * Calcula logaritmo natural (neperiano) con validación de dominio.
     * Utiliza la base e matemática para el cálculo logarítmico.
     */
    fun calcularLogaritmoNatural(valorOperando: Double): Double {
        if (valorOperando <= 0) {
            throw ErrorValorInvalido("El logaritmo natural solo acepta valores positivos")
        }
        val valorResultado = ln(valorOperando)
        almacenarOperacion("ln($valorOperando) = $valorResultado")
        return valorResultado
    }

    /**
     * Calcula la función exponencial (e^x) con control de desbordamiento.
     * Detecta y maneja resultados que excedan los límites numéricos.
     */
    fun calcularFuncionExponencial(valorExponente: Double): Double {
        val valorResultado = exp(valorExponente)
        if (valorResultado.isInfinite()) {
            throw ErrorValorInvalido("Resultado demasiado grande para exponencial")
        }
        almacenarOperacion("e^$valorExponente = $valorResultado")
        return valorResultado
    }

    /**
     * Convierte medidas angulares de grados a radianes.
     * Útil para preparar valores para funciones trigonométricas.
     */
    fun convertirGradosARadianes(valorEnGrados: Double): Double {
        val valorResultado = Math.toRadians(valorEnGrados)
        almacenarOperacion("$valorEnGrados° = $valorResultado rad")
        return valorResultado
    }

    /**
     * Convierte medidas angulares de radianes a grados.
     * Facilita la interpretación de resultados en el sistema sexagesimal.
     */
    fun convertirRadianesAGrados(valorEnRadianes: Double): Double {
        val valorResultado = Math.toDegrees(valorEnRadianes)
        almacenarOperacion("$valorEnRadianes rad = $valorResultado°")
        return valorResultado
    }

    /**
     * Calcula el factorial de un número entero con validaciones múltiples.
     * Incluye verificación de dominio y límites computacionales.
     */
    fun calcularFactorial(numeroEntero: Int): Double {
        if (numeroEntero < 0) {
            throw ErrorValorInvalido("El factorial no está definido para números negativos")
        }
        if (numeroEntero > 170) {
            throw ErrorValorInvalido("Factorial demasiado grande (máximo 170)")
        }

        var valorResultado = 1.0
        for (indice in 2..numeroEntero) {
            valorResultado *= indice
        }

        almacenarOperacion("$numeroEntero! = $valorResultado")
        return valorResultado
    }

    /**
     * Calcula el valor absoluto (módulo) de un número.
     * Devuelve la distancia del número respecto al origen.
     */
    fun obtenerValorAbsoluto(valorOperando: Double): Double {
        val valorResultado = abs(valorOperando)
        almacenarOperacion("|$valorOperando| = $valorResultado")
        return valorResultado
    }

    /**
     * Procesa y evalúa expresiones matemáticas complejas.
     * Utiliza un analizador sintáctico especializado para interpretar la expresión.
     */
    fun procesarExpresionMatematica(cadenaExpresion: String): Double {
        try {
            val analizadorSintactico = AnalizadorExpresiones(this)
            val valorResultado = analizadorSintactico.interpretar(cadenaExpresion.trim())
            almacenarOperacion("Expresión '$cadenaExpresion' = $valorResultado")
            return valorResultado
        } catch (excepcion: Exception) {
            throw ErrorExpresionInvalida("Error al evaluar '$cadenaExpresion': ${excepcion.message}")
        }
    }
}