
import random
import re
import threading
import time
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import operator
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

# Clases de agentes mantienen su estructura original
class CommunicationMessage:
    """
    Clase que encapsula los mensajes intercambiados entre agentes.
    Incluye metadatos para trazabilidad y control de flujo.
    """
    def __init__(self, origin_agent, destination_agent, message_category, payload, creation_time=None):
        self.origin_agent = origin_agent
        self.destination_agent = destination_agent
        self.message_category = message_category
        self.payload = payload
        self.creation_time = creation_time or time.time()
        self.is_processed = False

class InterAgentMessageQueue:
    """
    Sistema de cola de mensajes para coordinar la comunicación asíncrona
    entre todos los agentes del sistema distribuido.
    """
    def __init__(self):
        self.message_buffer = deque() # Cola principal de mensajes
        self.communication_log = [] # Historial completo de mensajes

    def dispatch_message(self, message):
        """
        Envía un mensaje al sistema añadiéndolo a la cola y registro.
        """
        self.message_buffer.append(message)
        self.communication_log.append(message)

    def retrieve_agent_messages(self, target_agent_id):
        """
        Extrae y devuelve todos los mensajes pendientes para un agente específico.
        """
        agent_messages = []
        remaining_messages = deque()

        # Procesamiento de toda la cola de mensajes
        while self.message_buffer:
            current_message = self.message_buffer.popleft()
            if (current_message.destination_agent == target_agent_id and
                not current_message.is_processed):
                agent_messages.append(current_message)
                current_message.is_processed = True
            else:
                remaining_messages.append(current_message)

        # Restauración de mensajes no procesados
        self.message_buffer = remaining_messages
        return agent_messages

class InputOutputAgent(Agent):
    """
    Agente responsable de la interfaz con el usuario.
    Recibe expresiones matemáticas y presenta resultados finales.
    """
    def __init__(self, agent_id, model):
        super().__init__(agent_id, model)
        self.mathematical_expression = ""
        self.computed_result = None
        self.processing_state = "idle" # Estados: idle, processing, completed

    def process_expression(self, user_expression):
        """
        Inicia el procesamiento de una expresión matemática del usuario.
        """
        self.mathematical_expression = user_expression
        self.computed_result = None
        self.processing_state = "processing"

        # Envío del mensaje al agente parser para análisis
        parsing_request = CommunicationMessage(
            self.unique_id, 1, "expression_parsing_request",
            {"mathematical_expression": user_expression}
        )
        self.model.message_system.dispatch_message(parsing_request)

    def step(self):
        """
        Procesa mensajes entrantes durante cada paso de simulación.
        """
        incoming_messages = self.model.message_system.retrieve_agent_messages(self.unique_id)
        for message in incoming_messages:
            if message.message_category == "computation_complete":
                self.computed_result = message.payload["final_result"]
                self.processing_state = "completed"

