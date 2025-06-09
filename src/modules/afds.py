"""
Módulo AFDs - Implementación completa de autómatas finitos deterministas
"""

"""
    Autómata Finito Determinista para validación de tarjetas de crédito y CURPs
    
    AFD para tarjetas (Σ, Q, q0, F, δ):
    - Σ = {dígitos 0-9, espacio, '/'}
    - Q = {q0, q1, ..., q27} (28 estados)
    - q0 = estado inicial
    - F = {q27} (estado de aceptación)
    - δ = (ver matriz de transiciones)
    
    AFD para CURPs (Σ, Q, q0, F, δ):
    - Σ = {letras A-Z, dígitos 0-9}
    - Q = {q0, q1, ..., q18} (19 estados)
    - q0 = estado inicial
    - F = {q18} (estado de aceptación)
    - δ = (ver matriz de transiciones)
"""

import os
from pathlib import Path

class ValidadorAFD:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
    
    def validar_tarjeta_credito(self, archivo=None, linea=None):
        if archivo:
            return self._validar_archivo_tarjetas(archivo)
        elif linea:
            return self._validar_linea_tarjeta(linea, 0)
        else:
            raise ValueError("Debe proporcionar archivo o línea a validar")
    
    def validar_curp(self, archivo=None, linea=None):
        if archivo:
            return self._validar_archivo_curps(archivo)
        elif linea:
            return self._validar_linea_curp(linea, 0)
        else:
            raise ValueError("Debe proporcionar archivo o línea a validar")
    
    # ========== Implementación completa para tarjetas ==========
    def _validar_archivo_tarjetas(self, archivo):
        archivo_path = self.data_dir / archivo
        resultados = []
        
        with open(archivo_path, 'r', encoding='utf-8') as f:
            for num_linea, linea in enumerate(f, 1):
                linea = linea.strip()
                valido, error = self._validar_linea_tarjeta(linea, num_linea)
                resultados.append({
                    'linea': num_linea,
                    'contenido': linea,
                    'valido': valido,
                    'error': error if error else ""
                })
        
        return resultados

    def _validar_linea_tarjeta(self, linea, num_linea):
    # Eliminar comentarios
        linea_limpia = linea.split('#')[0].strip()
    
        estado = 'q0'
        for pos, char in enumerate(linea_limpia):
        # Determinar tipo de carácter
            if char.isdigit():
                tipo = 'digito'
            elif char == ' ':
                tipo = 'espacio'
            elif char == '/':
                tipo = '/'
            else:
                tipo = 'otro'
        
        # Obtener siguiente estado
            try:
                estado = self.matriz_transiciones_tarjeta[estado][tipo]
            except KeyError:
                error_msg = self._generar_error_tarjeta(estado, pos, char, num_linea)
                return False, error_msg
        
            if estado is None:
                error_msg = self._generar_error_tarjeta(estado_previo=estado, 
                                                    pos=pos, 
                                                    char=char, 
                                                    num_linea=num_linea)
                return False, error_msg
    
    # Verificar estado final (q29) y validación semántica
        if estado != 'q29':
            return False, f"Línea {num_linea}: Cadena incompleta. Estado final: {estado}"
    
    # Validación semántica adicional
        partes = linea_limpia.split()
        if len(partes) != 6:
            return False, f"Línea {num_linea}: Formato incorrecto. Debe tener 6 partes separadas por espacios"
    
    # Validar fecha
        fecha = partes[4]
        try:
            mes = int(fecha[:2])
            año = int(fecha[3:])
            if mes < 1 or mes > 12:
                return False, f"Línea {num_linea}: Mes inválido ({mes:02d}). Debe estar entre 01 y 12."
        except:
            return False, f"Línea {num_linea}: Formato de fecha inválido ({fecha})"
    
        return True, ""

