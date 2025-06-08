import sys
import os
from pathlib import Path

# Asegurar que Python encuentre los módulos
sys.path.append(str(Path(__file__).parent))

try:
    from modules.generar_matriz import generar_matriz_universo, guardar_matriz
    from modules.mision_interestelar import Universo
    from ui.interfaz import InterfazUniverso
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Revisa la estructura de carpetas y los imports")
    sys.exit(1)

def main():
    # Generar nueva matriz aleatoria
    print("Generando universo aleatorio...")
    universo_data = generar_matriz_universo()
    
    # Asegurar que existe la carpeta data
    os.makedirs("data", exist_ok=True)
    guardar_matriz(universo_data, "data/matriz_universo.json")
    
    # Cargar el universo
    print("Cargando universo...")
    universo = Universo("data/matriz_universo.json")
    
    # Ejecutar interfaz
    print("Iniciando interfaz...")
    interfaz = InterfazUniverso(universo)
    interfaz.ejecutar()

if __name__ == "__main__":
    main()