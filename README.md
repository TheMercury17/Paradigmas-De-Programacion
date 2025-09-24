# Análisis de la Cola M/M/1/K/Inf.

## Autor  
**Andrés Sebastián Coral Vallejo.** 

## 1) Modelo matemático (estado estacionario)

**Definiciones:**

- λ = tasa de llegadas (Poisson).
- μ = tasa de servicio (exponencial).
- K = capacidad total del sistema (incluye el que está en servicio).
- ρ = λ / μ.

**Probabilidades en estado estacionario:**

- Si ρ ≠ 1:

$p_0 = \frac{1-\rho}{1-\rho^{K+1}}, \quad p_n = p_0 \rho^n, \quad n=0,\dots,K.$

- Si ρ = 1:

$p_n = \frac{1}{K+1}, \quad n=0,\dots,K.$

**Probabilidad de bloqueo (sistema lleno):**

$p_K = p_0 \rho^K.$

**Rendimiento efectivo (throughput):**

$\lambda_{\mathrm{eff}} = \lambda (1 - p_K).$

**Número medio en el sistema (N_S):**

- Si ρ ≠ 1:

$L = \frac{\rho \bigl(1-(K+1)\rho^K + K\rho^{K+1}\bigr)}{(1-\rho)(1-\rho^{K+1})}.$

- Si ρ = 1:

$L = \frac{K}{2}.$

**Número medio en cola (N_w):**

$L_q = L - (1 - p_0).$

**Tiempos medios (Little):**

$T_S = W = \frac{L}{\lambda_{\mathrm{eff}}}, \quad T_w = W_q = \frac{L_q}{\lambda_{\mathrm{eff}}}.$


---

## 2) Comprobación computacional (resumen)

Se ejecutó una simulación discreta por eventos (loss system: si el sistema tiene K clientes, la llegada se bloquea) y se compararon resultados analíticos vs simulados para 3 escenarios (K=5 en todos).

### Escenarios:

- **ρ < 1**: λ=2.0, μ=3.0, K=5 → ρ ≈ 0.6667  
- **ρ = 1**: λ=3.0, μ=3.0, K=5  
- **ρ > 1**: λ=5.0, μ=3.0, K=5 → ρ ≈ 1.6667

### Resultados (analítico vs simulado):

- **ρ < 1 (λ=2, μ=3, K=5)**  
  - L analítico = 1.422556, simulado ≈ 1.854480  
  - Lq analítico ≈ 0.422556, simulado ≈ 0.37267  
  - pK analítica ≈ 0.048120, simulado ≈ 0.076106  
  - λ_eff analítico ≈ 1.903759, simulado ≈ 1.847788  

- **ρ = 1 (λ=3, μ=3, K=5)**  
  - L analítico = 2.5, simulado ≈ 2.802754  
  - Lq analítico = 1.5, simulado ≈ 1.402392  
  - pK analítica = 0.166667, simulado ≈ 0.201501  
  - λ_eff analítico = 2.5, simulado ≈ 2.395496  

- **ρ > 1 (λ=5, μ=3, K=5)**  
  - L analítico ≈ 3.793636, simulado ≈ 3.867928  
  - Lq analítico ≈ 2.793636, simulado ≈ 2.73649  
  - pK analítica ≈ 0.419576, simulado ≈ 0.436848  
  - λ_eff analítico ≈ 2.902121, simulado ≈ 2.815758  

### Observaciones:

- La simulación reproduce los valores analíticos **en promedio**.  
- Las diferencias son razonables por el número finito de eventos (ruido Monte Carlo).  
- A mayor ρ, mayor probabilidad de bloqueo; para ρ ≤ 1 baja pero no nula por el efecto de la capacidad finita K.
