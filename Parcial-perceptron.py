# Importaciones necesarias para el funcionamiento del modelo de perceptrón
import random
import threading
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class PointDataAgent(Agent):
    """
    Agente que representa un punto de datos en el espacio 2D.
    Cada punto tiene coordenadas (x,y) y una etiqueta de clase.
    """
    def __init__(self, agent_id, model, position_x, position_y, class_label):
        super().__init__(agent_id, model)
        # Asignación de propiedades del punto de datos
        self.position_x = position_x
        self.position_y = position_y
        self.class_label = class_label
        self.predicted_class = 0  # Clasificación predicha inicialmente
        self.is_correct = False  # Indicador de clasificación correcta
        
        # Asignación inicial del color basado en la etiqueta verdadera
        self.display_color = 'blue' if class_label == -1 else 'red'
    
    def refresh_classification(self, prediction):
        """
        Actualiza el estado de clasificación del punto y su color de visualización.
        """
        self.predicted_class = prediction
        self.is_correct = (self.class_label == prediction)
        
        # Cambio de color según la correctitud de la clasificación
        if self.is_correct:
            self.display_color = 'lightgreen' if self.class_label == -1 else 'lightcoral'
        else:
            self.display_color = 'darkblue' if self.class_label == -1 else 'darkred'

class NeuralPerceptronAgent(Agent):
    """
    Agente que implementa el algoritmo de aprendizaje del perceptrón.
    Contiene los pesos, bias y la lógica de entrenamiento.
    """
    def __init__(self, agent_id, model, learning_rate=0.1):
        super().__init__(agent_id, model)
        self.learning_rate = learning_rate
        
        # Inicialización aleatoria de parámetros del perceptrón
        self.weight_vector = np.random.uniform(-1, 1, 2)
        self.bias_term = np.random.uniform(-1, 1)
        
        # Control del progreso del entrenamiento
        self.current_epoch = 0
        self.error_history = []
        self.has_converged = False
    
    def step(self):
        """
        Ejecuta una iteración de entrenamiento del perceptrón.
        """
        accumulated_error = 0
        
        # Procesamiento de todos los puntos de datos
        data_agents = [agent for agent in self.model.schedule.agents 
                      if isinstance(agent, PointDataAgent)]
        
        for data_point in data_agents:
            # Cálculo de la activación lineal
            linear_activation = (self.weight_vector[0] * data_point.position_x + 
                               self.weight_vector[1] * data_point.position_y + 
                               self.bias_term)
            
            # Aplicación de la función de activación (signo)
            prediction = 1 if linear_activation >= 0 else -1
            
            # Cálculo del error y actualización si es necesario
            classification_error = data_point.class_label - prediction
            accumulated_error += abs(classification_error)
            
            # Regla de actualización del perceptrón
            if classification_error != 0:
                self.weight_vector[0] += self.learning_rate * classification_error * data_point.position_x
                self.weight_vector[1] += self.learning_rate * classification_error * data_point.position_y
                self.bias_term += self.learning_rate * classification_error
            
            # Actualización del estado del punto de datos
            data_point.refresh_classification(prediction)
        
        # Registro del error y actualización del contador de épocas
        self.error_history.append(accumulated_error)
        self.current_epoch += 1
        
        # Criterio de parada: convergencia o máximo de iteraciones
        if accumulated_error == 0 or self.current_epoch >= self.model.max_iterations:
            self.model.running = False
    
    def calculate_decision_boundary(self, x_limits):
        """
        Calcula los puntos de la frontera de decisión para visualización.
        """
        # Verificación para evitar división por cero
        if abs(self.weight_vector[1]) > 1e-10:
            x_values = np.linspace(x_limits[0], x_limits[1], 100)
            y_values = -(self.weight_vector[0] * x_values + self.bias_term) / self.weight_vector[1]
            return x_values, y_values
        else:
            # Caso especial: línea vertical
            x_values = np.full(100, -self.bias_term / self.weight_vector[0] 
                              if abs(self.weight_vector[0]) > 1e-10 else 0)
            y_values = np.linspace(x_limits[0], x_limits[1], 100)
            return x_values, y_values

