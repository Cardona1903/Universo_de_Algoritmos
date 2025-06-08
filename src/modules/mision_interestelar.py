import pygame
import sys
import json
from typing import List, Tuple, Dict, Optional

class Celda:
    def __init__(self, fila: int, columna: int, costo_energia: int):
        self.fila = fila
        self.columna = columna
        self.costo_energia = costo_energia
        self.es_agujero_negro = False
        self.es_estrella_gigante = False
        self.es_entrada_agujero_gusano = False
        self.es_salida_agujero_gusano = False
        self.es_zona_recarga = False
        self.factor_recarga = 1
        self.carga_requerida = 0
        self.visitada = False

class AgujeroGusano:
    def __init__(self, entrada: Tuple[int, int], salida: Tuple[int, int]):
        self.entrada = entrada
        self.salida = salida
        self.usado = False

class Nave:
    def __init__(self, energia: int, posicion: Tuple[int, int]):
        self.energia = energia
        self.posicion = posicion
        self.camino = [posicion]
        self.energia_inicial = energia
        self.estrellas_disponibles = 0
        self.historial_energia = [energia]  # Para seguimiento de energía
        self.historial_estrellas = [0]      # Para seguimiento de estrellas

class Universo:
    def __init__(self, archivo_json: str):
        self.estrellas_gigantes_originales = []  # Mantener registro original
        self.estrellas_gigantes_activas = []     # Estrellas disponibles
        self.agujeros_gusano = []
        self.cargar_desde_json(archivo_json)
        self.nave = Nave(self.carga_inicial, tuple(self.origen))
        self.soluciones = []
    
    def cargar_desde_json(self, archivo_json: str):
        with open(archivo_json, 'r') as f:
            data = json.load(f)
        
        self.filas = data['matriz']['filas']
        self.columnas = data['matriz']['columnas']
        self.origen = data['origen']
        self.destino = data['destino']
        self.carga_inicial = data['cargaInicial']
        
        # Inicializar matriz
        self.matriz = [[Celda(i, j, data['matrizInicial'][i][j]) 
                      for j in range(self.columnas)] 
                      for i in range(self.filas)]
        
        # Configurar agujeros negros
        for an in data['agujerosNegros']:
            self.matriz[an[0]][an[1]].es_agujero_negro = True
        
        # Configurar estrellas gigantes (mantener dos listas)
        self.estrellas_gigantes_originales = data['estrellasGigantes'].copy()
        self.estrellas_gigantes_activas = data['estrellasGigantes'].copy()
        for eg in data['estrellasGigantes']:
            self.matriz[eg[0]][eg[1]].es_estrella_gigante = True
        
        # Configurar agujeros de gusano
        for ag in data['agujerosGusano']:
            entrada = tuple(ag['entrada'])
            salida = tuple(ag['salida'])
            self.agujeros_gusano.append(AgujeroGusano(entrada, salida))
            self.matriz[entrada[0]][entrada[1]].es_entrada_agujero_gusano = True
            self.matriz[salida[0]][salida[1]].es_salida_agujero_gusano = True
        
        # Configurar zonas de recarga
        for zr in data['zonasRecarga']:
            self.matriz[zr[0]][zr[1]].es_zona_recarga = True
            self.matriz[zr[0]][zr[1]].factor_recarga = zr[2]
        
        # Configurar celdas con carga requerida
        for ccr in data['celdasCargaRequerida']:
            coord = tuple(ccr['coordenada'])
            self.matriz[coord[0]][coord[1]].carga_requerida = ccr['cargaGastada']
    
    def reiniciar_estrellas(self):
        """Restablece las estrellas gigantes a su estado original"""
        self.estrellas_gigantes_activas = self.estrellas_gigantes_originales.copy()
        for eg in self.estrellas_gigantes_originales:
            self.matriz[eg[0]][eg[1]].es_estrella_gigante = True
    
    def es_valida(self, fila: int, columna: int) -> bool:
        return 0 <= fila < self.filas and 0 <= columna < self.columnas
    
    def es_segura(self, fila: int, columna: int) -> bool:
        celda = self.matriz[fila][columna]
        
        if celda.es_agujero_negro:
            return self.nave.estrellas_disponibles > 0
        
        if celda.carga_requerida > self.nave.energia:
            return False
        
        return True
    
    def mover_nave(self, fila: int, columna: int):
        celda = self.matriz[fila][columna]
        
        # Registrar estado antes del movimiento
        energia_previa = self.nave.energia
        estrellas_previa = self.nave.estrellas_disponibles
        
        # Consumir energía (excepto en zonas de recarga)
        if not celda.es_zona_recarga:
            self.nave.energia -= celda.costo_energia
        
        # Recolectar estrella gigante si está disponible
        if [fila, columna] in self.estrellas_gigantes_activas:
            self.nave.estrellas_disponibles += 1
            self.estrellas_gigantes_activas.remove([fila, columna])
            self.matriz[fila][columna].es_estrella_gigante = False
        
        # Zonas de recarga
        if celda.es_zona_recarga:
            self.nave.energia *= celda.factor_recarga
        
        # Usar estrella para destruir agujero negro
        if celda.es_agujero_negro and self.nave.estrellas_disponibles > 0:
            self.nave.estrellas_disponibles -= 1
            celda.es_agujero_negro = False
        
        # Actualizar posición y registro
        self.nave.posicion = (fila, columna)
        self.nave.camino.append((fila, columna))
        celda.visitada = True
        
        # Registrar cambios
        self.nave.historial_energia.append(self.nave.energia)
        self.nave.historial_estrellas.append(self.nave.estrellas_disponibles)
    
    def obtener_estado_nave_en_camino(self, paso: int) -> Tuple[int, int]:
        """Obtiene energía y estrellas en un paso específico del camino"""
        if paso < len(self.nave.historial_energia):
            return (self.nave.historial_energia[paso], 
                    self.nave.historial_estrellas[paso])
        return (0, 0)
    
    def es_destino(self, fila: int, columna: int) -> bool:
        return fila == self.destino[0] and columna == self.destino[1]
    
    def resolver(self):
        # Reiniciar estado antes de resolver
        self.reiniciar_estrellas()
        self.nave = Nave(self.carga_inicial, tuple(self.origen))
        self.soluciones = []
        
        # Resetear celdas visitadas
        for fila in self.matriz:
            for celda in fila:
                celda.visitada = False
        
        # Resetear agujeros de gusano
        for ag in self.agujeros_gusano:
            ag.usado = False
        
        self._resolver_backtracking(self.origen[0], self.origen[1])
        return self.soluciones
    
    def _resolver_backtracking(self, fila: int, columna: int) -> bool:
        if self.es_destino(fila, columna):
            self.soluciones.append({
                'camino': self.nave.camino.copy(),
                'energia': self.nave.historial_energia.copy(),
                'estrellas': self.nave.historial_estrellas.copy()
            })
            return True
        
        if self.nave.energia <= 0:
            return False
        
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        movimientos.sort(key=lambda m: abs(self.destino[0] - (fila + m[0])) + abs(self.destino[1] - (columna + m[1])))
        
        for df, dc in movimientos:
            nueva_fila, nueva_columna = fila + df, columna + dc
            
            if self.es_valida(nueva_fila, nueva_columna) and not self.matriz[nueva_fila][nueva_columna].visitada:
                celda = self.matriz[nueva_fila][nueva_columna]
                
                # Guardar estado completo para backtracking
                estado_anterior = {
                    'energia': self.nave.energia,
                    'estrellas': self.nave.estrellas_disponibles,
                    'camino': self.nave.camino.copy(),
                    'estrella_activa': [nueva_fila, nueva_columna] in self.estrellas_gigantes_activas,
                    'agujero_activo': celda.es_agujero_negro,
                    'visitada': celda.visitada
                }
                
                if self.es_segura(nueva_fila, nueva_columna):
                    self.mover_nave(nueva_fila, nueva_columna)
                    
                    # Manejar agujeros de gusano
                    for ag in self.agujeros_gusano:
                        if not ag.usado and (nueva_fila, nueva_columna) == ag.entrada:
                            ag.usado = True
                            self.mover_nave(ag.salida[0], ag.salida[1])
                            nueva_fila, nueva_columna = ag.salida
                            break
                    
                    if len(self.nave.camino) < 200:  # Límite para evitar stack overflow
                        if self._resolver_backtracking(nueva_fila, nueva_columna):
                            return True
                
                # Backtracking: restaurar estado completo
                self.nave.energia = estado_anterior['energia']
                self.nave.estrellas_disponibles = estado_anterior['estrellas']
                self.nave.camino = estado_anterior['camino'].copy()
                self.nave.historial_energia = self.nave.historial_energia[:len(self.nave.camino)]
                self.nave.historial_estrellas = self.nave.historial_estrellas[:len(self.nave.camino)]
                
                # Restaurar estado de la celda
                if estado_anterior['estrella_activa'] and [nueva_fila, nueva_columna] not in self.estrellas_gigantes_activas:
                    self.estrellas_gigantes_activas.append([nueva_fila, nueva_columna])
                    self.matriz[nueva_fila][nueva_columna].es_estrella_gigante = True
                
                self.matriz[nueva_fila][nueva_columna].es_agujero_negro = estado_anterior['agujero_activo']
                self.matriz[nueva_fila][nueva_columna].visitada = estado_anterior['visitada']
                
                # Restaurar agujeros de gusano
                for ag in self.agujeros_gusano:
                    if (nueva_fila, nueva_columna) == ag.entrada:
                        ag.usado = False
        
        return False