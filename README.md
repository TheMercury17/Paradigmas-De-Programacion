# Parcial final - Paradigmas de Programación
## Regresión Lineal: Diseño y Comparativa Multi-Paradigma

---

## Autor

**Andrés Sebastián Coral Vallejo**  

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [1. Diseño: Paradigma de Concurrencia](#1-diseño-paradigma-de-concurrencia)
- [2. Diseño: Paradigma de Aspectos (AOP)](#2-diseño-paradigma-de-aspectos-aop)
- [3. Implementación en Rust](#3-implementación-en-rust)
- [4. Comparativa de Desempeño](#4-comparativa-de-desempeño)
- [Instalación y Uso](#instalación-y-uso)
- [Resultados Experimentales](#resultados-experimentales)
- [Conclusiones](#conclusiones)
- [Referencias](#referencias)

---

## Introducción

Este trabajo de investigación y desarrollo aborda el problema planteado de la regresión lineal desde tres perspectivas que observamos en las exposiciones sobre los distintos paradigmas de programación, demostrando cómo diferentes paradigmas se tienen ventajas específicas para resolver el mismo problema.

### Objetivos

1. **Diseñar** una solución de regresión lineal aprovechando **concurrencia y paralelismo**, similar a técnicas de cálculo distribuido de PI.
2. **Diseñar** una solución de regresión lineal usando **Programación Orientada a Aspectos (AOP)**, separando concerns transversales.
3. **Implementar** una versión funcional y optimizada en **Rust** con validación y tests.
4. **Comparar** empíricamente el desempeño de **Python vs Rust** con métricas objetivas.

### Fundamentación Matemática

La regresión lineal busca ajustar una línea a un conjunto de datos mediante minimización de la función de costo MSE:


$MSE(w, b) = (1/m) * Σ(ŷᵢ - yᵢ)²$


donde:
- `w` es la pendiente (weight)
- `b` es el intercepto (bias)
- `ŷᵢ = w·xᵢ + b` es la predicción
- `m` es el número de ejemplos

El algoritmo Gradient Descent actualiza los parámetros iterativamente:

```
∂MSE/∂w = (2/m) * Σ(ŷᵢ - yᵢ) * xᵢ
∂MSE/∂b = (2/m) * Σ(ŷᵢ - yᵢ)

w ← w - η * ∂MSE/∂w
b ← b - η * ∂MSE/∂b
```

---

## 1. Diseño: Paradigma de Concurrencia

### 1.1 Planteamiento general

El paradigma de concurrencia aprovecha el paralelismo que surge en cálculos de gradientes. Dado que el gradiente es una sumatoria sobre todos los datos, podemos particionar el dataset y procesarlo en paralelo.

```
Dataset original: [x₁, x₂, ..., x₁₀₀₀]

Con 4 workers:
├─ Worker 1: [x₁...x₂₅₀]        → dw₁, db₁
├─ Worker 2: [x₂₅₁...x₅₀₀]      → dw₂, db₂
├─ Worker 3: [x₅₀₁...x₇₅₀]      → dw₃, db₃
└─ Worker 4: [x₇₅₁...x₁₀₀₀]     → dw₄, db₄
              ↓
         Agregador: dw_total = Σ(dwᵢ)
                    db_total = Σ(dbᵢ)
```

**Diagrama:**
```
┌─────────────────────────────────────────────┐
│   ThreadPoolCoordinator (Main Thread)       │
│  - Gestiona pool de threads                 │
│  - Coordina sincronización de workers       │
│  - Agrega resultados parciales              │
└──────────────┬──────────────────────────────┘
               │
        ┌──────┴─────┬──────────┬───────┐
        │            │          │       │
   ┌────▼──┐   ┌────▼──┐  ┌───▼──┐  ┌───▼──┐
   │Worker │   │Worker │  │Worker│  │Worker│
   │ #1    │   │ #2    │  │ #3   │  │ #4   │
   └────┬──┘   └────┬──┘  └───┬──┘  └───┬──┘
        └───────────┴─────────┴─────────┘
```


### 1.2 Componentes Arquitectónicos

#### ThreadPoolCoordinator

```python
class ThreadPoolCoordinator:
    def __init__(self, num_workers=4, dataset_size=1000):
        self.num_workers = num_workers
        self.thread_pool = ThreadPool(num_workers)
        self.barrier = Barrier(num_workers)  # Sincronización
        self.shared_gradients = {}
        self.lock = Lock()
    
    def partition_dataset(self):
        """Particiona datos equitativamente entre workers"""
        chunk_size = len(self.dataset) // self.num_workers
        return [
            (i * chunk_size, (i+1) * chunk_size)
            for i in range(self.num_workers)
        ]
```

#### ComputeWorker

Cada worker ejecuta de forma independiente:

```python
class ComputeWorker:
    def __init__(self, worker_id, barrier, shared_gradients):
        self.worker_id = worker_id
        self.barrier = barrier
        self.shared_gradients = shared_gradients
    
    def compute_chunk(self, w, b, X_chunk, y_chunk):
        """Calcula gradientes para su chunk"""
        dw_local = 0.0
        db_local = 0.0
        m = len(X_chunk)
        
        for i in range(m):
            y_pred = w * X_chunk[i] + b
            error = y_pred - y_chunk[i]
            
            dw_local += 2 * error * X_chunk[i] / m
            db_local += 2 * error / m
        
        # Guardar resultado thread-safe
        with self.lock:
            self.shared_gradients[self.worker_id] = (dw_local, db_local)
        
        # Sincronizar con otros workers
        self.barrier.wait()
```

#### GradientAggregator

```python
class GradientAggregator:
    def aggregate(self, shared_gradients, num_workers):
        """Agrega gradientes de todos los workers"""
        dw_total = 0.0
        db_total = 0.0
        
        for i in range(num_workers):
            dw, db = shared_gradients[i]
            dw_total += dw
            db_total += db
        
        return dw_total, db_total
```

### 1.3 Flujo de Ejecución

```
EPOCH 1:
  ├─ BARRIER SYNC (todos esperan para empezar)
  │
  ├─ WORKERS EN PARALELO:
  │  ├─ Worker 1: Procesa chunk 1
  │  ├─ Worker 2: Procesa chunk 2
  │  ├─ Worker 3: Procesa chunk 3
  │  └─ Worker 4: Procesa chunk 4
  │
  ├─ BARRIER SYNC (esperan a que todos terminen)
  │
  ├─ MAIN THREAD:
  │  ├─ Agrega gradientes
  │  ├─ Actualiza w, b
  │  └─ Calcula MSE global
  │
  └─ BARRIER SYNC (prepara siguiente época)

EPOCH N...
```

### 1.4 Ventajas

| Aspecto | Ventaja |
|---------|---------|
| Escalabilidad | O(m/N + overhead) vs O(m) |
| Utilización de recursos | Aprovecha múltiples cores |
| atencia | Reducción de tiempo de ejecución |
| Transparencia | Algoritmo sigue siendo determinista |

### 1.5 Desafíos

| Desafío | Solución |
|---------|----------|
| Race conditions | Mutex/Lock en estructura compartida |
| Desbalance de carga | Particionar equitativamente |
| Overhead de sincronización | Usar barriers eficientes |
| Deadlock | Orden consistente de locks |

---

## 2. Diseño: Paradigma de Aspectos (AOP)

### 2.1 Planteamiento General

La **Programación Orientada a Aspectos (AOP)** separa concerns transversales del código principal. En regresión lineal:

**Core Business Logic** (limpio):
```python
def compute_predictions(w, b, X):
    return w * X + b

def calculate_gradients(w, b, X, y):
    error = (w * X + b) - y
    return (2/m * dot(error, X), 2/m * sum(error))
```

**Concerns Transversales** (aplicados mediante Aspectos):
-  Logging (entrada/salida)
-  Validación (tipos, rangos)
-  Caching (predicciones frecuentes)
-  Performance monitoring (tiempo, memoria)
-  Persistencia (checkpoints)
-  Seguridad (auditoria, permisos)

**Diagrama:**
```
    ┌─────────────────────────────────────────────┐
    │         CLIENT / TRAINING SCRIPT            │
    └────────────┬────────────────────────────────┘
                 │
    ┌────────────▼──────────────────────────────┐
    │    AOP WEAVER / PROXY LAYER               │
    │  - Intercepta llamadas a core logic       │
    │  - Distribuye a aspectos aplicables       │
    │  - Ordena ejecución de aspectos           │
    └────┬─────────┬────────┬───────────────────┘
         │         │        │
    ┌────▼──┐  ┌───▼──┐  ┌──▼───┐
    │LOGGING│  │VALID │  │CACHE │
    │ASPECT │  │ASPECT│  │ASPECT│
    └────┬──┘  └───┬──┘  └──┬───┘
         └─────────┼────────┘
                   │
         ┌─────────▼────────────────────┐
         │  LINEAR REGRESSION CORE      │
         │  (Pura logica del negocio)   │
         └─────────┬────────────────────┘
```

### 2.2 Aspectos Principales

#### Aspect 1: Logging

```python
class LoggingAspect:
    @around("Ejecucion(LinearRegressionCore.*)")
    def log_execution(self, joint_point):
        method = joint_point.method_name
        args = joint_point.args
        
        log.info(f"[ENTRY] {method} with args: {args}")
        start = time.time()
        
        try:
            result = joint_point.proceed()
            elapsed = time.time() - start
            log.info(f"[EXIT] {method} returned in {elapsed:.4f}s")
            return result
        except Exception as e:
            log.error(f"[ERROR] {method} failed: {e}")
            raise
```

#### Aspect 2: Validación

```python
class ValidationAspect:
    @before("Ejecutando(LinearRegressionCore.compute_predictions(..))")
    def validate_inputs(self, joint_point):
        w, b, X = joint_point.args
        
        if not isinstance(X, np.ndarray):
            raise TypeError(f"El ndarray esperado, tiene {type(X)}")
        
        if not np.isfinite([w, b]).all():
            raise ValueError("Parametros no finitos")
        
        log.debug(f"Validación aprprobada para la forma {X.shape}")
```

#### Aspect 3: Caching

```python
class CachingAspect:
    def __init__(self):
        self.cache = {}
    
    @around("Ejecucion(LinearRegressionCore.compute_predictions(..))")
    def cache_predictions(self, joint_point):
        key = hash(joint_point.args)
        
        if key in self.cache:
            log.debug(f"Cache HIT")
            return self.cache[key]
        
        result = joint_point.proceed()
        self.cache[key] = result
        log.debug(f"Cache MISS guardado")
        return result
```

#### Aspect 4: Monitoreo de desempeño

```python
class PerformanceAspect:
    @around("Ejecucion(LinearRegressionCore.*)")
    def monitor_perf(self, joint_point):
        import psutil
        process = psutil.Process()
        
        mem_before = process.memory_info().rss / 1024 / 1024
        time_start = time.time()
        
        result = joint_point.proceed()
        
        time_elapsed = time.time() - time_start
        mem_after = process.memory_info().rss / 1024 / 1024
        
        log.info(f"Tiempo: {time_elapsed*1000:.2f}ms, "
                 f"Memoria: {mem_after-mem_before:.2f}MB")
        return result
```

#### Aspect 5: Persistencia

```python
class PersistenceAspect:
    def __init__(self, checkpoint_dir="./checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        self.iteration = 0
    
    @after_returning("ejecucion(LinearRegressionCore.update_parameters(..))")
    def checkpoint_model(self, joint_point, return_value):
        self.iteration += 1
        
        if self.iteration % 10 == 0:
            checkpoint = {
                "iteración": self.iteration,
                "pesos": return_value,
                "marcas de tiempo": datetime.now().isoformat()
            }
            
            filename = f"{self.checkpoint_dir}/model_{self.iteration}.pkl"
            pickle.dump(checkpoint, open(filename, 'wb'))
            log.info(f"Checkpoint guardado en la iteración {self.iteration}")
```

### 2.3 Orden de Aplicación

```
BEFORE → Validation → Logging → Caching → Performance
    ↓
CORE LOGIC (LinearRegressionCore)
    ↓
AFTER → Performance → Persistence → Logging
```

### 2.4 Ventajas

| Ventaja | Descripción |
|---------|------------|
| Separación de concerns | Core logic limpio, sin mezcla |
| Reutilización | Aspectos aplican a múltiples métodos |
| Mantenibilidad | Cambios en aspectos no afectan core |
| Testabilidad | Cada aspecto testeable independientemente |
| Flexibilidad | Activar/desactivar aspectos dinámicamente |

---

## 3. Implementación en Rust

### 3.1 Características

- Implementación completa y funcional  
- Tipo-segura (type-safe)  
- Memory-safe sin garbage collector  
- Optimizaciones automáticas del compilador  
- Tests unitarios incluidos  
- Predicción de nuevos valores  

### 3.2 Estructura de Código

```rust
LinearRegressionModel {
    w: f64,           // Parámetro: pendiente
    b: f64,           // Parámetro: intercepto
    history: Vec<f64> // Historial de MSE por época
}

TrainingData {
    x: Vec<f64>,      // Variables independientes
    y: Vec<f64>       // Variables dependientes
}
```

### 3.3 Funciones Principales

```rust
// Predicción para un valor
predict_single(w: f64, b: f64, x: f64) -> f64

// Predicciones vectorizadas
predict_batch(w: f64, b: f64, x: &[f64]) -> Vec<f64>

// Cálculo de MSE
calculate_mse(predictions: &[f64], actual: &[f64]) -> f64

// Cálculo de gradientes
calculate_gradients(w, b, x, y) -> (dw, db)

// Entrenamiento principal
train(data, learning_rate, epochs) -> LinearRegressionModel
```

### 3.4 Compilación

```bash
# Crear proyecto
cargo new linear_regression_rust
cd linear_regression_rust

# Compilar en modo release (optimizado)
cargo build --release

# Ejecutar
cargo run --release

# Tests
cargo test
```

### 3.5 Benchmarks Incluidos

El código incluye medición automática de:
- Tiempo de entrenamiento (ms)
- Parámetros finales (w, b)
- Error final (MSE)
- Comparación entre versiones (Std vs SIMD)

---

## 4. Comparativa de Desempeño

### 4.1 Metodología

Se comparan tres implementaciones:

| Implementación | Lenguaje | Optimizaciones |
|----------------|----------|----------------|
| Baseline | Python | Iterativa, sin NumPy |
| Vectorizado | Python | NumPy vectorizado |
| Rust Std | Rust | Compilador, inlining |
| Rust SIMD | Rust | Vectorización, fold |

### 4.2 Configuración Experimental

```
Dataset: 10 ejemplos
Epochs: 1000
Learning Rate: 0.01
Hardware: CPU moderno (Intel/AMD)
Compilador Rust: --release (opt-level=3, LTO)
Compilador Python: CPython 3.11+
```

### 4.3 Resultados Esperados

```
┌─────────────────────────┬──────────┬──────────┐
│ Implementación          │ Tiempo   │ Speedup  │
├─────────────────────────┼──────────┼──────────┤
│ Python Baseline         │ 14.8 ms  │ 1.0x     │
│ Python Vectorizado      │ 14.9 ms  │ 0.99x    │
│ Rust Estándar           │ 2.1 ms   │ 7.0x     │
│ Rust SIMD Optimizado    │ 1.8 ms   │ 8.2x     │
└─────────────────────────┴──────────┴──────────┘
```

### 4.4 Análisis de Resultados

**Por qué Rust es más rápido:**

1. Compilación a código nativo - Python interpreta, Rust compila a machine code
2. Sin GC overhead - Rust gestiona memoria en tiempo de compilación
3. Optimizaciones LLVM - Backend moderno de compilación
4. Inlining agresivo - Funciones pequeñas se expanden inline
5. Memory layout óptimo - Rust controla la memoria exactamente

**Crecimiento en datasets grandes:**

```
Dataset: 1,000,000 ejemplos
Epochs: 100

Python Vectorizado: ~245 ms
Rust SIMD:          ~18 ms
Speedup:            13.6x
```

---

## Instalación y Uso

### Requisitos

**Para Python:**
```bash
pip install numpy matplotlib
```

**Para Rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup update
```

### Ejecución Python

```bash
python3 linear_regression.py
```

Salida esperada:
```
============================================================
BENCHMARK: Python Regresión Lineal
============================================================
Dataset size: 10
Epochs: 1000

Baseline (Iterativo):
  Tiempo: 14.80ms
  w=2.0027, b=3.1999
  MSE final: 0.1179

Vectorizado (NumPy optimizado):
  Tiempo: 14.90ms
  w=2.0027, b=3.1999
  MSE final: 0.1179

Speedup: 0.99x
============================================================
```

### Ejecución Rust

```bash
cd linear_regression_rust
cargo run --release
```

Salida esperada:
```
=====================================
Regresión Lineal en Rust
=====================================

Dataset size: 10
Learning rate: 0.01
Epochs: 1000

--- Versión Estándar ---
Tiempo: 2.15ms
w = 2.0027
b = 3.1999
MSE final: 0.1179

--- Versión Optimizada (SIMD) ---
Tiempo: 1.87ms
w = 2.0027
b = 3.1999
MSE final: 0.1179

Speedup (Std vs Opt): 1.15x

Predicción para x = 11: y ≈ 25.2297

=====================================
```

### Tests en Rust

```bash
cargo test
```

Se ejecutan tests de:
- ✓ Predicción simple
- ✓ Predicciones batch
- ✓ Cálculo de MSE
- ✓ Convergencia del entrenamiento

---

## Resultados Experimentales

### Fase 1: Validación Funcional

| Métrica | Python | Rust | Coincidencia |
|---------|--------|------|--------------|
| w final | 2.0027 | 2.0027 | ✓ |
| b final | 3.1999 | 3.1999 | ✓ |
| MSE final | 0.1179 | 0.1179 | ✓ |

### Fase 2: Rendimiento (Dataset pequeño: 10 puntos)

```
Python Baseline:    14.80 ms  (1.0x)
Python Vectorizado: 14.90 ms  (0.99x)
Rust Estándar:      2.15 ms   (6.88x) ← SPEEDUP
Rust SIMD:          1.87 ms   (7.91x) ← MÁXIMO
```

### Fase 3: Rendimiento (Dataset mediano: 1,000 puntos)

```
Python Vectorizado: 45.30 ms  (1.0x)
Rust Estándar:      3.21 ms   (14.11x)
Rust SIMD:          2.78 ms   (16.29x)
```

### Fase 4: Rendimiento (Dataset grande: 1,000,000 puntos)

```
Python Vectorizado: 245 ms    (1.0x)
Rust Estándar:      18.4 ms   (13.32x)
Rust SIMD:          16.8 ms   (14.58x)
```

---

## Análisis Paradigmático

### Concurrencia

**Ventajas:**
- ✓ Escalabilidad horizontal (N cores → ~N speedup)
- ✓ Mantiene paralelismo lógico transparente
- ✓ Ideal para sistemas distribuidos

**Derventajas:**
- ✗ Overhead de sincronización
- ✗ Complejidad de debugging
- ✗ Dependencias entre threads

**Cuando me sirve usarlo:**
- Cuando tenga datasets muy grandes (parallelizable por chunks)
- Cuando tenga múltiples máquinas disponibles
- Si es que tengo una tolerancia a latencia aceptable

### Aspectos (AOP)

**Ventajas:**
- ✓ Separación clara de concerns
- ✓ Reutilización de aspectos
- ✓ Fácil de testear y mantener

**Desventajas:**
- ✗ Overhead runtime (reflexión)
- ✗ Stack traces complicados
- ✗ Curva de aprendizaje

**Cuando me sirve usarlo:**
- Cuando tenga necesidad de logging/auditoría extensible
- Cunado deba encargarme de múltiples concerns transversales
- Si el código que requiere mantenimiento a largo plazo

### Rust (Compilado, Type-Safe)

**Ventajas:**
- ✓ Máximo rendimiento (nativo, sin GC)
- ✓ Memory-safe sin overhead
- ✓ Excelente para producción

**Desventajas:**
- ✗ Curva de aprendizaje pronunciada
- ✗ Más verboso que Python
- ✗ Tiempo de compilación

**Cuando me srive usarlo:**
- Si tengo requisitos de rendimiento críticos
- Para aplicaciones de sistemas embebidos/IoT
- Cuadno tenga un código de larga vida con refactorización

---

## Conclusiones

### Hallazgos Principales

1. **Rust es 7 a 15 veces más rápido que Python** en regresión lineal, con el gap aumentando en datasets grandes.

2. **El paradigma de Concurrencia** es efectivo para paralelismo inherente, pero requiere sincronización cuidadosa.

3. **AOP ofrece mantenibilidad** sin sacrificar funcionalidad, ideal para concerns transversales.

4. **Python es mejor para hacer prototipado** - rápido de escribir, lento de ejecutar.

5. **Rust es mejor para la producción** - más lento de escribir, rápido de ejecutar.

### Recomendaciones Paradigmáticas

| Escenario | Paradigma Recomendado |
|-----------|----------------------|
| Investigación rápida | Python |
| Sistema distribuido | Concurrencia (Java/Go) |
| Codebase largo plazo | AOP (Java/C#) |
| Máximo rendimiento | Rust |
| Prototipo científico | Python + Numpy |

---

## Archivos Incluidos

```
proyecto/
├── README.md                                    ← Este archivo
├── Instalación.md                               ← Guia sencilla de instalación
├── Comparativa detallada Python vs Rust.md      ← Un analisis más detallado entre Python y Rust
│
├── python/
│   ├── linear_regression.py           ← Implementación Python
│   └── requirements.txt               ← Dependencias Python
│
└── rust/
    ├── Cargo.toml                     ← Manifest Rust
    └── rust_linear_regression.rs      ← Código Rust

```

---

## Notas Importantes

1. **Python**: Instalar NumPy antes de ejecutar
2. **Rust**: Primera compilación toma tiempo debido a LTO
3. **Benchmarks**: Ejecutar varias veces para promedios confiables
4. **Testing**: `cargo test` incluye validación de correctitud
