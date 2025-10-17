/**
 * Clase base para todas las excepciones relacionadas con el sistema de calculadora.
 * Proporciona una jerarquía unificada para el manejo de errores específicos
 * del dominio matemático y de procesamiento de expresiones.
 * 
 * @param mensajeError Descripción detallada del error ocurrido
 */
open class ErrorSistemaCalculadora(mensajeError: String) : Exception(mensajeError)

/**
 * Excepción especializada para errores de división por cero.
 * Se lanza cuando se intenta realizar una división con denominador nulo
 * o prácticamente nulo (dentro de la tolerancia numérica establecida).
 */
class ErrorDivisionCero : ErrorSistemaCalculadora("Error: División por cero no permitida")

/**
 * Excepción para valores numéricos que están fuera del dominio válido.
 * Incluye casos como raíces cuadradas de números negativos, logaritmos
 * de valores no positivos, y resultados que exceden límites computacionales.
 * 
 * @param descripcionError Descripción específica del problema con el valor
 */
class ErrorValorInvalido(descripcionError: String) : ErrorSistemaCalculadora("Valor inválido: $descripcionError")

/**
 * Excepción para errores de sintaxis en expresiones matemáticas.
 * Se utiliza cuando el analizador sintáctico encuentra elementos
 * malformados, paréntesis desbalanceados, o funciones no reconocidas.
 * 
 * @param descripcionError Descripción específica del error sintáctico encontrado
 */
class ErrorExpresionInvalida(descripcionError: String) : ErrorSistemaCalculadora("Expresión inválida: $descripcionError")