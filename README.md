# Segundo Parcial Paradigmas de Programación

## Autor

**Andrés Sebastián Coral Vallejo**

## Introducción

El presente informe documenta la implementación completa del segundo parcial de Paradigmas de Programación, enfocados en el desarrollo de sistemas basados en el paradigma de agentes utilizando el framework Mesa de Python. Ambas implementaciones demuestran la aplicación práctica de conceptos avanzados de programación multiagente, donde entidades autónomas colaboran para resolver problemas complejos de manera distribuida.

Los proyectos desarrollados incluyen:
- (1) un sistema de simulación de perceptrón neuronal para clasificación binaria de datos linealmente separables.
- (2) una calculadora distribuida donde cada operación aritmética es gestionada por agentes especializados que se comunican entre sí para resolver expresiones matemáticas complejas.
- (3) una calculadora científica

***
### Requerimientos previos: `pip install mesa==0.8.9 numpy matplotlib tk`

## 1. Modelamiento de un Perceptrón usando el Paradigma de Agentes

### 1.1 Diseño Arquitectónico del Sistema

El sistema de perceptrón basado en agentes implementa una arquitectura modular donde cada componente cumple un rol específico en el proceso de aprendizaje automático. La arquitectura se fundamenta en tres tipos principales de agentes que interactúan dentro del framework Mesa para simular el comportamiento de una red neuronal simple.

![Arquitectura del sistema de perceptrón basado en agentes](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/764475a09eb25e1e4a0e79691d7b2f2c/023394fd-e1eb-4f9e-b79f-2edb06890de1/afb56f12.png)

Arquitectura del sistema de perceptrón basado en agentes

La **arquitectura del sistema** se estructura en cuatro niveles jerárquicos: la interfaz de usuario (**PerceptronUserInterface**) que maneja la interacción con el usuario y la visualización, el modelo coordinador (**PerceptronSimulationModel**) que gestiona la simulación global, el agente neuronal (**NeuralPerceptronAgent**) que implementa el algoritmo de aprendizaje, y múltiples agentes de datos (**PointDataAgent**) que representan los puntos de entrenamiento en el espacio bidimensional.

### 1.2 Implementación de Agentes Especializados

#### 1.2.1 Agente de Punto de Datos (PointDataAgent)

El **PointDataAgent** representa cada punto de datos en el espacio de características bidimensional. Cada instancia mantiene sus coordenadas cartesianas $(x, y)$, su etiqueta de clase verdadera $(-1 \text{ o } +1)$, y su estado de clasificación actual. La implementación incluye un sistema de colorización dinámica que actualiza visualmente el estado de cada punto según la correctitud de su clasificación.

```python
def refresh_classification(self, prediction):
    self.predicted_class = prediction
    self.is_correct = (self.class_label == prediction)
    if self.is_correct:
        self.display_color = 'lightgreen' if self.class_label == -1 else 'lightcoral'
    else:
        self.display_color = 'darkblue' if self.class_label == -1 else 'darkred'
```

Este agente implementa un mecanismo de retroalimentación visual que permite identificar instantáneamente qué puntos están siendo clasificados correctamente durante el proceso de entrenamiento, facilitando el análisis del comportamiento del perceptrón.[^2]

#### 1.2.2 Agente Perceptrón Neural (NeuralPerceptronAgent)

El **NeuralPerceptronAgent** constituye el núcleo del sistema de aprendizaje automático. Implementa el algoritmo clásico del perceptrón de Rosenblatt con la regla de actualización de pesos basada en el error de clasificación. El agente mantiene un vector de pesos $\mathbf{w} = [w_1, w_2]$ y un término de sesgo $b$, todos inicializados aleatoriamente en el rango $[-1, 1]$.

La **función de activación** se define como:

$$
f(x) = \begin{cases} 
+1 & \text{si } \mathbf{w}^T\mathbf{x} + b \geq 0 \\
-1 & \text{si } \mathbf{w}^T\mathbf{x} + b < 0 
\end{cases}
$$

La **regla de actualización de pesos** se implementa según la fórmula:

