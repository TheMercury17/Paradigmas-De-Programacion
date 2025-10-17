import kotlin.math.*

/**
 * Analizador sintáctico especializado para interpretar y evaluar expresiones matemáticas.
 * Implementa un parser recursivo descendente que respeta la precedencia de operadores
 * y maneja funciones matemáticas avanzadas a través de la calculadora científica.
 * 
 * @param sistemaCalculoAvanzado Instancia de la calculadora científica para operaciones
 */
class AnalizadorExpresiones(private val sistemaCalculoAvanzado: SistemCalculoCientifico) {

    // Índice actual de procesamiento en la cadena de expresión
    private var indiceActual = 0

    // Cadena de expresión matemática que se está procesando
    private lateinit var cadenaExpresion: String

    /**
     * Método principal para interpretar y evaluar una expresión matemática completa.
     * Inicializa el analizador y procesa la expresión desde el nivel más alto de precedencia.
     * 
     * @param expresionEntrada Cadena que contiene la expresión matemática a evaluar
     * @return Valor numérico resultado de la evaluación
     * @throws ErrorExpresionInvalida Si hay caracteres no procesados al final
     */
    fun interpretar(expresionEntrada: String): Double {
        // Preparación de la expresión eliminando espacios en blanco
        cadenaExpresion = expresionEntrada.replace(" ", "")
        indiceActual = 0

        // Procesamiento de la expresión completa
        val valorResultado = analizarExpresionCompleta()

        // Validación de que toda la expresión fue procesada
        if (indiceActual < cadenaExpresion.length) {
            throw ErrorExpresionInvalida("Caracteres inesperados al final de la expresión")
        }

        return valorResultado
    }

    /**
     * Analiza el nivel más alto de precedencia: sumas y restas.
     * Procesa términos conectados por operadores de adición o sustracción.
     */
    private fun analizarExpresionCompleta(): Double {
        var valorAcumulado = analizarTerminoMultiplicativo()

        while (indiceActual < cadenaExpresion.length) {
            val simboloOperador = cadenaExpresion[indiceActual]

            if (simboloOperador == '+' || simboloOperador == '-') {
                indiceActual++
                val siguienteTermino = analizarTerminoMultiplicativo()

                valorAcumulado = if (simboloOperador == '+') {
                    sistemaCalculoAvanzado.efectuarSuma(valorAcumulado, siguienteTermino)
                } else {
                    sistemaCalculoAvanzado.efectuarResta(valorAcumulado, siguienteTermino)
                }
            } else {
                break
            }
        }

        return valorAcumulado
    }

    /**
     * Analiza términos multiplicativos: multiplicaciones y divisiones.
     * Maneja la precedencia intermedia de operadores aritméticos.
     */
    private fun analizarTerminoMultiplicativo(): Double {
        var valorAcumulado = analizarFactorElemental()

        while (indiceActual < cadenaExpresion.length) {
            val simboloOperador = cadenaExpresion[indiceActual]

            if (simboloOperador == '*' || simboloOperador == '/') {
                indiceActual++
                val siguienteFactor = analizarFactorElemental()

                valorAcumulado = if (simboloOperador == '*') {
                    sistemaCalculoAvanzado.efectuarMultiplicacion(valorAcumulado, siguienteFactor)
                } else {
                    sistemaCalculoAvanzado.efectuarDivision(valorAcumulado, siguienteFactor)
                }
            } else {
                break
            }
        }

        return valorAcumulado
    }

    /**
     * Analiza factores elementales: números, signos unarios y expresiones parentizadas.
     * Maneja el nivel de precedencia más alto en la jerarquía de operadores.
     */
    private fun analizarFactorElemental(): Double {
        // Validación de expresión completa
        if (indiceActual >= cadenaExpresion.length) {
            throw ErrorExpresionInvalida("Expresión incompleta")
        }

        // Procesamiento de signo negativo unario
        if (cadenaExpresion[indiceActual] == '-') {
            indiceActual++
            return -analizarFactorElemental()
        }

        // Procesamiento de signo positivo unario (opcional)
        if (cadenaExpresion[indiceActual] == '+') {
            indiceActual++
            return analizarFactorElemental()
        }

        // Procesamiento de expresiones entre paréntesis
        if (cadenaExpresion[indiceActual] == '(') {
            indiceActual++
            val valorInterior = analizarExpresionCompleta()

            if (indiceActual >= cadenaExpresion.length || cadenaExpresion[indiceActual] != ')') {
                throw ErrorExpresionInvalida("Paréntesis no balanceados")
            }

            indiceActual++
            return valorInterior
        }

        // Procesamiento de números o funciones matemáticas
        return analizarNumeroOFuncionMatematica()
    }

