import sys
import os
from pathlib import Path
from modules.generar_matriz import generar_matriz_universo, guardar_matriz
from modules.mision_interestelar import Universo
from ui.interfaz import InterfazUniverso

def main():
    try:
        # Configuración inicial
        print("Iniciando el juego...")
        
        # Generar o cargar matriz
        os.makedirs("data", exist_ok=True)
        archivo_matriz = "data/matriz_universo.json"
        
        if not os.path.exists(archivo_matriz):
            print("Generando nueva matriz...")
            universo_data = generar_matriz_universo()
            guardar_matriz(universo_data, archivo_matriz)
        
        # Cargar universo
        print("Cargando universo...")
        universo = Universo(archivo_matriz)
        
        # Iniciar interfaz
        print("Iniciando interfaz gráfica...")
        interfaz = InterfazUniverso(universo)
        interfaz.ejecutar()
        
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()