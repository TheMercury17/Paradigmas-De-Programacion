# Aplicación Web de Regresión Lineal - Spring Boot + Kotlin

## Autor

**Andrés Sebastián Coral Vallejo & Javier Felipe Rosero Sandoval**

## Introducción

El proyecto cosiste de una aplicación web de regresión lineal desarrollada con **Spring Boot** y **Kotlin**. Este sistema permite a los usuarios realizar análisis estadísticos de regresión lineal de manera interactiva mediante una interfaz web moderna y funcional. La aplicación implementa el método de mínimos cuadrados para calcular la línea de mejor ajuste para conjuntos de datos bidimensionales, proporcionando visualizaciones gráficas y métricas de calidad estadística.

El proyecto demuestra la aplicación práctica de conceptos fundamentales de:
- **(1)** Desarrollo backend con arquitectura MVC utilizando Spring Boot y Kotlin
- **(2)** Implementación de algoritmos estadísticos mediante el método de mínimos cuadrados
- **(3)** Creación de interfaces web interactivas con HTML5, CSS3 y JavaScript vanilla
- **(4)** Comunicación cliente-servidor mediante APIs RESTful con serialización JSON

***

### Requerimientos previos: 
- JDK 17 o superior
- IntelliJ IDEA (recomendado) o cualquier IDE compatible
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

***

## 1. Marco Teórico: Regresión Lineal y Método de Mínimos Cuadrados

### 1.1 Fundamentos de Regresión Lineal

La **regresión lineal** es una técnica estadística fundamental utilizada para modelar la relación entre una variable dependiente $(y)$ y una o más variables independientes $(x)$. En el caso de la regresión lineal simple, se busca encontrar una línea recta que mejor se ajuste a un conjunto de puntos de datos en el plano cartesiano bidimensional.

La **ecuación general** de una línea de regresión se expresa como:

$$
y = mx + b
$$

Donde:
- $m$ representa la **pendiente** de la línea (rate of change)
- $b$ representa la **intersección** con el eje Y (valor cuando $x = 0$)
- $x$ es la variable independiente
- $y$ es la variable dependiente

<p align="center">
  <img src="attached_image:5" alt="Caso Normal - Aplicación funcionando" />
</p>

*Figura 1: Interfaz de la aplicación mostrando el cálculo de regresión lineal con visualización gráfica*

### 1.2 Método de Mínimos Cuadrados

El **método de mínimos cuadrados** es el procedimiento matemático empleado para determinar los parámetros óptimos de la línea de regresión. Este método minimiza la suma de los cuadrados de las diferencias (residuos) entre los valores observados y los valores predichos por el modelo.

La **función objetivo** a minimizar es:

$$
SSE = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \sum_{i=1}^{n} (y_i - (mx_i + b))^2
$$

Donde $SSE$ (Sum of Squared Errors) es la suma de errores cuadrados que se busca minimizar.

Las **fórmulas de cálculo** para los parámetros de la regresión son:

**Pendiente (m):**
$$
m = \frac{N \cdot \sum(x_i y_i) - \sum x_i \cdot \sum y_i}{N \cdot \sum(x_i^2) - (\sum x_i)^2}
$$

**Intersección (b):**
$$
b = \frac{\sum y_i - m \cdot \sum x_i}{N}
$$

Donde:
- $N$ es el número total de puntos de datos
- $\sum$ denota la sumatoria sobre todos los puntos
- $x_i, y_i$ son las coordenadas del i-ésimo punto

### 1.3 Coeficiente de Determinación (R²)

El **coeficiente de determinación** $R^2$ es una métrica estadística que indica qué proporción de la variabilidad en los datos es explicada por el modelo de regresión. Este valor oscila entre 0 y 1, donde:

- **$R^2 = 1.0$**: Ajuste perfecto, el modelo explica el 100% de la variabilidad
- **$R^2 = 0.0$**: El modelo no explica ninguna variabilidad
- **$0 < R^2 < 1$**: El modelo explica parcialmente la variabilidad de los datos

La **fórmula del coeficiente R²** se define como:

$$
R^2 = 1 - \frac{SS_{res}}{SS_{tot}}
$$

Donde:
- $SS_{res} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$ es la suma de cuadrados de los residuos
- $SS_{tot} = \sum_{i=1}^{n} (y_i - \bar{y})^2$ es la suma total de cuadrados
- $\bar{y}$ es la media de los valores observados

**Interpretación práctica:**
- $R^2 > 0.7$: Excelente ajuste (verde)
- $0.3 < R^2 < 0.7$: Ajuste moderado (amarillo)
- $R^2 < 0.3$: Ajuste pobre (rojo)

***

## 2. Arquitectura y Tecnologías Utilizadas

### 2.1 Stack Tecnológico

La aplicación ha sido construida utilizando un stack tecnológico moderno orientado a la JVM (Java Virtual Machine), combinando las mejores prácticas de desarrollo backend y frontend. A continuación se detallan las principales tecnologías empleadas:

#### 2.1.1 Backend Technologies

**Kotlin 1.9.21**
- Lenguaje de programación principal elegido por su **concisión sintáctica**, **seguridad de tipos nulos** (null safety), **interoperabilidad total con Java** y características funcionales modernas
- Reduce significativamente el código boilerplate comparado con Java mediante data classes, extension functions y smart casts
- Proporciona expresividad superior manteniendo compatibilidad con el ecosistema JVM

**Spring Boot 3.2.1**
- Framework empresarial de facto para desarrollo Java/Kotlin que proporciona:
  - **Configuración automática** (auto-configuration) mediante convenciones
  - **Servidor embebido** Tomcat eliminando necesidad de deployment externo
  - **Inyección de dependencias** mediante el contenedor IoC (Inversion of Control)
  - **Spring MVC** para implementación de arquitectura Modelo-Vista-Controlador
- Simplifica enormemente el desarrollo de aplicaciones web eliminando configuración XML extensa

