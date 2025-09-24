import mesa
import random
import math
import heapq
from collections import deque


class Customer(mesa.Agent):
    # Cliente con tiempos: cuando entró a la cola y cuándo empezó el servicio.
    def __init__(self, unique_id, model, time_entered_queue):
        super().__init__(unique_id, model)
        self.time_entered_queue = time_entered_queue
        self.time_entered_service = None


class Server(mesa.Agent):
    # Servidor que guarda el cliente en servicio, el tiempo de finalización previsto
    # y el tiempo acumulado de utilización.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.customer_being_served = None
        self.next_completion_time = float('inf')
        self.utilization_time = 0


class MMnQueueModel(mesa.Model):
    # Modelo de colas M/M/n (simulación por eventos)
    def __init__(self, num_servers=3, mean_arrival_rate=0.9, mean_service_time=1.4,
                 max_run_time=340000, stats_reset_time=5000):
        super().__init__()

        # parámetros del modelo
        self.num_servers = num_servers
        self.mean_arrival_rate = mean_arrival_rate      # λ (llegadas por unidad de tiempo)
        self.mean_service_time = mean_service_time      # media del tiempo de servicio (E[S])
        self.max_run_time = max_run_time
        self.stats_reset_time = stats_reset_time        # tiempo en que se reinician estadísticas

        # estructuras de simulación
        self.queue = deque()           # cola FIFO de clientes
        self.current_time = 0.0        # reloj de la simulación
        self.arrival_count = 0         # contador de IDs de llegada
        self.next_arrival_time = 0.0

        # acumuladores para estadísticas temporales y por cliente
        self.stats_start_time = 0.0
        self.total_customer_queue_time = 0.0   # integral de N_queue(t) dt
        self.total_customer_service_time = 0.0 # integral de N_service(t) dt
        self.total_time_in_queue = 0.0         # suma de tiempos individuales en cola
        self.total_time_in_system = 0.0        # suma de tiempos individuales en sistema
        self.total_queue_throughput = 0        # clientes que iniciaron servicio
        self.total_system_throughput = 0       # clientes completados

        self.event_queue = []  # heap de eventos: (tiempo, tipo, dato)

        # crea un AgentSet de servidores usando Mesa (n servidores)
        self.servers = mesa.AgentSet(self, num_servers, Server)

        # programar la primera llegada
        self.schedule_arrival()

        # calcular medidas teóricas aproximadas
        self.compute_theoretical_measures()

        # recolector de datos (Datacollector de Mesa), usa los acumuladores anteriores
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Queue Length": lambda m: len(m.queue),
                "Avg Queue Length": lambda m: m.total_customer_queue_time / max(0.001,
                                                                                m.current_time - m.stats_start_time),
                "Server Utilization": lambda m: 100 * m.total_customer_service_time /
                                                max(0.001, m.current_time - m.stats_start_time) / m.num_servers,
                "Avg Time in Queue": lambda m: m.total_time_in_queue / max(1, m.total_queue_throughput),
                "Avg Time in System": lambda m: m.total_time_in_system / max(1, m.total_system_throughput),
                "Expected Utilization": lambda m: 100 * m.expected_utilization,
                "Expected Queue Length": lambda m: m.expected_queue_length,
                "Expected Queue Time": lambda m: m.expected_queue_time
            }
        )

    # -----------------------
    # Generador exponencial
    # -----------------------
    def random_exponential(self, mean):
        # devuelve un exponencial con media "mean": -ln(1-u) * mean
        return -math.log(1.0 - random.random()) * mean

    # -----------------------
    # Programación de eventos
    # -----------------------
    def schedule_arrival(self):
        # programa la próxima llegada si no hemos pasado max_run_time
        if self.current_time < self.max_run_time:
            # interarrival mean = 1/λ -> se pasa como mean a random_exponential
            interarrival_time = self.random_exponential(1.0 / self.mean_arrival_rate)
            self.next_arrival_time = self.current_time + interarrival_time
            heapq.heappush(self.event_queue, (self.next_arrival_time, "arrival", None))

    def schedule_service_completion(self, server):
        # programa el fin de servicio para un servidor dado
        service_time = self.random_exponential(self.mean_service_time)
        completion_time = self.current_time + service_time
        server.next_completion_time = completion_time
        heapq.heappush(self.event_queue, (completion_time, "service_completion", server.unique_id))

    def next_server_complete(self):
        # devuelve el servidor con menor tiempo de finalización (si hay servidores ocupados)
        busy_servers = [s for s in self.servers if s.customer_being_served is not None]
        if busy_servers:
            return min(busy_servers, key=lambda s: s.next_completion_time)
        return None

    # -----------------------
    # Eventos: llegada y servicio
    # -----------------------
    def arrive(self):
        # crear cliente con tiempo de entrada = current_time, añadir a cola
        customer = Customer(self.arrival_count, self, self.current_time)
        self.queue.append(customer)

        self.arrival_count += 1

        # programar la siguiente llegada
        self.schedule_arrival()

        # intentar iniciar servicio si hay servidores libres
        self.begin_service()

    def begin_service(self):
        # busca servidores libres y asigna clientes de la cola en FIFO
        available_servers = [s for s in self.servers if s.customer_being_served is None]

        while self.queue and available_servers:
            customer = self.queue.popleft()

            server = available_servers.pop(0)
            server.customer_being_served = customer

            # marcar inicio de servicio para el cliente
            customer.time_entered_service = self.current_time

            # tiempo que estuvo en cola (delay)
            queue_time = customer.time_entered_service - customer.time_entered_queue
            self.total_time_in_queue += queue_time
            self.total_queue_throughput += 1

            # programar fin de servicio para este servidor
            self.schedule_service_completion(server)

    def complete_service(self, server_id):
        # cuando un servidor termina, localizarlo por su unique_id
        server = next(s for s in self.servers if s.unique_id == server_id)
        customer = server.customer_being_served

        if customer:
            # tiempo en sistema = tiempo actual - tiempo de entrada a la cola
            system_time = self.current_time - customer.time_entered_queue
            self.total_time_in_system += system_time
            self.total_system_throughput += 1

            # liberar servidor
            server.customer_being_served = None
            server.next_completion_time = float('inf')

            # intentar empezar servicio con el siguiente de la cola
            self.begin_service()

    # -----------------------
    # Reinicio / acumuladores
    # -----------------------
    def reset_stats(self):
        # reinicia acumuladores (para medir después del periodo transitorio)
        self.total_customer_queue_time = 0.0
        self.total_customer_service_time = 0.0
        self.total_time_in_queue = 0.0
        self.total_time_in_system = 0.0
        self.total_queue_throughput = 0
        self.total_system_throughput = 0
        self.stats_start_time = self.current_time

    def update_usage_stats(self, event_time):
        # antes de procesar el evento en event_time, se actualizan las integrales:
        # incrementos = delta_time * (n en cola) y delta_time * (n en servicio)
        if event_time > self.current_time:
            delta_time = event_time - self.current_time
            in_queue = len(self.queue)
            in_process = sum(1 for s in self.servers if s.customer_being_served is not None)

            self.total_customer_queue_time += delta_time * in_queue
            self.total_customer_service_time += delta_time * in_process

            # actualizar utilización por servidor
            for server in self.servers:
                if server.customer_being_served is not None:
                    server.utilization_time += delta_time

            # avanzar reloj
            self.current_time = event_time

    # -----------------------
    # Medidas teóricas (aproximadas)
    # -----------------------
    def compute_theoretical_measures(self):
        # "balance_factor" = λ * E[S] (carga ofrecida)
        balance_factor = self.mean_arrival_rate * self.mean_service_time
        n = self.num_servers

        # si carga por servidor < 1, calcula aproximación (similar a Erlang-C)
        if balance_factor / n < 1:
            k_sum = 1.0
            power_product = 1.0
            factorial_product = 1.0

            # suma de términos hasta n-1
            for i in range(1, n):
                power_product *= balance_factor
                factorial_product *= i
                k_sum += power_product / factorial_product

            # término n
            power_product *= balance_factor
            factorial_product *= n
            k = k_sum / (k_sum + power_product / factorial_product)

            busy_probability = (1 - k) / (1 - balance_factor * k / n)
            self.expected_utilization = balance_factor / n
            self.expected_queue_length = busy_probability * self.expected_utilization / (1 - self.expected_utilization)
            self.expected_queue_time = busy_probability * self.mean_service_time / (n * (1 - self.expected_utilization))
        else:
            # sistema saturado/inestable
            self.expected_utilization = 1.0
            self.expected_queue_length = float('inf')
            self.expected_queue_time = float('inf')

    # -----------------------
    # Bucle por evento (un paso)
    # -----------------------
    def step(self):
        # si ya pasó el tiempo máximo, no hacer nada
        if self.current_time >= self.max_run_time:
            return

        # si no hay eventos programados, añadimos un end_run y (si procede) reset_stats
        if not self.event_queue:
            heapq.heappush(self.event_queue, (self.max_run_time, "end_run", None))

            if self.stats_reset_time > self.current_time:
                heapq.heappush(self.event_queue, (self.stats_reset_time, "reset_stats", None))

        # procesar el siguiente evento
        if self.event_queue:
            event_time, event_type, event_data = heapq.heappop(self.event_queue)

            # actualizar integrales hasta event_time
            self.update_usage_stats(event_time)

            # despachar tipos de evento
            if event_type == "arrival":
                self.arrive()
            elif event_type == "service_completion":
                self.complete_service(event_data)
            elif event_type == "reset_stats":
                self.reset_stats()
            elif event_type == "end_run":
                # forzar reloj a tiempo máximo
                self.current_time = self.max_run_time

        # recalcular medidas teóricas (opcional)
        self.compute_theoretical_measures()

        # recolectar datos si Datacollector está activo
        self.datacollector.collect(self)


