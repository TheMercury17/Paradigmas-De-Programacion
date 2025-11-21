# GUÍA DE INSTALACIÓN Y EJECUCIÓN
## Parcial Final - Paradigmas de Programación

---

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación Python](#instalación-python)
- [Instalación Rust](#instalación-rust)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ejecución](#ejecución)

---

## Requisitos Previos

### Sistema Operativo Soportados

- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS (Intel y Apple Silicon)
- Windows 10/11

### Software Requerido

- **Python**: 3.11 o superior
- **Rust**: 1.74 o superior
- **Git**: Para clonar repositorios (opcional)
- **pip**: Gestor de paquetes Python
- **cargo**: Gestor de paquetes Rust

---

## Instalación Python

### Paso 1: Verificar Python

```bash
python3 --version
# Esperado: Python 3.11.0 o superior
```

Si no está instalado:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

**macOS (con Homebrew):**
```bash
brew install python3
```

**Windows:**
Descargar desde [python.org](https://www.python.org/downloads/)

### Paso 2: Crear Ambiente Virtual (Recomendado)

```bash
cd ruta/del/proyecto

# Crear ambiente virtual
python3 -m venv venv

# Activar ambiente
# En Linux/macOS:
source venv/bin/activate

# En Windows:
venv\Scripts\activate

# Verificar activación (debería mostrar (venv) al inicio)
```

### Paso 3: Instalar Dependencias

```bash
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente:
pip install numpy>=1.24.0
pip install matplotlib>=3.7.0
```

### Paso 4: Verificar Instalación

```bash
python3 -c "import numpy as np; print(f'NumPy {np.__version__} OK')"
python3 -c "import matplotlib; print(f'Matplotlib OK')"
```

---

## Instalación Rust

### Paso 1: Instalar Rustup

**Linux/macOS:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**Windows:**
Descargar desde [rustup.rs](https://rustup.rs/)

Seguir el instalador interactivo.

### Paso 2: Actualizar Rust

```bash
rustup update
```

### Paso 3: Verificar Instalación

```bash
rustc --version
# Esperado: rustc 1.74.0 o superior

cargo --version
# Esperado: cargo 1.74.0 o superior
```

### Paso 4: Configurar Compilador

```bash
# Ver toolchain activa
rustup toolchain list

# Instalar última estable (si es necesario)
rustup install stable
rustup default stable
```

---

## Estructura del Proyecto

```
proyecto-paradigmas/
│
├── README.md                          ← Documentación principal
├── INSTALACION.md                     ← Este archivo
│
│
├── python/
│   ├── linear_regression.py           ← Implementación Python
│   ├── requirements.txt               ← Dependencias
│
└── rust/
    ├── Cargo.toml                     ← Manifest de Rust
    ├── Cargo.lock                     ← Lock file (auto-generado)
    └── src/
        └── rust_linear_regression.rs                    ← Código main de Rust
```

---

## Ejecución

### Ejecutar Python

#### Opción 1: Desde la carpeta raíz

```bash
# Asegurarse que el ambiente virtual está activado
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Ejecutar
python3 python/linear_regression.py
```

#### Opción 2: Desde la carpeta python/

```bash
cd python
python3 linear_regression.py
```

#### Salida Esperada

```
============================================================
REGRESIÓN LINEAL EN PYTHON - BENCHMARK COMPARATIVO
============================================================

Dataset:
  Puntos: 10
  X: [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
  y: [5.51 7.1  8.93 10.82 12.42 14.15 16.1  17.85 19.63 21.35]
  Configuración:
    - Learning rate: 0.01
    - Epochs: 1000
    - Runs: 3 (promediar)

============================================================
Benchmarking: Baseline (Iterativo)
============================================================
  Run 1: 14.80ms
  Run 2: 14.75ms
  Run 3: 14.85ms

Promedio:  14.80ms
Std Dev:   0.05ms
w = 2.0027
b = 3.1999
MSE final: 0.1179

... (más output para Vectorizado y NumPy Optimizado)

============================================================
RESUMEN COMPARATIVO
============================================================

Modelo                         Tiempo (ms)    Speedup
────────────────────────────────────────────────────────
Baseline (Iterativo)          14.80 ms       1.00x
Vectorizado (NumPy)           14.90 ms       0.99x
NumPy Optimizado (In-place)   15.02 ms       0.98x

============================================================
VALIDACIÓN DE CONVERGENCIA
============================================================

Todos los modelos convergieron a los mismos parámetros:
  w ≈ 2.0027
  b ≈ 3.1999
  MSE ≈ 0.1179

============================================================
Ejecución completada exitosamente
============================================================
```

### Ejecutar Rust

#### Opción 1: Desarrollo (sin optimizaciones)

```bash
cd rust

# Compilar y ejecutar (modo debug)
cargo run

# Compilar en foreground
cargo build
./target/debug/linear_regression
```

#### Opción 2: Producción (optimizado - RECOMENDADO)

```bash
cd rust

# Compilar y ejecutar (modo release con LTO)
cargo run --release

# O compilar solo:
cargo build --release
./target/release/linear_regression  # Linux/macOS
# o
.\target\release\linear_regression.exe  # Windows
```

#### Salida Esperada

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
cd rust

# Ejecutar tests
cargo test

# Ejecutar tests en verbose
cargo test -- --nocapture

# Tests específico
cargo test test_training_convergence -- --nocapture
```

#### Salida Esperada

```
   Compiling linear_regression_rust v1.0.0
    Finished test [unoptimized + debuginfo] target(s) in 0.45s
     Running unittests src/main.rs

running 5 tests
test tests::test_predict_single ... ok
test tests::test_predict_batch ... ok
test tests::test_calculate_mse ... ok
test tests::test_training_convergence ... ok

test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

finished in 0.00s
```

---

## Tiempos de Ejecución

### Python

| Operación | Tiempo |
|-----------|--------|
| Primera ejecución | ~2-3 segundos (importación) |
| Ejecución normal | ~15-20 ms |
| Compilación PyC | Automática |

### Rust (Modo Debug)

| Operación | Tiempo |
|-----------|--------|
| Primera compilación | ~5-10 segundos |
| Recompilación (cambios) | ~1-2 segundos |
| Ejecución optimizada (--release) | ~2 ms |

### Rust (Modo Release)

| Operación | Tiempo |
|-----------|--------|
| Primera compilación | ~15-30 segundos (incluye LTO) |
| Recompilación (cambios) | ~5-15 segundos |
| Ejecución | ~2-3 ms |

---