    /**
     * Determina si el elemento actual es una función matemática o un número literal.
     * Delega el procesamiento al método apropiado según el tipo de elemento.
     */
    private fun analizarNumeroOFuncionMatematica(): Double {
        return if (indiceActual < cadenaExpresion.length && cadenaExpresion[indiceActual].isLetter()) {
            val nombreFuncion = extraerNombreFuncion()
            procesarFuncionMatematica(nombreFuncion)
        } else {
            extraerValorNumerico()
        }
    }

    /**
     * Extrae el nombre completo de una función matemática.
     * Lee caracteres alfabéticos consecutivos para formar el identificador.
     */
    private fun extraerNombreFuncion(): String {
        val posicionInicial = indiceActual

        while (indiceActual < cadenaExpresion.length && cadenaExpresion[indiceActual].isLetter()) {
            indiceActual++
        }

        return cadenaExpresion.substring(posicionInicial, indiceActual)
    }

    /**
     * Extrae y convierte un valor numérico de la expresión.
     * Maneja tanto números enteros como decimales con punto flotante.
     */
    private fun extraerValorNumerico(): Double {
        val posicionInicial = indiceActual

        // Procesamiento de dígitos enteros
        while (indiceActual < cadenaExpresion.length && cadenaExpresion[indiceActual].isDigit()) {
            indiceActual++
        }

        // Procesamiento de parte decimal si existe
        if (indiceActual < cadenaExpresion.length && cadenaExpresion[indiceActual] == '.') {
            indiceActual++
            while (indiceActual < cadenaExpresion.length && cadenaExpresion[indiceActual].isDigit()) {
                indiceActual++
            }
        }

        // Validación de que se encontró al menos un dígito
        if (posicionInicial == indiceActual) {
            throw ErrorExpresionInvalida("Se esperaba un número en posición $indiceActual")
        }

        return cadenaExpresion.substring(posicionInicial, indiceActual).toDouble()
    }

    /**
     * Procesa y evalúa funciones matemáticas con sus argumentos.
     * Mapea nombres de funciones a sus implementaciones en la calculadora científica.
     * 
     * @param identificadorFuncion Nombre de la función matemática a evaluar
     * @return Resultado de la evaluación de la función
     */
    private fun procesarFuncionMatematica(identificadorFuncion: String): Double {
        // Validación de sintaxis de función (debe tener paréntesis de apertura)
        if (indiceActual >= cadenaExpresion.length || cadenaExpresion[indiceActual] != '(') {
            throw ErrorExpresionInvalida("Se esperaba '(' después de la función $identificadorFuncion")
        }

        indiceActual++
        val valorArgumento = analizarExpresionCompleta()

        // Validación de paréntesis de cierre
        if (indiceActual >= cadenaExpresion.length || cadenaExpresion[indiceActual] != ')') {
            throw ErrorExpresionInvalida("Se esperaba ')' para la función $identificadorFuncion")
        }

        indiceActual++

        // Mapeo de funciones a sus implementaciones específicas
        return when (identificadorFuncion.lowercase()) {
            "sin", "sen" -> sistemaCalculoAvanzado.calcularSeno(valorArgumento)
            "cos" -> sistemaCalculoAvanzado.calcularCoseno(valorArgumento)
            "tan" -> sistemaCalculoAvanzado.calcularTangente(valorArgumento)
            "sqrt", "raiz" -> sistemaCalculoAvanzado.extraerRaizCuadrada(valorArgumento)
            "log" -> sistemaCalculoAvanzado.calcularLogaritmoDecimal(valorArgumento)
            "ln" -> sistemaCalculoAvanzado.calcularLogaritmoNatural(valorArgumento)
            "exp" -> sistemaCalculoAvanzado.calcularFuncionExponencial(valorArgumento)
            "abs" -> sistemaCalculoAvanzado.obtenerValorAbsoluto(valorArgumento)
            else -> throw ErrorExpresionInvalida("Función desconocida: $identificadorFuncion")
        }
    }
}