**Thymeleaf**
- Motor de plantillas del lado del servidor que permite renderizar HTML dinámico
- Se integra naturalmente con Spring Boot mediante auto-configuration
- Permite crear vistas web que pueden ser visualizadas tanto en navegador como en modo de prototipo
- Soporta expresiones SpEL (Spring Expression Language) para manipulación de datos

**Gradle (Kotlin DSL)**
- Herramienta de automatización de construcción y gestión de dependencias
- Utiliza scripts escritos en Kotlin DSL para definir configuración del proyecto
- Gestiona descarga automática de librerías externas desde repositorios Maven Central
- Compila código Kotlin a bytecode JVM optimizado

#### 2.1.2 Frontend Technologies

**HTML5**
- Estructura semántica de la interfaz de usuario
- Validación nativa de formularios mediante atributos HTML5
- Elementos modernos como `<canvas>` para renderizado gráfico

**CSS3**
- Diseño responsivo mediante CSS Grid y Media Queries
- Efectos visuales avanzados: gradientes, sombras, transiciones
- Paleta de colores consistente con tonos púrpura/azul (#667eea, #764ba2)

**JavaScript (ES6+)**
- Lógica de interacción del usuario sin frameworks adicionales
- Comunicación asíncrona con backend mediante Fetch API
- Manipulación dinámica del DOM para actualización de resultados

**Chart.js**
- Librería JavaScript especializada en visualización de datos
- Renderizado de gráficos de dispersión (scatter plots) y líneas
- Interactividad con tooltips y responsive design automático

### 2.2 Patrón Arquitectónico: MVC (Modelo-Vista-Controlador)

La aplicación sigue el patrón arquitectónico **Modelo-Vista-Controlador (MVC)**, ampliamente utilizado en desarrollo web. Este patrón separa la lógica de negocio, la presentación de datos y el manejo de peticiones en componentes independientes y reutilizables.

<p align="center">
  <img src="attached_image:1" alt="Caso Una Variable - Error de validación" />
</p>

*Figura 2: Validación de datos - el sistema requiere al menos 2 puntos para calcular la regresión*

**Componentes de la Arquitectura MVC:**

**Modelo (Models):**
- Representan las estructuras de datos de la aplicación
- Incluyen: `DataPoint`, `RegressionRequest`, `RegressionResult`
- Encapsulan la información que fluye entre capas
- Utilizan data classes de Kotlin para inmutabilidad y métodos automáticos

**Vista (View):**
- Archivo `index.html` que constituye la interfaz de usuario
- Responsable de presentar datos de manera visual y atractiva
- Utiliza HTML, CSS y JavaScript para rendering e interacción
- Actualiza dinámicamente en respuesta a eventos del usuario

**Controlador (Controllers):**
- `RegressionController`: Maneja peticiones API REST
- `WebController`: Sirve la página HTML principal
- Gestionan peticiones HTTP, procesan entrada del usuario
- Invocan lógica de negocio y devuelven respuestas apropiadas

**Servicio (Service Layer):**
- `LinearRegressionService`: Contiene lógica de negocio principal
- Implementa algoritmos matemáticos para regresión lineal
- Desacoplado de controladores para reutilización y testing
- Marcado con @Service para inyección de dependencias

### 2.3 Estructura del Proyecto

El proyecto está organizado siguiendo las convenciones de Spring Boot y las mejores prácticas de desarrollo en Kotlin:

```
linear-regression-app/
├── src/main/kotlin/com/regresionlineal/
│   ├── Application.kt                    # Punto de entrada
│   ├── controller/
│   │   ├── RegressionController.kt       # API REST endpoints
│   │   └── WebController.kt              # Vista HTML
│   ├── models/
│   │   ├── DataPoint.kt                  # Modelo de punto (x,y)
│   │   ├── RegressionRequest.kt          # DTO de solicitud
│   │   └── RegressionResult.kt           # DTO de respuesta
│   └── service/
│       └── LinearRegressionService.kt    # Lógica de negocio
└── src/main/resources/
    ├── application.properties            # Configuración
    └── templates/
        └── index.html                    # Interfaz web
```

Esta estructura promueve:
- **Separación de responsabilidades** clara entre capas
- **Facilidad de navegación** del código
- **Escalabilidad** para añadir nuevas funcionalidades
- **Mantenibilidad** mediante organización lógica

***

## 3. Implementación del Backend: Componentes Kotlin

### 3.1 Modelos de Datos (Data Classes)

#### 3.1.1 DataPoint.kt - Representación de Puntos

La clase `DataPoint` representa un punto individual en el plano cartesiano bidimensional. Utiliza la palabra clave **`data class`** de Kotlin, que automáticamente genera métodos útiles como `equals()`, `hashCode()`, `toString()` y `copy()`.

```kotlin
package com.regresionlineal.models

/**
 * Clase de datos que representa un punto (x, y) para la regresión lineal
 */
data class DataPoint(
    val x: Double,
    val y: Double
)
```

**Características clave:**
- **Inmutabilidad**: Uso de `val` garantiza que coordenadas no puedan modificarse
- **Tipo Double**: Permite precisión en cálculos numéricos de punto flotante
- **Simplicidad**: Solo 4 líneas de código vs. ~30 en Java tradicional
- **Métodos automáticos**: Kotlin genera implementaciones optimizadas

**Propósito:**
Encapsular las coordenadas $(x, y)$ de cada punto de datos ingresado por el usuario. La inmutabilidad asegura que los datos no puedan ser modificados accidentalmente durante el procesamiento, garantizando integridad de los cálculos estadísticos.

#### 3.1.2 RegressionRequest.kt - DTO de Solicitud

Clase que encapsula la solicitud HTTP enviada desde el cliente al servidor. Contiene la lista de puntos de datos que el usuario desea analizar.

```kotlin
package com.regresionlineal.models

/**
 * Clase para recibir la solicitud con los puntos de datos
 */
data class RegressionRequest(
    val points: List<DataPoint>
)
```

**Propósito:**
Facilitar la **deserialización automática de JSON a objetos Kotlin**. Cuando el cliente envía datos en formato JSON, Spring Boot automáticamente convierte ese JSON en una instancia de `RegressionRequest` mediante Jackson, simplificando enormemente el manejo de datos y eliminando código de parsing manual.

#### 3.1.3 RegressionResult.kt - DTO de Respuesta

Clase que contiene todos los resultados del cálculo de regresión lineal que serán enviados de vuelta al cliente como respuesta.

```kotlin
package com.regresionlineal.models

/**
 * Clase de datos que contiene los resultados del cálculo de regresión lineal
 */
data class RegressionResult(
    val slope: Double,              // Pendiente (m)
    val intercept: Double,          // Intersección (b)
    val equation: String,           // Ecuación en formato y = mx + b
    val rSquared: Double,           // Coeficiente de determinación R²
    val points: List<DataPoint>     // Puntos originales
)
```

**Propósito:**
Estructurar toda la información resultante del análisis en un formato coherente y fácil de serializar a JSON. Incluye tanto los parámetros calculados (pendiente, intersección) como métricas de calidad (R²) y una representación textual legible de la ecuación. Spring Boot automáticamente convierte esta instancia a JSON para la respuesta HTTP.

### 3.2 Capa de Servicio: LinearRegressionService.kt

Esta clase constituye el **núcleo computacional** de la aplicación. Implementa el algoritmo de regresión lineal mediante el método de mínimos cuadrados. La anotación `@Service` indica a Spring Boot que esta clase es un componente gestionado que puede ser inyectado en otras clases.

#### 3.2.1 Función Principal: calculateRegression()

Esta es la función principal que orquesta todo el proceso de cálculo. Su implementación sigue estos pasos algorítmicos:

```kotlin
fun calculateRegression(points: List<DataPoint>): RegressionResult {
    // Paso 1: Validación de datos
    require(points.size >= 2) { "Se necesitan al menos 2 puntos" }
    
    val n = points.size.toDouble()
    
    // Paso 2: Cálculo de sumas necesarias
    val sumX = points.sumOf { it.x }
    val sumY = points.sumOf { it.y }
    val sumXY = points.sumOf { it.x * it.y }
    val sumX2 = points.sumOf { it.x.pow(2) }
    val sumY2 = points.sumOf { it.y.pow(2) }
    
    // Paso 3: Validación de variabilidad en X
    val xVariance = (n * sumX2 - sumX.pow(2))
    require(abs(xVariance) > 1e-10) { "Todos los valores de X son iguales" }
    
    // Paso 4: Cálculo de pendiente (m)
    val slope = (n * sumXY - sumX * sumY) / xVariance
    
    // Paso 5: Cálculo de intersección (b)
    val intercept = (sumY - slope * sumX) / n
    
    // Paso 6: Cálculo de R²
    val rSquared = calculateRSquared(points, slope, intercept, sumY, sumY2, n)
    
    // Paso 7: Formato de ecuación
    val equation = formatEquation(slope, intercept)
    
    return RegressionResult(slope, intercept, equation, rSquared, points)
}
```

**Análisis detallado de cada paso:**

**Paso 1 - Validación de datos:**
Verifica que haya al menos 2 puntos (requisito mínimo para trazar una línea). Utiliza la función `require()` de Kotlin que lanza `IllegalArgumentException` si la condición no se cumple, proporcionando manejo de errores declarativo.

<p align="center">
  <img src="attached_image:4" alt="Caso Vacío - Validación" />
</p>

*Figura 3: Estado inicial de la aplicación - requiere ingreso de datos*

**Paso 2 - Cálculo de sumas necesarias:**
Calcula $\sum x$, $\sum y$, $\sum xy$, $\sum x^2$ y $\sum y^2$ utilizando funciones de orden superior de Kotlin (`sumOf`). Estas sumas son los componentes fundamentales de las fórmulas de mínimos cuadrados.

**Paso 3 - Validación de variabilidad:**
Verifica que los valores de X no sean todos iguales calculando la varianza. Si todos los X son idénticos, la línea sería vertical (pendiente infinita), lo cual es indefinido en regresión lineal estándar.

**Paso 4 - Cálculo de la pendiente (m):**
Aplica la fórmula:
$$m = \frac{N \cdot \sum(xy) - \sum x \cdot \sum y}{N \cdot \sum(x^2) - (\sum x)^2}$$

El numerador representa la covarianza entre X e Y, mientras que el denominador representa la varianza de X.

**Paso 5 - Cálculo de la intersección (b):**
Aplica la fórmula:
$$b = \frac{\sum y - m \cdot \sum x}{N}$$

Esta fórmula asegura que la línea pase por el punto medio $(\bar{x}, \bar{y})$ de los datos.

**Paso 6 - Cálculo del coeficiente R²:**
Invoca la función privada `calculateRSquared()` que implementa la fórmula $R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$.

**Paso 7 - Formato de la ecuación:**
Genera una representación textual legible de la ecuación en formato `y = mx + b`, manejando correctamente los signos.

#### 3.2.2 Función Auxiliar: calculateRSquared()

Función privada que calcula el coeficiente de determinación:

```kotlin
private fun calculateRSquared(
    points: List<DataPoint>,
    slope: Double,
    intercept: Double,
    sumY: Double,
    sumY2: Double,
    n: Double
): Double {
    val meanY = sumY / n
    
    // Suma de cuadrados de residuos (SS_res)
    val ssRes = points.sumOf { point ->
        val predicted = slope * point.x + intercept
        (point.y - predicted).pow(2)
    }
    
    // Suma total de cuadrados (SS_tot)
    val ssTot = sumY2 - n * meanY.pow(2)
    
    // Caso especial: todos los Y son iguales
    return if (abs(ssTot) < 1e-10) 1.0 else 1.0 - (ssRes / ssTot)
}
```

**Explicación del cálculo:**

1. **Media de Y**: $\bar{y} = \frac{\sum y}{N}$
2. **SS_res**: Para cada punto, calcula el valor predicho $\hat{y} = mx + b$ y luego suma $(y - \hat{y})^2$
3. **SS_tot**: Variabilidad total $\sum(y - \bar{y})^2$
4. **R²**: $1 - \frac{SS_{res}}{SS_{tot}}$

El caso especial retorna 1.0 si todos los valores Y son idénticos (variabilidad cero).

#### 3.2.3 Función de Formato: formatEquation()

Convierte valores numéricos a una representación textual estética:

```kotlin
private fun formatEquation(slope: Double, intercept: Double): String {
    val slopeStr = String.format("%.4f", slope)
    val interceptStr = String.format("%.4f", abs(intercept))
    val sign = if (intercept >= 0) "+" else "-"
    return "y = ${slopeStr}x $sign $interceptStr"
}
```

**Ejemplo de salida:**
- `y = 2.5000x + 3.1234`
- `y = 1.2345x - 0.5678`

<p align="center">
  <img src="attached_image:2" alt="Caso Valores Extremos" />
</p>

*Figura 4: La aplicación maneja correctamente valores extremos y calcula regresiones con alta precisión*

### 3.3 Capa de Controladores

#### 3.3.1 RegressionController.kt - API REST

Controlador REST que expone endpoints de API para que el frontend pueda realizar operaciones relacionadas con la regresión lineal.

```kotlin
@RestController
@RequestMapping("/api/regression")
@CrossOrigin(origins = ["*"])
class RegressionController(
    private val regressionService: LinearRegressionService
) {
    
    @PostMapping("/calculate")
    fun calculateRegression(@RequestBody request: RegressionRequest): ResponseEntity<*> {
        return try {
            if (request.points.isEmpty()) {
                return ResponseEntity.badRequest()
                    .body(mapOf("error" to "Se requiere al menos un punto"))
            }
            
            val result = regressionService.calculateRegression(request.points)
            ResponseEntity.ok(result)
            
        } catch (e: IllegalArgumentException) {
            ResponseEntity.badRequest()
                .body(mapOf("error" to e.message))
        } catch (e: Exception) {
            ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(mapOf("error" to "Error inesperado: ${e.message}"))
        }
    }
    
    @GetMapping("/health")
    fun healthCheck(): ResponseEntity<Map<String, Any>> {
        return ResponseEntity.ok(mapOf(
            "status" to "OK",
            "service" to "Linear Regression API",
            "version" to "1.0.0"
        ))
    }
}
```

**Anotaciones clave:**

- `@RestController`: Combina `@Controller` y `@ResponseBody`, indica que retorna datos (JSON) en lugar de vistas HTML
- `@RequestMapping("/api/regression")`: Define prefijo de ruta base para todos los endpoints
- `@CrossOrigin(origins = ["*"])`: Habilita CORS permitiendo acceso desde diferentes dominios/puertos

**Endpoint POST /api/regression/calculate:**

Proceso de ejecución:
1. **Recepción**: Spring Boot deserializa JSON a `RegressionRequest` automáticamente
2. **Validación inicial**: Verifica que la lista de puntos no esté vacía
3. **Invocación del servicio**: Llama a `regressionService.calculateRegression()`
4. **Manejo de errores**: 
   - `IllegalArgumentException` → HTTP 400 (Bad Request)
   - Otras excepciones → HTTP 500 (Internal Server Error)
5. **Respuesta**: HTTP 200 (OK) con `RegressionResult` serializado a JSON

**Endpoint GET /api/regression/health:**

Endpoint de diagnóstico para verificar que el servicio está funcionando. Retorna JSON con información de estado, útil para monitoreo y pruebas de integración.

#### 3.3.2 WebController.kt - Servidor de Vistas

Controlador simple que sirve la página HTML principal:

```kotlin
@Controller
class WebController {
    
    @GetMapping("/")
    fun index(): String {
        return "index"
    }
}
```

**Diferencia con RegressionController:**
- Usa `@Controller` (no `@RestController`)
- Retorna nombre de vista (String) en lugar de datos
- Spring Boot busca `index.html` en `src/main/resources/templates/`
- Thymeleaf procesa la plantilla y renderiza HTML

### 3.4 Clase Principal: Application.kt

Punto de entrada de la aplicación Spring Boot:

```kotlin
@SpringBootApplication
class LinearRegressionApplication

fun main(args: Array<String>) {
    runApplication<LinearRegressionApplication>(*args)
}
```

**Anotación @SpringBootApplication:**
Combina tres anotaciones esenciales:
- `@Configuration`: Marca la clase como fuente de definiciones de beans
- `@EnableAutoConfiguration`: Habilita configuración automática de Spring Boot
- `@ComponentScan`: Escanea paquetes en busca de componentes (`@Controller`, `@Service`, etc.)

El operador spread `*args` desempaqueta el array para pasarlo como varargs.

### 3.5 Configuración: application.properties

Archivo de configuración que define parámetros de ejecución:

```properties
# Configuración del servidor
server.port=8080

# Configuración de Spring Boot
spring.application.name=Linear Regression App

# Configuración de logging
logging.level.root=INFO
logging.level.com.regresionlineal=DEBUG

# Configuración de Thymeleaf
spring.thymeleaf.cache=false
spring.thymeleaf.prefix=classpath:/templates/
spring.thymeleaf.suffix=.html
```

**Parámetros clave:**

- `server.port=8080`: Puerto donde el servidor embebido escucha peticiones
- `logging.level.*`: Niveles de detalle de logs (INFO general, DEBUG específico)
- `spring.thymeleaf.cache=false`: Desactiva caché durante desarrollo para ver cambios inmediatos
- `spring.thymeleaf.prefix/suffix`: Configuración de ubicación de plantillas

***

## 4. Implementación del Frontend: Interfaz Web Interactiva

### 4.1 Estructura HTML5

La interfaz de usuario está completamente contenida en el archivo `index.html` y combina HTML5, CSS3 y JavaScript vanilla (sin frameworks adicionales) para crear una experiencia interactiva y visualmente atractiva.

#### 4.1.1 Organización Semántica

```html
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Calculadora de Regresión Lineal</h1>
            <p>Desarrollado con Spring Boot + Kotlin</p>
        </div>
        
        <div class="content">
            <!-- Sección de Entrada de Datos -->
            <div class="input-section">...</div>
            
            <!-- Sección de Resultados -->
            <div class="results-section">...</div>
        </div>
    </div>
</body>
```

**Componentes principales:**

**Encabezado (Header):**
- Título principal con emoji para identificación visual rápida
- Subtítulo descriptivo indicando tecnologías utilizadas
- Degradado de color para efecto moderno

**Contenedor de Contenido:**
Utiliza **CSS Grid** para diseño de dos columnas responsivo que se adapta automáticamente a diferentes tamaños de pantalla.

### 4.2 Componentes de la Interfaz

#### 4.2.1 Sección de Entrada de Datos

```html
<div class="input-section">
    <h2>📝 Entrada de Datos</h2>
    
    <!-- Mensaje de validación -->
    <div id="errorMessage" class="error-message" style="display: none;"></div>
    <div id="successMessage" class="success-message" style="display: none;"></div>
    
    <!-- Campos de entrada -->
    <div class="input-group">
        <input type="number" id="xValue" placeholder="Valor X" step="any" required>
        <input type="number" id="yValue" placeholder="Valor Y" step="any" required>
        <button onclick="addPoint()" class="btn-primary">➕ Agregar Punto</button>
    </div>
    
    <!-- Tabla de puntos -->
    <div class="points-table">
        <table id="pointsTable">
            <thead>
                <tr>
                    <th>#</th>
                    <th>X</th>
                    <th>Y</th>
                    <th>Acción</th>
                </tr>
            </thead>
            <tbody id="pointsBody"></tbody>
        </table>
    </div>
    
    <!-- Botones de acción -->
    <button onclick="calculateRegression()" class="btn-calculate">
        🧮 Calcular Regresión
    </button>
    <button onclick="clearAll()" class="btn-secondary">🗑️ Limpiar Todo</button>
    <button onclick="loadExample()" class="btn-warning">💡 Cargar Ejemplo</button>
</div>
```

**Características:**

- **Campos de entrada**: Tipo `number` con `step="any"` para permitir decimales
- **Validación HTML5**: Atributo `required` para validación básica
- **Tabla dinámica**: Actualizada mediante JavaScript al agregar/eliminar puntos
- **Botones de acción**: Iconos emoji para mejor UX visual

#### 4.2.2 Sección de Resultados

```html
<div class="results-section">
    <h2>📊 Resultados</h2>
    
    <div id="initialMessage" class="placeholder-message">
        Ingresa al menos 2 puntos y calcula la regresión
    </div>
    
    <div id="resultsContent" style="display: none;">
        <!-- Ecuación de regresión -->
        <div class="result-box equation-box">
            <h3 id="equationResult">y = mx + b</h3>
        </div>
        
        <!-- Métricas estadísticas -->
        <div class="metrics-grid">
            <div class="metric-item">
                <label>Pendiente (m):</label>
                <span id="slopeValue">-</span>
            </div>
            <div class="metric-item">
                <label>Intersección (b):</label>
                <span id="interceptValue">-</span>
            </div>
            <div class="metric-item">
                <label>R² (Coeficiente):</label>
                <span id="rSquaredValue" class="r-squared">-</span>
            </div>
        </div>
        
        <!-- Gráfico -->
        <div class="chart-container">
            <h3>Gráfico</h3>
            <canvas id="regressionChart"></canvas>
        </div>
    </div>
</div>
```

**Elementos clave:**

- **Mensaje inicial**: Placeholder mostrado antes de calcular
- **Ecuación**: Mostrada con formato destacado
- **Grid de métricas**: Diseño organizado de resultados numéricos
- **Canvas Chart.js**: Elemento HTML5 canvas para renderizado gráfico

<p align="center">
  <img src="attached_image:3" alt="Caso Datos Inválidos" />
</p>

*Figura 5: Manejo de errores - validación cuando se ingresan caracteres no numéricos*

### 4.3 Lógica JavaScript

El código JavaScript gestiona toda la interacción del usuario y la comunicación con el backend.

#### 4.3.1 Variables Globales y Estado

```javascript
let dataPoints = [];
let regressionChart = null;
```

- `dataPoints`: Array que almacena todos los puntos ingresados
- `regressionChart`: Referencia al objeto Chart.js para actualización/destrucción

#### 4.3.2 Función addPoint() - Agregar Puntos

```javascript
function addPoint() {
    const xInput = document.getElementById('xValue');
    const yInput = document.getElementById('yValue');
    
    const x = parseFloat(xInput.value);
    const y = parseFloat(yInput.value);
    
    if (isNaN(x) || isNaN(y)) {
        showError('Por favor ingresa valores numéricos válidos');
        return;
    }
    
    dataPoints.push({ x, y });
    updatePointsTable();
    
    xInput.value = '';
    yInput.value = '';
    xInput.focus();
    
    showSuccess('Punto agregado correctamente');
}
```

**Flujo de ejecución:**
1. Captura valores de inputs
2. Convierte a números mediante `parseFloat()`
3. Valida que sean números válidos
4. Añade al array global
5. Actualiza tabla visual
6. Limpia campos y enfoca para siguiente entrada

#### 4.3.3 Función calculateRegression() - Comunicación con Backend

```javascript
async function calculateRegression() {
    if (dataPoints.length < 2) {
        showError('Se necesitan al menos 2 puntos');
        return;
    }
    
    try {
        const response = await fetch('/api/regression/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ points: dataPoints })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al calcular');
        }
        
        const result = await response.json();
        displayResults(result);
        showSuccess('Regresión calculada exitosamente');
        
    } catch (error) {
        showError(error.message);
    }
}
```

**Análisis detallado:**

**Paso 1 - Validación:** Verifica mínimo 2 puntos antes de proceder

**Paso 2 - Petición HTTP:**
- Utiliza **Fetch API** moderna (async/await)
- Método POST a `/api/regression/calculate`
- Headers: `Content-Type: application/json`
- Body: JSON serializado con `JSON.stringify()`

**Paso 3 - Manejo de respuesta:**
- Verifica `response.ok` (status 200-299)
- Si hay error, extrae mensaje del JSON de error
- Si exitoso, parsea JSON de respuesta

**Paso 4 - Visualización:**
- Llama a `displayResults()` con datos recibidos
- Muestra mensaje de éxito

**Paso 5 - Manejo de errores:**
- Bloque try-catch captura errores de red o procesamiento
- Muestra mensajes informativos al usuario

#### 4.3.4 Función displayResults() - Actualización de UI

```javascript
function displayResults(result) {
    document.getElementById('initialMessage').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'block';
    
    // Mostrar ecuación
    document.getElementById('equationResult').textContent = result.equation;
    
    // Mostrar métricas
    document.getElementById('slopeValue').textContent = result.slope.toFixed(4);
    document.getElementById('interceptValue').textContent = result.intercept.toFixed(4);
    
    // R² con color condicional
    const r2Element = document.getElementById('rSquaredValue');
    r2Element.textContent = result.rSquared.toFixed(4);
    r2Element.className = 'r-squared';
    if (result.rSquared > 0.7) {
        r2Element.classList.add('good');
    } else if (result.rSquared < 0.3) {
        r2Element.classList.add('poor');
    }
    
    // Actualizar gráfico
    updateChart(result);
}
```

**Actualizaciones realizadas:**
1. Oculta mensaje placeholder
2. Muestra sección de resultados
3. Renderiza ecuación textual
4. Muestra métricas con formato (4 decimales)
5. Aplica color al R² según calidad (verde/amarillo/rojo)
6. Invoca actualización de gráfico

#### 4.3.5 Función updateChart() - Visualización con Chart.js

```javascript
function updateChart(result) {
    const ctx = document.getElementById('regressionChart').getContext('2d');
    
    // Destruir gráfico anterior si existe
    if (regressionChart) {
        regressionChart.destroy();
    }
    
    // Preparar datos de puntos
    const scatterData = result.points.map(p => ({ x: p.x, y: p.y }));
    
    // Calcular línea de regresión
    const xValues = result.points.map(p => p.x);
    const minX = Math.min(...xValues);
    const maxX = Math.max(...xValues);
    
    const lineData = [
        { x: minX, y: result.slope * minX + result.intercept },
        { x: maxX, y: result.slope * maxX + result.intercept }
    ];
    
    // Crear gráfico
    regressionChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Puntos de Datos',
                    data: scatterData,
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    pointRadius: 6
                },
                {
                    label: 'Línea de Regresión',
                    data: lineData,
                    type: 'line',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 3,
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Variable X' } },
                y: { title: { display: true, text: 'Variable Y' } }
            }
        }
    });
}
```

**Proceso de renderizado:**

1. **Destrucción**: Elimina gráfico previo para evitar superposiciones
2. **Preparación de datos**: Convierte puntos a formato Chart.js
3. **Cálculo de línea**: Determina puntos extremos usando ecuación $y = mx + b$
4. **Configuración de datasets**:
   - Dataset 1: Puntos originales (scatter, azul)
   - Dataset 2: Línea de regresión (line, roja)
5. **Opciones**: Responsividad, títulos de ejes, tooltips

### 4.4 Diseño Visual (CSS3)

Los estilos CSS crean una interfaz moderna y atractiva:

#### 4.4.1 Características de Diseño

**Gradientes:**
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**Sombras y Profundidad:**
```css
.container {
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
```

**Transiciones Suaves:**
```css
button {
    transition: all 0.3s ease;
}

.metric-item {
    transition: transform 0.2s ease;
}
```

**Diseño Responsivo:**
```css
@media (max-width: 768px) {
    .content {
        grid-template-columns: 1fr;
    }
}
```

***

## 5. Flujo de Datos y Comunicación Cliente-Servidor

### 5.1 Diagrama de Flujo Completo

El siguiente diagrama conceptual describe el flujo completo de datos desde que el usuario ingresa información hasta que visualiza los resultados:

```
1. Usuario ingresa punto (x, y)
   ↓
2. JavaScript captura y almacena en array
   ↓
3. Usuario presiona "Calcular Regresión"
   ↓
4. JavaScript serializa datos a JSON
   ↓
5. Petición HTTP POST al backend
   ↓
6. RegressionController recibe petición
   ↓
7. Spring Boot deserializa JSON a RegressionRequest
   ↓
8. Validación de datos
   ↓
9. Invocación de LinearRegressionService
   ↓
10. Cálculo matemático (mínimos cuadrados)
    ↓
11. Cálculo de R²
    ↓
12. Creación de RegressionResult
    ↓
13. Spring Boot serializa a JSON
    ↓
14. Respuesta HTTP al cliente
    ↓
15. JavaScript parsea JSON
    ↓
16. Actualización del DOM
    ↓
17. Renderizado del gráfico Chart.js
    ↓
18. Usuario visualiza resultados
```

### 5.2 Formato de Comunicación JSON

#### 5.2.1 Request (Cliente → Servidor)

```json
{
  "points": [
    {"x": 1.0, "y": 2.0},
    {"x": 2.0, "y": 4.0},
    {"x": 3.0, "y": 5.0},
    {"x": 4.0, "y": 4.0},
    {"x": 5.0, "y": 5.0}
  ]
}
```

#### 5.2.2 Response (Servidor → Cliente)

```json
{
  "slope": 0.6000,
  "intercept": 2.2000,
  "equation": "y = 0.6000x + 2.2000",
  "rSquared": 0.6000,
  "points": [
    {"x": 1.0, "y": 2.0},
    {"x": 2.0, "y": 4.0},
    {"x": 3.0, "y": 5.0},
    {"x": 4.0, "y": 4.0},
    {"x": 5.0, "y": 5.0}
  ]
}
```

#### 5.2.3 Error Response

```json
{
  "error": "Se necesitan al menos 2 puntos para calcular la regresión lineal"
}
```

***

## 6. Guía del Usuario: Instalación y Uso

### 6.1 Requisitos del Sistema

**Software necesario:**
- **JDK 17 o superior**: Java Development Kit para compilar y ejecutar código Kotlin
- **IntelliJ IDEA**: IDE recomendado (Community o Ultimate Edition)
- **Navegador web moderno**: Chrome, Firefox, Edge o Safari actualizado
- **Conexión a internet**: Solo para descarga inicial de dependencias Gradle

### 6.2 Instalación y Configuración

#### Paso 1: Abrir el Proyecto
1. Inicie IntelliJ IDEA
2. Seleccione `File → Open`
3. Navegue hasta la carpeta del proyecto `linear-regression-app`
4. Haga clic en `OK` para abrir el proyecto

#### Paso 2: Sincronización de Gradle
1. Al abrir el proyecto, IntelliJ detectará que es un proyecto Gradle
2. Aparecerá una notificación solicitando "Load Gradle Changes"
3. Haga clic en "Load Gradle Changes" o en el ícono de sincronización (🔄)
4. Espere 3-5 minutos mientras Gradle descarga dependencias
5. La barra de progreso en la parte inferior mostrará el estado

#### Paso 3: Verificación del JDK
1. Vaya a `File → Project Structure → Project`
2. Verifique que el SDK del proyecto sea JDK 17 o superior
3. Si no está configurado, seleccione o descargue un JDK apropiado

#### Paso 4: Ejecutar la Aplicación
1. En el explorador de proyectos, navegue a:
   `src/main/kotlin/com/regresionlineal/Application.kt`
2. Abra el archivo `Application.kt`
3. Localice el ícono de triángulo verde (▶) junto a `fun main`
4. Haga clic en el triángulo y seleccione "Run LinearRegressionApplication"
5. La consola mostrará logs de inicio de Spring Boot
6. Espere el mensaje: `Started LinearRegressionApplication in X seconds`

#### Paso 5: Acceder a la Interfaz Web
1. Abra su navegador web preferido
2. Navegue a: `http://localhost:8080`
3. La interfaz de la aplicación debería cargarse inmediatamente
4. Si el puerto 8080 está ocupado, modifique `application.properties`

### 6.3 Uso de la Aplicación

#### Paso 1: Ingresar Datos
1. Localice los campos de entrada "Valor X" y "Valor Y"
2. Ingrese un valor numérico para X (puede incluir decimales)
3. Ingrese el valor correspondiente para Y
4. Presione "➕ Agregar Punto" o simplemente presione Enter
5. El punto aparecerá en la tabla de datos
6. Repita hasta tener al menos 2 puntos (recomendado: 5 o más)

#### Paso 2: Usar Datos de Ejemplo (Opcional)
1. Haga clic en "💡 Cargar Ejemplo"
2. Se cargarán automáticamente varios puntos de datos
3. Útil para ver la aplicación en acción rápidamente

#### Paso 3: Gestionar Puntos Individuales
1. En la tabla, cada fila tiene un botón "✖" a la derecha
2. Haga clic para eliminar un punto específico si cometió un error
3. La tabla se actualizará automáticamente

#### Paso 4: Calcular la Regresión
1. Con al menos 2 puntos ingresados
2. Haga clic en "🧮 Calcular Regresión"
3. La aplicación enviará datos al servidor
4. Los resultados aparecerán en la sección derecha

#### Paso 5: Interpretar Resultados
- **Ecuación**: Fórmula $y = mx + b$ con valores calculados
- **Pendiente (m)**: Cuánto aumenta Y por cada unidad de X
- **Intersección (b)**: Valor de Y cuando X = 0
- **R²**:
  - Cercano a 1.0 (verde): Excelente ajuste
  - Entre 0.3-0.7 (amarillo): Ajuste moderado
  - Cercano a 0 (rojo): Ajuste pobre
- **Gráfico**: Puntos azules (datos originales) + línea roja (regresión)

#### Paso 6: Limpiar y Comenzar de Nuevo
1. Haga clic en "🗑️ Limpiar Todo"
2. Esto eliminará todos los puntos, resultados y gráfico
3. La aplicación estará lista para un nuevo análisis

### 6.4 Consejos de Uso

✅ **Mejores prácticas:**
- Ingrese al menos 5-10 puntos para resultados más confiables
- Datos con relación lineal fuerte producen R² más altos
- Verifique que haya ingresado al menos 2 puntos
- Asegúrese que los valores de X no sean todos idénticos
- Los valores ingresados deben ser números válidos
- El gráfico es interactivo: pase el mouse sobre puntos para ver coordenadas

### 6.5 Solución de Problemas Comunes

**Problema: El puerto 8080 está en uso**
- **Solución**: Modifique `application.properties` y cambie `server.port=8080` a otro puerto disponible (8081, 9090, etc.)

**Problema: Error "Cannot resolve symbol" en IntelliJ**
- **Solución**: Asegúrese que Gradle completó la sincronización. Intente `File → Invalidate Caches / Restart`

**Problema: La página no carga en el navegador**
- **Solución**: Verifique que la aplicación esté corriendo (revise consola de IntelliJ). Confirme URL correcta. Limpie caché del navegador.

**Problema: "Error al calcular la regresión"**
- **Solución**: Asegúrese de tener al menos 2 puntos con valores de X diferentes. Verifique que los números ingresados sean válidos.

***

## 7. Casos de Prueba y Validación

### 7.1 Caso Normal: Funcionamiento Estándar

<p align="center">
  <img src="attached_image:5" alt="Caso Normal" />
</p>

*Figura 6: Caso de uso normal - 5 puntos con relación lineal, R² = 0.6000*

**Datos de entrada:**
- (1, 2), (2, 4), (3, 5), (4, 4), (5, 5)

**Resultados:**
- Ecuación: $y = 0.6000x + 2.2000$
- R²: 0.6000 (ajuste moderado)

### 7.2 Caso Validación: Menos de 2 Puntos

<p align="center">
  <img src="attached_image:1" alt="Caso Una Variable" />
</p>

*Figura 7: Validación - error cuando hay menos de 2 puntos*

**Comportamiento:**
Sistema valida y previene cálculo con datos insuficientes

### 7.3 Caso Extremo: Valores Grandes

<p align="center">
  <img src="attached_image:2" alt="Caso Valores Extremos" />
</p>

*Figura 8: Manejo de valores extremos - la aplicación calcula correctamente regresiones con números grandes*

**Datos de entrada:**
- (2345434, 45234324), (45333, 532423), (52423, 53434)

**Resultados:**
- Ecuación: $y = 19.5684x - 663059.8121$
- R²: 0.9999 (ajuste casi perfecto)

### 7.4 Caso Error: Datos Inválidos

<p align="center">
  <img src="attached_image:3" alt="Caso Datos Inválidos" />
</p>

*Figura 9: Validación de tipos - el sistema rechaza caracteres no numéricos*

**Comportamiento:**
Validación en tiempo real que previene entrada de caracteres no numéricos

### 7.5 Caso Inicial: Estado Vacío

<p align="center">
  <img src="attached_image:4" alt="Caso Vacío" />
</p>

*Figura 10: Estado inicial de la aplicación sin datos ingresados*

**Comportamiento:**
Interfaz limpia esperando entrada del usuario con mensaje instructivo

***

## 8. Conclusiones y Análisis Final

### 8.1 Logros del Proyecto

La aplicación web de regresión lineal presentada en este documento representa una **implementación completa y funcional** de un sistema de análisis estadístico moderno. A través de la integración de Kotlin, Spring Boot y tecnologías web estándar, se ha logrado crear una herramienta que es simultáneamente potente, fácil de usar y educativa.

**Aspectos destacados:**

1. **Arquitectura limpia y mantenible**: La separación clara de responsabilidades entre modelos, controladores y servicios siguiendo el patrón MVC hace que el código sea fácil de entender, mantener y extender.

2. **Implementación matemática rigurosa**: Los algoritmos de mínimos cuadrados y cálculo de R² siguen estándares estadísticos establecidos, garantizando resultados precisos y confiables para análisis de datos.

3. **Experiencia de usuario intuitiva**: La interfaz gráfica permite a usuarios sin conocimientos técnicos profundos realizar análisis de regresión de manera sencilla mediante una interfaz visual clara.

4. **Tecnologías modernas**: El uso de Kotlin y Spring Boot demuestra las capacidades de las herramientas actuales para desarrollo rápido de aplicaciones web robustas con código conciso.

5. **Visualización efectiva**: La integración de Chart.js proporciona representaciones gráficas que facilitan la comprensión de los resultados numéricos, haciendo el análisis más accesible.

6. **Validación robusta**: El sistema incluye múltiples capas de validación tanto en frontend como backend, garantizando integridad de datos y manejo apropiado de errores.

### 8.2 Ventajas de las Tecnologías Utilizadas

**Kotlin + Spring Boot:**
- Código conciso y expresivo (50-70% menos código que Java tradicional)
- Seguridad de tipos nulos evitando NullPointerException
- Inyección de dependencias automática
- Configuración por convención eliminando XML
- Servidor embebido simplificando deployment

**JavaScript Vanilla + Chart.js:**
- Sin dependencias de frameworks pesados (React, Angular)
- Rendimiento óptimo en navegadores modernos
- Visualizaciones profesionales con mínimo código
- Interactividad nativa del navegador

### 8.3 Posibles Extensiones Futuras

El proyecto es altamente **extensible** y podría incorporar funcionalidades adicionales:

1. **Regresión múltiple**: Soporte para múltiples variables independientes
2. **Exportación de datos**: Generar informes PDF o CSV con resultados
3. **Análisis estadístico avanzado**: Intervalos de confianza, pruebas de hipótesis
4. **Persistencia de datos**: Guardar análisis en base de datos
5. **Comparación de modelos**: Evaluar diferentes tipos de regresión
6. **API REST completa**: CRUD de análisis guardados
7. **Autenticación**: Sistema de usuarios con análisis privados
8. **Regresión polinomial**: Ajuste de curvas de mayor grado

### 8.4 Aplicaciones Prácticas

Este sistema puede ser utilizado en diversos contextos:

- **Educación**: Enseñanza de estadística y análisis de datos
- **Investigación científica**: Análisis preliminar de datos experimentales
- **Negocios**: Predicción de tendencias y análisis de ventas
- **Ingeniería**: Calibración de sensores y análisis de mediciones
- **Economía**: Modelado de relaciones entre variables económicas

### 8.5 Reflexión Final

Este proyecto no solo cumple con los requisitos técnicos de una aplicación de regresión lineal, sino que también sirve como un **excelente ejemplo** de cómo construir aplicaciones web modernas siguiendo las mejores prácticas de ingeniería de software. La combinación de tecnologías backend robustas (Spring Boot + Kotlin) con frontend interactivo (HTML5 + JavaScript + Chart.js) demuestra la potencia y versatilidad de las herramientas actuales de desarrollo.

La aplicación es **mantenible**, **escalable** y **educativa**, representando una base sólida sobre la cual se pueden construir sistemas más complejos de análisis estadístico y visualización de datos.

---

## Referencias y Recursos Adicionales

### Documentación Oficial
- Spring Boot: https://spring.io/projects/spring-boot
- Kotlin: https://kotlinlang.org/docs/home.html
- Chart.js: https://www.chartjs.org/docs/latest/
- Thymeleaf: https://www.thymeleaf.org/documentation.html

### Conceptos Estadísticos
- Método de Mínimos Cuadrados: https://en.wikipedia.org/wiki/Least_squares
- Coeficiente de Determinación: https://en.wikipedia.org/wiki/Coefficient_of_determination
- Regresión Lineal: https://www.stat.yale.edu/Courses/1997-98/101/linreg.htm

---
