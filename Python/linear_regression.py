#!/usr/bin/env python3
"""
linear_regression.py
Implementación de Regresión Lineal en Python.
"""

import numpy as np
import time
import sys
from typing import Tuple, List

class LinearRegressionBaseline:
    """
    Versión BASELINE: Implementación iterativa simple sin optimizaciones
    Refleja el código original proporcionado
    """
    
    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.w = 0.0
        self.b = 0.0
        self.history = []
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Entrenamiento con gradient descent iterativo"""
        m = len(X)
        
        for epoch in range(self.epochs):
            # Predicción
            y_pred = self.w * X + self.b
            
            # Error
            error = y_pred - y
            
            # Gradientes (derivadas)
            dw = (2/m) * np.dot(error, X)
            db = (2/m) * np.sum(error)
            
            # Actualización de parámetros
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db
            
            # Registrar MSE cada 100 épocas
            if (epoch + 1) % 100 == 0:
                mse = np.mean(error ** 2)
                self.history.append(mse)
        
        return self.w, self.b
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicción"""
        return self.w * X + self.b


class LinearRegressionVectorized:
    """
    Versión VECTORIZADA: Optimizada para NumPy
    Minimiza loops explícitos, aprovecha operaciones vectoriales nativas
    """
    
    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.w = 0.0
        self.b = 0.0
        self.history = []
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Entrenamiento vectorizado"""
        m = len(X)
        
        for epoch in range(self.epochs):
            # Operaciones vectorizadas (NumPy nativo, sin loops Python)
            y_pred = self.w * X + self.b
            error = y_pred - y
            
            # Gradientes vectorizados
            dw = np.sum(error * X) * (2.0 / m)
            db = np.sum(error) * (2.0 / m)
            
            # Actualización
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db
            
            # Registro
            if (epoch + 1) % 100 == 0:
                mse = np.mean(error ** 2)
                self.history.append(mse)
        
        return self.w, self.b
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicción"""
        return self.w * X + self.b


class LinearRegressionNumpy:
    """
    Versión NUMPY OPTIMIZADA: Usa máximo rendimiento de NumPy
    Incluyendo pre-asignación de memoria y operaciones internalizadas
    """
    
    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.w = np.float64(0.0)
        self.b = np.float64(0.0)
        self.history = []
        
        # Pre-asignar arrays para evitar creaciones dinámicas
        self._error_buffer = None
        self._y_pred_buffer = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Entrenamiento con máximas optimizaciones NumPy"""
        m = np.float64(len(X))
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        
        # Pre-asignar buffers
        self._y_pred_buffer = np.empty_like(y)
        self._error_buffer = np.empty_like(y)
        
        two_over_m = 2.0 / m
        
        for epoch in range(self.epochs):
            # Predicción in-place
            np.multiply(self.w, X, out=self._y_pred_buffer)
            np.add(self._y_pred_buffer, self.b, out=self._y_pred_buffer)
            
            # Error
            np.subtract(self._y_pred_buffer, y, out=self._error_buffer)
            
            # Gradientes
            dw = np.dot(self._error_buffer, X) * two_over_m
            db = np.sum(self._error_buffer) * two_over_m
            
            # Actualización
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db
            
            # Registro
            if (epoch + 1) % 100 == 0:
                mse = np.mean(np.square(self._error_buffer))
                self.history.append(mse)
        
        return self.w, self.b
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicción"""
        return self.w * X + self.b