class PerceptronSimulationModel(Model):
    """
    Modelo principal que coordina la simulación del perceptrón.
    Genera los datos y controla el flujo de ejecución.
    """
    def __init__(self, num_points=50, learning_rate=0.1, max_iterations=100, data_range=10):
        super().__init__()
        self.num_data_points = num_points
        self.max_iterations = max_iterations
        self.coordinate_range = data_range
        self.running = True
        
        # Inicialización del programador de agentes
        self.schedule = RandomActivation(self)
        
        # Generación de la línea de separación verdadera (aleatoria)
        slope_param = random.uniform(-1, 1)
        intercept_param = random.uniform(-data_range/4, data_range/4)
        
        # Creación de puntos de datos linealmente separables
        for point_index in range(num_points):
            x_coord = random.uniform(-data_range, data_range)
            y_coord = random.uniform(-data_range, data_range)
            
            # Asignación de etiqueta basada en la posición respecto a la línea
            true_label = 1 if y_coord > slope_param * x_coord + intercept_param else -1
            
            self.schedule.add(PointDataAgent(point_index + 1, self, x_coord, y_coord, true_label))
        
        # Creación del agente perceptrón
        self.perceptron_agent = NeuralPerceptronAgent(0, self, learning_rate)
        self.schedule.add(self.perceptron_agent)
    
    def step(self):
        """
        Ejecuta un paso de la simulación si está en funcionamiento.
        """
        if self.running:
            self.schedule.step()

