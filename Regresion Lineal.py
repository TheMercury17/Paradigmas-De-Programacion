from __future__ import annotations
import numpy as np
import os
import json
from typing import Optional, Tuple, Dict


class LinearRegressionOOP:
    """Regresión lineal orientada a objetos.

    Parámetros
    ----------
    fit_intercept : bool
        Si True, añade una columna de unos a X para aprender el término independiente.
    method : str
        'normal' para usar la ecuación normal (analítica), 'gd' para usar descenso por gradiente.
    lr : float
        Tasa de aprendizaje (solo para method='gd').
    epochs : int
        Número de iteraciones para descenso por gradiente (solo para method='gd').
    verbose : bool
        Si True, imprime progreso durante el entrenamiento (solo para GD).
    """

    def __init__(self,
                 fit_intercept: bool = True,
                 method: str = 'normal',
                 lr: float = 0.01,
                 epochs: int = 1000,
                 verbose: bool = False):
        assert method in ('normal', 'gd'), "method debe ser 'normal' o 'gd'"
        self.fit_intercept = fit_intercept
        self.method = method
        self.lr = float(lr)
        self.epochs = int(epochs)
        self.verbose = bool(verbose)

        self.theta: Optional[np.ndarray] = None  # parámetros del modelo (p+1, 1) si intercept
        self.n_features_in_: Optional[int] = None
        self.is_fitted_: bool = False
        self.history_: Dict[str, list] = {'loss': []}  # historial (sólo si se usa GD)

    # ---------------------- utilidades internas ----------------------
    def _prepare_X(self, X: np.ndarray) -> np.ndarray:
        """Convierte X a matriz 2D numpy y añade columna de 1s si fit_intercept.

        Acepta X como 1D (vector) o 2D.
        Devuelve matriz (n_samples, n_features(+1)).
        """
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.ndim != 2:
            raise ValueError("X debe ser array 1D o 2D")
        if self.fit_intercept:
            ones = np.ones((X.shape[0], 1))
            X = np.hstack([ones, X])
        return X

    def _prepare_y(self, y: np.ndarray) -> np.ndarray:
        """Asegura que y sea vector columna (n_samples, 1)."""
        y = np.asarray(y)
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        if y.ndim != 2 or y.shape[1] != 1:
            raise ValueError("y debe ser vector 1D o array columna (n,1)")
        return y

    # ---------------------- métodos públicos ----------------------
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearRegressionOOP':
        """Ajusta el modelo a los datos X, y.

        Dependiendo de self.method, usa la ecuación normal o descenso por gradiente.

        Devuelve self para permitir encadenamiento.
        """
        Xp = self._prepare_X(X)
        yp = self._prepare_y(y)

        n_samples, n_features = Xp.shape
        self.n_features_in_ = n_features - (1 if self.fit_intercept else 0)

        if self.method == 'normal':
            # solución analítica usando pseudo-inversa (estable incluso si X^T X no es invertible)
            # theta: (n_features, 1)
            # theta = pinv(Xp.T @ Xp) @ Xp.T @ yp
            XtX = Xp.T.dot(Xp)
            Xty = Xp.T.dot(yp)
            # usar pseudoinversa para estabilidad
            theta = np.linalg.pinv(XtX).dot(Xty)
            self.theta = theta
            self.is_fitted_ = True
            return self

        # ---------------- GD ----------------
        # inicialización
        theta = np.zeros((n_features, 1), dtype=float)
        m = float(n_samples)

        for epoch in range(self.epochs):
            preds = Xp.dot(theta)  # (n,1)
            error = preds - yp      # (n,1)
            grad = (Xp.T.dot(error)) / m  # (n_features, 1)
            theta = theta - self.lr * grad

            # registrar loss (MSE)
            loss = float((error ** 2).mean())
            self.history_['loss'].append(loss)

            if self.verbose and (epoch % max(1, self.epochs // 10) == 0):
                print(f'[GD] epoch {epoch+1}/{self.epochs} - loss: {loss:.6f}')

        self.theta = theta
        self.is_fitted_ = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Devuelve predicciones para X.

        Retorna vector 1D (n,) para conveniente uso con sklearn-like APIs.
        """
        if not self.is_fitted_:
            raise ValueError('El modelo no está ajustado. Llama a fit() primero.')
        Xp = self._prepare_X(X)
        preds = Xp.dot(self.theta)
        return preds.ravel()

    def mse(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        y_true = self._prepare_y(y_true).ravel()
        y_pred = np.asarray(y_pred).ravel()
        return float(np.mean((y_true - y_pred) ** 2))

    def r2_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        y_true = self._prepare_y(y_true).ravel()
        y_pred = np.asarray(y_pred).ravel()
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot != 0 else 0.0

    def summary(self) -> str:
        """Devuelve un resumen textual del modelo: coeficientes e información básica."""
        if not self.is_fitted_:
            return 'Modelo no ajustado.'
        coef = self.coefficients()
        lines = []
        lines.append('LinearRegressionOOP summary:')
        lines.append(f'  método: {self.method}')
        lines.append(f'  fit_intercept: {self.fit_intercept}')
        lines.append(f'  n_features_in_: {self.n_features_in_}')
        lines.append('  parámetros (theta):')
        for i, v in enumerate(coef):
            lines.append(f'    theta[{i:>2}] = {v:.6f}')
        return '\n'.join(lines)

    def coefficients(self) -> np.ndarray:
        """Devuelve theta como vector 1D para facilitar lectura."""
        if self.theta is None:
            raise ValueError('El modelo no tiene parámetros. Ajusta con fit().')
        return self.theta.ravel()

    # ---------------------- persistencia ----------------------
    def save(self, path: str) -> None:
        """Guarda parámetros y metadatos en un archivo .npz (numpy) y un .json con meta.

        path: nombre sin extensión o ruta; guardará path + '.npz' y path + '.json'.
        """
        base, ext = os.path.splitext(path)
        npz_path = base + '.npz'
        meta_path = base + '.json'

        np.savez(npz_path, theta=self.theta)
        meta = {
            'fit_intercept': self.fit_intercept,
            'method': self.method,
            'lr': self.lr,
            'epochs': self.epochs,
            'n_features_in_': self.n_features_in_
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f)

    @classmethod
    def load(cls, path: str) -> 'LinearRegressionOOP':
        """Carga modelo desde los archivos guardados con save()."""
        base, ext = os.path.splitext(path)
        npz_path = base + '.npz'
        meta_path = base + '.json'
        if not os.path.exists(npz_path):
            raise FileNotFoundError(f'Archivo no encontrado: {npz_path}')
        npz = np.load(npz_path, allow_pickle=True)
        theta = npz['theta']
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        obj = cls(fit_intercept=meta.get('fit_intercept', True),
                  method=meta.get('method', 'normal'),
                  lr=meta.get('lr', 0.01),
                  epochs=meta.get('epochs', 1000),
                  verbose=False)
        obj.theta = theta
        obj.n_features_in_ = meta.get('n_features_in_')
        obj.is_fitted_ = True
        return obj


# ---------------------- ejemplo de uso (script) ----------------------
if __name__ == '__main__':
    # Ejemplo reproducible: generamos datos sintéticos con una relación lineal
    import matplotlib.pyplot as plt

    np.random.seed(42)
    n = 200
    # una variable explicativa (carat) y ruido
    X = np.random.uniform(0.2, 3.0, size=(n, 1))  # carat entre 0.2 y 3.0
    true_slope = 7800.0
    true_intercept = -2300.0
    noise = np.random.normal(0, 800, size=(n, 1))
    y = true_intercept + true_slope * X + noise

    # separa train/test
    idx = np.arange(n)
    np.random.shuffle(idx)
    split = int(0.7 * n)
    train_idx = idx[:split]
    test_idx = idx[split:]

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Ajuste con ecuación normal (rápida y exacta para este ejemplo)
    model_normal = LinearRegressionOOP(fit_intercept=True, method='normal')
    model_normal.fit(X_train, y_train)
    preds_normal = model_normal.predict(X_test)

    # Ajuste con GD (para comparar)
    model_gd = LinearRegressionOOP(fit_intercept=True, method='gd', lr=0.001, epochs=5000, verbose=False)
    model_gd.fit(X_train, y_train)
    preds_gd = model_gd.predict(X_test)

    # Métricas
    mse_normal = model_normal.mse(y_test, preds_normal)
    r2_normal = model_normal.r2_score(y_test, preds_normal)

    mse_gd = model_gd.mse(y_test, preds_gd)
    r2_gd = model_gd.r2_score(y_test, preds_gd)

    print('\n--- Modelo (ecuación normal) ---')
    print(model_normal.summary())
    print(f'MSE (test): {mse_normal:.2f}, R2 (test): {r2_normal:.4f}')

    print('\n--- Modelo (descenso por gradiente) ---')
    print(model_gd.summary())
    print(f'MSE (test): {mse_gd:.2f}, R2 (test): {r2_gd:.4f}')

    # Grafica comparativa
    plt.figure(figsize=(8,6))
    plt.scatter(X_train, y_train, alpha=0.3, label='train')
    plt.scatter(X_test, y_test, marker='x', color='black', label='test')

    # líneas predichas (ordenar por X para trazar correctamente)
    xs = np.linspace(X.min(), X.max(), 100).reshape(-1,1)
    ys_norm = model_normal.predict(xs)
    ys_gd = model_gd.predict(xs)
    plt.plot(xs, ys_norm, label='regresión (normal)', linewidth=2)
    plt.plot(xs, ys_gd, label='regresión (GD)', linewidth=1, linestyle='--')

    plt.xlabel('carat (ejemplo sintético)')
    plt.ylabel('price (ejemplo sintético)')
    plt.legend()
    plt.title('Comparación: ecuación normal vs descenso por gradiente')
    plt.tight_layout()
    plt.show()

