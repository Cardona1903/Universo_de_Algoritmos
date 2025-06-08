import json
import random
from typing import List, Dict, Tuple

def generar_matriz_universo():
    # Configuración básica
    filas = 30
    columnas = 30
    origen = [0, 0]
    destino = [filas-1, columnas-1]
    carga_inicial = 200
    
    # Generar matriz inicial con valores aleatorios (0-10)
    matriz_inicial = [[random.randint(0, 10) for _ in range(columnas)] for _ in range(filas)]
    
    # Generar agujeros negros (5 posiciones aleatorias)
    agujeros_negros = []
    for _ in range(5):
        while True:
            fila = random.randint(0, filas-1)
            columna = random.randint(0, columnas-1)
            # No poner en origen/destino ni repetidos
            if [fila, columna] != origen and [fila, columna] != destino and [fila, columna] not in agujeros_negros:
                agujeros_negros.append([fila, columna])
                break
    
    # Generar estrellas gigantes (5 posiciones aleatorias)
    estrellas_gigantes = []
    for _ in range(5):
        while True:
            fila = random.randint(0, filas-1)
            columna = random.randint(0, columnas-1)
            # No poner en origen/destino/agujeros negros ni repetidos
            if ([fila, columna] != origen and [fila, columna] != destino and 
                [fila, columna] not in agujeros_negros and [fila, columna] not in estrellas_gigantes):
                estrellas_gigantes.append([fila, columna])
                break
    
    # Generar agujeros de gusano (3 pares entrada/salida)
    agujeros_gusano = []
    for _ in range(3):
        while True:
            # Entrada
            entrada_fila = random.randint(0, filas-1)
            entrada_col = random.randint(0, columnas-1)
            # Salida
            salida_fila = random.randint(0, filas-1)
            salida_col = random.randint(0, columnas-1)
            
            # Validar posiciones
            if ([entrada_fila, entrada_col] != origen and [entrada_fila, entrada_col] != destino and
                [entrada_fila, entrada_col] not in agujeros_negros and
                [entrada_fila, entrada_col] not in estrellas_gigantes and
                [salida_fila, salida_col] != origen and [salida_fila, salida_col] != destino and
                [entrada_fila, entrada_col] != [salida_fila, salida_col]):
                
                # Verificar que no se solapen con otros agujeros de gusano
                entrada_valida = True
                for ag in agujeros_gusano:
                    if [entrada_fila, entrada_col] == ag["entrada"] or [entrada_fila, entrada_col] == ag["salida"]:
                        entrada_valida = False
                    if [salida_fila, salida_col] == ag["entrada"] or [salida_fila, salida_col] == ag["salida"]:
                        entrada_valida = False
                
                if entrada_valida:
                    agujeros_gusano.append({
                        "entrada": [entrada_fila, entrada_col],
                        "salida": [salida_fila, salida_col]
                    })
                    break
    
    # Generar zonas de recarga (10 posiciones con factores 2-5)
    zonas_recarga = []
    for _ in range(10):
        while True:
            fila = random.randint(0, filas-1)
            columna = random.randint(0, columnas-1)
            factor = random.randint(2, 5)
            
            # Validar posición
            if ([fila, columna] != origen and [fila, columna] != destino and
                [fila, columna] not in agujeros_negros and
                [fila, columna] not in estrellas_gigantes and
                not any([fila, columna] == ag["entrada"] or [fila, columna] == ag["salida"] for ag in agujeros_gusano) and
                [fila, columna] not in [z[:2] for z in zonas_recarga]):
                
                zonas_recarga.append([fila, columna, factor])
                break
    
    # Generar celdas con carga requerida (3 posiciones con valores 5-15)
    celdas_carga_requerida = []
    for _ in range(3):
        while True:
            fila = random.randint(0, filas-1)
            columna = random.randint(0, columnas-1)
            carga = random.randint(5, 15)
            
            # Validar posición
            if ([fila, columna] != origen and [fila, columna] != destino and
                [fila, columna] not in agujeros_negros and
                [fila, columna] not in estrellas_gigantes and
                not any([fila, columna] == ag["entrada"] or [fila, columna] == ag["salida"] for ag in agujeros_gusano) and
                [fila, columna] not in [z[:2] for z in zonas_recarga] and
                [fila, columna] not in [c["coordenada"] for c in celdas_carga_requerida]):
                
                celdas_carga_requerida.append({
                    "coordenada": [fila, columna],
                    "cargaGastada": carga
                })
                break
    
    # Crear estructura final
    universo = {
        "matriz": {
            "filas": filas,
            "columnas": columnas
        },
        "origen": origen,
        "destino": destino,
        "agujerosNegros": agujeros_negros,
        "estrellasGigantes": estrellas_gigantes,
        "agujerosGusano": agujeros_gusano,
        "zonasRecarga": zonas_recarga,
        "celdasCargaRequerida": celdas_carga_requerida,
        "cargaInicial": carga_inicial,
        "matrizInicial": matriz_inicial
    }
    
    return universo

def guardar_matriz(universo, archivo="matriz_universo.json"):
    with open(archivo, 'w') as f:
        json.dump(universo, f, indent=2)

if __name__ == "__main__":
    print("Generando nueva matriz universo aleatoria...")
    universo = generar_matriz_universo()
    guardar_matriz(universo)
    print("Matriz generada y guardada en matriz_universo.json")