$$
\mathbf{w}_{nuevo} = \mathbf{w}_{anterior} + \eta \cdot e \cdot \mathbf{x}
$$

$$
b_{nuevo} = b_{anterior} + \eta \cdot e
$$

donde $\eta$ es la tasa de aprendizaje y $e = y_{verdadero} - y_{predicho}$ es el error de clasificación.

### 1.3 Generación de Datos y Separabilidad Lineal

El sistema genera automáticamente conjuntos de datos linealmente separables mediante la definición de una línea de separación aleatoria. El algoritmo crea una función lineal $y = mx + c$ con pendiente y intercepto aleatorios, y asigna etiquetas a los puntos según su posición relativa respecto a esta línea.

### 1.4 Visualización y Interface Gráfica

La interfaz gráfica implementa controles interactivos incluyendo sliders para la **tasa de aprendizaje** (0.01-1.0) y el **número máximo de iteraciones** (10-500). El sistema proporciona visualización en tiempo real del proceso de entrenamiento mediante dos gráficos simultáneos: el espacio de características mostrando los puntos de datos con codificación de color según su estado de clasificación, y un gráfico de evolución del error total a lo largo de las épocas de entrenamiento.

![Simulación del perceptrón en entrenamiento con puntos de datos y frontera de decisión](https://user-gen-media-assets.s3.amazonaws.com/seedream_images/1b4f0343-91c8-4b35-93ec-649c3a92af17.png)

Simulación del perceptrón en entrenamiento con puntos de datos y frontera de decisión

### 1.5 Métricas de Desempeño y Convergencia

El sistema implementa múltiples métricas de evaluación del aprendizaje. El **error de clasificación total** se calcula como la suma de errores absolutos en cada época. La **convergencia** se determina cuando el error total alcanza cero o se alcanza el número máximo de iteraciones. Adicionalmente, el sistema rastrea la evolución de los pesos y el sesgo, proporcionando información detallada sobre la dinámica del aprendizaje.

***

## 2. Implementación de una Calculadora Basada en el Paradigma de Agentes

### 2.1 Arquitectura Distribuida Multi-Agente

La calculadora distribuida implementa una arquitectura sofisticada donde cada operación aritmética es gestionada por un agente especializado autónomo. El sistema utiliza un paradigma de **computación distribuida** donde la resolución de expresiones matemáticas complejas emerge de la colaboración entre múltiples agentes que se comunican a través de un sistema de mensajería asíncrona.

![Arquitectura del sistema de calculadora distribuida basada en agentes](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/764475a09eb25e1e4a0e79691d7b2f2c/2b245bf4-9c2c-419d-8166-2e26b20e6b36/afb56f12.png)

Arquitectura del sistema de calculadora distribuida basada en agentes

La **arquitectura del sistema** comprende siete agentes especializados que operan de manera coordinada: el **InputOutputAgent** (ID: 0) maneja la interfaz con el usuario, el **MathematicalParserAgent** (ID: 1) realiza análisis sintáctico y coordinación, y cinco **SpecializedOperationAgents** (IDs: 2-6) ejecutan operaciones específicas (suma, resta, multiplicación, división y potenciación). Todos los agentes se comunican a través del **InterAgentMessageQueue**, un sistema centralizado de mensajería que garantiza la entrega ordenada y trazable de mensajes.

### 2.2 Sistema de Comunicación Inter-Agente

#### 2.2.1 Mensajería Asíncrona

El sistema implementa un protocolo de comunicación basado en mensajes encapsulados que incluyen metadatos completos para trazabilidad y control de flujo. Cada mensaje contiene información sobre el agente origen, destino, categoría, carga útil y timestamp de creación.

```python
class CommunicationMessage:
    def __init__(self, origin_agent, destination_agent, message_category, payload, creation_time=None):
        self.origin_agent = origin_agent
        self.destination_agent = destination_agent
        self.message_category = message_category
        self.payload = payload
        self.creation_time = creation_time or time.time()
        self.is_processed = False
```


#### 2.2.2 Cola de Mensajes Distribuida

El **InterAgentMessageQueue** implementa un sistema de cola FIFO (First In, First Out) que mantiene un buffer de mensajes activos y un log histórico completo de todas las comunicaciones. Este diseño permite tanto el procesamiento eficiente de mensajes pendientes como el análisis posterior del flujo de comunicación para propósitos de debugging y optimización.

### 2.3 Análisis Sintáctico y Conversión Postfija

#### 2.3.1 Algoritmo Shunting Yard

El **MathematicalParserAgent** implementa el algoritmo Shunting Yard para convertir expresiones en notación infija a notación postfija (RPN - Reverse Polish Notation). Este algoritmo maneja correctamente la precedencia de operadores y el agrupamiento con paréntesis.

La **tabla de precedencia** se define como:

- Exponenciación (^): Precedencia 3
- Multiplicación (*) y División (/): Precedencia 2
- Suma (+) y Resta (-): Precedencia 1


#### 2.3.2 Evaluación Distribuida

Una vez convertida la expresión a notación postfija, el sistema evalúa cada operación de manera distribuida. Para cada operador encontrado, el parser determina el agente especializado correspondiente y envía una solicitud de operación con los operandos apropiados.

### 2.4 Agentes de Operación Especializados

Cada **SpecializedOperationAgent** se inicializa con una función matemática específica y mantiene un contador de operaciones realizadas. Los agentes implementan manejo robusto de errores, incluyendo la detección de divisiones por cero y overflow numérico.

```python
def compute_operation(self, operation_data):
    try:
        computation_result = self.mathematical_function(first_value, second_value)
    except Exception:
        computation_result = float('inf')  # Manejo de errores
```


### 2.5 Interface Gráfica y Visualización de Comunicación

La interfaz gráfica proporciona tres componentes principales: un panel de entrada para expresiones matemáticas, un área de visualización de resultados, y un registro detallado de comunicación inter-agente que muestra el flujo completo de mensajes durante la evaluación.

![Interfaz de calculadora distribuida mostrando comunicación entre agentes](https://user-gen-media-assets.s3.amazonaws.com/seedream_images/04f0a28e-f5b2-4386-8330-1e91fd257ce6.png)

Interfaz de calculadora distribuida mostrando comunicación entre agentes

El **registro de comunicación** muestra cada intercambio de mensajes con información detallada incluyendo agentes participantes, tipo de mensaje, operaciones específicas y resultados intermedios. Esto proporciona transparencia completa del proceso de cálculo distribuido y facilita la comprensión del comportamiento del sistema.

### 2.6 Métricas del Sistema y Estadísticas

El sistema rastrea métricas de desempeño incluyendo el número total de mensajes intercambiados y operaciones ejecutadas. Estas estadísticas proporcionan insights sobre la eficiencia del algoritmo de comunicación y la carga de trabajo distribuida entre los agentes especializados.

***

## 3. Implementación de una Calculadora Científica usando el Paradigma de Objetos en Kotlin

*Esta sección se desarrollará en una fase posterior del proyecto según las instrucciones recibidas.*

***

## Conclusiones

Las implementaciones desarrolladas demuestran la viabilidad y elegancia del paradigma de agentes para resolver problemas complejos de manera distribuida. El sistema de perceptrón ilustra cómo los agentes pueden colaborar en tareas de aprendizaje automático, mientras que la calculadora distribuida muestra la potencia de la descomposición funcional en sistemas multiagente.

Ambos sistemas exhiben **propiedades emergentes** características de los sistemas multiagente: comportamientos complejos que surgen de la interacción entre agentes simples. La modularidad inherente de la arquitectura basada en agentes facilita la mantenibilidad, extensibilidad y escalabilidad de las soluciones implementadas.

Las interfaces gráficas desarrolladas no solo proporcionan funcionalidad operativa sino también **transparencia algorítmica**, permitiendo a los usuarios observar y comprender los procesos internos de comunicación y coordinación entre agentes. Esta característica es especialmente valiosa para propósitos educativos y de investigación en el campo de los sistemas distribuidos inteligentes.

