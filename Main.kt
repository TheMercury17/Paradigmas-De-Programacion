// ---------------------------------------------
// Algoritmos implementados:
// 1. Verificación de número primo
// 2. Algoritmo de Euclides (máximo común divisor)
// 3. Factorial de un número
// 4. Búsqueda en profundidad (DFS) en un grafo
// ---------------------------------------------

fun main() {
    println("===== PROGRAMA DE ALGORITMOS EN KOTLIN =====")

    // -----------------------------
    // 1. ALGORITMO DE NÚMERO PRIMO
    // -----------------------------
    val numeroPrimo = 29
    println("\n[1] Verificación de número primo:")
    println("¿$numeroPrimo es primo? -> ${esPrimo(numeroPrimo)}")

    // -----------------------------
    // 2. ALGORITMO DE EUCLIDES (MCD)
    // -----------------------------
    val a = 56
    val b = 98
    println("\n[2] Algoritmo de Euclides (MCD):")
    println("El MCD de $a y $b es -> ${mcd(a, b)}")

    // -----------------------------
    // 3. ALGORITMO FACTORIAL
    // -----------------------------
    val n = 5
    println("\n[3] Factorial:")
    println("El factorial de $n es -> ${factorial(n)}")

    // -----------------------------
    // 4. BÚSQUEDA EN PROFUNDIDAD (DFS)
    // -----------------------------
    println("\n[4] Búsqueda en profundidad (DFS):")
    val grafo = mapOf(
        1 to listOf(2, 3),
        2 to listOf(4, 5),
        3 to listOf(6),
        4 to emptyList(),
        5 to emptyList(),
        6 to emptyList()
    )
    val inicio = 1
    println("Recorrido DFS desde el nodo $inicio:")
    dfs(grafo, inicio, mutableSetOf())
}

// -----------------------------
// Función para verificar si un número es primo
// -----------------------------
fun esPrimo(num: Int): Boolean {
    if (num <= 1) return false
    for (i in 2..Math.sqrt(num.toDouble()).toInt()) {
        if (num % i == 0) return false
    }
    return true
}

// -----------------------------
// Algoritmo de Euclides para MCD
// -----------------------------
fun mcd(a: Int, b: Int): Int {
    return if (b == 0) a else mcd(b, a % b)
}

// -----------------------------
// Factorial (definición recursiva)
// -----------------------------
fun factorial(n: Int): Long {
    return if (n == 0) 1 else n * factorial(n - 1)
}

// -----------------------------
// DFS (Depth First Search) Recursivo
// -----------------------------
fun dfs(grafo: Map<Int, List<Int>>, nodo: Int, visitados: MutableSet<Int>) {
    if (nodo in visitados) return
    print("$nodo ")
    visitados.add(nodo)
    for (vecino in grafo[nodo] ?: emptyList()) {
        dfs(grafo, vecino, visitados)
    }
}