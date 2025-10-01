# Ejercicio en clase 01/10/2025.

## Autor  
**Andrés Sebastián Coral Vallejo.** 

El ejercicio de hoy tomó en consideración a [Grokking-Artificial-Intelligence](https://github.com/rishal-hurbans/Grokking-Artificial-Intelligence-Algorithms/tree/master/ch08-machine_learning) como nos indicó el profesor.

---
## Comparación de los resultados entre `ml_linear_regression.py` y `ml_scikitlearn_linear_regression.py`.
---

### A) Modelo manual (archivo ml_linear_regression.py) — dataset pequeño del script

Se usaron 10 datos de entrenamiento (10 ejemplos).

Coeficientes (entrenado sobre $X = carat * 1000$):

 - Pendiente b1 = 3.1385915127885973 (por unidad escalada).

 - Intercepto b0 = −426.3289692171861.

Si convertimos la pendiente a precio por 1 carat (considerando que el código multiplicó $carat×1000$):

 - $Pendiente por 1 carat ≈ 3.1385915 × 1000 = 3138.59 (unidades monetarias por carat).$

 - $R² (forma correcta, comparando price_test vs predicciones) = 0.9269514332 (≈ 0.927).$


### B) Modelo scikit-learn (usando ml_data_preparation.Data con diamonds.csv)

División por defecto en ml_data_preparation.Data:
  - train_test_split(..., test_size=0.5) → 26970 ejemplos en train y 26970 en test (dataset total 53,940).

Regresión lineal (prediciendo price desde carat):
 - $Pendiente (slope) = 7791.112752637774 (precio por 1 carat).$
 - $Intercepto = −2278.5878610780373.$
 - $MSE (test) = 2,394,423.8479396133.$
 - $R² (test) = 0.8488493110150753 (≈ 0.849).$

Observación: Si se re-entrena una versión con $carat * 1000$ para comprobar la escala, se observa que El R² y MSE permanecen iguales;
la pendiente cambia por el factor de escala (como era de esperarse): pendiente ≈ 7.7911 cuando el input es $carat * 1000$ (esto concuerda matemáticamente con la versión sin escalar).










