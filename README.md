# Calculadora con Sucesor/Predecesor (Haskell)

## Autor  
**Andrés Sebastián Coral Vallejo** 

---

## Descripción
Programa didáctico en **Haskell** que implementa operaciones aritméticas básicas usando las funciones **sucesor** y **predecesor** como bloques constructores:

- Suma de enteros (usando sucesor repetido).  
- Multiplicación (como suma repetida).  
- Resta (usando predecesor repetido).  
- División entera (restas repetidas para contar el cociente).  
- Suma de números reales (implementada directamente con `+`).

Incluye una interfaz de consola con menú, validación de entrada y limpieza de pantalla según el sistema operativo.
En el programa se omitió el uso de las tildes para evitar problemas con la visualización en algunas consolas.
---

## Funciones principales
- `sucesor :: Int -> Int` — devuelve `n + 1`.  
- `predecesor :: Int -> Int` — devuelve `n - 1`.  
- `add :: Int -> Int -> Int` — suma `a` y `b` aplicando `sucesor` `b` veces a `a`.  
- `multiplicar :: Int -> Int -> Int` — suma repetida de `a` `b` veces.  
- `restar :: Int -> Int -> Int` — aplica `predecesor` `b` veces a `a`.  
- `dividir :: Int -> Int -> Int` — devuelve el **cociente entero** de `a` ÷ `b` mediante restas repetidas. *(Actualmente lanza `error` si el divisor es `0`.)*  
- `addReal :: Double -> Double -> Double` — suma directa de reales.  

---

## Interfaz y formato
- Menú interactivo con opciones (sumar, multiplicar, restar, dividir, sumar reales, salir).  

- **Prompts exactos** para entrada de datos:
  - `Digite el dato a : `
  - `Digite el dato b : `
  - `Digite el dato x : `
  - `Digite el dato y : `

- Validación de entradas:
  - Enteros: `Int >= 0` (o `> 0` para divisor).  
  - Reales: `Double`.  
  - Mensajes de error piden reintentar si la entrada es inválida.
- Tras mostrar el resultado se solicita:
  ```
  Escribe 'salir' para salir o presiona Enter para volver al menu:
  ```
  — el usuario decide si vuelve al menú o finaliza.

---

## Limpieza de pantalla y detección de SO
- Se detecta el sistema operativo con `System.Info.os`.  
  - `esWindows :: Bool` comprueba prefijos (`"mingw"`, `"cygwin"`, `"win"`).  
- `limpiarPantalla :: IO ()` ejecuta:
  - `cls` en Windows, o  
  - `clear` en Linux/Mac,  
  mediante `System.Process.callCommand`.  

Consulté como hacerlo a traves de: https://stackoverflow.com/questions/2472391/how-do-i-clear-the-terminal-screen-in-haskell
---