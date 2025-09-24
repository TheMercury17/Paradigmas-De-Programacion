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

$p_0 = \frac{1-\rho}{1-\rho^{K+1}}, \quad p_n = p_0 \rho^n, \quad n=0,\dots,K$

- Si ρ = 1:

$p_n = \frac{1}{K+1}, \quad n=0,\dots,K$

**Probabilidad de bloqueo (sistema lleno):**

$p_K = p_0 \rho^K$

**Rendimiento efectivo (throughput):**

$\lambda_{\mathrm{eff}} = \lambda (1 - p_K)$

**Número medio en el sistema (N_S):**

- Si ρ ≠ 1:

$L = \frac{\rho \bigl(1-(K+1)\rho^K + K\rho^{K+1}\bigr)}{(1-\rho)(1-\rho^{K+1})}$

- Si ρ = 1:

$L = \frac{K}{2}$

**Número medio en cola (N_w):**

$L_q = L - (1 - p_0)$

**Tiempos medios (Little):**

$T_S = W = \frac{L}{\lambda_{\mathrm{eff}}}, \quad T_w = W_q = \frac{L_q}{\lambda_{\mathrm{eff}}}$


---

## 2) Comprobación computacional (resumen)

### Escenarios:

Se toma **K = 10** y **μ = 5** como 5 clientes por unidad de tiempo y se varía **λ** entre 0.1 y 2 para analizar tres escenarios:

###  Escenario 1. Baja carga (λ = 0.1, ρ = 0.02) donde:
- $P_0 \approx 0.981$  
- $P_K \approx 0.000$  
- $\lambda_{eff} \approx 0.100$  
- $N_s \approx 0.020$  
- $N_w \approx 0.001$  
- $T_s \approx 0.200$  
- $T_w \approx 0.010$  
 El sistema se encuentra casi vacío y tiene esperas mínimas.

###  Escenario 2. Carga media (λ = 1, ρ = 0.2) donde:
- $P_0 \approx 0.834$  
- $P_K \approx 1.07 \times 10^{-7}$  
- $\lambda_{eff} \approx 1.0$  
- $N_s \approx 0.25$  
- $N_w \approx 0.084$  
- $T_s \approx 0.25$  
- $T_w \approx 0.084$  
 El sistema ve un flujo estable y empieza a observarse algo de cola.

###  Escenario 3. Alta carga (λ = 2, ρ = 0.4) donde:
- $P_0 \approx 0.600$  
- $P_K \approx 1.58 \times 10^{-4}$  
- $\lambda_{eff} \approx 2.0$  
- $N_s \approx 0.67$  
- $N_w \approx 0.27$  
- $T_s \approx 0.33$  
- $T_w \approx 0.13$  
 El sistema empieza a congestionarse dentro del limite de su capacidad.

---

## 3) Explicación detallada del archivo CodigoCola.py:

1. **Objetivo general**  
   Es un simulador `M/M/n` por eventos (cola FIFO, llegadas Poisson / servicio exponencial).  
   Usa un *heap* de eventos (`event_queue`) para avanzar el tiempo de un evento al siguiente (llegadas y finalizaciones de servicio).

2. **Generación de tiempos**
   - `random_exponential(mean)` devuelve una variable exponencial con **media** `mean`.
   - Para las llegadas se llama con `mean = 1.0 / mean_arrival_rate` (correcto: la media de los interarrivos es `1/λ`).
   - Para el servicio se usa `mean_service_time` como media de servicio (E[S]).

3. **Estructuras de datos**
   - `queue` (deque) almacena `Customer` esperando.
   - `servers` es un `AgentSet` de Mesa que contiene `num_servers` instancias `Server`.  
     Cada `Server` tiene `customer_being_served` y `next_completion_time`.
   - `event_queue` es una lista utilizada como heap por `heapq` con tuplas `(time, event_type, data)`.

4. **Flujo de eventos**
   - `schedule_arrival()` programa la próxima llegada si no se ha alcanzado `max_run_time`.  
     Inserta `(t_arrival, "arrival", None)` en el heap.
   - Cuando se procesa un evento `"arrival"`, `arrive()` crea un `Customer`, lo añade a `queue`,  
     aumenta `arrival_count`, programa la siguiente llegada y llama a `begin_service()` para asignar servidores libres.
   - `begin_service()` obtiene servidores libres, extrae clientes de la cola (FIFO), marca `time_entered_service`,  
     acumula el tiempo de cola del cliente y programa el `service_completion` para ese servidor.
   - Cuando el heap entrega un evento `"service_completion"`, `complete_service(server_id)` busca el servidor por `unique_id`,  
     calcula el tiempo en sistema del cliente que sale, actualiza acumuladores y libera el servidor.  
     También llama a `begin_service()` para arrancar al siguiente cliente en cola si existe.

5. **Promedios temporales / acumuladores**
   - `update_usage_stats(event_time)` se llama **antes** de procesar el evento para acumular áreas:  
     añade `delta * in_queue` a `total_customer_queue_time` y `delta * in_process` a `total_customer_service_time`.  
     También suma `delta` a `utilization_time` de cada servidor ocupado.  
     Esto permite calcular promedios temporales (promedio de N_queue y utilización de servidores en porcentaje).
   - Las métricas por cliente (tiempo promedio en cola, en sistema) se obtienen dividiendo:  
     - `total_time_in_queue / total_queue_throughput`  
     - `total_time_in_system / total_system_throughput`

6. **Medidas teóricas**
   - `compute_theoretical_measures()` calcula una aproximación parecida a Erlang-C usando la carga ofrecida `a = λ * E[S]`.  
   - Si `a/n < 1` calcula `expected_utilization`, `expected_queue_length` y `expected_queue_time`.  
   - Si la carga por servidor ≥ 1 se marca como inestable.
   - **Nota**: la expresión usada no es exactamente la implementación estándar de Erlang-C  
     (falta el cálculo explícito de p0 y la fórmula de Erlang-C exacta), pero es una aproximación en la línea del código original.

7. **Bucle principal**
   - `run_simulation()` crea el modelo y llama `model.step()` repetidamente hasta `max_run_time`.  
   - Dentro de `step()` se procesa exactamente **un** evento (avanza el reloj al tiempo del siguiente evento y despacha la lógica).  
   - Se van acumulando y recolectando datos.  
   - Al terminar imprime resultados basados en los acumuladores.