# Matriz de transiciones corregida
    matriz_transiciones_tarjeta = {
    # Primer grupo de 4 dígitos
    'q0': {'digito': 'q1', 'espacio': None, '/': None, 'otro': None},
    'q1': {'digito': 'q2', 'espacio': None, '/': None, 'otro': None},
    'q2': {'digito': 'q3', 'espacio': None, '/': None, 'otro': None},
    'q3': {'digito': 'q4', 'espacio': None, '/': None, 'otro': None},
    'q4': {'digito': None, 'espacio': 'q5', '/': None, 'otro': None},
    
    # Segundo grupo de 4 dígitos
    'q5': {'digito': 'q6', 'espacio': None, '/': None, 'otro': None},
    'q6': {'digito': 'q7', 'espacio': None, '/': None, 'otro': None},
    'q7': {'digito': 'q8', 'espacio': None, '/': None, 'otro': None},
    'q8': {'digito': 'q9', 'espacio': None, '/': None, 'otro': None},
    'q9': {'digito': None, 'espacio': 'q10', '/': None, 'otro': None},
    
    # Tercer grupo de 4 dígitos
    'q10': {'digito': 'q11', 'espacio': None, '/': None, 'otro': None},
    'q11': {'digito': 'q12', 'espacio': None, '/': None, 'otro': None},
    'q12': {'digito': 'q13', 'espacio': None, '/': None, 'otro': None},
    'q13': {'digito': 'q14', 'espacio': None, '/': None, 'otro': None},
    'q14': {'digito': None, 'espacio': 'q15', '/': None, 'otro': None},
    
    # Cuarto grupo de 4 dígitos
    'q15': {'digito': 'q16', 'espacio': None, '/': None, 'otro': None},
    'q16': {'digito': 'q17', 'espacio': None, '/': None, 'otro': None},
    'q17': {'digito': 'q18', 'espacio': None, '/': None, 'otro': None},
    'q18': {'digito': 'q19', 'espacio': None, '/': None, 'otro': None},
    'q19': {'digito': None, 'espacio': 'q20', '/': None, 'otro': None},
    
    # Fecha (mm/aa)
    'q20': {'digito': 'q21', 'espacio': None, '/': None, 'otro': None},
    'q21': {'digito': 'q22', 'espacio': None, '/': None, 'otro': None},
    'q22': {'digito': None, 'espacio': None, '/': 'q23', 'otro': None},
    'q23': {'digito': 'q24', 'espacio': None, '/': None, 'otro': None},
    'q24': {'digito': 'q25', 'espacio': None, '/': None, 'otro': None},
    'q25': {'digito': None, 'espacio': 'q26', '/': None, 'otro': None},
    
    # CVV (3 dígitos)
    'q26': {'digito': 'q27', 'espacio': None, '/': None, 'otro': None},
    'q27': {'digito': 'q28', 'espacio': None, '/': None, 'otro': None},
    'q28': {'digito': 'q29', 'espacio': None, '/': None, 'otro': None},
    'q29': {}  # Estado final
    }

    def _generar_error_tarjeta(self, estado_previo, pos, char, num_linea):
        esperado_map = {
        'q0': 'primer dígito (0-9)',
        'q1': 'segundo dígito (0-9)',
        'q2': 'tercer dígito (0-9)',
        'q3': 'cuarto dígito (0-9)',
        'q4': 'espacio después del primer grupo',
        'q5': 'primer dígito del segundo grupo',
        'q6': 'segundo dígito del segundo grupo',
        'q7': 'tercer dígito del segundo grupo',
        'q8': 'cuarto dígito del segundo grupo',
        'q9': 'espacio después del segundo grupo',
        'q10': 'primer dígito del tercer grupo',
        'q11': 'segundo dígito del tercer grupo',
        'q12': 'tercer dígito del tercer grupo',
        'q13': 'cuarto dígito del tercer grupo',
        'q14': 'espacio después del tercer grupo',
        'q15': 'primer dígito del cuarto grupo',
        'q16': 'segundo dígito del cuarto grupo',
        'q17': 'tercer dígito del cuarto grupo',
        'q18': 'cuarto dígito del cuarto grupo',
        'q19': 'espacio antes de la fecha',
        'q20': 'primer dígito del mes (0-1)',
        'q21': 'segundo dígito del mes (0-9)',
        'q22': "barra '/' para separar fecha",
        'q23': 'primer dígito del año (0-9)',
        'q24': 'segundo dígito del año (0-9)',
        'q25': 'espacio antes del CVV',
        'q26': 'primer dígito del CVV (0-9)',
        'q27': 'segundo dígito del CVV (0-9)',
        'q28': 'tercer dígito del CVV (0-9)'
        }
    
        esperado = esperado_map.get(estado_previo, "carácter válido según el formato de tarjeta")
    
    # Manejar caracteres especiales para mejor visualización
        char_display = char if char.isprintable() else f"ASCII {ord(char)}"
    
        return (f"Línea {num_linea}: Error en posición {pos+1}. "
                f"Carácter '{char_display}' inesperado. Se esperaba: {esperado}")

    
    # ========== Implementación mejorada para CURP ==========
    def _validar_archivo_curps(self, archivo):
        archivo_path = self.data_dir / archivo
        resultados = []
    
        with open(archivo_path, 'r', encoding='utf-8') as f:
            for num_linea, linea in enumerate(f, 1):
                linea_limpia = linea.split('#')[0].strip()  # Ignorar comentarios
                valido, error = self._validar_linea_curp(linea_limpia, num_linea)
                resultados.append({
                    'linea': num_linea,
                    'contenido': linea_limpia,
                    'valido': valido,
                    'error': error if error else ""
                })
    
        return resultados

    def _validar_linea_curp(self, linea, num_linea):
    # Eliminar comentarios y espacios
        linea_limpia = linea.split('#')[0].strip().upper()
    
    # Estado inicial
        estado = 'q0'
    
        for pos, char in enumerate(linea_limpia):
        # Determinar tipo de carácter
            if char.isalpha():
                if estado == 'q10' and char in ('H', 'M'):  # Caso especial para sexo
                    tipo = 'sexo'
                else:
                    tipo = 'letra'
            elif char.isdigit():
                tipo = 'digito'
            else:
                tipo = 'otro'
        
        # Obtener siguiente estado
            try:
                estado = self.matriz_transiciones_curp[estado][tipo]
            except KeyError:
                error_msg = self._generar_error_curp(estado, pos, char, num_linea)
                return False, error_msg
        
            if estado is None:
                error_msg = self._generar_error_curp(estado, pos, char, num_linea)
                return False, error_msg
    
    # Verificar estado final
        if estado != 'q18':
            return False, f"Línea {num_linea}: CURP incompleta. Estado final: {estado}"
    
    # Validación semántica adicional
        error_semantico = self._validar_semantica_curp(linea_limpia, num_linea)
        if error_semantico:
            return False, error_semantico
    
        return True, ""