def run_simulation():
    model = MMnQueueModel()

    print("Iniciando simulación de colas M/M/n")
    print("=" * 50)

    # bucle principal: ejecuta pasos hasta alcanzar tiempo máximo
    while model.current_time < model.max_run_time:
        model.step()

        if int(model.current_time) % 10000 == 0:
            print(f"Tiempo: {model.current_time:.1f}, "
                  f"Longitud de cola: {len(model.queue)}, "
                  f"Clientes atendidos: {model.total_system_throughput}")

    # imprimir resultados finales usando los acumuladores
    print("\n" + "=" * 50)
    print("RESULTADOS FINALES DE LA SIMULACIÓN")
    print("=" * 50)

    if model.current_time > model.stats_start_time:
        avg_queue_length = model.total_customer_queue_time / (model.current_time - model.stats_start_time)
        server_utilization = 100 * model.total_customer_service_time / (
                model.current_time - model.stats_start_time) / model.num_servers
    else:
        avg_queue_length = 0
        server_utilization = 0

    avg_time_in_queue = model.total_time_in_queue / max(1, model.total_queue_throughput)
    avg_time_in_system = model.total_time_in_system / max(1, model.total_system_throughput)

    print(f"Longitud promedio de cola: {avg_queue_length:.3f}")
    print(f"Utilización de servidores: {server_utilization:.1f}%")
    print(f"Tiempo promedio en cola: {avg_time_in_queue:.3f}")
    print(f"Tiempo promedio en sistema: {avg_time_in_system:.3f}")


    print(f"\nMEDIDAS TEÓRICAS (M/M/{model.num_servers})")
    print(f"Utilización esperada: {100 * model.expected_utilization:.1f}%")

    if model.expected_queue_length != float('inf'):
        print(f"Longitud esperada de cola: {model.expected_queue_length:.3f}")
        print(f"Tiempo esperado en cola: {model.expected_queue_time:.3f}")
        print(f"Tiempo esperado en sistema: {model.expected_queue_time + model.mean_service_time:.3f}")
    else:
        print("El sistema es inestable (utilización >= 100%)")

    return model


# OBSERVACIÓN: aquí el autor puso una condición invertida: si el módulo NO es __main__ entonces ejecuta.
# Normalmente se usa `if __name__ == "__main__":` para ejecutar al ejecutar el archivo como script.
if __name__ == "__main__":
    model = run_simulation()
