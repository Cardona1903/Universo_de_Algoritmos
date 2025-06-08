import pygame
from pygame.locals import *
import sys
import threading
from typing import List, Tuple

# Configuración de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
MORADO = (128, 0, 128)
CYAN = (0, 255, 255)
NARANJA = (255, 165, 0)
ROSA = (255, 192, 203)

class InterfazUniverso:
    def __init__(self, universo, ancho_ventana=1000, alto_ventana=800):
        self.universo = universo
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.tamano_celda = min(
            (ancho_ventana - 300) // universo.columnas,
            (alto_ventana - 100) // universo.filas
        )
        self.margen_x = (ancho_ventana - 300 - universo.columnas * self.tamano_celda) // 2
        self.margen_y = (alto_ventana - universo.filas * self.tamano_celda) // 2
        
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
        pygame.display.set_caption("Misión Interestelar")
        self.fuente = pygame.font.SysFont('Arial', 16)
        self.fuente_grande = pygame.font.SysFont('Arial', 24)
        
        self.imagen_nave = pygame.Surface((self.tamano_celda//2, self.tamano_celda//2))
        self.imagen_nave.fill(AZUL)
        
        self.solucion_actual = 0
        self.pasos_solucion = 0
        self.mostrar_animacion = False
        self.pausa_animacion = False
        self.velocidad_animacion = 500  # ms entre pasos
        self.calculando = False
        self.hilo_resolucion = None

    def dibujar_matriz(self):
        self.pantalla.fill(BLANCO)
        
        # Dibujar matriz
        for i in range(self.universo.filas):
            for j in range(self.universo.columnas):
                rect = pygame.Rect(
                    self.margen_x + j * self.tamano_celda,
                    self.margen_y + i * self.tamano_celda,
                    self.tamano_celda,
                    self.tamano_celda
                )
                
                celda = self.universo.matriz[i][j]
                
                # Color de fondo según tipo de celda (CORREGIDO)
                if celda.es_agujero_negro:
                    color = NEGRO
                elif celda.es_estrella_gigante and [i, j] in self.universo.estrellas_gigantes_activas:
                    color = AMARILLO
                elif celda.es_entrada_agujero_gusano:
                    color = MORADO
                elif celda.es_salida_agujero_gusano:
                    color = CYAN
                elif celda.es_zona_recarga:
                    color = VERDE
                elif celda.carga_requerida > 0:
                    color = NARANJA
                else:
                    color = GRIS
                
                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, BLANCO, rect, 1)
                
                # Mostrar costo de energía
                texto = self.fuente.render(str(celda.costo_energia), True, NEGRO)
                self.pantalla.blit(texto, (rect.x + 5, rect.y + 5))
                
                # Mostrar carga requerida si aplica
                if celda.carga_requerida > 0:
                    texto_carga = self.fuente.render(f"R:{celda.carga_requerida}", True, ROJO)
                    self.pantalla.blit(texto_carga, (rect.x + 5, rect.y + rect.height - 20))
        
        # Dibujar nave
        nave_fila, nave_columna = self.universo.nave.posicion
        nave_rect = pygame.Rect(
            self.margen_x + nave_columna * self.tamano_celda + self.tamano_celda//4,
            self.margen_y + nave_fila * self.tamano_celda + self.tamano_celda//4,
            self.tamano_celda//2,
            self.tamano_celda//2
        )
        self.pantalla.blit(self.imagen_nave, nave_rect)
        
        # Dibujar información del panel lateral
        self.dibujar_panel_lateral()
        
        # Dibujar camino si hay solución
        if hasattr(self.universo, 'soluciones') and self.universo.soluciones and self.solucion_actual < len(self.universo.soluciones):
            solucion = self.universo.soluciones[self.solucion_actual]
            
            # Dibujar todo el camino en gris claro
            for paso in solucion['camino']:
                rect = pygame.Rect(
                    self.margen_x + paso[1] * self.tamano_celda + self.tamano_celda//3,
                    self.margen_y + paso[0] * self.tamano_celda + self.tamano_celda//3,
                    self.tamano_celda//3,
                    self.tamano_celda//3
                )
                pygame.draw.rect(self.pantalla, ROSA, rect)
            
            # Dibujar el camino recorrido hasta ahora en azul
            if self.mostrar_animacion and self.pasos_solucion < len(solucion['camino']):
                for i in range(self.pasos_solucion + 1):
                    paso = solucion['camino'][i]
                    rect = pygame.Rect(
                        self.margen_x + paso[1] * self.tamano_celda + self.tamano_celda//4,
                        self.margen_y + paso[0] * self.tamano_celda + self.tamano_celda//4,
                        self.tamano_celda//2,
                        self.tamano_celda//2
                    )
                    pygame.draw.rect(self.pantalla, AZUL, rect)
        
        # Mostrar mensaje si está calculando
        if self.calculando:
            texto_calculando = self.fuente_grande.render("Calculando solución...", True, ROJO)
            self.pantalla.blit(texto_calculando, (self.ancho_ventana // 2 - 100, 20))

    def dibujar_panel_lateral(self):
        panel_rect = pygame.Rect(
            self.ancho_ventana - 280,
            20,
            260,
            self.alto_ventana - 40
        )
        pygame.draw.rect(self.pantalla, GRIS, panel_rect)
        pygame.draw.rect(self.pantalla, NEGRO, panel_rect, 2)
        
        # Título
        titulo = self.fuente_grande.render("Misión Interestelar", True, NEGRO)
        self.pantalla.blit(titulo, (panel_rect.x + 10, panel_rect.y + 10))
        
        # Información de la nave (ACTUALIZADO para animación)
        if hasattr(self.universo, 'soluciones') and self.universo.soluciones and self.solucion_actual < len(self.universo.soluciones):
            solucion = self.universo.soluciones[self.solucion_actual]
            if self.mostrar_animacion and self.pasos_solucion < len(solucion['energia']):
                energia = solucion['energia'][self.pasos_solucion]
                estrellas = solucion['estrellas'][self.pasos_solucion]
            else:
                energia = self.universo.nave.energia
                estrellas = self.universo.nave.estrellas_disponibles
        else:
            energia = self.universo.nave.energia
            estrellas = self.universo.nave.estrellas_disponibles
        
        energia_texto = self.fuente.render(f"Energía: {max(0, energia)}", True, NEGRO)
        estrellas_texto = self.fuente.render(f"Estrellas: {estrellas}", True, NEGRO)
        posicion_texto = self.fuente.render(f"Posición: {self.universo.nave.posicion}", True, NEGRO)
        
        self.pantalla.blit(energia_texto, (panel_rect.x + 10, panel_rect.y + 50))
        self.pantalla.blit(estrellas_texto, (panel_rect.x + 10, panel_rect.y + 80))
        self.pantalla.blit(posicion_texto, (panel_rect.x + 10, panel_rect.y + 110))
        
        # Leyenda
        leyenda_titulo = self.fuente.render("Leyenda:", True, NEGRO)
        self.pantalla.blit(leyenda_titulo, (panel_rect.x + 10, panel_rect.y + 150))
        
        # Elementos de la leyenda
        elementos = [
            (GRIS, "Celda normal"),
            (VERDE, "Zona recarga"),
            (AMARILLO, "Estrella gigante"),
            (NEGRO, "Agujero negro"),
            (MORADO, "Entrada agujero gusano"),
            (CYAN, "Salida agujero gusano"),
            (NARANJA, "Carga requerida"),
            (AZUL, "Nave"),
            (ROSA, "Camino solución")
        ]
        
        for i, (color, texto) in enumerate(elementos):
            pygame.draw.rect(self.pantalla, color, (panel_rect.x + 10, panel_rect.y + 180 + i * 30, 20, 20))
            texto_leyenda = self.fuente.render(texto, True, NEGRO)
            self.pantalla.blit(texto_leyenda, (panel_rect.x + 40, panel_rect.y + 180 + i * 30))
        
        # Controles
        controles_titulo = self.fuente.render("Controles:", True, NEGRO)
        self.pantalla.blit(controles_titulo, (panel_rect.x + 10, panel_rect.y + 450))
        
        controles = [
            "R: Resolver",
            "A: Animación",
            "P: Pausar animación",
            "→: Siguiente solución",
            "←: Solución anterior",
            "Espacio: Siguiente paso",
            "ESC: Salir"
        ]
        
        for i, texto in enumerate(controles):
            texto_control = self.fuente.render(texto, True, NEGRO)
            self.pantalla.blit(texto_control, (panel_rect.x + 10, panel_rect.y + 480 + i * 25))

    def resolver_en_hilo(self):
        if not self.calculando:
            self.calculando = True
            self.hilo_resolucion = threading.Thread(target=self._resolver_background)
            self.hilo_resolucion.start()

    def _resolver_background(self):
        self.universo.resolver()
        self.calculando = False
        self.solucion_actual = 0
        self.pasos_solucion = 0
        self.mostrar_animacion = False

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                if self.hilo_resolucion and self.hilo_resolucion.is_alive():
                    self.hilo_resolucion.join()
                pygame.quit()
                sys.exit()
            
            elif evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    if self.hilo_resolucion and self.hilo_resolucion.is_alive():
                        self.hilo_resolucion.join()
                    pygame.quit()
                    sys.exit()
                
                elif evento.key == K_r and not self.calculando:
                    self.resolver_en_hilo()
                
                elif evento.key == K_a:
                    if hasattr(self.universo, 'soluciones') and self.universo.soluciones:
                        self.mostrar_animacion = not self.mostrar_animacion
                        self.pasos_solucion = 0
                
                elif evento.key == K_p:
                    self.pausa_animacion = not self.pausa_animacion
                
                elif evento.key == K_RIGHT:
                    if hasattr(self.universo, 'soluciones') and self.universo.soluciones:
                        self.solucion_actual = (self.solucion_actual + 1) % len(self.universo.soluciones)
                        self.pasos_solucion = 0
                
                elif evento.key == K_LEFT:
                    if hasattr(self.universo, 'soluciones') and self.universo.soluciones:
                        self.solucion_actual = (self.solucion_actual - 1) % len(self.universo.soluciones)
                        self.pasos_solucion = 0
                
                elif evento.key == K_SPACE:
                    if (hasattr(self.universo, 'soluciones') and self.universo.soluciones and 
                        self.pasos_solucion < len(self.universo.soluciones[self.solucion_actual]['camino']) - 1):
                        self.pasos_solucion += 1

    def actualizar_animacion(self):
        if (self.mostrar_animacion and not self.pausa_animacion and 
            hasattr(self.universo, 'soluciones') and self.universo.soluciones and
            self.solucion_actual < len(self.universo.soluciones) and
            self.pasos_solucion < len(self.universo.soluciones[self.solucion_actual]['camino']) - 1):
            
            self.pasos_solucion += 1
            pygame.time.delay(self.velocidad_animacion)

    def ejecutar(self):
        reloj = pygame.time.Clock()
        
        while True:
            self.manejar_eventos()
            self.actualizar_animacion()
            self.dibujar_matriz()
            pygame.display.flip()
            reloj.tick(60)