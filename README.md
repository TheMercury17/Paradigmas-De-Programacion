# Trabajo en clase - Algoritmos en Kotlin.

## Autor  
**Andrés Sebastián Coral Vallejo.** 

---

- 1) Algoritmo de número primo.
- 2) Algoritmo de Euclides `Maximo común divisor (#1,#2)`
- 3) Algoritmo factorial.
- 4) Algoritmo de busqueda en profundidad `(DFS)`

---

## 1) Algoritmo de número primo.

### Idea / algoritmo
Se usa **división por prueba (trial division)**: para saber si `num` es primo, probamos dividir `num` por todos los enteros `i` desde `2` hasta `√num`.  
Si **ninguno** divide exactamente, entonces `num` es primo; si **alguno** divide, no es primo.

**Justificación:**  
Si `num = x * y` y ambos `x,y > 1`, entonces uno de ellos debe ser ≤ `√num`. Si no hay divisor ≤ `√num`, no puede existir factor no trivial.

### Código
```kotlin
fun esPrimo(num: Int): Boolean {
    if (num <= 1) return false
    for (i in 2..Math.sqrt(num.toDouble()).toInt()) {
        if (num % i == 0) return false
    }
    return true
}
````

### Complejidad

* Tiempo: O(√n)
* Espacio: O(1)

### Casos borde

* `num <= 1` → no primo.
* `num = 2` → primo.
* Números grandes → puede volverse lento.

### Ejemplo

Para `num = 29`: divisores probados `2..5`. Ninguno divide → **29 es primo**.


---

## 2) Algoritmo de Euclides `Maximo común divisor (#1,#2)`

### Idea / algoritmo

Basado en la propiedad:

```
gcd(a, b) = gcd(b, a mod b)
gcd(a, 0) = a
```

### Código

```kotlin
fun mcd(a: Int, b: Int): Int {
    return if (b == 0) a else mcd(b, a % b)
}
```

### Complejidad

* Tiempo: O(log min(a, b))
* Espacio: O(log min(a, b)) por recursión.

### Ejemplo

Para `a = 56, b = 98`:

* gcd(56, 98) → gcd(98, 56)
* gcd(98, 56) → gcd(56, 42)
* gcd(56, 42) → gcd(42, 14)
* gcd(42, 14) → gcd(14, 0) → **14**

### Casos borde

* `gcd(a, 0) = |a|`
* Manejar negativos usando `abs`.


---

## 3) Algoritmo factorial.

### Idea / algoritmo

Definición recursiva:

```
0! = 1
n! = n * (n-1)!  (para n > 0)
```

### Código

```kotlin
fun factorial(n: Int): Long {
    return if (n == 0) 1 else n * factorial(n - 1)
}
```

### Complejidad

* Tiempo: O(n)
* Espacio: O(n) por recursión.

### Casos borde

* `n < 0` → recursión infinita (se debe validar).
* Overflow: `Long` se desborda a partir de `21!`.

### Ejemplo

Para `n = 5`: 5 × 4 × 3 × 2 × 1 = **120**.

---

## 4) Algoritmo de busqueda en profundidad `(DFS)`

### Idea / algoritmo

Explora los nodos en profundidad primero, antes de retroceder. Se usa un conjunto `visitados` para evitar ciclos infinitos.

### Código

```kotlin
fun dfs(grafo: Map<Int, List<Int>>, nodo: Int, visitados: MutableSet<Int>) {
    if (nodo in visitados) return
    print("$nodo ")
    visitados.add(nodo)
    for (vecino in grafo[nodo] ?: emptyList()) {
        dfs(grafo, vecino, visitados)
    }
}
```

### Complejidad

* Tiempo: O(V + E)
* Espacio: O(V) por `visitados` + O(depth) por la pila de recursión.

### Ejemplo

Grafo:

```kotlin
val grafo = mapOf(
    1 to listOf(2, 3),
    2 to listOf(4, 5),
    3 to listOf(6),
    4 to emptyList(),
    5 to emptyList(),
    6 to emptyList()
)
```

Inicio `1` → recorrido: **1 2 4 5 3 6**

### Casos borde

* Grafo desconectado: sólo recorre una componente.
* Ciclos: se evitan con `visitados`.
* Profundidad muy grande: usar versión iterativa.

