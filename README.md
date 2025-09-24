# Trabajo en clase - Algoritmos en Kotlin.

## Autor  
**Andrés Sebastián Coral Vallejo.** 

---

- Algoritmo de número primo.
- Algoritmo de Euclides (Maximo común divisor (#1,#2)).
- Algoritmo factorial.
- Algoritmo de busqueda en profundidad (DFS).

---

## 1) Algoritmo de número primo.

### Idea / algoritmo
Se usa **división por prueba (trial division)**: para saber si `num` es primo, probamos dividir `num` por todos los enteros `i` desde `2` hasta `√num`.  
Si **ninguno** divide exactamente, entonces `num` es primo; si **alguno** divide, no es primo.

**Justificación:**  
Si `num = x * y` y ambos `x,y > 1`, entonces uno de ellos debe ser ≤ `√num`. Si no hay divisor ≤ `√num`, no puede existir factor no trivial.

---

## 2) Algoritmo de Euclides `Maximo común divisor (#1,#2)`

### Idea / algoritmo

Basado en la propiedad:

```
gcd(a, b) = gcd(b, a mod b)
gcd(a, 0) = a
```

---

## 3) Algoritmo factorial.

### Idea / algoritmo

Definición recursiva:

```
0! = 1
n! = n * (n-1)!  (para n > 0)
```


---

## 4) Algoritmo de busqueda en profundidad `(DFS)`

### Idea / algoritmo

Explora los nodos en profundidad primero, antes de retroceder. Se usa un conjunto `visitados` para evitar ciclos infinitos.
