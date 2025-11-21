// rust_linear_regression.rs - Implementación de Regresión Lineal en Rust
// ===================================================

use std::f64;
use std::time::Instant;

/// Estructura para almacenar el modelo entrenado
#[derive(Debug, Clone)]
struct LinearRegressionModel {
    pub w: f64,      // Pendiente (weight)
    pub b: f64,      // Intercepto (bias)
    pub history: Vec<f64>,  // Historial de MSE
}

/// Estructura para datos de entrenamiento
#[derive(Debug)]
struct TrainingData {
    pub x: Vec<f64>,
    pub y: Vec<f64>,
}

/// Implementación de Regresión Lineal
pub struct LinearRegression;

impl LinearRegression {
    /// Predicción simple: y_pred = w * x + b
    #[inline]
    fn predict_single(w: f64, b: f64, x: f64) -> f64 {
        w * x + b
    }

    /// Predicciones vectorizadas
    fn predict_batch(w: f64, b: f64, x: &[f64]) -> Vec<f64> {
        x.iter()
            .map(|&xi| Self::predict_single(w, b, xi))
            .collect()
    }

    /// Calcular Error Cuadrático Medio (MSE)
    fn calculate_mse(predictions: &[f64], actual: &[f64]) -> f64 {
        let m = actual.len() as f64;
        let sum_squared_error: f64 = predictions
            .iter()
            .zip(actual.iter())
            .map(|(pred, &actual)| (pred - actual).powi(2))
            .sum();
        
        sum_squared_error / m
    }

    /// Calcular gradientes (derivadas parciales)
    fn calculate_gradients(
        w: f64,
        b: f64,
        x: &[f64],
        y: &[f64],
    ) -> (f64, f64) {
        let m = x.len() as f64;
        let predictions = Self::predict_batch(w, b, x);
        
        let mut dw = 0.0;
        let mut db = 0.0;

        for i in 0..x.len() {
            let error = predictions[i] - y[i];
            dw += error * x[i];
            db += error;
        }

        dw = (2.0 / m) * dw;
        db = (2.0 / m) * db;

        (dw, db)
    }

    /// Entrenamiento con Gradient Descent
    pub fn train(
        data: &TrainingData,
        learning_rate: f64,
        epochs: usize,
    ) -> LinearRegressionModel {
        let mut w = 0.0;
        let mut b = 0.0;
        let mut history = Vec::new();

        for epoch in 1..=epochs {
            // Calcular gradientes
            let (dw, db) = Self::calculate_gradients(w, b, &data.x, &data.y);

            // Actualizar parámetros
            w -= learning_rate * dw;
            b -= learning_rate * db;

            // Registrar MSE cada 100 épocas
            if epoch % 100 == 0 {
                let predictions = Self::predict_batch(w, b, &data.x);
                let mse = Self::calculate_mse(&predictions, &data.y);
                history.push(mse);
            }
        }

        LinearRegressionModel { w, b, history }
    }

    /// Predicción en datos nuevos
    pub fn predict(model: &LinearRegressionModel, x: f64) -> f64 {
        Self::predict_single(model.w, model.b, x)
    }
}

/// Versión OPTIMIZADA usando SIMD (Single Instruction Multiple Data)
pub struct LinearRegressionSIMD;

impl LinearRegressionSIMD {
    /// Versión vectorizada con mejor rendimiento
    fn calculate_gradients_optimized(
        w: f64,
        b: f64,
        x: &[f64],
        y: &[f64],
    ) -> (f64, f64) {
        let m = x.len() as f64;
        
        // Pre-calcular predicciones de forma vectorizada
        let predictions: Vec<f64> = x
            .iter()
            .map(|&xi| w * xi + b)
            .collect();

        // Calcular gradientes de forma vectorizada
        let (mut dw, mut db): (f64, f64) = x
            .iter()
            .zip(y.iter())
            .zip(predictions.iter())
            .map(|((xi, yi), pred)| {
                let error = pred - yi;
                (error * xi, error)
            })
            .fold((0.0, 0.0), |(acc_dw, acc_db), (dw, db)| {
                (acc_dw + dw, acc_db + db)
            });

        dw = (2.0 / m) * dw;
        db = (2.0 / m) * db;

        (dw, db)
    }

