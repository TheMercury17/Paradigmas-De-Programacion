# Comparación de algoritmos factorial: Recursivo vs Iterativo

**Autor:** Andrés Sebastián Coral Vallejo

## Objetivo
Comparar rendimiento (tiempo y uso de memoria) de dos implementaciones del factorial — recursiva e iterativa — en Python y en C.

---

## Requisitos / dependencias

### Python
- Python 3.8+
- Pip
- Repositorio: `python/requirements.txt` contiene las dependencias necesarias:
  - memory_profiler
  - matplotlib
  - pandas

Instalación rápida (Linux/macOS):
```bash
python3 -m pip install -r python/requirements.txt
```

> Nota: `memory_profiler` requiere `psutil` en algunas plataformas; `pip` lo resolverá.

### C (Linux)
- `gcc` (o `clang`)
- `make`
- `/usr/bin/time` (normalmente viene con `time` o como paquete `time`)
- `valgrind` (opcional, para análisis de memoria más profundo)

Instalación rápida (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install build-essential make valgrind time -y
```

> El script `scripts/install_deps.sh` intenta automatizar la instalación en entornos Debian/Ubuntu. Léelo antes de ejecutarlo.

---

## Cómo ejecutar los benchmarks (resumen)

1. Instalar dependencias Python:
```bash
python3 -m pip install -r python/requirements.txt
```

2. Ejecutar benchmark Python (genera `results/python_results.csv`):
```bash
bash scripts/run_python_bench.sh
```

3. Ejecutar benchmark C (genera `results/c_results.csv`):
```bash
bash scripts/run_c_bench.sh
```

4. Generar gráficos combinados (usa los CSV generados):
```bash
python3 python/plot_results.py
```

Los PNG resultantes se guardarán en `results/`.

---

## Consideraciones importantes

- **Enteros grandes:** Python maneja enteros arbitrariamente grandes; en C usamos `unsigned long long` por simplicidad (desbordamiento a partir de ~21!). Si necesitas comparar **exactamente** el mismo dominio numérico sin overflow, considera usar `GMP` en C (no incluido aquí).
- **Profundidad de recursión (Python):** la recursión profunda puede alcanzar el límite de recursión (por defecto ~1000). Los scripts manejan esto y saltan n muy grandes para la versión recursiva.
- **Medición de memoria (C):** dentro del programa es difícil obtener un pico de memoria portable. Los scripts usan `/usr/bin/time -v` para capturar `Maximum resident set size` por proceso. Para análisis más detallado se recomienda `valgrind --tool=massif`.