# Matriz de transiciones completa para CURP
    matriz_transiciones_curp = {
    # Primeras 4 letras (Apellidos y nombre)
    'q0': {'letra': 'q1', 'digito': None, 'sexo': None, 'otro': None},
    'q1': {'letra': 'q2', 'digito': None, 'sexo': None, 'otro': None},
    'q2': {'letra': 'q3', 'digito': None, 'sexo': None, 'otro': None},
    'q3': {'letra': 'q4', 'digito': None, 'sexo': None, 'otro': None},
    
    # Fecha de nacimiento (6 dígitos AAMMDD)
    'q4': {'letra': None, 'digito': 'q5', 'sexo': None, 'otro': None},
    'q5': {'letra': None, 'digito': 'q6', 'sexo': None, 'otro': None},
    'q6': {'letra': None, 'digito': 'q7', 'sexo': None, 'otro': None},
    'q7': {'letra': None, 'digito': 'q8', 'sexo': None, 'otro': None},
    'q8': {'letra': None, 'digito': 'q9', 'sexo': None, 'otro': None},
    'q9': {'letra': None, 'digito': 'q10', 'sexo': None, 'otro': None},
    
    # Sexo (H/M)
    'q10': {'letra': None, 'digito': None, 'sexo': 'q11', 'otro': None},
    
    # Entidad federativa (2 letras)
    'q11': {'letra': 'q12', 'digito': None, 'sexo': None, 'otro': None},
    'q12': {'letra': 'q13', 'digito': None, 'sexo': None, 'otro': None},
    
    # Consonantes internas y otros (3 letras)
    'q13': {'letra': 'q14', 'digito': None, 'sexo': None, 'otro': None},
    'q14': {'letra': 'q15', 'digito': None, 'sexo': None, 'otro': None},
    'q15': {'letra': 'q16', 'digito': None, 'sexo': None, 'otro': None},
    
    # Homoclave (2 dígitos)
    'q16': {'letra': None, 'digito': 'q17', 'sexo': None, 'otro': None},
    'q17': {'letra': None, 'digito': 'q18', 'sexo': None, 'otro': None},
    'q18': {}  # Estado final
    }

    def _validar_semantica_curp(self, curp, num_linea):
        """Validaciones semánticas adicionales para la CURP"""
    # Validar fecha
        fecha_str = curp[4:10]
        try:
            año = int(fecha_str[:2])
            mes = int(fecha_str[2:4])
            dia = int(fecha_str[4:6])
        
            if mes < 1 or mes > 12:
                return f"Línea {num_linea}: Mes inválido ({mes:02d}) en la CURP"
            if dia < 1 or dia > 31:
                return f"Línea {num_linea}: Día inválido ({dia:02d}) en la CURP"
        
        # Validar mes/día según mes
            if mes in [4,6,9,11] and dia > 30:
                return f"Línea {num_linea}: Día inválido para el mes ({dia:02d}/{mes:02d})"
            if mes == 2 and dia > 29:
                return f"Línea {num_linea}: Febrero no puede tener más de 29 días"
            
        except ValueError:
            return f"Línea {num_linea}: Formato de fecha inválido en la CURP"
    
    # Validar entidad federativa (primeras 2 letras después del sexo)
        entidad = curp[11:13]
        estados_validos = ['AS', 'BC', 'BS', 'CC', 'CS', 'CH', 'CL', 'CM', 'DF', 'DG',
                        'GT', 'GR', 'HG', 'JC', 'MC', 'MN', 'MS', 'NT', 'NL', 'OC',
                        'PL', 'QT', 'QR', 'SP', 'SL', 'SR', 'TC', 'TL', 'TS', 'VZ',
                        'YN', 'ZS', 'NE']
    
        if entidad not in estados_validos:
            return f"Línea {num_linea}: Entidad federativa inválida ({entidad})"
    
        return None

    def _generar_error_curp(self, estado_previo, pos, char, num_linea):
        esperado_map = {
        'q0': 'primera letra del apellido paterno',
        'q1': 'segunda letra del apellido paterno',
        'q2': 'primera letra del apellido materno',
        'q3': 'primera letra del nombre',
        'q4': 'primer dígito del año (0-9)',
        'q5': 'segundo dígito del año (0-9)',
        'q6': 'primer dígito del mes (0-1)',
        'q7': 'segundo dígito del mes (0-9)',
        'q8': 'primer dígito del día (0-3)',
        'q9': 'segundo dígito del día (0-9)',
        'q10': "'H' (hombre) o 'M' (mujer)",
        'q11': 'primera letra de la entidad federativa',
        'q12': 'segunda letra de la entidad federativa',
        'q13': 'primera consonante interna',
        'q14': 'segunda consonante interna',
        'q15': 'tercera consonante interna',
        'q16': 'primer dígito de la homoclave (0-9)',
        'q17': 'segundo dígito de la homoclave (0-9)'
        }
    
        esperado = esperado_map.get(estado_previo, "carácter válido según el formato de CURP")
        char_display = char if char.isprintable() else f"ASCII {ord(char)}"
    
        return (f"Línea {num_linea}: Error en posición {pos+1}. "
                f"Carácter '{char_display}' inesperado. Se esperaba: {esperado}")

# src/modules/afds.py
def mostrar_visualizacion(self, tipo_afd):
    from .visualizador_afd import AFDVisualizer  # Importación relativa
    visualizador = AFDVisualizer()
    visualizador.run(tipo_afd)

#---------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    validador = ValidadorAFD()
    
    print("=== Validación de tarjetas ===")
    resultados_tarjetas = validador.validar_tarjeta_credito(archivo="tarjetas.txt")
    for res in resultados_tarjetas:
        status = "VÁLIDA" if res['valido'] else f"INVÁLIDA - {res['error']}"
        print(f"Línea {res['linea']}: {status}")
    
    print("\n=== Validación de CURPs ===")
    resultados_curps = validador.validar_curp(archivo="curps.txt")
    for res in resultados_curps:
        status = "VÁLIDA" if res['valido'] else f"INVÁLIDA - {res['error']}"
        print(f"Línea {res['linea']}: {status}")

    # Mostrar la interfaz gráfica
    from visualizador_afd import AFDVisualizer
    visualizador = AFDVisualizer()
    visualizador.run("ambos", validador)