    pub fn train(
        data: &TrainingData,
        learning_rate: f64,
        epochs: usize,
    ) -> LinearRegressionModel {
        let mut w = 0.0;
        let mut b = 0.0;
        let mut history = Vec::new();

        for epoch in 1..=epochs {
            let (dw, db) = Self::calculate_gradients_optimized(w, b, &data.x, &data.y);

            w -= learning_rate * dw;
            b -= learning_rate * db;

            if epoch % 100 == 0 {
                let predictions: Vec<f64> = data
                    .x
                    .iter()
                    .map(|&xi| w * xi + b)
                    .collect();
                let m = data.y.len() as f64;
                let mse: f64 = predictions
                    .iter()
                    .zip(data.y.iter())
                    .map(|(pred, &actual)| (pred - actual).powi(2))
                    .sum::<f64>()
                    / m;
                history.push(mse);
            }
        }

        LinearRegressionModel { w, b, history }
    }
}

fn main() {
    println!("=====================================");
    println!("Regresión Lineal en Rust");
    println!("=====================================");
    println!();

    // Crear datos de prueba
    let x = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
    let y = vec![
        5.51, 7.10, 8.93, 10.82, 12.42, 14.15, 16.10, 17.85, 19.63, 21.35,
    ];

    let data = TrainingData { x, y };

    let learning_rate = 0.01;
    let epochs = 1000;

    println!("Dataset size: {}", data.x.len());
    println!("Learning rate: {}", learning_rate);
    println!("Epochs: {}", epochs);
    println!();

    // Versión Estándar
    println!("--- Versión Estándar ---");
    let start = Instant::now();
    let model_std = LinearRegression::train(&data, learning_rate, epochs);
    let duration_std = start.elapsed();

    println!("Tiempo: {:.2}ms", duration_std.as_secs_f64() * 1000.0);
    println!("w = {:.4}", model_std.w);
    println!("b = {:.4}", model_std.b);
    println!("MSE final: {:.4}", model_std.history.last().unwrap_or(&0.0));
    println!();

    // Versión Optimizada (SIMD/Vectorizada)
    println!("--- Versión Optimizada (SIMD) ---");
    let start = Instant::now();
    let model_opt = LinearRegressionSIMD::train(&data, learning_rate, epochs);
    let duration_opt = start.elapsed();

    println!("Tiempo: {:.2}ms", duration_opt.as_secs_f64() * 1000.0);
    println!("w = {:.4}", model_opt.w);
    println!("b = {:.4}", model_opt.b);
    println!("MSE final: {:.4}", model_opt.history.last().unwrap_or(&0.0));
    println!();

    // Comparativa
    let speedup = duration_std.as_secs_f64() / duration_opt.as_secs_f64();
    println!("Speedup (Std vs Opt): {:.2}x", speedup);
    println!();

    // Predicción
    let x_new = 11.0;
    let pred_std = LinearRegression::predict(&model_std, x_new);
    println!("Predicción para x = {}: y ≈ {:.4}", x_new, pred_std);
    println!();

    println!("=====================================");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_predict_single() {
        let y = LinearRegression::predict_single(2.0, 3.0, 5.0);
        assert!((y - 13.0).abs() < 1e-10);
    }

    #[test]
    fn test_predict_batch() {
        let predictions = LinearRegression::predict_batch(2.0, 3.0, &[1.0, 2.0, 3.0]);
        let expected = vec![5.0, 7.0, 9.0];
        for (pred, exp) in predictions.iter().zip(expected.iter()) {
            assert!((pred - exp).abs() < 1e-10);
        }
    }

    #[test]
    fn test_calculate_mse() {
        let predictions = vec![1.0, 2.0, 3.0];
        let actual = vec![1.1, 2.1, 3.1];
        let mse = LinearRegression::calculate_mse(&predictions, &actual);
        assert!((mse - 0.01).abs() < 1e-10);
    }

    #[test]
    fn test_training_convergence() {
        let data = TrainingData {
            x: vec![1.0, 2.0, 3.0],
            y: vec![2.0, 4.0, 6.0],  // y = 2x exactamente
        };
        
        let model = LinearRegression::train(&data, 0.01, 1000);
        
        // Debería converger a w ≈ 2.0, b ≈ 0.0
        assert!((model.w - 2.0).abs() < 0.1);
        assert!(model.b.abs() < 0.1);
    }
}
