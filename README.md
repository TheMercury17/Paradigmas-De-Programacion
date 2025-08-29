# RNA con wolfram: Simulación de compuertas lógicas (Wolfram Language)

## Autor  
**Andrés Sebastián Coral Vallejo** 

---

## Descripción

Este proyecto contiene una *notebook* de Wolfram/Mathematica que entrena redes neuronales muy simples para emular las compuertas lógicas **AND**, **OR** y **XOR**, y además simula señales de pulso en el tiempo para ver cuándo la compuerta se "activa".

---

## Requisitos

- Wolfram Mathematica o Wolfram Engine.
- No se requieren librerías externas.
- Se puede ejecutar muy facil desde wolframcloud (Lo programé desde ahí)

---

## Estructura del notebook

- **Definición y entrenamiento de redes**: funciones que crean y entrenan redes para AND/OR/XOR.
- **Simulación de pulsos**: función que recibe dos listas de 0/1 (A y B) y muestra una tabla por instante de tiempo, junto con gráficos de entradas y salida (valor continuo y binario).
- **Ejemplos**: patrones de pulso predefinidos y llamadas de ejemplo para ejecutar las simulaciones.

---

## Cómo ejecutar

1. Abre `Simulacion de compuertas.nb` en Mathematica.
2. Evalúa todas las celdas (por ejemplo, `Evaluation -> Evaluate Notebook`).
3. Opcional: ejecuta las celdas de ejemplo más abajo para entrenar las redes y correr las simulaciones.

---

## Funciones principales (resumen rápido)

- `CreateAndTrainGate[gate, hiddenNeurons, maxRounds, learningRate]`
  - `gate`: "AND", "OR" o "XOR" (string)
  - `hiddenNeurons`: número de neuronas en la capa oculta (útil para XOR)
  - `maxRounds`: número máximo de rondas/epochs de entrenamiento
  - `learningRate`: tasa de aprendizaje (ADAM)
  - Devuelve la red neuronal entrenada.

- `SimulateGatePulses[trainedNet, sigA, sigB, title, threshold]`
  - `trainedNet`: red entrenada (valor devuelto por `CreateAndTrainGate`).
  - `sigA`, `sigB`: listas de 0/1 de la misma longitud que representan pulsos en el tiempo.
  - `title`: título impreso en los resultados (opcional).
  - `threshold`: umbral para convertir la salida continua en binaria (por defecto `0.5`).
  - Muestra tabla y gráficos; devuelve una asociación con los resultados.

---

## Parámetros que se pueden cambiar (para experimentar)

- **`hiddenNeurons`**: Aumentar si la red no aprende bien (XOR suele necesitar >=2).
- **`maxRounds`**: Más rondas permiten un aprendizaje más profundo (p. ej. 200, 400).
- **`learningRate`**: Ajustar la velocidad de convergencia (p. ej. `0.01`).
- **Listas de pulsos (`sigA`, `sigB`)**: Modificar la longitud y la posición de los `1` para simular distintos patrones.
- **`threshold`** en `SimulateGatePulses`: Ajustar el nivel a partir del cual la salida se considera "activa" (útil si la salida no es exactamente 0/1).

---

## Salida esperada

Para cada simulación, el notebook imprimirá:

- Un título con el nombre de la compuerta y la simulación.
- Una tabla con filas por instante de tiempo: (t, A, B, salida continua, salida binaria).
- Una Gráfica explicativa del fucionamiento.

Esto permite ver de forma visual cuándo la compuerta "se activa" (salida cercana a 1) según los pulsos.
