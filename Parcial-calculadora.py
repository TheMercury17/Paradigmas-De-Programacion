# Sistema de calculadora distribuida basada en agentes usando Mesa Framework
import random
import re
import threading
import time
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import operator
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

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
        self.message_buffer = deque()  # Cola principal de mensajes
        self.communication_log = []    # Historial completo de mensajes

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
        self.processing_state = "idle"  # Estados: idle, processing, completed
    
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
            '^': 3,    # Exponenciación (máxima precedencia)
            '*': 2,    # Multiplicación
            '/': 2,    # División  
            '+': 1,    # Suma
            '-': 1     # Resta (mínima precedencia)
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
                    operator_stack.pop()  # Remover '('
        
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
                evaluation_stack.append(operation_id)  # Placeholder para resultado
        
        # Almacenamiento del identificador del resultado final
        self.final_operation_id = evaluation_stack[0] if evaluation_stack else None
    
    def determine_operation_agent(self, operator_symbol):
        """
        Mapea operadores matemáticos a sus agentes especializados correspondientes.
        """
        agent_mapping = {
            '+': 2,  # AgenteSuma
            '-': 3,  # AgenteResta  
            '*': 4,  # AgenteMultiplicacion
            '/': 5,  # AgenteDivision
            '^': 6   # AgentePotencia
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
        self.operations_count = 0  # Contador de operaciones realizadas
    
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

class CalculatorGraphicalInterface:
    """
    Interfaz gráfica principal para interactuar con el sistema de calculadora distribuida.
    """
    def __init__(self):
        self.calculator_model = DistributedCalculatorModel()
        self.initialize_user_interface()
    
    def initialize_user_interface(self):
        """
        Configura todos los elementos de la interfaz gráfica de usuario.
        """
        # Ventana principal
        self.main_window = tk.Tk()
        self.main_window.title("Sistema de Calculadora Distribuida - Arquitectura Multi-Agente")
        self.main_window.geometry("1200x800")
        
        # Contenedor principal
        primary_container = ttk.Frame(self.main_window)
        primary_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel de entrada de expresiones
        expression_panel = ttk.LabelFrame(primary_container, text="Entrada de Expresión Matemática")
        expression_panel.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(expression_panel, text="Expresión a evaluar:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.expression_input = tk.StringVar(value="3 ^ 2 + 5 * 4")
        ttk.Entry(expression_panel, textvariable=self.expression_input, width=35).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(expression_panel, text="Evaluar", command=self.evaluate_expression).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(expression_panel, text="Limpiar Todo", command=self.clear_interface).grid(row=0, column=3, padx=5, pady=5)
        
        # Panel de resultados
        result_panel = ttk.LabelFrame(primary_container, text="Resultado de la Evaluación")
        result_panel.pack(fill=tk.X, pady=(0, 10))
        
        self.result_display = tk.StringVar(value="Ingrese una expresión matemática y presione Evaluar")
        result_label = ttk.Label(result_panel, textvariable=self.result_display, font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        # Panel de comunicación entre agentes
        communication_panel = ttk.LabelFrame(primary_container, text="Registro de Comunicación Inter-Agente")
        communication_panel.pack(fill=tk.BOTH, expand=True)
        
        self.communication_display = scrolledtext.ScrolledText(
            communication_panel, height=15, wrap=tk.WORD, font=('Consolas', 9)
        )
        self.communication_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel de estadísticas del sistema
        statistics_panel = ttk.LabelFrame(primary_container, text="Métricas del Sistema")
        statistics_panel.pack(fill=tk.X, pady=(10, 0))
        
        self.statistics_display = tk.StringVar(value="Mensajes intercambiados: 0 | Operaciones ejecutadas: 0")
        ttk.Label(statistics_panel, textvariable=self.statistics_display).pack(pady=5)
    
    def evaluate_expression(self):
        """
        Procesa la expresión ingresada por el usuario utilizando el sistema distribuido.
        """
        user_expression = self.expression_input.get().strip()
        
        if not user_expression:
            return
        
        # Limpieza del display de comunicación
        self.communication_display.delete(1.0, tk.END)
        
        # Reinicialización del modelo para nuevo cálculo
        self.calculator_model = DistributedCalculatorModel()
        
        # Registro inicial en el display
        self.communication_display.insert(tk.END, f"Iniciando evaluación de: {user_expression}\n")
        self.communication_display.insert(tk.END, "=" * 60 + "\n\n")
        
        # Procesamiento de la expresión
        evaluation_result = self.calculator_model.compute_mathematical_expression(user_expression)
        
        # Actualización del resultado
        if evaluation_result is not None:
            self.result_display.set(f"{user_expression} = {evaluation_result}")
        else:
            self.result_display.set("Error durante la evaluación de la expresión")
        
        # Actualización de displays informativos
        self.display_communication_log()
        self.refresh_system_statistics()
    
    def clear_interface(self):
        """
        Limpia completamente la interfaz restaurando el estado inicial.
        """
        self.expression_input.set("")
        self.result_display.set("Ingrese una expresión matemática y presione Evaluar")
        self.communication_display.delete(1.0, tk.END)
        self.statistics_display.set("Mensajes intercambiados: 0 | Operaciones ejecutadas: 0")
    
    def display_communication_log(self):
        """
        Muestra el registro detallado de comunicación entre agentes.
        """
        # Mapeo de identificadores a nombres descriptivos
        agent_names = {
            0: "AgenteEntradaSalida", 1: "AgenteAnalizador",
            2: "AgenteSuma", 3: "AgenteResta", 4: "AgenteMultiplicacion",
            5: "AgenteDivision", 6: "AgentePotencia"
        }
        
        # Procesamiento del historial de mensajes
        for message_index, message in enumerate(self.calculator_model.message_system.communication_log, 1):
            sender_name = agent_names.get(message.origin_agent, f"Agente_{message.origin_agent}")
            receiver_name = agent_names.get(message.destination_agent, f"Agente_{message.destination_agent}")
            
            # Encabezado del mensaje
            self.communication_display.insert(tk.END, f"{message_index:2d}. {sender_name} → {receiver_name}\n")
            self.communication_display.insert(tk.END, f"    Categoría: {message.message_category}\n")
            
            # Detalles específicos según el tipo de mensaje
            if message.message_category == "execute_operation":
                payload = message.payload
                operation_detail = f"    Operación: {payload['first_value']} {payload['mathematical_operator']} {payload['second_value']}"
                self.communication_display.insert(tk.END, operation_detail + "\n")
            
            elif message.message_category in ("operation_completed", "computation_complete"):
                result_detail = f"    Resultado: {message.payload.get('computed_value', message.payload.get('final_result'))}"
                self.communication_display.insert(tk.END, result_detail + "\n")
            
            self.communication_display.insert(tk.END, "\n")
        
        # Desplazamiento automático al final
        self.communication_display.see(tk.END)
    
    def refresh_system_statistics(self):
        """
        Actualiza las métricas estadísticas del sistema.
        """
        total_messages = len(self.calculator_model.message_system.communication_log)
        
        # Cálculo del total de operaciones realizadas
        operation_agents = [
            self.calculator_model.addition_agent,
            self.calculator_model.subtraction_agent,
            self.calculator_model.multiplication_agent,
            self.calculator_model.division_agent,
            self.calculator_model.exponentiation_agent
        ]
        
        total_operations = sum(agent.operations_count for agent in operation_agents)
        
        # Actualización del display de estadísticas
        statistics_text = f"Mensajes intercambiados: {total_messages} | Operaciones ejecutadas: {total_operations}"
        self.statistics_display.set(statistics_text)
    
    def launch_application(self):
        """
        Inicia el bucle principal de la interfaz gráfica.
        """
        self.main_window.mainloop()

def initialize_application():
    """
    Función principal para inicializar y ejecutar la aplicación.
    """
    print("SISTEMA DE CALCULADORA DISTRIBUIDA BASADA EN MULTI-AGENTES")
    print("=" * 65)
    print("Framework Mesa v0.8.9 - Arquitectura de Agentes Especializados")
    print("Inicializando interfaz gráfica...")
    
    try:
        calculator_application = CalculatorGraphicalInterface()
        calculator_application.launch_application()
    except Exception as initialization_error:
        print(f"Error durante la inicialización: {initialization_error}")
        import traceback
        traceback.print_exc()

# Punto de entrada principal del programa
if __name__ == '__main__':
    initialize_application()