class MathematicalParserAgent(Agent):
    """
    Agente especializado en análisis sintáctico de expresiones matemáticas.
    Convierte notación infija a postfija y coordina operaciones distribuidas.
    """
    def __init__(self, agent_id, model):
        super().__init__(agent_id, model)
        # Tabla de precedencia de operadores matemáticos
        self.operator_precedence = {
            '^': 3, # Exponenciación (máxima precedencia)
            '*': 2, # Multiplicación
            '/': 2, # División
            '+': 1, # Suma
            '-': 1  # Resta (mínima precedencia)
        }
        # Control de operaciones pendientes y resultados
        self.operation_queue = []
        self.intermediate_results = {}

    def tokenize_expression(self, math_expression):
        """
        Descompone una expresión matemática en tokens individuales.
        Reconoce números decimales, operadores y paréntesis.
        """
        # Expresión regular para capturar números y operadores
        token_pattern = r'\d*\.?\d+|[+\-*/^()]'
        tokens = re.findall(token_pattern, math_expression.replace(' ', ''))
        return tokens

    def convert_to_postfix(self, token_list):
        """
        Implementa el algoritmo Shunting Yard para conversión a notación postfija.
        """
        output_queue = []
        operator_stack = []

        for current_token in token_list:
            # Procesamiento de números
            if re.match(r'\d*\.?\d+', current_token):
                output_queue.append(float(current_token))

            # Procesamiento de operadores
            elif current_token in self.operator_precedence:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.operator_precedence and
                       self.operator_precedence[operator_stack[-1]] >= 
                       self.operator_precedence[current_token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(current_token)

            # Procesamiento de paréntesis
            elif current_token == '(':
                operator_stack.append(current_token)

            elif current_token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop() # Remover '('

        # Vaciado de la pila de operadores
        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    def step(self):
        """
        Procesa mensajes y coordina el análisis de expresiones.
        """
        incoming_messages = self.model.message_system.retrieve_agent_messages(self.unique_id)
        for message in incoming_messages:
            if message.message_category == "expression_parsing_request":
                expression = message.payload["mathematical_expression"]
                self.analyze_expression(expression)
            elif message.message_category == "operation_completed":
                operation_id = message.payload["operation_identifier"]
                result_value = message.payload["computed_value"]
                self.intermediate_results[operation_id] = result_value
                self.verify_completion_status()

    def analyze_expression(self, expression):
        """
        Analiza completamente una expresión y coordina su evaluación.
        """
        try:
            # Tokenización y conversión a postfijo
            token_sequence = self.tokenize_expression(expression)
            postfix_notation = self.convert_to_postfix(token_sequence)
            self.evaluate_postfix_expression(postfix_notation)
        except Exception as parsing_error:
            # Envío de error al agente de entrada/salida
            error_message = CommunicationMessage(
                self.unique_id, 0, "computation_complete",
                {"final_result": f"Error de análisis: {parsing_error}"}
            )
            self.model.message_system.dispatch_message(error_message)

    def evaluate_postfix_expression(self, postfix_tokens):
        """
        Evalúa una expresión en notación postfija utilizando agentes especializados.
        """
        evaluation_stack = []
        operation_counter = 0

        for token in postfix_tokens:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:
                # Verificación de operandos suficientes
                if len(evaluation_stack) < 2:
                    raise ValueError("Expresión matemática mal formada")

                # Extracción de operandos
                second_operand = evaluation_stack.pop()
                first_operand = evaluation_stack.pop()

                # Generación de identificador único para la operación
                operation_id = f"calc_op_{operation_counter}"
                operation_counter += 1

                # Determinación del agente responsable
                responsible_agent = self.determine_operation_agent(token)

                # Envío de solicitud de operación
                operation_request = CommunicationMessage(
                    self.unique_id, responsible_agent, "execute_operation",
                    {
                        "operation_identifier": operation_id,
                        "mathematical_operator": token,
                        "first_value": first_operand,
                        "second_value": second_operand
                    }
                )
                self.model.message_system.dispatch_message(operation_request)
                self.operation_queue.append(operation_id)
                evaluation_stack.append(operation_id) # Placeholder para resultado

        # Almacenamiento del identificador del resultado final
        self.final_operation_id = evaluation_stack[0] if evaluation_stack else None

    def determine_operation_agent(self, operator_symbol):
        """
        Mapea operadores matemáticos a sus agentes especializados correspondientes.
        """
        agent_mapping = {
            '+': 2, # AgenteSuma
            '-': 3, # AgenteResta
            '*': 4, # AgenteMultiplicacion
            '/': 5, # AgenteDivision
            '^': 6  # AgentePotencia
        }
        return agent_mapping.get(operator_symbol, 2)

    def verify_completion_status(self):
        """
        Verifica si todas las operaciones han sido completadas y envía el resultado final.
        """
        if not self.operation_queue:
            return

        # Verificación de que todas las operaciones estén completas
        all_operations_complete = all(
            op_id in self.intermediate_results
            for op_id in self.operation_queue
        )

        if all_operations_complete:
            # Obtención del resultado final
            final_result = self.intermediate_results[self.operation_queue[-1]]

            # Envío del resultado al agente de entrada/salida
            completion_message = CommunicationMessage(
                self.unique_id, 0, "computation_complete",
                {"final_result": final_result}
            )
            self.model.message_system.dispatch_message(completion_message)

            # Limpieza de estado
            self.operation_queue.clear()
            self.intermediate_results.clear()

class SpecializedOperationAgent(Agent):
    """
    Agente base para operaciones matemáticas especializadas.
    Cada instancia maneja un tipo específico de operación aritmética.
    """
    def __init__(self, agent_id, model, operation_description, mathematical_function):
        super().__init__(agent_id, model)
        self.operation_description = operation_description
        self.mathematical_function = mathematical_function
        self.operations_count = 0 # Contador de operaciones realizadas

    def step(self):
        """
        Procesa solicitudes de operaciones matemáticas.
        """
        pending_messages = self.model.message_system.retrieve_agent_messages(self.unique_id)
        for message in pending_messages:
            if message.message_category == "execute_operation":
                self.compute_operation(message.payload)

    def compute_operation(self, operation_data):
        """
        Ejecuta la operación matemática específica y devuelve el resultado.
        """
        first_value = operation_data["first_value"]
        second_value = operation_data["second_value"]
        operation_id = operation_data["operation_identifier"]

        try:
            # Cálculo utilizando la función matemática asignada
            computation_result = self.mathematical_function(first_value, second_value)
        except Exception:
            # Manejo de errores (división por cero, overflow, etc.)
            computation_result = float('inf')

        # Incremento del contador de operaciones
        self.operations_count += 1

        # Envío del resultado al agente parser
        result_message = CommunicationMessage(
            self.unique_id, 1, "operation_completed",
            {
                "operation_identifier": operation_id,
                "computed_value": computation_result
            }
        )
        self.model.message_system.dispatch_message(result_message)

class DistributedCalculatorModel(Model):
    """
    Modelo principal que coordina el sistema completo de calculadora distribuida.
    Gestiona todos los agentes y el sistema de mensajería.
    """
    def __init__(self):
        super().__init__()

        # Inicialización del sistema de comunicación
        self.message_system = InterAgentMessageQueue()
        self.schedule = RandomActivation(self)

        # Creación de agentes del sistema
        self.input_output_agent = InputOutputAgent(0, self)
        self.mathematical_parser = MathematicalParserAgent(1, self)

        # Registro de agentes principales
        self.schedule.add(self.input_output_agent)
        self.schedule.add(self.mathematical_parser)

        # Creación de agentes de operaciones especializadas
        self.addition_agent = SpecializedOperationAgent(2, self, "Adición", operator.add)
        self.subtraction_agent = SpecializedOperationAgent(3, self, "Sustracción", operator.sub)
        self.multiplication_agent = SpecializedOperationAgent(4, self, "Multiplicación", operator.mul)

        # Agente de división con manejo especial de división por cero
        division_function = lambda a, b: a / b if abs(b) > 1e-15 else float('inf')
        self.division_agent = SpecializedOperationAgent(5, self, "División", division_function)
        self.exponentiation_agent = SpecializedOperationAgent(6, self, "Exponenciación", operator.pow)

        # Registro de todos los agentes de operaciones
        operation_agents = [
            self.addition_agent, self.subtraction_agent, self.multiplication_agent,
            self.division_agent, self.exponentiation_agent
        ]
        for agent in operation_agents:
            self.schedule.add(agent)

    def compute_mathematical_expression(self, user_expression):
        """
        Método principal para procesar expresiones matemáticas del usuario.
        """
        self.input_output_agent.process_expression(user_expression)

        # Ejecución del sistema hasta completar el cálculo
        while self.input_output_agent.processing_state == "processing":
            self.step()

        return self.input_output_agent.computed_result

    def step(self):
        """
        Ejecuta un paso de simulación para todos los agentes.
        """
        self.schedule.step()

# NUEVA INTERFAZ GRÁFICA MEJORADA
class ModernCalculatorGUI:
    """
    Interfaz gráfica moderna y mejorada para la calculadora distribuida.
    Diseño más atractivo con mejor organización y experiencia de usuario.
    """

    def __init__(self):
        self.calculator_model = DistributedCalculatorModel()
        self.setup_styles()
        self.create_main_interface()

    def setup_styles(self):
        """
        Configura estilos modernos para todos los widgets ttk.
        """
        style = ttk.Style()

        # Configuración del tema base
        style.theme_use('clam')

        # Colores principales
        self.colors = {
            'primary': '#2E86C1',
            'secondary': '#28B463', 
            'accent': '#F39C12',
            'success': '#27AE60',
            'warning': '#E74C3C',
            'dark': '#2C3E50',
            'light': '#ECF0F1',
            'white': '#FFFFFF'
        }

        # Estilos personalizados
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), foreground=self.colors['dark'])
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'), foreground=self.colors['primary'])
        style.configure('Info.TLabel', font=('Segoe UI', 10), foreground=self.colors['dark'])
        style.configure('Result.TLabel', font=('Segoe UI', 14, 'bold'), 
                       foreground=self.colors['success'], background=self.colors['light'])

        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Warning.TButton', font=('Segoe UI', 10, 'bold'))

    def create_main_interface(self):
        """
        Crea la interfaz principal con diseño moderno y organizado.
        """
        # Ventana principal
        self.root = tk.Tk()
        self.root.title("🧮 Calculadora Distribuida Multi-Agente")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.colors['light'])

        # Configuración de grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Container principal con padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=2)
        main_container.grid_columnconfigure(1, weight=1)

        # Header
        self.create_header(main_container)

        # Panel principal dividido en dos columnas
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_rowconfigure(2, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        right_panel = ttk.Frame(main_container)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Componentes del panel izquierdo
        self.create_input_section(left_panel)
        self.create_result_section(left_panel)
        self.create_communication_section(left_panel)

        # Componentes del panel derecho  
        self.create_statistics_section(right_panel)
        self.create_history_section(right_panel)
        self.create_help_section(right_panel)

        # Footer
        self.create_footer(main_container)

    def create_header(self, parent):
        """
        Crea el encabezado principal con título y descripción.
        """
        header_frame = ttk.Frame(parent, padding="0 0 20 0")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Título principal
        title_label = ttk.Label(header_frame, text="🧮 Calculadora Distribuida Multi-Agente", 
                              style="Title.TLabel")
        title_label.pack(anchor="center", pady=(0, 5))

        # Descripción
        desc_label = ttk.Label(header_frame, 
                             text="Sistema inteligente de cálculo basado en arquitectura de agentes especializados",
                             style="Info.TLabel")
        desc_label.pack(anchor="center")

        # Separador
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=10)

    def create_input_section(self, parent):
        """
        Crea la sección de entrada de expresiones con diseño mejorado.
        """
        input_frame = ttk.LabelFrame(parent, text="📝 Entrada de Expresión", padding="15")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        input_frame.grid_columnconfigure(1, weight=1)

        # Campo de entrada con mejor estilo
        ttk.Label(input_frame, text="Expresión:", style="Info.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.expression_var = tk.StringVar(value="3 ^ 2 + 5 * 4 - 2 / 2")
        entry_frame = ttk.Frame(input_frame)
        entry_frame.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 10))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.expression_entry = ttk.Entry(entry_frame, textvariable=self.expression_var, 
                                        font=('Consolas', 12), width=50)
        self.expression_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.expression_entry.bind('<Return>', lambda e: self.evaluate_expression())

        # Botones de acción con mejor diseño
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        eval_btn = ttk.Button(button_frame, text="🚀 Evaluar", 
                            command=self.evaluate_expression, style="Primary.TButton")
        eval_btn.pack(side="left", padx=(0, 10))

        clear_btn = ttk.Button(button_frame, text="🧹 Limpiar Todo", 
                             command=self.clear_all, style="Warning.TButton")
        clear_btn.pack(side="left", padx=(0, 10))

        examples_btn = ttk.Button(button_frame, text="💡 Ejemplos", 
                                command=self.show_examples, style="Success.TButton")
        examples_btn.pack(side="left")

    def create_result_section(self, parent):
        """
        Crea la sección de resultados con mejor presentación.
        """
        result_frame = ttk.LabelFrame(parent, text="🎯 Resultado", padding="15")
        result_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Frame interno para el resultado con fondo destacado
        result_inner = tk.Frame(result_frame, bg=self.colors['light'], 
                              relief="sunken", bd=2)
        result_inner.pack(fill="x", pady=5)

        self.result_var = tk.StringVar(value="🔄 Ingrese una expresión y presione Evaluar")
        self.result_label = tk.Label(result_inner, textvariable=self.result_var, 
                                   font=('Consolas', 12, 'bold'), 
                                   bg=self.colors['light'], fg=self.colors['success'],
                                   pady=10, wraplength=600)
        self.result_label.pack()

    def create_communication_section(self, parent):
        """
        Crea la sección de comunicación entre agentes con mejor visualización.
        """
        comm_frame = ttk.LabelFrame(parent, text="📡 Comunicación Inter-Agente", padding="10")
        comm_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        comm_frame.grid_rowconfigure(1, weight=1)
        comm_frame.grid_columnconfigure(0, weight=1)

        # Controles superiores
        controls_frame = ttk.Frame(comm_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(controls_frame, text="Monitor de actividad:", style="Info.TLabel").pack(side="left")

        clear_comm_btn = ttk.Button(controls_frame, text="🗑️ Limpiar Log", 
                                  command=self.clear_communication_log)
        clear_comm_btn.pack(side="right")

        # Área de texto mejorada
        text_frame = ttk.Frame(comm_frame)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.comm_text = scrolledtext.ScrolledText(text_frame, height=15, 
                                                 font=('Consolas', 9), wrap=tk.WORD,
                                                 bg='#FAFAFA', fg=self.colors['dark'])
        self.comm_text.grid(row=0, column=0, sticky="nsew")

        # Configuración de tags para coloreado
        self.comm_text.tag_config('agent_name', foreground=self.colors['primary'], font=('Consolas', 9, 'bold'))
        self.comm_text.tag_config('operation', foreground=self.colors['accent'], font=('Consolas', 9, 'bold'))
        self.comm_text.tag_config('result', foreground=self.colors['success'], font=('Consolas', 9, 'bold'))
        self.comm_text.tag_config('error', foreground=self.colors['warning'], font=('Consolas', 9, 'bold'))

    def create_statistics_section(self, parent):
        """
        Crea la sección de estadísticas del sistema con gráficos.
        """
        stats_frame = ttk.LabelFrame(parent, text="📊 Estadísticas del Sistema", padding="15")
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Métricas principales
        self.stats_var = tk.StringVar(value="📈 Mensajes: 0 | ⚡ Operaciones: 0 | ⏱️ Tiempo: 0.00s")
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_var, style="Info.TLabel")
        stats_label.pack(pady=5)

        # Indicadores visuales
        indicators_frame = ttk.Frame(stats_frame)
        indicators_frame.pack(fill="x", pady=(10, 0))

        # Barra de progreso (simulada)
        ttk.Label(indicators_frame, text="Actividad:", style="Info.TLabel").pack(anchor="w")
        self.activity_progress = ttk.Progressbar(indicators_frame, mode='determinate', length=200)
        self.activity_progress.pack(fill="x", pady=5)

    def create_history_section(self, parent):
        """
        Crea la sección de historial de cálculos.
        """
        history_frame = ttk.LabelFrame(parent, text="📚 Historial de Cálculos", padding="10")
        history_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        history_frame.grid_rowconfigure(1, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)

        # Controles del historial
        hist_controls = ttk.Frame(history_frame)
        hist_controls.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(hist_controls, text="Últimos cálculos:", style="Info.TLabel").pack(side="left")

        clear_hist_btn = ttk.Button(hist_controls, text="🗑️ Limpiar", 
                                  command=self.clear_history)
        clear_hist_btn.pack(side="right")

        # Lista de historial
        hist_frame = ttk.Frame(history_frame)
        hist_frame.grid(row=1, column=0, sticky="nsew")
        hist_frame.grid_rowconfigure(0, weight=1)
        hist_frame.grid_columnconfigure(0, weight=1)

        # Crear Treeview para mejor presentación del historial
        self.history_tree = ttk.Treeview(hist_frame, columns=('expression', 'result'), 
                                       show='headings', height=8)
        self.history_tree.heading('expression', text='Expresión')
        self.history_tree.heading('result', text='Resultado')
        self.history_tree.column('expression', width=200)
        self.history_tree.column('result', width=100)
        self.history_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el historial
        hist_scroll = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history_tree.yview)
        hist_scroll.grid(row=0, column=1, sticky="ns")
        self.history_tree.configure(yscrollcommand=hist_scroll.set)

        # Inicializar historial
        self.calculation_history = []

    def create_help_section(self, parent):
        """
        Crea la sección de ayuda y información.
        """
        help_frame = ttk.LabelFrame(parent, text="❓ Ayuda y Ejemplos", padding="15")
        help_frame.grid(row=2, column=0, sticky="ew")

        help_text = """
🔢 Operadores soportados:
  + Suma        - Resta
  * Multiplicación  / División  
  ^ Potenciación    ( ) Paréntesis

💡 Ejemplos:
  • 3 + 4 * 2
  • (5 - 3) ^ 2  
  • 10 / 2 + 3 * 4
  • 2 ^ 3 + 4 ^ 2
        """

        help_label = ttk.Label(help_frame, text=help_text, style="Info.TLabel", 
                             justify="left", font=('Segoe UI', 9))
        help_label.pack(anchor="w")

    def create_footer(self, parent):
        """
        Crea el footer con información del sistema.
        """
        footer_frame = ttk.Frame(parent, padding="10 10 0 0")
        footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        ttk.Separator(footer_frame, orient="horizontal").pack(fill="x", pady=(0, 10))

        footer_text = "🤖 Sistema Multi-Agente | 🎯 Mesa Framework v0.8.9 | ⚡ Procesamiento Distribuido"
        ttk.Label(footer_frame, text=footer_text, style="Info.TLabel").pack(anchor="center")

    def evaluate_expression(self):
        """
        Evalúa la expresión con indicadores visuales de progreso.
        """
        expression = self.expression_var.get().strip()
        if not expression:
            messagebox.showwarning("Entrada vacía", "Por favor ingrese una expresión matemática.")
            return

        # Limpiar comunicación anterior
        self.comm_text.delete(1.0, tk.END)

        # Indicador de procesamiento
        self.result_var.set("🔄 Procesando expresión...")
        self.activity_progress.start()
        self.root.update()

        try:
            # Reinicializar modelo
            self.calculator_model = DistributedCalculatorModel()

            # Registrar inicio
            start_time = time.time()
            self.log_communication(f"🚀 Iniciando evaluación: {expression}\n{'='*50}\n", 'operation')

            # Procesar expresión
            result = self.calculator_model.compute_mathematical_expression(expression)

            # Calcular tiempo
            end_time = time.time()
            processing_time = end_time - start_time

            # Actualizar resultado
            if result is not None:
                self.result_var.set(f"✅ {expression} = {result}")
                self.add_to_history(expression, str(result))
                self.log_communication(f"\n🎯 Resultado final: {result}", 'result')
            else:
                self.result_var.set("❌ Error en la evaluación")
                self.log_communication("\n❌ Error durante el procesamiento", 'error')

            # Actualizar estadísticas y comunicación
            self.update_statistics(processing_time)
            self.display_communication_log()

        except Exception as e:
            self.result_var.set(f"❌ Error: {str(e)}")
            self.log_communication(f"\n❌ Error crítico: {str(e)}", 'error')

        finally:
            self.activity_progress.stop()

    def update_statistics(self, processing_time):
        """
        Actualiza las estadísticas del sistema.
        """
        total_messages = len(self.calculator_model.message_system.communication_log)

        operation_agents = [
            self.calculator_model.addition_agent,
            self.calculator_model.subtraction_agent,
            self.calculator_model.multiplication_agent,
            self.calculator_model.division_agent,
            self.calculator_model.exponentiation_agent
        ]

        total_operations = sum(agent.operations_count for agent in operation_agents)

        stats_text = f"📈 Mensajes: {total_messages} | ⚡ Operaciones: {total_operations} | ⏱️ Tiempo: {processing_time:.3f}s"
        self.stats_var.set(stats_text)

        # Actualizar barra de progreso basada en actividad
        activity_level = min(100, (total_messages + total_operations) * 10)
        self.activity_progress['value'] = activity_level

    def display_communication_log(self):
        """
        Muestra el log de comunicación con colores y formato mejorado.
        """
        agent_names = {
            0: "🔌 AgenteEntradaSalida", 1: "🧠 AgenteAnalizador",
            2: "➕ AgenteSuma", 3: "➖ AgenteResta", 4: "✖️ AgenteMultiplicacion",
            5: "➗ AgenteDivision", 6: "🔺 AgentePotencia"
        }

        for idx, message in enumerate(self.calculator_model.message_system.communication_log, 1):
            sender = agent_names.get(message.origin_agent, f"Agente_{message.origin_agent}")
            receiver = agent_names.get(message.destination_agent, f"Agente_{message.destination_agent}")

            # Encabezado del mensaje
            self.log_communication(f"{idx:2d}. {sender} → {receiver}\n", 'agent_name')
            self.log_communication(f"    📋 Categoría: {message.message_category}\n", 'info')

            # Detalles específicos
            if message.message_category == "execute_operation":
                payload = message.payload
                operation_text = f"    🔢 Operación: {payload['first_value']} {payload['mathematical_operator']} {payload['second_value']}\n"
                self.log_communication(operation_text, 'operation')

            elif message.message_category in ("operation_completed", "computation_complete"):
                result_value = message.payload.get('computed_value', message.payload.get('final_result'))
                result_text = f"    ✅ Resultado: {result_value}\n"
                self.log_communication(result_text, 'result')

            self.log_communication("\n")

        self.comm_text.see(tk.END)

    def log_communication(self, text, tag=None):
        """
        Añade texto al log de comunicación con formato.
        """
        if tag:
            self.comm_text.insert(tk.END, text, tag)
        else:
            self.comm_text.insert(tk.END, text)

    def add_to_history(self, expression, result):
        """
        Añade un cálculo al historial.
        """
        self.calculation_history.append((expression, result))
        self.history_tree.insert('', 0, values=(expression, result))

        # Mantener solo los últimos 20 cálculos
        if len(self.calculation_history) > 20:
            self.calculation_history.pop(0)
            # Remover el último elemento del treeview
            items = self.history_tree.get_children()
            if items:
                self.history_tree.delete(items[-1])

    def show_examples(self):
        """
        Muestra ejemplos de expresiones en un popup.
        """
        examples = [
            "3 + 4 * 2",
            "(5 - 3) ^ 2", 
            "10 / 2 + 3 * 4",
            "2 ^ 3 + 4 ^ 2",
            "((3 + 4) * 2) - 1",
            "5 ^ 2 / 5 + 3"
        ]

        examples_window = tk.Toplevel(self.root)
        examples_window.title("💡 Ejemplos de Expresiones")
        examples_window.geometry("400x300")
        examples_window.transient(self.root)
        examples_window.grab_set()

        ttk.Label(examples_window, text="Seleccione un ejemplo:", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=10)

        for example in examples:
            btn = ttk.Button(examples_window, text=example, 
                           command=lambda e=example: self.use_example(e, examples_window))
            btn.pack(pady=5, padx=20, fill="x")

    def use_example(self, example, window):
        """
        Usa un ejemplo seleccionado.
        """
        self.expression_var.set(example)
        window.destroy()

    def clear_all(self):
        """
        Limpia toda la interfaz.
        """
        self.expression_var.set("")
        self.result_var.set("🔄 Ingrese una expresión y presione Evaluar")
        self.comm_text.delete(1.0, tk.END)
        self.stats_var.set("📈 Mensajes: 0 | ⚡ Operaciones: 0 | ⏱️ Tiempo: 0.00s")
        self.activity_progress['value'] = 0

    def clear_communication_log(self):
        """
        Limpia solo el log de comunicación.
        """
        self.comm_text.delete(1.0, tk.END)

    def clear_history(self):
        """
        Limpia el historial de cálculos.
        """
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.calculation_history.clear()

    def run(self):
        """
        Inicia la aplicación.
        """
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """
        Maneja el cierre de la aplicación.
        """
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()

def main():
    """
    Función principal para inicializar la aplicación.
    """
    print("🧮 SISTEMA DE CALCULADORA DISTRIBUIDA MULTI-AGENTE")
    print("=" * 55)
    print("🚀 Interfaz Gráfica Moderna - Mesa Framework v0.8.9")
    print("⚡ Inicializando aplicación...")

    try:
        app = ModernCalculatorGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