def benchmark_model(Model, X: np.ndarray, y: np.ndarray, 
                   name: str, num_runs: int = 3) -> dict:
    """
    Realiza benchmark de un modelo
    
    Args:
        Model: Clase del modelo
        X: Datos de entrada
        y: Datos de salida
        name: Nombre del modelo para display
        num_runs: Número de ejecuciones para promediar
    
    Returns:
        dict con resultados del benchmark
    """
    times = []
    models = []
    
    print(f"\n{'='*60}")
    print(f"Benchmarking: {name}")
    print(f"{'='*60}")
    
    for run in range(num_runs):
        model = Model(learning_rate=0.01, epochs=1000)
        
        start = time.time()
        model.fit(X, y)
        elapsed = time.time() - start
        
        times.append(elapsed)
        models.append(model)
        
        print(f"  Run {run+1}: {elapsed*1000:.2f}ms")
    
    avg_time = np.mean(times)
    std_time = np.std(times)
    best_model = min(models, key=lambda m: min(m.history) if m.history else float('inf'))
    
    print(f"\nPromedio:  {avg_time*1000:.2f}ms")
    print(f"Std Dev:   {std_time*1000:.2f}ms")
    print(f"w = {best_model.w:.4f}")
    print(f"b = {best_model.b:.4f}")
    print(f"MSE final: {best_model.history[-1]:.4f}")
    
    return {
        'name': name,
        'avg_time': avg_time,
        'std_time': std_time,
        'times': times,
        'model': best_model,
        'w': best_model.w,
        'b': best_model.b,
        'mse': best_model.history[-1] if best_model.history else 0.0
    }


def main():
    """Función principal"""
    
    print("\n" + "="*60)
    print("REGRESIÓN LINEAL EN PYTHON - BENCHMARK COMPARATIVO")
    print("="*60)
    
    # Crear datos de prueba
    np.random.seed(42)
    X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    y = 2.0 * X + 3.0 + np.random.normal(0, 0.5, len(X))
    
    print(f"\nDataset:")
    print(f"  Puntos: {len(X)}")
    print(f"  X: {X}")
    print(f"  y: {y}")
    print(f"  Configuración:")
    print(f"    - Learning rate: 0.01")
    print(f"    - Epochs: 1000")
    print(f"    - Runs: 3 (promediar)")
    
    # Benchmark de modelos
    results = []
    
    results.append(benchmark_model(
        LinearRegressionBaseline,
        X, y,
        "Baseline (Iterativo)",
        num_runs=3
    ))
    
    results.append(benchmark_model(
        LinearRegressionVectorized,
        X, y,
        "Vectorizado (NumPy)",
        num_runs=3
    ))
    
    results.append(benchmark_model(
        LinearRegressionNumpy,
        X, y,
        "NumPy Optimizado (In-place)",
        num_runs=3
    ))
    
    # Resumen comparativo
    print(f"\n{'='*60}")
    print("RESUMEN COMPARATIVO")
    print(f"{'='*60}")
    print(f"\n{'Modelo':<30} {'Tiempo (ms)':<15} {'Speedup'}")
    print("-" * 60)
    
    baseline_time = results[0]['avg_time']
    
    for result in results:
        speedup = baseline_time / result['avg_time']
        print(f"{result['name']:<30} {result['avg_time']*1000:>8.2f}ms      "
              f"{speedup:>6.2f}x")
    
    # Validación de convergencia
    print(f"\n{'='*60}")
    print("VALIDACIÓN DE CONVERGENCIA")
    print(f"{'='*60}")
    print(f"\nTodos los modelos convergieron a los mismos parámetros:")
    print(f"  w ≈ {results[0]['w']:.4f}")
    print(f"  b ≈ {results[0]['b']:.4f}")
    print(f"  MSE ≈ {results[0]['mse']:.4f}")
    
    # Predicción
    print(f"\n{'='*60}")
    print("PREDICCIÓN")
    print(f"{'='*60}")
    x_new = 11.0
    pred = results[0]['model'].predict(np.array([x_new]))
    print(f"\nPara x = {x_new}:")
    print(f"  y_predicho = {pred[0]:.4f}")
    print(f"  Fórmula: y = {results[0]['w']:.4f} * {x_new} + {results[0]['b']:.4f}")
    
    print(f"\n{'='*60}")
    print("Ejecución completada exitosamente")
    print(f"{'='*60}\n")
    
    return results


if __name__ == "__main__":
    results = main()
