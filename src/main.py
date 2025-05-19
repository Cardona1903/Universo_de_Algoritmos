import sys
from utils.matrix_loader import load_universe_data, print_universe_info
from utils.path_finder import NaveEspacial

def main():
    # Cargar datos del universo
    try:
        data = load_universe_data('../data/matriz_universo.json')
        print_universe_info(data)
    except FileNotFoundError:
        print("Error: No se encontró el archivo JSON.")
        sys.exit(1)
    
    # Crear la nave espacial
    nave = NaveEspacial(data)
    
    # Iniciar desde el origen
    inicio_fila, inicio_col = data['origen']
    
    print("\nIniciando búsqueda de ruta...")
    if nave.resolver(inicio_fila, inicio_col):
        print("\n¡Ruta encontrada!")
        print(f"Carga final: {nave.carga_actual}")
        print("Camino:")
        for paso in nave.camino_actual:
            print(paso)
    else:
        print("\nNo se encontró una ruta válida.")
    
    if nave.caminos_validos:
        print(f"\nSe encontraron {len(nave.caminos_validos)} rutas válidas.")
        for i, camino in enumerate(nave.caminos_validos, 1):
            print(f"\nRuta {i}:")
            print(" -> ".join(str(paso) for paso in camino))

if __name__ == "__main__":
    main()