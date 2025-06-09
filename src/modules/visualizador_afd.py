import tkinter as tk
from tkinter import ttk, scrolledtext

class AFDVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Visualizador de Matrices AFD")
        self.root.geometry("1000x700")
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña para tarjetas
        self.tab_tarjeta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tarjeta, text='Tarjetas de Crédito')
        self.create_tarjeta_tab()
        
        # Pestaña para CURP
        self.tab_curp = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_curp, text='CURP')
        self.create_curp_tab()
        
        # Botón de salida
        btn_salir = ttk.Button(self.root, text="Salir", command=self.root.quit)
        btn_salir.pack(pady=10)
    
    def create_tarjeta_tab(self):
        # Frame principal
        main_frame = ttk.Frame(self.tab_tarjeta)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Matriz de Transición - Tarjetas de Crédito", 
                         font=('Arial', 12, 'bold'))
        title.pack(pady=10)
        
        # Texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_tarjeta = tk.Text(text_frame, wrap=tk.NONE, 
                                   yscrollcommand=scrollbar.set,
                                   font=('Courier New', 10),
                                   padx=10, pady=10)
        self.text_tarjeta.pack(fill='both', expand=True)
        scrollbar.config(command=self.text_tarjeta.yview)
        
        # Configurar tags para colores
        self.text_tarjeta.tag_configure('estado', foreground='blue', font=('Courier New', 10, 'bold'))
        self.text_tarjeta.tag_configure('transicion', foreground='green')
        self.text_tarjeta.tag_configure('bloqueado', foreground='red')
        
        # Información sobre el AFD
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=10)
        
        info = """
        AFD para tarjetas (Σ, Q, q0, F, δ):
        - Σ = {dígitos 0-9, espacio, '/'}
        - Q = {q0, q1, ..., q29} (30 estados)
        - q0 = estado inicial
        - F = {q29} (estado de aceptación)
        """
        ttk.Label(info_frame, text=info, justify=tk.LEFT).pack(anchor='w')
    
    def create_curp_tab(self):
        # Frame principal
        main_frame = ttk.Frame(self.tab_curp)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Matriz de Transición - CURP", 
                         font=('Arial', 12, 'bold'))
        title.pack(pady=10)
        
        # Texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_curp = tk.Text(text_frame, wrap=tk.NONE, 
                                yscrollcommand=scrollbar.set,
                                font=('Courier New', 10),
                                padx=10, pady=10)
        self.text_curp.pack(fill='both', expand=True)
        scrollbar.config(command=self.text_curp.yview)
        
        # Configurar tags para colores
        self.text_curp.tag_configure('estado', foreground='blue', font=('Courier New', 10, 'bold'))
        self.text_curp.tag_configure('transicion', foreground='green')
        self.text_curp.tag_configure('bloqueado', foreground='red')
        
        # Información sobre el AFD
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=10)
        
        info = """
        AFD para CURPs (Σ, Q, q0, F, δ):
        - Σ = {letras A-Z, dígitos 0-9}
        - Q = {q0, q1, ..., q18} (19 estados)
        - q0 = estado inicial
        - F = {q18} (estado de aceptación)
        """
        ttk.Label(info_frame, text=info, justify=tk.LEFT).pack(anchor='w')
    
    def display_matriz_tarjeta(self, matriz):
        self.text_tarjeta.delete(1.0, tk.END)
        
        # Encabezados de columnas
        headers = ["Estado", "Dígito", "Espacio", "/", "Otro"]
        header_line = " | ".join(f"{h:^15}" for h in headers)
        self.text_tarjeta.insert(tk.END, f"{header_line}\n")
        self.text_tarjeta.insert(tk.END, "-"*len(header_line) + "\n")
        
        # Filas de la matriz
        for estado, transiciones in matriz.items():
            self.text_tarjeta.insert(tk.END, f"{estado:^15}", 'estado')
            
            for simbolo in ['digito', 'espacio', '/', 'otro']:
                destino = transiciones.get(simbolo, None)
                if destino is None:
                    self.text_tarjeta.insert(tk.END, f"{'Bloqueado':^15}", 'bloqueado')
                else:
                    self.text_tarjeta.insert(tk.END, f"{destino:^15}", 'transicion')
                
                self.text_tarjeta.insert(tk.END, " | ")
            
            self.text_tarjeta.insert(tk.END, "\n")
    
    def display_matriz_curp(self, matriz):
        self.text_curp.delete(1.0, tk.END)
        
        # Encabezados de columnas
        headers = ["Estado", "Letra", "Dígito", "Sexo", "Otro"]
        header_line = " | ".join(f"{h:^15}" for h in headers)
        self.text_curp.insert(tk.END, f"{header_line}\n")
        self.text_curp.insert(tk.END, "-"*len(header_line) + "\n")
        
        # Filas de la matriz
        for estado, transiciones in matriz.items():
            self.text_curp.insert(tk.END, f"{estado:^15}", 'estado')
            
            for simbolo in ['letra', 'digito', 'sexo', 'otro']:
                destino = transiciones.get(simbolo, None)
                if destino is None:
                    self.text_curp.insert(tk.END, f"{'Bloqueado':^15}", 'bloqueado')
                else:
                    self.text_curp.insert(tk.END, f"{destino:^15}", 'transicion')
                
                self.text_curp.insert(tk.END, " | ")
            
            self.text_curp.insert(tk.END, "\n")
    
    def run(self, tipo_afd, validador):
        if tipo_afd == "tarjeta" or tipo_afd == "ambos":
            self.display_matriz_tarjeta(validador.matriz_transiciones_tarjeta)
        
        if tipo_afd == "curp" or tipo_afd == "ambos":
            self.display_matriz_curp(validador.matriz_transiciones_curp)
        
        self.root.mainloop()