class PerceptronUserInterface:
    """
    Interfaz gráfica de usuario para controlar y visualizar el perceptrón.
    """
    def __init__(self):
        self.simulation_model = None
        self.is_running = False
        
        # Configuración de la ventana principal
        self.main_window = tk.Tk()
        self.main_window.title('Sistema Perceptrón - Mesa Framework v0.8.9')
        self.main_window.geometry('1200x800')
        
        self._setup_interface()
        self.main_window.mainloop()
    
    def _setup_interface(self):
        """
        Construye todos los elementos de la interfaz gráfica.
        """
        main_container = ttk.Frame(self.main_window)
        main_container.pack(fill=tk.BOTH, expand=1)
        
        # Panel de controles
        control_panel = ttk.LabelFrame(main_container, text='Panel de Configuración')
        control_panel.pack(fill=tk.X, pady=5)
        
        # Control de tasa de aprendizaje
        ttk.Label(control_panel, text='Velocidad de Aprendizaje').grid(row=0, column=0)
        self.learning_rate_var = tk.DoubleVar(value=0.1)
        ttk.Scale(control_panel, from_=0.01, to=1, variable=self.learning_rate_var,
                 orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, padx=5)
        ttk.Label(control_panel, textvariable=self.learning_rate_var).grid(row=0, column=2)
        
        # Control de iteraciones máximas
        ttk.Label(control_panel, text='Máximo de Épocas').grid(row=1, column=0)
        self.max_iterations_var = tk.IntVar(value=100)
        ttk.Scale(control_panel, from_=10, to=500, variable=self.max_iterations_var,
                 orient=tk.HORIZONTAL, length=200).grid(row=1, column=1, padx=5)
        ttk.Label(control_panel, textvariable=self.max_iterations_var).grid(row=1, column=2)
        
        # Panel de botones
        button_container = ttk.Frame(control_panel)
        button_container.grid(row=2, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_container, text='Comenzar Entrenamiento', 
                  command=self.begin_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_container, text='Reiniciar Sistema', 
                  command=self.reset_system).pack(side=tk.LEFT)
        
        # Área de información textual
        self.info_display = tk.Text(main_container, height=4)
        self.info_display.pack(fill=tk.X)
        
        # Panel de visualización
        visualization_panel = ttk.LabelFrame(main_container, text='Visualización del Aprendizaje')
        visualization_panel.pack(fill=tk.BOTH, expand=1)
        
        # Configuración de gráficos
        plot_figure = Figure(figsize=(6, 4))
        self.main_plot = plot_figure.add_subplot(211)
        self.error_plot = plot_figure.add_subplot(212)
        
        self.plot_canvas = FigureCanvasTkAgg(plot_figure, visualization_panel)
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    
    def begin_training(self):
        """
        Inicia o detiene el proceso de entrenamiento.
        """
        if self.is_running:
            self.is_running = False
            return
        
        # Creación de nuevo modelo con parámetros actualizados
        self.simulation_model = PerceptronSimulationModel(
            num_points=50, 
            learning_rate=self.learning_rate_var.get(),
            max_iterations=self.max_iterations_var.get(), 
            data_range=10
        )
        
        self.is_running = True
        # Inicio del hilo de ejecución
        threading.Thread(target=self._execute_simulation, daemon=True).start()
    
    def reset_system(self):
        """
        Reinicia el sistema completo limpiando visualizaciones.
        """
        self.is_running = False
        self.info_display.delete(1.0, tk.END)
        self.main_plot.clear()
        self.error_plot.clear()
        self.plot_canvas.draw()
    
    def _execute_simulation(self):
        """
        Bucle principal de ejecución de la simulación.
        """
        while self.is_running and self.simulation_model.running:
            self.simulation_model.step()
            self._refresh_display()
            time.sleep(0.1)  # Pausa para visualización
        
        self.is_running = False
    
    def _refresh_display(self):
        """
        Actualiza todas las visualizaciones con el estado actual.
        """
        model = self.simulation_model
        
        # Limpieza de gráficos
        self.main_plot.clear()
        self.error_plot.clear()
        
        # Obtención de puntos de datos para visualización
        data_points = [agent for agent in model.schedule.agents 
                      if isinstance(agent, PointDataAgent)]
        
        # Graficación de puntos con colores y formas distintivas
        for point in data_points:
            marker_style = 'o' if point.class_label == -1 else '^'
            self.main_plot.scatter(point.position_x, point.position_y, 
                                 c=point.display_color, marker=marker_style)
        
        # Dibujado de la frontera de decisión
        boundary_x, boundary_y = model.perceptron_agent.calculate_decision_boundary(
            (-model.coordinate_range, model.coordinate_range))
        self.main_plot.plot(boundary_x, boundary_y, 'g-', linewidth=2)
        
        # Configuración del gráfico principal
        self.main_plot.set_title(f'Época de Entrenamiento: {model.perceptron_agent.current_epoch}')
        self.main_plot.grid(True, alpha=0.3)
        
        # Gráfico de evolución del error
        self.error_plot.plot(range(len(model.perceptron_agent.error_history)), 
                            model.perceptron_agent.error_history, 'r-', linewidth=2)
        self.error_plot.set_xlabel('Número de Época')
        self.error_plot.set_ylabel('Error Total')
        self.error_plot.grid(True, alpha=0.3)
        
        # Actualización del canvas
        self.plot_canvas.draw()
        
        # Actualización del texto informativo
        current_error = (model.perceptron_agent.error_history[-1] 
                        if model.perceptron_agent.error_history else 0)
        self.info_display.delete(1.0, tk.END)
        info_text = f'Época Actual: {model.perceptron_agent.current_epoch}\n'
        info_text += f'Error de Clasificación: {current_error}\n'
        info_text += f'Pesos: [{model.perceptron_agent.weight_vector[0]:.3f}, {model.perceptron_agent.weight_vector[1]:.3f}]\n'
        info_text += f'Bias: {model.perceptron_agent.bias_term:.3f}'
        self.info_display.insert(tk.END, info_text)

# Punto de entrada principal del programa
if __name__ == '__main__':
    print("Iniciando Sistema de Perceptrón con Mesa Framework...")
    PerceptronUserInterface()