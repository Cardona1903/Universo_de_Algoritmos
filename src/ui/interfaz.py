import pygame
from pygame.locals import *
import sys
import threading
import os
from typing import List, Tuple

# Configuración de colores (para fondos o casos de error)
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
        
        # Cargar imágenes
        self.cargar_imagenes()
        
        # Variables de animación
        self.solucion_actual = 0
        self.pasos_solucion = 0
        self.mostrar_animacion = False
        self.pausa_animacion = False
        self.velocidad_animacion = 500
        self.calculando = False
        self.hilo_resolucion = None

    def cargar_imagenes(self):
        """Carga y escala todas las imágenes necesarias"""
        try:
            # Ruta base para los assets (ajustar según estructura del proyecto)
            assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
            
            # Cargar y redimensionar cada imagen
            tam_icono = (self.tamano_celda - 10, self.tamano_celda - 10)
            tam_icono_leyenda = (20, 20)  # Tamaño para los íconos en la leyenda
            
            # Cargar fondo del espacio exterior
            self.imagen_fondo = pygame.image.load(os.path.join(assets_path, 'fondo_espacio_exterior.png'))
            self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (self.tamano_celda, self.tamano_celda))
            
            # Intentar cargar imágenes personalizadas
            self.imagen_nave = pygame.image.load(os.path.join(assets_path, 'nave.png'))
            self.imagen_nave = pygame.transform.scale(self.imagen_nave, (self.tamano_celda//2, self.tamano_celda//2))
            self.imagen_nave_leyenda = pygame.transform.scale(self.imagen_nave, tam_icono_leyenda)
            
            self.imagen_normal = pygame.Surface((self.tamano_celda, self.tamano_celda))
            self.imagen_normal.fill(GRIS)
            self.imagen_normal_leyenda = pygame.Surface(tam_icono_leyenda)
            self.imagen_normal_leyenda.fill(GRIS)
            
            self.imagen_agujero_negro = pygame.image.load(os.path.join(assets_path, 'agujero_negro.png'))
            self.imagen_agujero_negro = pygame.transform.scale(self.imagen_agujero_negro, tam_icono)
            self.imagen_agujero_negro_leyenda = pygame.transform.scale(self.imagen_agujero_negro, tam_icono_leyenda)
            
            self.imagen_estrella = pygame.image.load(os.path.join(assets_path, 'estrella.png'))
            self.imagen_estrella = pygame.transform.scale(self.imagen_estrella, tam_icono)
            self.imagen_estrella_leyenda = pygame.transform.scale(self.imagen_estrella, tam_icono_leyenda)
            
            self.imagen_portal_entrada = pygame.image.load(os.path.join(assets_path, 'portal_entrada.png'))
            self.imagen_portal_entrada = pygame.transform.scale(self.imagen_portal_entrada, tam_icono)
            self.imagen_portal_entrada_leyenda = pygame.transform.scale(self.imagen_portal_entrada, tam_icono_leyenda)
            
            self.imagen_portal_salida = pygame.image.load(os.path.join(assets_path, 'portal_salida.png'))
            self.imagen_portal_salida = pygame.transform.scale(self.imagen_portal_salida, tam_icono)
            self.imagen_portal_salida_leyenda = pygame.transform.scale(self.imagen_portal_salida, tam_icono_leyenda)
            
            self.imagen_recarga = pygame.image.load(os.path.join(assets_path, 'recarga.png'))
            self.imagen_recarga = pygame.transform.scale(self.imagen_recarga, tam_icono)
            self.imagen_recarga_leyenda = pygame.transform.scale(self.imagen_recarga, tam_icono_leyenda)
            
            self.imagen_requerida = pygame.image.load(os.path.join(assets_path, 'requerida.png'))
            self.imagen_requerida = pygame.transform.scale(self.imagen_requerida, tam_icono)
            self.imagen_requerida_leyenda = pygame.transform.scale(self.imagen_requerida, tam_icono_leyenda)
            
            # Imagen para el camino solución (rosa)
            self.imagen_camino = pygame.Surface(tam_icono_leyenda)
            self.imagen_camino.fill(ROSA)
            
            self.usar_imagenes = True
        except Exception as e:
            print(f"Error cargando imágenes: {e}. Usando representación con colores.")
            self.usar_imagenes = False

    def dibujar_matriz(self):
        self.pantalla.fill(NEGRO)  # Fondo negro para el espacio
        
        # Dibujar matriz con fondo de espacio exterior
        for i in range(self.universo.filas):
            for j in range(self.universo.columnas):
                rect = pygame.Rect(
                    self.margen_x + j * self.tamano_celda,
                    self.margen_y + i * self.tamano_celda,
                    self.tamano_celda,
                    self.tamano_celda
                )
                
                celda = self.universo.matriz[i][j]
                
                # Dibujar fondo de espacio exterior
                if self.usar_imagenes:
                    self.pantalla.blit(self.imagen_fondo, rect)
                else:
                    pygame.draw.rect(self.pantalla, NEGRO, rect)
                
                # Dibujar borde de celda
                pygame.draw.rect(self.pantalla, (50, 50, 100), rect, 1)
                
                # Dibujar ícono según tipo de celda
                if self.usar_imagenes:
                    if celda.es_agujero_negro:
                        self.pantalla.blit(self.imagen_agujero_negro, (rect.x + 5, rect.y + 5))
                    elif celda.es_estrella_gigante and [i, j] in self.universo.estrellas_gigantes_activas:
                        self.pantalla.blit(self.imagen_estrella, (rect.x + 5, rect.y + 5))
                    elif celda.es_entrada_agujero_gusano:
                        self.pantalla.blit(self.imagen_portal_entrada, (rect.x + 5, rect.y + 5))
                    elif celda.es_salida_agujero_gusano:
                        self.pantalla.blit(self.imagen_portal_salida, (rect.x + 5, rect.y + 5))
                    elif celda.es_zona_recarga:
                        self.pantalla.blit(self.imagen_recarga, (rect.x + 5, rect.y + 5))
                    elif celda.carga_requerida > 0:
                        self.pantalla.blit(self.imagen_requerida, (rect.x + 5, rect.y + 5))
                else:
                    # Representación con colores si no hay imágenes
                    if celda.es_agujero_negro:
                        pygame.draw.rect(self.pantalla, NEGRO, rect)
                    elif celda.es_estrella_gigante and [i, j] in self.universo.estrellas_gigantes_activas:
                        pygame.draw.rect(self.pantalla, AMARILLO, rect)
                    elif celda.es_entrada_agujero_gusano:
                        pygame.draw.rect(self.pantalla, MORADO, rect)
                    elif celda.es_salida_agujero_gusano:
                        pygame.draw.rect(self.pantalla, CYAN, rect)
                    elif celda.es_zona_recarga:
                        pygame.draw.rect(self.pantalla, VERDE, rect)
                    elif celda.carga_requerida > 0:
                        pygame.draw.rect(self.pantalla, NARANJA, rect)
                
                # Mostrar costo de energía (pequeño en esquina)
                texto_costo = self.fuente.render(str(celda.costo_energia), True, BLANCO)
                self.pantalla.blit(texto_costo, (rect.x + 5, rect.y + 5))
                
                # Mostrar carga requerida si aplica
                if celda.carga_requerida > 0:
                    texto_carga = self.fuente.render(f"R:{celda.carga_requerida}", True, ROJO)
                    self.pantalla.blit(texto_carga, (rect.x + 5, rect.y + rect.height - 20))
        
        # Dibujar nave solo si no estamos en animación o estamos en el paso inicial
        if not self.mostrar_animacion or self.pasos_solucion == 0:
            nave_fila, nave_columna = self.universo.nave.posicion
            nave_rect = pygame.Rect(
                self.margen_x + nave_columna * self.tamano_celda + self.tamano_celda//4,
                self.margen_y + nave_fila * self.tamano_celda + self.tamano_celda//4,
                self.tamano_celda//2,
                self.tamano_celda//2
            )
            self.pantalla.blit(self.imagen_nave, nave_rect)
        
        # Resto del código de dibujado (panel lateral, solución, etc.)
        self.dibujar_panel_lateral()
        
        # Dibujar camino si hay solución
        if hasattr(self.universo, 'soluciones') and self.universo.soluciones and self.solucion_actual < len(self.universo.soluciones):
            solucion = self.universo.soluciones[self.solucion_actual]
            
            # Dibujar todo el camino en rosa claro
            for paso in solucion['camino']:
                rect = pygame.Rect(
                    self.margen_x + paso[1] * self.tamano_celda + self.tamano_celda//3,
                    self.margen_y + paso[0] * self.tamano_celda + self.tamano_celda//3,
                    self.tamano_celda//3,
                    self.tamano_celda//3
                )
                pygame.draw.rect(self.pantalla, ROSA, rect)
            
            # Dibujar la nave en su posición actual durante la animación
            if self.mostrar_animacion and self.pasos_solucion < len(solucion['camino']):
                paso_actual = solucion['camino'][self.pasos_solucion]
                nave_rect = pygame.Rect(
                    self.margen_x + paso_actual[1] * self.tamano_celda + self.tamano_celda//4,
                    self.margen_y + paso_actual[0] * self.tamano_celda + self.tamano_celda//4,
                    self.tamano_celda//2,
                    self.tamano_celda//2
                )
                self.pantalla.blit(self.imagen_nave, nave_rect)
        
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
        pygame.draw.rect(self.pantalla, (30, 30, 50), panel_rect)  # Fondo oscuro para el panel
        pygame.draw.rect(self.pantalla, (100, 100, 150), panel_rect, 2)  # Borde azulado
        
        # Título
        titulo = self.fuente_grande.render("Misión Interestelar", True, BLANCO)
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
        
        energia_texto = self.fuente.render(f"Energía: {max(0, energia)}", True, BLANCO)
        estrellas_texto = self.fuente.render(f"Estrellas: {estrellas}", True, BLANCO)
        posicion_texto = self.fuente.render(f"Posición: {self.universo.nave.posicion}", True, BLANCO)
        
        self.pantalla.blit(energia_texto, (panel_rect.x + 10, panel_rect.y + 50))
        self.pantalla.blit(estrellas_texto, (panel_rect.x + 10, panel_rect.y + 80))
        self.pantalla.blit(posicion_texto, (panel_rect.x + 10, panel_rect.y + 110))
        
        # Leyenda
        leyenda_titulo = self.fuente.render("Leyenda:", True, BLANCO)
        self.pantalla.blit(leyenda_titulo, (panel_rect.x + 10, panel_rect.y + 150))
        
        # Elementos de la leyenda con imágenes
        elementos = [
           
            (self.imagen_recarga_leyenda, "Zona recarga"),
            (self.imagen_estrella_leyenda, "Estrella gigante"),
            (self.imagen_agujero_negro_leyenda, "Agujero negro"),
            (self.imagen_portal_entrada_leyenda, "Entrada agujero gusano"),
            (self.imagen_portal_salida_leyenda, "Salida agujero gusano"),
            (self.imagen_requerida_leyenda, "Carga requerida"),
            (self.imagen_nave_leyenda, "Nave"),
            (self.imagen_camino, "Camino solución")
        ]
        
        for i, (imagen, texto) in enumerate(elementos):
            self.pantalla.blit(imagen, (panel_rect.x + 10, panel_rect.y + 180 + i * 30))
            texto_leyenda = self.fuente.render(texto, True, BLANCO)
            self.pantalla.blit(texto_leyenda, (panel_rect.x + 40, panel_rect.y + 180 + i * 30))
        
        # Controles
        controles_titulo = self.fuente.render("Controles:", True, BLANCO)
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
            texto_control = self.fuente.render(texto, True, BLANCO)
            self.pantalla.blit(texto_control, (panel_rect.x + 10, panel_rect.y + 480 + i * 25))

    # ... (resto de los métodos se mantienen igual)
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