class NaveEspacial:
    def __init__(self, data):
        self.matriz = data['matrizInicial']
        self.filas = data['matriz']['filas']
        self.columnas = data['matriz']['columnas']
        self.origen = tuple(data['origen'])
        self.destino = tuple(data['destino'])
        self.agujeros_negros = set(tuple(coord) for coord in data['agujerosNegros'])
        self.estrellas_gigantes = set(tuple(coord) for coord in data['estrellasGigantes'])
        self.agujeros_gusano = {(tuple(ag['entrada']), tuple(ag['salida'])) for ag in data['agujerosGusano']}
        self.zonas_recarga = {(tuple(coord[:2]), coord[2]) for coord in data['zonasRecarga']}
        self.celdas_carga = {(tuple(celda['coordenada']), celda['cargaGastada']) for celda in data['celdasCargaRequerida']}
        self.carga_actual = data['cargaInicial']
        self.carga_minima = 0
        self.camino_actual = []
        self.caminos_validos = []
        self.estrellas_usadas = set()
        self.agujeros_usados = set()
        
    def es_valida(self, fila, columna):
        # Verifica si la celda está dentro de los límites de la matriz
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            # Verifica si no es un agujero negro
            if (fila, columna) not in self.agujeros_negros:
                # Verifica si cumple con los requisitos de carga
                if (fila, columna) in self.celdas_carga:
                    return self.carga_actual >= self.celdas_carga[(fila, columna)]
                return True
        return False
    
    def mover(self, fila, columna):
        # Verificar si es una zona de recarga primero
        if (fila, columna) in {coord for coord, _ in self.zonas_recarga}:
            multiplicador = next(mult for coord, mult in self.zonas_recarga if coord == (fila, columna))
            self.carga_actual *= multiplicador
        else:
            # Restar el costo de energía de la celda
            costo = self.matriz[fila][columna]
            self.carga_actual -= costo
            
        # Verificar si estamos en un agujero de gusano
        for entrada, salida in self.agujeros_gusano:
            if (fila, columna) == entrada and entrada not in self.agujeros_usados:
                self.agujeros_usados.add(entrada)
                return salida  # Retorna la salida del agujero de gusano
                
        # Verificar si estamos en una estrella gigante
        if (fila, columna) in self.estrellas_gigantes and (fila, columna) not in self.estrellas_usadas:
            self.estrellas_usadas.add((fila, columna))
            self.destruir_agujero_negro_adyacente(fila, columna)
            
        return (fila, columna)
    
    def destruir_agujero_negro_adyacente(self, fila, columna):
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
        for dr, dc in direcciones:
            nueva_fila, nueva_col = fila + dr, columna + dc
            if (nueva_fila, nueva_col) in self.agujeros_negros:
                self.agujeros_negros.remove((nueva_fila, nueva_col))
                break  # Solo destruye un agujero negro
    
    def resolver(self, fila, columna):
        # Condición de terminación: llegar al destino con carga suficiente
        if (fila, columna) == self.destino and self.carga_actual >= self.carga_minima:
            self.caminos_validos.append(self.camino_actual.copy())
            return True
            
        if not self.es_valida(fila, columna):
            return False
            
        # Guardar el estado actual
        carga_anterior = self.carga_actual
        agujeros_negros_anterior = self.agujeros_negros.copy()
        estrellas_usadas_anterior = self.estrellas_usadas.copy()
        agujeros_usados_anterior = self.agujeros_usados.copy()
        
        # Mover a la celda actual
        nueva_pos = self.mover(fila, columna)
        self.camino_actual.append(nueva_pos)
        
        # Si la nueva posición es diferente (agujero de gusano), actualizamos fila, columna
        if nueva_pos != (fila, columna):
            fila, columna = nueva_pos
            
        # Explorar todas las direcciones posibles
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
        for dr, dc in direcciones:
            if self.resolver(fila + dr, columna + dc):
                return True
                
        # Backtracking: revertir cambios si no se encontró solución
        self.camino_actual.pop()
        self.carga_actual = carga_anterior
        self.agujeros_negros = agujeros_negros_anterior
        self.estrellas_usadas = estrellas_usadas_anterior
        self.agujeros_usados = agujeros_usados_anterior
        
        return False