# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:24:25 2026

@author: diego
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# =====================================================================
# BASE DE DATOS DE VEHÍCULOS (PARÁMETROS FÍSICOS Y VE)
# =====================================================================
base_datos_coches = {
    "Motor Genérico (Por defecto)": {
        "cilindros": 4, "r": 0.043, "l": 0.140, "ancho_cilindro": 0.086, 
        "rc": 10.0, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 180, 360, 540], # 4 cilindros en línea. Un impacto cada 180º.
        "rpm_ref": [800, 2000, 3500, 5000, 6000, 6500, 7000],
        "curva_ve": [0.75, 0.85, 0.95, 1.00, 0.85, 0.70, 0.10],
        "factor_egr": 2.0,
        "cf_C1": 40000.0,
        "cf_C2": 0.005,
        "cf_C3": 900.0,
        "cf_C4": 90.0,
        "volumen_colector": 0.004,
        "area_tubo_Ska-P": 0.002,
    },
    "Porsche 911 Turbo S (992)": {
        "cilindros": 6, "r": 0.0382, "l": 0.1376, "ancho_cilindro": 0.102, 
        "rc": 8.7, "presion_turbo_base": 2.55, 
        "angulos_encendido": [0, 120, 240, 360, 480, 600], # Motor Bóxer de 6 cilindros. Ciclo perfecto de 120º.
        "rpm_ref": [800, 2500, 4000, 5500, 6750, 7200, 7500],
        "curva_ve": [0.70, 0.98, 1.00, 0.95, 0.88, 0.80, 0.10],
        "factor_egr": 1.2,
        "cf_C1": 48000.0,
        "cf_C2": 0.0065,
        "cf_C3": 1000.0,
        "cf_C4": 105.0,
        "volumen_colector": 0.008, 
        "area_tubo_Ska-P": 0.0035
    },
    "Land Rover Discovery (2000)": {
        "cilindros": 8, "r": 0.0355, "l": 0.140, "ancho_cilindro": 0.094, 
        "rc": 9.3, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 90, 180, 270, 360, 450, 540, 630], # V8 Cross-Plane. Impacto al cigüeñal cada 90º.
        "rpm_ref": [800, 2000, 2600, 3500, 5000, 5500, 6000],
        "curva_ve": [0.75, 0.95, 1.00, 0.85, 0.60, 0.20, 0.05],
        "factor_egr": 2.2,
        "cf_C1": 52000.0,
        "cf_C2": 0.006,
        "cf_C3": 1100.0,
        "cf_C4": 130.0,
        "volumen_colector": 0.006,
        "area_tubo_Ska-P": 0.0025
    },
    "Ferrari 250 GTO": {
        "cilindros": 12, "r": 0.0294, "l": 0.125, "ancho_cilindro": 0.073, 
        "rc": 9.8, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660], # V12 a 60 grados. Una turbina, empuje cada 60º.
        "rpm_ref": [1000, 3000, 4500, 6000, 7000, 7500, 8000],
        "curva_ve": [0.50, 0.75, 0.90, 1.00, 0.95, 0.90, 0.10],
        "factor_egr": 2.5,
        "cf_C1": 65000.0,
        "cf_C2": 0.007,
        "cf_C3": 1100.0,
        "cf_C4": 120.0,
        "volumen_colector": 0.005,
        "area_tubo_Ska-P": 0.0045
    },
    "Mercedes GLC Coupé (300 4MATIC)": {
        "cilindros": 4, "r": 0.046, "l": 0.150, "ancho_cilindro": 0.083, 
        "rc": 10.5, "presion_turbo_base": 2.0, 
        "angulos_encendido": [0, 180, 360, 540], # 4 cilindros en línea.
        "rpm_ref": [800, 1800, 3000, 4500, 6000, 6500],
        "curva_ve": [0.70, 0.90, 1.00, 0.95, 0.75, 0.10],
        "factor_egr": 1.5,
        "cf_C1": 38000.0,
        "cf_C2": 0.0055,
        "cf_C3": 850.0,
        "cf_C4": 85.0,
        "volumen_colector": 0.005,
        "area_tubo_Ska-P": 0.002
    },
    "Lamborghini Miura P400": {
        "cilindros": 12, "r": 0.0310, "l": 0.1250, "ancho_cilindro": 0.082, 
        "rc": 10.4, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660], # V12 transversal. Empuje constante cada 60º.
        "rpm_ref": [1000, 3000, 5000, 6000, 7000, 8000, 8500],
        "curva_ve": [0.40, 0.65, 0.85, 0.95, 1.00, 0.90, 0.10],
        "factor_egr": 2.6,
        "cf_C1": 68000.0,
        "cf_C2": 0.007,
        "cf_C3": 1150.0,
        "cf_C4": 125.0,
        "volumen_colector": 0.006,
        "area_tubo_Ska-P": 0.004
    },
    "Ford Mustang Fastback (1969)": {
        "cilindros": 8, "r": 0.0505, "l": 0.165, "ancho_cilindro": 0.1049, 
        "rc": 10.6, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 90, 180, 270, 360, 450, 540, 630], # V8 americano clásico.
        "rpm_ref": [800, 2000, 3000, 4000, 5200, 6000, 6500],
        "curva_ve": [0.65, 0.85, 1.00, 0.95, 0.80, 0.60, 0.10],
        "factor_egr": 3.2,
        "cf_C1": 55000.0,
        "cf_C2": 0.0065,
        "cf_C3": 1200.0,
        "cf_C4": 140.0,
        "volumen_colector": 0.007,
        "area_tubo_Ska-P": 0.0035
    },
    "BMW M4 CSL": {
        "cilindros": 6, "r": 0.045, "l": 0.144, "ancho_cilindro": 0.084, 
        "rc": 9.3, "presion_turbo_base": 2.7, 
        "angulos_encendido": [0, 120, 240, 360, 480, 600], # 6 cilindros en línea.
        "rpm_ref": [1000, 2750, 4000, 5500, 6500, 7200, 7500],
        "curva_ve": [0.65, 0.95, 1.00, 0.98, 0.90, 0.85, 0.10],
        "factor_egr": 1.3,
        "cf_C1": 45000.0,
        "cf_C2": 0.006,
        "cf_C3": 950.0,
        "cf_C4": 95.0,
        "volumen_colector": 0.007,
        "area_tubo_Ska-P": 0.003
    },
    "Mercedes-Benz 300 SLR Uhlenhaut Coupé (1955)": {
        "cilindros": 8, "r": 0.0390, "l": 0.140, "ancho_cilindro": 0.078, 
        "rc": 9.0, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 90, 180, 270, 360, 450, 540, 630], # 8 cilindros en línea.
        "rpm_ref": [1000, 3000, 5000, 6500, 7400, 8000],
        "curva_ve": [0.50, 0.80, 0.95, 1.00, 0.90, 0.10],
        "factor_egr": 2.8,
        "cf_C1": 60000.0,
        "cf_C2": 0.0065,
        "cf_C3": 1050.0,
        "cf_C4": 130.0,
        "volumen_colector": 0.004,
        "area_tubo_Ska-P": 0.005
    },
    "Jaguar E-Type Series 1": {
        "cilindros": 6, "r": 0.0530, "l": 0.160, "ancho_cilindro": 0.087, 
        "rc": 9.0, "presion_turbo_base": 1.0, 
        "angulos_encendido": [0, 120, 240, 360, 480, 600], # 6 cilindros en línea clásico.
        "rpm_ref": [800, 2000, 3500, 4500, 5500, 6000],
        "curva_ve": [0.60, 0.85, 1.00, 0.95, 0.85, 0.10],
        "factor_egr": 3.0,
        "cf_C1": 46000.0,
        "cf_C2": 0.006,
        "cf_C3": 1000.0,
        "cf_C4": 115.0,
        "volumen_colector": 0.006,
        "area_tubo_Ska-P": 0.003
    }
}

# =====================================================================
# PARÁMETROS FÍSICOS Y CINEMÁTICA
# =====================================================================
M = 0.45         
m = 1.0e-26      
dt = 0.0001                

theta_sym = sp.Symbol('theta')
r_sym = sp.Symbol('r') 
l_sym = sp.Symbol('l') 

x_sym = r_sym * sp.cos(theta_sym) + sp.sqrt(l_sym**2 - (r_sym**2) * sp.sin(theta_sym)**2)
dx_dtheta_sym = sp.diff(x_sym, theta_sym)         
d2x_dtheta2_sym = sp.diff(dx_dtheta_sym, theta_sym) 

calc_dx_dtheta = sp.lambdify((theta_sym, r_sym, l_sym), dx_dtheta_sym, 'numpy')
calc_d2x_dtheta2 = sp.lambdify((theta_sym, r_sym, l_sym), d2x_dtheta2_sym, 'numpy')

def posicion_piston(theta, r, l):
    x = r * np.cos(theta) + np.sqrt(l**2 - (r**2) * (np.sin(theta)**2))
    return x

def volumen_cilindro(x, r, l, ancho_cilindro, volumen_camara):
    radio_cilindro = ancho_cilindro / 2.0
    area_piston = np.pi * (radio_cilindro**2)
    altura_maxima = r + l 
    altura_libre_gas = altura_maxima - x 
    # Ya no ponemos volumen_camara = 0.00005 aquí porque viene de fuera
    volumen_total = (area_piston * altura_libre_gas) + volumen_camara
    return volumen_total, area_piston
   
def cinematica_exacta_piston(theta, omega, alfa, r, l):
    vel = calc_dx_dtheta(theta, r, l) * omega
    accel = calc_d2x_dtheta2(theta, r, l) * (omega**2) + calc_dx_dtheta(theta, r, l) * alfa
    return vel, accel

# =====================================================================
# TERMODINÁMICA Y FUERZAS
# =====================================================================
R_ideal = 8.314      # Constante universal de los gases ideales (J/(mol·K))
k_B = 1.38e-23       # Constante de Boltzmann (J/K)
M_molar_aire = 0.02897 # Masa molar del aire seco (kg/mol) calculada por proporciones de N2 y O2

# Valores ajustados al Poder Calorífico de la gasolina
delta_E_normal = 5.0e-20   
delta_E_carreras = 6.5e-20 

# La inyección ahora calcula el aire físico según el tamaño real del cilindro
def inyectar_mezcla(porcentaje_acelerador, presion_turbo, rpm_actual, rpms_ref, curva_ve, ancho, r_manivela):
    eficiencia_volumetrica = np.interp(rpm_actual, rpms_ref, curva_ve)
    vol_desplazado = np.pi * ((ancho / 2.0)**2) * (r_manivela * 2.0)
    
    # 1. FÍSICA PURA: Temperatura y Presión reales
    # Un atmosférico entra a 300 K. Si hay turbo, el aire se calienta por la compresión.
    # Por cada bar extra de presión, la temperatura sube unos 40 K (asumiendo intercooler).
    T_admision = 300.0 + (presion_turbo - 1.0) * 40.0 
    P_admision = 101325.0 * presion_turbo
    
    # 2. Ley de Gases Ideales completa (Calcula la masa exacta según P, V y T)
    moles_totales_teoricos = (P_admision * vol_desplazado) / (8.314 * T_admision)
    
    # 3. Restricción de la válvula (acelerador) y dinámica de fluidos (VE)
    moles_actuales = moles_totales_teoricos * (porcentaje_acelerador / 100.0) * eficiencia_volumetrica
    
    N_bolitas = int(1000 * (porcentaje_acelerador / 100.0) * eficiencia_volumetrica)
    v_inicial = np.sqrt((2 * k_B * T_admision) / m)
    
    return moles_actuales, N_bolitas, T_admision, v_inicial

def encender_chispa(v_actual, tipo_combustible="normal"):
    "Al final no uso esto y simplemnte queda como un remanente puesto que el nuevo código es mucho más avanzado"
    if tipo_combustible == "carreras": delta_E = delta_E_carreras
    else: delta_E = delta_E_normal
        
    energia_cinetica_actual = 0.5 * m * (v_actual**2)
    nueva_energia_cinetica = energia_cinetica_actual + delta_E
    nueva_velocidad = np.sqrt((2 * nueva_energia_cinetica) / m)
    nueva_temperatura = (m * (nueva_velocidad**2)) / (2 * k_B)
    return nueva_velocidad, nueva_temperatura

def calcular_presion(moles, temperatura, volumen):
    presion_pascales = (moles * R_ideal * temperatura) / volumen
    return presion_pascales

P_atmosferica = 101325.0

def calcular_calor_woschni(presion_Pa, presion_mot_Pa, temp_gas, volumen, area_expuesta, ancho_cilindro, rpm, vel_media_piston, dt, temp_pared=450.0):
    p_kPa = presion_Pa / 1000.0 # 1. Trampa de unidades: Woschni exige kPa
    
    # 2. Velocidad media del gas (w) según Woschni. 
    # C1 y C2 cambian según si estamos en compresión/expansión. Simplificaremos con constantes estándar para ciclos regulares.
    C1 = 2.28  # Constante de turbulencia base
    C2 = 0.0   # Solo se activa con la combustión, lo manejaremos en el bucle si hay diferencia de presión
    
    if presion_Pa > presion_mot_Pa:
        C2 = 3.24e-3  # Factor de expansión de la llama
        
    # w = C1 * Sp + C2 * (Vd * T1 / (p1 * V1)) * (p - p_mot) ... Woschni completo
    # Para el modelo 0D, una aproximación robusta de la velocidad es:
    w = C1 * vel_media_piston + C2 * abs(presion_Pa - presion_mot_Pa)
    if w < 0.1: w = 0.1 # Evitar singularidades
    
    # 3. Correlación empírica (Cuidado: B está en metros en la base de datos)
    h_c = 3.26 * (ancho_cilindro**-0.2) * (p_kPa**0.8) * (temp_gas**-0.55) * (w**0.8)
    
    # 4. Cálculo del calor perdido (Q = h * A * dT * dt) en Joules
    # Si el gas está más frío que la pared, no hay pérdida (o la pared calienta al gas, pero lo ignoramos para simplificar).
    if temp_gas > temp_pared:
        dQ_perdido = h_c * area_expuesta * (temp_gas - temp_pared) * dt
    else:
        dQ_perdido = 0.0
        
    return dQ_perdido

# MEJORA simulación del motor
def calcular_flujo_molar_valvula(P_arriba, P_abajo, T_arriba, area_valvula):
    """
    Para calcular el flujo másico real necesitamos modelar cómo un gas compresible (aire) se "atasca" al pasar por un orificio
    (la válvula). Si la diferencia de presiones es extrema, el gas alcanza la velocidad del sonido (Mach 1) en el cuello de la 
    válvula. En ese punto, por mucho vacío que haga el cilindro, el flujo se estrangula (Flujo Sónico o Choked Flow) y no puede
    entrar más rápido. Esto es el límite físico real de cualquier motor.
    """
    
    # Si la contrapresión es mayor, el flujo se invierte o se detiene. Para simplificar, lo cortamos en 0.
    if P_arriba <= P_abajo: return 0.0
    # En la vida real, si la presión dentro del cilindro es mayor que la del colector de admisión mientras la válvula está abierta,
    # el gas fluye hacia atrás (esto se llama reversión). Ocurre a menudo a bajas RPM con árboles de levas muy agresivos.
    # Lo simplificamos a 0 porque si permitimos que el gas retroceda matemáticamente en el simulador sin crear un "colector de
    # admisión virtual" que almacene ese gas caliente y lo mezcle, el simulador colapsaría. Perderíamos la cuenta de los moles de
    # aire fresco, y peor aún, las temperaturas se volverían fallarían al escupir fuego hacia la admisión. Cortar el flujo a 0.0
    # (simulando que la válvula actúa como un diodo perfecto) es el estándar aceptado en modelos 0D para mantener la estabilidad
    # numérica sin sacrificar demasiada precisión en la curva de potencia.

    Cd = 0.6  # Coeficiente de descarga estándar de una válvula de asiento. Empíricamente, en el banco de pruebas de flujo
    # (flow bench), una válvula de motor de serie solo deja pasar alrededor del 60% del aire que teóricamente cabría por ese hueco.
    gamma = 1.4 # Coeficiente Adiabático. La termodinámica dicta que los gases diatómicos (N2 y O2 qu eforman el aire)
    # tienen 5 grados de libertad a temperatura ambiente, lo queda como resultado 1.4. definiendo el comportamiento del aire al ser aplastado.
    R_esp = 287.05 # Constante Específica del Aire, R específico del aire (J/kg·K)
    # Se debe a que la ecuación de Saint-Venant para fluidos funciona pesando la masa en kilogramos, no en moles.
    
    relacion_presiones = P_abajo / P_arriba
    
    # Condición de estrangulamiento sónico (Flujo Choked)
    critico = (2.0 / (gamma + 1.0)) ** (gamma / (gamma - 1.0))
    
    if relacion_presiones < critico:
        # El gas ha alcanzado la velocidad del sonido (Mach 1), ya no puede ir más rápido
        psi = np.sqrt(gamma * ((2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (gamma - 1.0))))
    else:
        # Flujo subsónico (el gas se acelera suavemente según la diferencia de presión)
        termino = (relacion_presiones ** (2.0 / gamma)) - (relacion_presiones ** ((gamma + 1.0) / gamma))
        psi = np.sqrt(max(0.0, (2.0 * gamma / (gamma - 1.0)) * termino))
        
    # Ecuación de Saint-Venant para caudal másico (kg/s)
    flujo_masico_kg_s = Cd * area_valvula * (P_arriba / np.sqrt(R_esp * T_arriba)) * psi
    
    # Lo pasamos a moles por segundo para tu simulador
    flujo_molar_mol_s = flujo_masico_kg_s / M_molar_aire
    return flujo_molar_mol_s


# Coeficientes de Fricción Adimensionales (μ) aproximados según el tipo de lubricante
# Un pistón metálico lubricado rozando contra un cilindro metálico obedece a la Fricción de Coulomb, cuyo coeficiente adimensional
# empírico real en motores oscila entre 0.01 y 0.05 dependiendo de lo denso que sea el aceite.
# De ahí salen los valores: no son viscosidades, son verdaderos coeficientes de rozamiento que varía según el aceite que usemos.




# Multiplicadores de viscosidad para el modelo de Chen-Flynn
# 1.00 es la fricción estándar. Un aceite 10W-60 es más espeso y genera más arrastre (+15%).
aceites_motor = {
    "Mobil 1 (0W-40)": 1.00,         
    "Castrol EDGE (5W-30)": 1.05,    
    "Liqui Moly (10W-60)": 1.15,     
    "Petronas Syntium (0W-20)": 0.90 
} # Aproximaciones empíricas

def calcular_fuerza_y_torque_indicado(presion_gas, area_piston, theta, r, l):
    # Calcula el torque puro generado por el gas, sin restar fricción todavía
    presion_neta = presion_gas - 101325.0
    fuerza_bruta = presion_neta * area_piston
    
    termino_raiz = np.sqrt(l**2 - (r**2) * (np.sin(theta)**2))
    factor_geometrico = np.sin(theta) * (1 + (r * np.cos(theta)) / termino_raiz)
    
    torque_indicado = fuerza_bruta * r * factor_geometrico
    return fuerza_bruta, torque_indicado

def calcular_caballos(torque, rpm):
    # Fórmula física pura: Potencia (W) = Torque (Nm) * Velocidad Angular (rad/s)
    omega_rad_s = rpm * (2 * np.pi / 60.0)
    potencia_vatios = torque * omega_rad_s

    # Conversión métrica exacta: 1 CV = 735.498 W
    cv_real = potencia_vatios / 735.498 
    return cv_real

# =====================================================================
# EL BUCLE PRINCIPAL (360 GRADOS INTACTOS Y PUROS)
# =====================================================================
def simular_ciclo_motor(coche_elegido, activar_turbo=True, porcentaje_acelerador=100.0, tipo_combustible="normal", aceite="Mobil 1 (0W-40)", rpm_inicial=800.0, es_hidrogeno=False, octanaje=95.0):
    
    # 0. EXTRACCIÓN DE DATOS Y CÁLCULO DE LA CÁMARA
    coche = base_datos_coches[coche_elegido] # Entramos en la base de datos y cogemos toda la información del coche que se ha seleccionado en la interfaz.
    num_cilindros = coche["cilindros"]
    r = coche["r"]
    l = coche["l"]
    ancho_cilindro = coche["ancho_cilindro"]
    factor_egr_coche = coche["factor_egr"]
    rc = coche["rc"] # Extraemos la nueva variable "Relación de Compresión" que se añadió a la base de datos (ej, 9.8 para el Porsche).
    volumen_colector = coche["volumen_colector"]
    area_tubo_escape = coche["area_tubo_Ska-P"]
    
    # Calculamos el volumen de la cámara paramétrico para este coche
    carrera = r * 2.0 # El recorrido total del pistón de arriba a abajo (la carrera o stroke) 
        # es exactamente el doble del radio de la manivela del cigüeñal.
    area_base = np.pi * ((ancho_cilindro / 2.0)**2) # Es la fórmula clásica del área de un círculo (pi*r^2$) 
        # para saber la superficie plana de la cabeza del pistón.
    volumen_desplazado = area_base * carrera # Multiplicando el área plana por el recorrido, obtenemos la "Cilindrada Unitaria" 
        # (el espacio que el pistón barre al moverse).
    volumen_camara = volumen_desplazado / (rc - 1.0) # Es la fórmula universal de la ingeniería automotriz para deducir el volumen 
        # de la cámara de combustión (el hueco que queda arriba) a partir de la Relación de Compresión real del coche.
    # -------------------------------------------------------------
    
    # --- MEJORA: VOLUMEN DE INTERSTICIOS (Crevices) ---
    # El hueco microscópico de los anillos del pistón que atrapará el gas.
    V_crevice = volumen_camara * 0.015 
    temp_pared = 450.0 # Al estar rodeado de metal, el gas que entre ahí bajará instantáneamente a la temperatura de ese metal
    # Tomar 450 K es el estándar termodinamico empírico absoluto en la industria para simulaciones 0D.
    # -------------------------------------------------------------
    
    if activar_turbo and coche["presion_turbo_base"] > 1.0: presion_turbo_real = coche["presion_turbo_base"]
    else: presion_turbo_real = 1.0

    inercia_motor = 0.5 
    rpm_actual = rpm_inicial 
    omega = (rpm_actual * 2 * np.pi) / 60.0     

    # Calculamos cuánta masa (moles) debería entrar según la eficiencia volumétrica (VE) y el volumen físico real
    moles_totales, _, temp_admision, vel_particulas_base = inyectar_mezcla(
        porcentaje_acelerador, presion_turbo_real, rpm_actual, coche["rpm_ref"], coche["curva_ve"], ancho_cilindro, r
    )
    
    # --- AJUSTES PROPORCIONALES PARA HIDRÓGENO ---
    # Una combustión real de gasolina dura unos 50 grados de cigüeñal
    duracion_chispa = 50.0 * (np.pi / 180.0) # Lo pasamos de grados a radianes
    multiplicador_energia = 1.0
    
    if es_hidrogeno:
        moles_totales *= 0.70         
        # El hidrógeno tiene una velocidad de llama laminar altísima, quema en la mitad de tiempo
        duracion_chispa = 25.0 * (np.pi / 180.0) 
        multiplicador_energia = 1.21
    # ---------------------------------------------
    
    # Listas vacías para telemetría
    datos_theta, datos_posicion, datos_volumen = [], [], []
    datos_presion, datos_fuerza, datos_torque, datos_rpm = [], [], [], []
    datos_temperatura, datos_velocidad, datos_aceleracion = [], [], []
    
    alfa_actual = 0.0  
    theta_actual = 0.0       
    chispa_encendida = False 
    
    # --- VARIABLES PARA EL CONTROL TERMODINÁMICO ---
    area_valvula_max = area_base * 0.30 # Definimos que las válvulas de admisión/escape ocupan aprox el 30% del área del cilindro

    # ------En la nueva actualización no ponemos esto ------
    # moles_actuales = 1e-5     # Al principio (0º), la válvula acaba de abrirse, no hay gas dentro aún. 
    # No ponemos "moles_actuales = 0.0" para evitar división por cero (además que nunca hay vacio total)
    # -------------

    # --- GAS INICIAL (El ciclo fantasma lo estabilizará) ---
    moles_actuales = 1e-5
    moles_residuales = 1e-5
    temp_actual = 300.0
    
    # --- NUEVO: ESTADO INICIAL DEL COLECTOR DE ESCAPE (PLENUM) ---
    temp_colector = 600.0       # El escape está caliente
    presion_colector = 101325.0 # Empieza a presión atmosférica
    # Ley de los gases ideales para saber cuántos moles hay aparcados en el tubo al arrancar
    moles_colector = (presion_colector * volumen_colector) / (R_ideal * temp_colector)
    
    presion_actual = 101325.0 # Presión atmosférica inicial
    volumen_anterior = None   # La creamos vacía antes de arrancar
    # llevar la cuenta del porcentaje de ángulo recorrido (que es independiente del tiempo)
    # y asegurarnos de inyectar exactamente la energía correspondiente a ese porcentaje
    energia_ya_inyectada = 0.0# Esto nos permitirá llevar la cuenta
    
    P_ivc = 101325.0 # Es la presión atmosférica estándar al nivel del mar (en Pascales).
    V_ivc = 1.0      # V_ivc = 1.0: Es 1 metro cúbico.
    capturado_ivc = False
    ciclo_anterior = 0 # <--- Rastreador de cruce de frontera
    # Los ponemos aquí (antes de que empiece el bucle while) para "declarar" que esas variables existen en la memoria.
    # Si no, Python podría llegar a una línea de cálculo, ver que P_ivc no existe, y detenerse en seco con un NameError.
    # --- NUEVO: Rastreador de pico de presión para Chen-Flynn ---
    P_max_ciclo = 101325.0
    # --- NUEVO: Control de Autoignición (Livengood-Wu) ---
    integral_knock = 0.0 # Es un acumulador de los daños del motor
    motor_detonado = False
    
    # Un ciclo Otto de 4 tiempos completo son 2 vueltas de cigüeñal (720 grados = 4*pi radianes)
    # while theta_actual <= 4 * np.pi:
    # Cambiamos la línea anterior del while por esta condición doble para uqe cuand ola velocidad angular caiga, se pare el bucle
    # while theta_actual <= 4 * np.pi and omega > 0.0:
        
    # Dejamos que el motor dé 4 vueltas de cigüeñal (2 ciclos de 4 tiempos) el "Ciclo de Convergencia" usado por la industria.
    # El primer ciclo es "fantasma" para estabilizar los gases residuales de forma natural.
    # No es un apaño porque en la ingeniería de simulación computacional (como en GT-SUITE o Ricardo WAVE),
    # lo usan y recibe el nombre de "Convergencia al estado estacionario".
    while theta_actual <= 8 * np.pi and omega > 0.0:
        theta_ciclo = theta_actual % (4 * np.pi) # El ángulo del ciclo actual (vuelve a 0 cada 720 grados)
        ciclo_actual_num = int(theta_actual / (4 * np.pi)) # Lo pasamos a entero para que no queden decimales sueltos
        
        # 1. CINEMÁTICA (Dónde está el pistón y a qué velocidad geométrica se mueve)
        pos_x = posicion_piston(theta_actual, r, l)
        
        # OJO AQUÍ: Le pasamos 'volumen_camara' al final de la función
        volumen, area = volumen_cilindro(pos_x, r, l, ancho_cilindro, volumen_camara)
        
        vel_piston, accel_piston = cinematica_exacta_piston(theta_actual, omega, alfa_actual, r, l)
        
        # MEJORA del simulador
        # Área dinámica: Culata + Cabeza del pistón (2 * area) + Área lateral descubierta
        # pos_x es la distancia desde el centro del cigüeñal. La altura expuesta es la altura máxima menos pos_x.
        altura_maxima = r + l 
        altura_expuesta = altura_maxima - pos_x
        area_total_expuesta = (2 * area) + (np.pi * ancho_cilindro * altura_expuesta)
        # Velocidad media del pistón (2 * carrera * RPM / 60)
        vel_media_piston = (2 * (2*r) * rpm_actual) / 60.0
        
        # -------------------------------------------------------------
        # DINÁMICA DEL COLECTOR DE ESCAPE (Ocurre en todo momento)
        # -------------------------------------------------------------
        if moles_colector > 0.0:
            # 1. Calculamos a qué presión está el tubo en este instante exacto
            presion_colector = calcular_presion(moles_colector, temp_colector, volumen_colector)
            # 2. El gas escapa a la calle (101325.0 Pa) regido por el flujo estrangulado de Saint-Venant
            moles_salen_calle = calcular_flujo_molar_valvula(presion_colector, 101325.0, temp_colector, area_tubo_escape) * dt
            # 3. Restamos los moles que se han ido a la atmósfera
            moles_colector = max(1e-5, moles_colector - moles_salen_calle)
        
        # 2. ESTADOS DEL MOTOR (TERMODINÁMICA)
        
        # FASE 1: ADMISIÓN (De 0º a 180º)
        if 0.0 <= theta_ciclo < np.pi:
            # FOTO AL HUMO: Capturamos los moles residuales justo al empezar. Disparador por cambio de ciclo absoluto (se supone que es Infalible)
            if ciclo_actual_num > ciclo_anterior: 
                moles_residuales = moles_actuales
                capturado_ivc = False
                ciclo_anterior = ciclo_actual_num # Actualizamos para no volver a entrar hasta el siguiente
            
            # Perfil de la leva (la válvula abre y cierra formando una curva senoidal)
            area_valvula_actual = area_valvula_max * np.sin(theta_ciclo)
            # La apertura empieza en cero, acelera suavemente hasta la apertura máxima en el centro de la fase, y vuelve a cerrarse
            # suavemente. La forma matemática más limpia, rápida y natural que describe algo que va de 0 a 1 y vuelve a 0 formando
            # una campana suave en un ciclo continuo es una onda senoidal (seno).
            
            # Presión del colector de admisión (Atmosférica o Turbo)
            P_colector = 101325.0 * presion_turbo_real
            
            # Saint-Venant calcula cuántos moles de aire fresco entran en este milisegundo
            moles_nuevos = calcular_flujo_molar_valvula(P_colector, presion_actual, temp_admision, area_valvula_actual) * dt
            
            # Mezcla termodinámica: El aire fresco (ej. 300K) entra y se mezcla con el gas residual (600K).
            # La nueva temperatura es la media ponderada por la cantidad de masa de cada uno.
            if moles_nuevos > 0.0:
                temp_mezcla = ((moles_actuales * temp_actual) + (moles_nuevos * temp_admision)) / (moles_actuales + moles_nuevos)
                # Formula de la Ley de Conservación de la energía: Energia_Total = EnergiaResidual + Energia_Nueva
                # Que se puede escribir como: (n_actual + n_nuevos) * T_mezcla = (n_actual * T_actual) + (n_nuevos * T_admision)
                temp_actual = temp_mezcla
                moles_actuales += moles_nuevos # Los que añadimos al introducir el combustible
                vel_particulas = np.sqrt((2 * k_B * temp_actual) / m) # Al cambiar la T cambia la E y en consecuencia la V
            
            # --- MEJORA: Woschni en Admisión ---
            # El aire choca contra los metales del bloque. Usamos 1 atm como presión motorizada.
            dQ_paredes = calcular_calor_woschni(
                presion_Pa=presion_actual, presion_mot_Pa=101325.0, temp_gas=temp_actual, 
                volumen=volumen, area_expuesta=area_total_expuesta, ancho_cilindro=ancho_cilindro, 
                rpm=rpm_actual, vel_media_piston=vel_media_piston, dt=dt, temp_pared=450.0
            )
            Cv_aire = 20.8 + max(0.0, 0.005 * (temp_actual - 300.0))
            if moles_actuales > 0.0001:
                temp_actual = max(300.0, temp_actual - (dQ_paredes / (moles_actuales * Cv_aire)))
                vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            
            # La presión del cilindro ahora es dinámica (P = nRT/V). Al bajar el pistón, el volumen crece. 
            # Si el turbo empuja mucha masa (n), la presión se mantiene alta. Si gira a 8000 RPM, V crece 
            # tan rápido que 'n' no da abasto y se crea un vacío que resta potencia.
            presion_actual = calcular_presion(moles_actuales, temp_actual, volumen)
        
        
        # FASE 2: COMPRESIÓN (De 180º a 360º)
        elif np.pi <= theta_ciclo < 2 * np.pi:
            
            energia_ya_inyectada = 0.0
            
            # MEJORA del simulador
            # Capturamos P1 y V1 al cruzar la barrera de pi (180º) por primera vez
            if not capturado_ivc:
                P_ivc = presion_actual
                V_ivc = volumen
                # Cálculo del humo para saber qué porcentaje de lo que hay aquí dentro es humo antiguo que no reaccionará
                if moles_actuales > 0:
                    X_r = moles_residuales / moles_actuales 
                else:
                    X_r = 0.0
                
                capturado_ivc = True  # Ponemos la bandera para que no vuelva a entrar aquí
                
            # CINEMÁTICA DE LAS BOLITAS (Compresión Adiabática que no se incluye en la mejora del motor):
            # Al subir el pistón, el volumen se reduce (volumen < volumen_anterior).
            # Matemáticamente, el rebote de las bolitas contra una pared que se acerca 
            # se modela con el coeficiente adiabático (gamma = 1.4 para el aire).
            # Esto sube la temperatura drásticamente sin aportar calor externo.
            
            if volumen_anterior is not None:
                # Relación de compresión de este milisegundo exacto
                ratio_compresion_dt = volumen_anterior / volumen 
                
                # La temperatura sube por el aplastamiento de las bolitas
                temp_actual = temp_actual * (ratio_compresion_dt ** (1.4 - 1.0))
                
                # Actualizamos la velocidad microscópica de las bolitas
                vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            # Con los moles fijos, menos volumen y muchísima más temperatura, 
            # la presión se disparará sola al aplicar la Ley de los Gases Ideales después de los if/elif.
            
            # --- MEJORA: INTERSTICIOS GEOMÉTRICOS (Crevices) ---
            moles_escondidos = (presion_actual * V_crevice) / (R_ideal * temp_pared) # Moles de gasolina que se quedan en los anillos
            moles_activos = max(0.0001, moles_actuales - moles_escondidos)
            
            # Calcular la presión actual (dictada unicamente por el gas libre en el cilindro) para alimentar a Woschni
            presion_actual = calcular_presion(moles_activos, temp_actual, volumen)
            
            # Presión motorizada analítica
            gamma = 1.4 if temp_actual < 1000 else 1.3 # El gamma cae a altas T
            # if/else escrito en una sola línea (operador ternario). Hace esto:
                # Si la temperatura es menor de 1000 Kelvin, la variable gamma vale 1.4.
                # Si la temperatura es 1000 Kelvin o mayor, gamma vale 1.3.
            presion_mot_actual = P_ivc * ((V_ivc / volumen)**gamma)
            
            # Calculamos el calor perdido en este milisegundo
            dQ_paredes = calcular_calor_woschni(                # Al poner nombre_del_parametro = valor, fuerzo a que cada dato
                presion_Pa=presion_actual,                      # vaya a su sitio correcto. Cuando una función tiene 10 parámetros,
                presion_mot_Pa=presion_mot_actual,              # es facilísimo despistarse y pasarle las rpm donde iba el volumen,
                temp_gas=temp_actual,                           # o el dt donde iba el ancho_cilindro. Python no daría error, pero
                volumen=volumen,                                # el cálculo no sería el correcto. Escribirlo de esta forma
                area_expuesta=area_total_expuesta,              # (llamada Keyword Arguments) es una práctica profesional
                ancho_cilindro=ancho_cilindro,                  # para evitar errores catastróficos, sabiendo siempre qué se está
                rpm=rpm_actual,                                 # enviando a la función.
                vel_media_piston=vel_media_piston, 
                dt=dt, 
                temp_pared=450.0
            )
            
            # La Temperatura es la única variable que significa exactamente lo mismo tanto en la escala macroscópica
            # (el motor entero) como en la escala microscópica (bolita solitaria)            
            # --- MEJORA: Calor Específico Variable --- A 300K la capacidad calorífica a volumen constante (Cv) del aire es ~20.8 J/(mol·K)
            # A 2000K sube a ~30 J/molK debido a la activación de modos vibracionales (disociaciones de moleculas)
            Cv_aire = 20.8 + max(0.0, 0.005 * (temp_actual - 300.0))
            # Usamos el Cv_aire (20.8 J/mol·K) porque estamos modificando la Energía Interna del gas. La Ley de Joule demuestra
            # que la energía interna de un gas ideal depende única y exclusivamente de su temperatura, y esa relación matemática
            # se define siempre usando el Cv (dU = n*Cv*dT), independientemente de si el pistón se está moviendo o no en ese instante.
            # Usamos el Cv del aire, porque la inmensa mayoria de moles que prenden en el motor son de aire.
            
            # 2. ¿Cuánta temperatura perdemos por ese calor fugado? (dT = Q / (n * Cv))
            # Añadimos un pequeño escudo por si los moles son cero en algún milisegundo extraño
            if moles_activos > 0.0001:
                caida_temp = dQ_paredes / (moles_activos * Cv_aire)
            else:
                caida_temp = 0.0
            
            # 3. Actualizamos la temperatura macroscópica
            temp_actual = max(300.0, temp_actual - caida_temp) # Evitamos que la energía baje de 0 + nunca por debajo del ambiente
            # Si en un momento dado, por un pico de presión extremo o un paso de tiempo (dt) muy grande, la fórmula de Woschni
            # calcula que se pierde más calor del que tiene el gas, la resta daría un número negativo
            # Luego "np.sqrt()" La raíz cuadrada de un número negativo destruye el programa y lanza un error.
            # La función max(A, B) elige el número que sea más grande. Al poner max(300.0, la_resta), decimos a Python:
            # "Haz la resta. Si sale bien, pon eso. Pero si la resta da menos de 300.0, ignórala y pon 300.0".
            # No ponemos 0.0 porque elevar un número a una potencia negativa es lo mismo que dividir por lo que (temp_gas-0.55)
            # es exactamente igual a 1 / (temp_gas0.55). Si la temperatura es 0.0 el código intentaría dividir entre cero.
            # Python detendría la simulación en seco con un error fatal de ZeroDivisionError.
            # Con poner 300.0 vale por ser la temperatura ambiente y al ser temperaturas de miles de grados es bastante bajo.
            
            # 4. Actualizamos el mundo microscópico para que la velocidad de las bolitas coincida
            # Fórmula de la Teoría Cinética de los Gases (T = (m*v**2)/2*k_B)
            vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            
            # --- NUEVO: INTEGRAL DE LIVENGOOD-WU (Riesgo de Detonación) ---
            # Solo calculamos el knock si el motor no ha detonado ya y si hay gasolina (el H2 tiene otra cinética)
            if not motor_detonado and not es_hidrogeno:
                # 1. Ajustamos la barrera térmica de la gasolina según su Octanaje (RON)
                # 95 RON es la base. Con 98 RON, la energía de activación sube, resistiendo más temperatura.
                energia_activacion = 8000.0 * (octanaje / 95.0) 
                # 2. Fórmula de Arrhenius para el retraso a la autoignición (tau). 
                # Presión Alta y Temperatura Alta = tau se vuelve en un número minúsculo (el tiempo se agota).
                # Usamos un try/except oculto controlando el exponente para evitar desbordamientos matemáticos
                exponente = energia_activacion / max(300.0, temp_actual)
                if exponente < 50.0: # Límite de seguridad para el float64 de numpy
                    tau = 0.0001 * ((101325.0 / presion_actual)**1.2) * np.exp(exponente)
                    
                    # 3. Sumamos la fracción de daño de este milisegundo a la integral
                    integral_knock += (dt / tau)
                    
                    # 4. Si la suma llega al 100% (1.0) antes de que la bujía lo queme todo... BOOM.
                    if integral_knock >= 1.0:
                        motor_detonado = True
        
        # FASE 3: EXPANSIÓN Y COMBUSTIÓN (De 360º a 540º)
        elif 2 * np.pi <= theta_ciclo < 3 * np.pi:
            
            # 1. EXPANSIÓN ADIABÁTICA (El enfriamiento real y físico)
            # El pistón baja, aumentando el volumen. Al igual que en la compresión, usamos el proceso adiabático.
            # Pero como el volumen nuevo es MAYOR, el ratio es menor a 1, por lo que la temperatura caerá naturalmente.
            # (El gas gasta su propia energía térmica en empujar el pistón).
            
            # 1. EXPANSIÓN ADIABÁTICA
            if volumen_anterior is not None:
                ratio_expansion_dt = volumen_anterior / volumen 
                temp_actual = temp_actual * (ratio_expansion_dt ** (1.4 - 1.0))
                
                vel_particulas = np.sqrt((2 * k_B * temp_actual) / m) # ---> Actualizamos la velocidad antes de la chispa <---
            
            # 2. LA CHISPA SUAVE (Simulamos la velocidad del frente de llama)
            # Basada en posición absoluta, 100% independiente de dt y RPM
            # En lugar de explotar todo en un milisegundo, la llama dura unos 20 grados.
            # 20 grados equivalen a aprox 0.35 radianes. Pero ponemos duración de chispa porque dependerá si usamos gasolina o H2
            inicio_chispa = 2 * np.pi
            # La llama se frena: Alargamos los grados que tarda en quemar según el humo
            duracion_chispa_real = duracion_chispa * (1.0 + factor_egr_coche * X_r)
            fin_chispa = inicio_chispa + duracion_chispa_real
            
            if inicio_chispa <= theta_ciclo <= fin_chispa:
                if tipo_combustible == "carreras": delta_E = 6.5e-20
                else: delta_E = 5.0e-20
                
                delta_E *= multiplicador_energia
                
                # --- MODELO CINÉTICO DE WIEBE ---
                # Parámetros empíricos (a = 5.0 y m = 2.0 son el estándar universal para motores Otto)
                a_wiebe = 5.0
                m_wiebe = 2.0
                # La función de Wiebe no es una ley física pura, es una correlación empírica.
                # El parámetro a (factor de eficiencia) determina cuánto combustible se ha quemado al llegar al final de los grados
                # estipulados. Un valor de a = 5 garantiza que al terminar el periodo se haya quemado el 99.3% del combustible, lo
                # cual coincide exactamente con la eficiencia térmica de los motores Otto de 4 tiempos.
                # El parámetro m (factor de forma) modela cómo crece el núcleo de la llama. Con m = 2, la ecuación crea una curva
                # en "S". Al principio quema muy poco (núcleo incipiente), en el medio explota la mayor parte de la energía
                # (frente de llama expandiéndose), y al final se frena suavemente (la llama choca contra las paredes frías).
                
                # Progreso geométrico relativo del cigüeñal (de 0.0 a 1.0)
                theta_relativo = (theta_ciclo - inicio_chispa) / duracion_chispa_real # Aplicamos la nueva duración
                # Normalizamos el avance de la combustión. No importa si el motor va a 800 RPM o a 7000 RPM,
                # theta_relativo siempre será un valor que va de 0.0 (justo al saltar la chispa) a 1.0 (al apagarse la llama).

                # Fracción de masa quemada (x_b) según la ecuación en "S" de Wiebe (aplicando la ecuancion de Wive)
                x_b = 1.0 - np.exp(-a_wiebe * (theta_relativo ** (m_wiebe + 1.0)))
                
                # Cuánta energía TOTAL debería haber liberado la llama hasta este ángulo exacto
                energia_total_ideal = delta_E * x_b
                # En lugar de calcular cuánta energía se quema en el instante dt (lo cual es muy propenso a errores si los tiempos varían),
                # se calcula cuánta energía debería haber en total en la cámara en ese ángulo exacto (energia_total_ideal).
                # Al restarle energia_ya_inyectada (que guarda el estado del fotograma anterior de la simulación),
                # se obtiene matemáticamente la energia_aportada exacta de ese instante, sin perder ningún Joule por el redondeo de Python.
                
                # Inyectamos solo la diferencia que falta desde el dt anterior (Derivada implícita)
                energia_aportada_teorica = energia_total_ideal - energia_ya_inyectada
                energia_ya_inyectada = energia_total_ideal # Actualizamos la cuenta
                
                # Estas 4 líneas son para asfixiar la llama (efecto crevice):
                moles_escondidos = (presion_actual * V_crevice) / (R_ideal * temp_pared)
                moles_activos = max(0.0001, moles_actuales - moles_escondidos)
                fraccion_activa = moles_activos / moles_actuales
                energia_aportada = energia_aportada_teorica * fraccion_activa
                
                # --- MEJORA: DISOCIACIÓN TÉRMICA (El muro térmico) ---
                # A partir de 2000 K, el gas empieza a desarmarse (disociación) absorbiendo energía masivamente.
                # Lo simulamos restando un porcentaje (epsilon) a la energía que iba a generar presión.
                if temp_actual > 2000.0:
                    # Función cuadrática: a 2000K corta 0%, a 2500K corta el 25%, a 3000K corta el 100% (muro absoluto).
                    epsilon = min(1.0, ((temp_actual - 2000.0) / 1000.0)**2)
                else:
                    epsilon = 0.0
                    
                energia_aportada_util = energia_aportada * (1.0 - epsilon)
                
                # Sumamos la energía útil a las bolitas microscópicas
                energia_cinetica_actual = 0.5 * m * (vel_particulas**2)
                nueva_energia_cinetica = energia_cinetica_actual + energia_aportada_util
                
                vel_particulas = np.sqrt((2 * nueva_energia_cinetica) / m)
                temp_actual = (m * (vel_particulas**2)) / (2 * k_B)
            
            elif theta_ciclo > fin_chispa:
                # RED DE SEGURIDAD NUMÉRICA: Inyectamos la energía que el 'dt' se saltó
                if energia_ya_inyectada > 0.0: 
                    if tipo_combustible == "carreras": delta_E = 6.5e-20
                    else: delta_E = 5.0e-20
                    
                    delta_E *= multiplicador_energia
                    
                    # Inyectamos exactamente lo que faltaba para el 100%
                    energia_aportada_teorica = delta_E - energia_ya_inyectada
                    energia_ya_inyectada = 0.0 # Ahora sí reseteamos para el próximo ciclo
                    
                    # Líneas para hacer esa última inyección proporcional
                    moles_escondidos = (presion_actual * V_crevice) / (R_ideal * temp_pared)
                    moles_activos = max(0.0001, moles_actuales - moles_escondidos)
                    fraccion_activa = moles_activos / moles_actuales
                    energia_aportada = energia_aportada_teorica * fraccion_activa
                    
                    # --- MEJORA: DISOCIACIÓN TÉRMICA (El muro térmico) ---
                    if temp_actual > 2000.0:
                        epsilon = min(1.0, ((temp_actual - 2000.0) / 1000.0)**2)
                    else:
                        epsilon = 0.0
                        
                    energia_aportada_util = energia_aportada * (1.0 - epsilon)
                    
                    # Sumamos la energía útil a las bolitas microscópicas
                    energia_cinetica_actual = 0.5 * m * (vel_particulas**2)
                    nueva_energia_cinetica = energia_cinetica_actual + energia_aportada_util
                    
                    vel_particulas = np.sqrt((2 * nueva_energia_cinetica) / m)
                    temp_actual = (m * (vel_particulas**2)) / (2 * k_B)
                else:
                    # Expansión normal si la energía ya se inyectó completamente
                    vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            
            # --- MEJORA: INTERSTICIOS GEOMÉTRICOS (Crevices) ---
            moles_escondidos = (presion_actual * V_crevice) / (R_ideal * temp_pared) # Moles de gasolina que se quedan en los anillos
            moles_activos = max(0.0001, moles_actuales - moles_escondidos)
            
            # Calcular la presión actual (dictada unicamente por el gas libre en el cilindro) para alimentar a Woschni
            presion_actual = calcular_presion(moles_activos, temp_actual, volumen)
            
            # Presión motorizada analítica
            gamma = 1.4 if temp_actual < 1000 else 1.3 # El gamma cae a altas T
            # if/else escrito en una sola línea (operador ternario). Hace esto:
                # Si la temperatura es menor de 1000 Kelvin, la variable gamma vale 1.4.
                # Si la temperatura es 1000 Kelvin o mayor, gamma vale 1.3.
            presion_mot_actual = P_ivc * ((V_ivc / volumen)**gamma)
            
            # Calculamos el calor perdido en este milisegundo
            dQ_paredes = calcular_calor_woschni(                # Al poner nombre_del_parametro = valor, fuerzo a que cada dato
                presion_Pa=presion_actual,                      # vaya a su sitio correcto. Cuando una función tiene 10 parámetros,
                presion_mot_Pa=presion_mot_actual,              # es facilísimo despistarse y pasarle las rpm donde iba el volumen,
                temp_gas=temp_actual,                           # o el dt donde iba el ancho_cilindro. Python no daría error, pero
                volumen=volumen,                                # el cálculo no sería el correcto. Escribirlo de esta forma
                area_expuesta=area_total_expuesta,              # (llamada Keyword Arguments) es una práctica profesional
                ancho_cilindro=ancho_cilindro,                  # para evitar errores catastróficos, sabiendo siempre qué se está
                rpm=rpm_actual,                                 # enviando a la función.
                vel_media_piston=vel_media_piston, 
                dt=dt, 
                temp_pared=450.0
            )
            
            # La Temperatura es la única variable que significa exactamente lo mismo tanto en la escala macroscópica
            # (el motor entero) como en la escala microscópica (bolita solitaria)            
            # --- MEJORA: Calor Específico Variable --- A 300K la capacidad calorífica a volumen constante (Cv) del aire es ~20.8 J/(mol·K)
            # A 2000K sube a ~30 J/molK debido a la activación de modos vibracionales (disociaciones de moleculas)
            Cv_aire = 20.8 + max(0.0, 0.005 * (temp_actual - 300.0))
            # Usamos el Cv_aire (20.8 J/mol·K) porque estamos modificando la Energía Interna del gas. La Ley de Joule demuestra
            # que la energía interna de un gas ideal depende única y exclusivamente de su temperatura, y esa relación matemática
            # se define siempre usando el Cv (dU = n*Cv*dT), independientemente de si el pistón se está moviendo o no en ese instante.
            # Usamos el Cv del aire, porque la inmensa mayoria de moles que prenden en el motor son de aire.
            
            # 2. ¿Cuánta temperatura perdemos por ese calor fugado? (dT = Q / (n * Cv))
            # Añadimos un pequeño escudo por si los moles son cero en algún milisegundo extraño
            if moles_activos > 0.0001:
                caida_temp = dQ_paredes / (moles_activos * Cv_aire)
            else:
                caida_temp = 0.0
            
            # 3. Actualizamos la temperatura macroscópica
            temp_actual = max(300.0, temp_actual - caida_temp) # Evitamos que la energía baje de 0 + nunca por debajo del ambiente
            # Si en un momento dado, por un pico de presión extremo o un paso de tiempo (dt) muy grande, la fórmula de Woschni
            # calcula que se pierde más calor del que tiene el gas, la resta daría un número negativo
            # Luego "np.sqrt()" La raíz cuadrada de un número negativo destruye el programa y lanza un error.
            # La función max(A, B) elige el número que sea más grande. Al poner max(300.0, la_resta), decimos a Python:
            # "Haz la resta. Si sale bien, pon eso. Pero si la resta da menos de 300.0, ignórala y pon 300.0".
            # No ponemos 0.0 porque elevar un número a una potencia negativa es lo mismo que dividir por lo que (temp_gas-0.55)
            # es exactamente igual a 1 / (temp_gas0.55). Si la temperatura es 0.0 el código intentaría dividir entre cero.
            # Python detendría la simulación en seco con un error fatal de ZeroDivisionError.
            # Con poner 300.0 vale por ser la temperatura ambiente y al ser temperaturas de miles de grados es bastante bajo.
            
            # 4. Actualizamos el mundo microscópico para que la velocidad de las bolitas coincida
            # Fórmula de la Teoría Cinética de los Gases (T = (m*v**2)/2*k_B)
            vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            
            # --- NUEVO: INTEGRAL DE LIVENGOOD-WU (Riesgo de Detonación en Combustión) ---
            # Solo evaluamos si el motor está sano, usa gasolina, y la llama aún no ha terminado
            if not motor_detonado and not es_hidrogeno and (theta_ciclo < fin_chispa):
                energia_activacion = 8000.0 * (octanaje / 95.0) 
                exponente = energia_activacion / max(300.0, temp_actual)
                
                if exponente < 50.0:
                    tau = 0.0001 * ((101325.0 / presion_actual)**1.2) * np.exp(exponente)
                    integral_knock += (dt / tau)
                    
                    if integral_knock >= 1.0:
                        motor_detonado = True
        
        # FASE 4: ESCAPE (De 540º a 720º)
        elif 3 * np.pi <= theta_ciclo <= 4 * np.pi:
            
            # Perfil de la leva de escape (senoidal de 3*pi a 4*pi)
            area_valvula_actual = area_valvula_max * np.sin(theta_ciclo - 3 * np.pi)
            # Al restarle 3*pi a la posición actual, engañamos a la fórmula. Cuando el motor va por el grado 540 (3*pi),
            # la ecuación hace: np.sin(3*pi - 3*pi) = np.sin(0). Así obligamos a la curva senoidal a empezardesde cero
            # en el momento en que se abre la válvula de escape.
            
            # --- MEJORA 0D PLENUM: TRANSFERENCIA DE MASA ---
            # El cilindro ya no empuja contra una presión atmosférica matemática, 
            # sino contra la presión real acumulada en el paso anterior (presion_colector).
            moles_por_segundo = calcular_flujo_molar_valvula(presion_actual, presion_colector, temp_actual, area_valvula_actual)
            moles_salen_cilindro = moles_por_segundo * dt
            
            # El cilindro pierde masa, pero el colector la gana (Conservación de la masa absoluta)
            moles_actuales = max(1e-5, moles_actuales - moles_salen_cilindro)
            moles_colector += moles_salen_cilindro
            
            # Actualización de temperaturas
            proporcion_vaciado = (4 * np.pi - theta_ciclo) / np.pi
            temp_actual = 600.0 + (temp_actual - 600.0) * proporcion_vaciado
            vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            
            # --- MEJORA: Woschni en Escape ---
            # El gas hirviendo transfiere calor masivamente a la válvula y la culata al salir.
            dQ_paredes = calcular_calor_woschni(
                presion_Pa=presion_actual, presion_mot_Pa=101325.0, temp_gas=temp_actual, 
                volumen=volumen, area_expuesta=area_total_expuesta, ancho_cilindro=ancho_cilindro, 
                rpm=rpm_actual, vel_media_piston=vel_media_piston, dt=dt, temp_pared=450.0
            )
            Cv_aire = 20.8 + max(0.0, 0.005 * (temp_actual - 300.0))
            if moles_actuales > 0.0001:
                temp_actual = max(300.0, temp_actual - (dQ_paredes / (moles_actuales * Cv_aire)))
                vel_particulas = np.sqrt((2 * k_B * temp_actual) / m)
            
            # La presión del cilindro al chocar contra este tapón
            presion_actual = calcular_presion(moles_actuales, temp_actual, volumen)
        
        # ------------------------------------------------------------
        # Otra forma pero no vale porque K es una aproximación 
        
            # La válvula de escape se abre, pero el tubo de escape genera restricción (Pumping Losses)
            # Presión = P_atmosferica + K * (RPM^2)
            # Donde K es el coeficiente de restricción geométrica del tubo de escape (ej. 0.002)
#            k_escape = 0.002 
#            contrapresion = k_escape * (rpm_actual**2)
#            presion_actual = 101325.0 + contrapresion # Ecuación de Darcy-Weisbach para dinámica de fluidos.
            
            # El pistón sube, empujando el humo hacia fuera. Los moles van disminuyendo progresivamente hasta casi cero al llegar arriba.
#            proporcion_vaciado = (4 * np.pi - theta_actual) / np.pi
#            moles_actuales = moles_totales * proporcion_vaciado
            
            # La temperatura cae drásticamente al salir el gas caliente y perder presión
#            temp_actual = 300.0 + (temp_actual - 300.0) * proporcion_vaciado
        # -------------------------------------------------------------
        
    # 3. TERMODINÁMICA MACROSCÓPICA (Ley de los Gases Ideales)
        # En la Fase 1 y 4, la válvula está abierta y la presión ya la hemos fijado a la del colector/escape.
        # Pero en la Fase 2 y 3 (válvulas cerradas), la presión se rige por la Ley de los Gases:
        if np.pi <= theta_ciclo < 3 * np.pi:
            presion_actual = calcular_presion(moles_actuales, temp_actual, volumen)
        
    # 4. DINÁMICA DE SÓLIDOS (Torque y Fricción)
        # 1. Actualizamos la presión máxima vista en este ciclo (necesaria para la fricción de cojinetes)
        if presion_actual > P_max_ciclo: 
            P_max_ciclo = presion_actual
            # En cada paso dt el código comprueba si la presión actual ha superado el récord del ciclo.
            # Esto asegura que capturemos el pico exacto de la combustión
        
        # 2. Torque termodinámico puro (Indicado)
        fuerza, torque_ind = calcular_fuerza_y_torque_indicado(presion_actual, area, theta_actual, r, l)
        
        # 3. MODELO DE CHEN-FLYNN DINÁMICO (Leyendo los diccionarios de la base de datos)
        # Presión Media Efectiva de Fricción (PMEF) multiplicada por el factor del aceite
        PMEF = (coche["cf_C1"] + (coche["cf_C2"] * P_max_ciclo) + (coche["cf_C3"] * vel_media_piston) + (coche["cf_C4"] * (vel_media_piston**2))) * aceites_motor[aceite]
        # Constantes empíricas ajustadas para trabajar en Pascales
            # C1. Fricción base constante (Bomba de agua, alternador, distribución)
            # C2. Factor de carga (Cojinetes aplastados proporcionalmente por el pico de presión)
            # C3. Rozamiento hidrodinámico mixto (Anillos del pistón contra la camisa a media velocidad)
            # C4. Arrastre puro y bombeo de aceite a altas RPM
        # No tengo un laboratorio físico, ni un banco de pruebas, ni acceso a los documentos técnicos clasificados de las fábricas
        # de Ferrari o Porsche. Por tanto, esos números no son valores absolutos de laboratorio sacados de un manual de taller
        # confidencial. Lo que he proporcionado son estimaciones de ingeniería altamente fundamentadas. En el mundo de la
        # simulación 0D, cuando no se tiene el motor físico delante, los coeficientes de Chen-Flynn se deducen a partir de la
        # arquitectura y la época del motor.

        # Convertimos esa presión matemática en un Torque de Fricción real (Nm) que se opone al cigüeñal
        torque_friccion = (PMEF * volumen_desplazado) / (4 * np.pi) # formula física universal
        
        # --- PENALIZACIÓN POR DETONACIÓN (FÍSICA REALISTA) ---
        if motor_detonado:
            # En la realidad, si el motor revienta (biela doblada o pistón perforado), 
            # pierde su capacidad de generar trabajo. El torque del gas (indicado) desaparece.
            # El motor se convierte en un trozo de metal inerte. Multiplicamos la fricción 
            # simulando el arrastre de los metales rotos, obligando al motor a calarse rápidamente.
            torque_efectivo = 0.0 - (torque_friccion * 2.5) 
        else:
            # El torque real al freno (el que llega a las ruedas) en condiciones normales es el indicado menos la fricción
            torque_efectivo = torque_ind - torque_friccion
        
        # 5. TELEMETRÍA (Guardamos la "caja negra" del coche grabando solo el segundo ciclo estabilizado, a partir de 720º)
        if theta_actual >= 4 * np.pi:
            datos_theta.append(theta_actual - 4 * np.pi) # Reseteamos la X a 0 para la gráfica
            datos_posicion.append(pos_x)
            datos_volumen.append(volumen)
            datos_presion.append(presion_actual)
            datos_fuerza.append(fuerza)
            
            datos_torque.append(torque_efectivo) # ATENCIÓN: Guardamos el torque_efectivo, que ya incluye el peaje mecánico de Chen-Flynn
            
            datos_rpm.append(rpm_actual)
            datos_temperatura.append(temp_actual)
            datos_velocidad.append(vel_piston)
            datos_aceleracion.append(accel_piston)
        
        # 6. INTEGRACIÓN NUMÉRICA (El avance del tiempo de Euler)
        aceleracion_angular = torque_efectivo / inercia_motor
        omega += aceleracion_angular * dt
        rpm_actual = (omega * 60.0) / (2 * np.pi)
        alfa_actual = aceleracion_angular
        volumen_anterior = volumen # Guardamos la foto del volumen antes de avanzar el tiempo
        # Avanzamos el reloj
        theta_actual += omega * dt
    
    # =====================================================================
    # 7. POST-PROCESADO: EQUILIBRADO MULTICILÍNDRICO
    # =====================================================================
    if len(datos_theta) == 0:
        return [], [], [], [], [], [], [], [0.0] * num_cilindros, [], 0.0, 0.0
    # Significa "es exactamente igual a cero". En conjunto, la condición if len(datos_theta) == 0: significa:
        # "Si la lista de ángulos está vacía (tiene 0 elementos), porque el motor ha detonado y se ha parado antes de llegar a
        # la fase donde empezamos a guardar datos...".
    
    arr_theta = np.array(datos_theta)
    arr_torque_1cil = np.array(datos_torque)
    arr_torque_total = np.zeros_like(arr_torque_1cil)
    
    # Extraemos la lista de ángulos reales (en grados) del diccionario
    angulos_grados = coche["angulos_encendido"]
    
    for i in range(num_cilindros):
        # 1. Cogemos el ángulo del cilindro 'i' y lo pasamos a radianes
        desfase_rad = angulos_grados[i] * (np.pi / 180.0)
        
        # 2. Desfasamos el eje X aplicando el retraso específico de ese cilindro
        theta_shift = (arr_theta - desfase_rad) % (4 * np.pi)
        
        # 3. Interpolamos la curva de torque para ese desfase
        torque_i = np.interp(theta_shift, arr_theta, arr_torque_1cil)
        
        # 4. Sumamos al cigüeñal
        arr_torque_total += torque_i
        
    torque_promedio = np.mean(arr_torque_total) # El torque promedio real es la media de esta curva combinada
    
    rpm_final = datos_rpm[-1]
    cv_promedio = calcular_caballos(torque_promedio, np.mean(datos_rpm))
    
    # ATENCIÓN: Devolvemos 'arr_torque_total.tolist()' en lugar de 'datos_torque'del primer código que programe
    return datos_theta, datos_posicion, datos_velocidad, datos_aceleracion, datos_temperatura, datos_presion, datos_fuerza, arr_torque_total.tolist(), datos_volumen, cv_promedio, rpm_final



"""
# =====================================================================
# BANCO DE POTENCIA (TEST PARA SPYDER)
# =====================================================================
if __name__ == "__main__":
    
    print("\n" + "="*50)
    print(" INICIANDO BANCO DE POTENCIA VIRTUAL")
    print("="*50)
    
    coches_a_probar = ["Porsche 911 Turbo S (992)", "Land Rover Discovery (2000)"]
    
    # Vamos a probar cada coche a estas revoluciones
    rpms_de_prueba = [1000, 3000, 5000, 6750] 
    
    for coche in coches_a_probar:
        print(f"\n---> TESTEANDO: {coche}")
        print("RPM\t|\tPOTENCIA (CV)")
        print("-" * 30)
        
        for rpm_test in rpms_de_prueba:
            # Ejecutamos 1 ciclo exacto a estas RPM
            resultados = simular_ciclo_motor(
                coche_elegido=coche, 
                activar_turbo=True, 
                porcentaje_acelerador=100.0, 
                rpm_inicial=rpm_test
            )
            
            # El resultado 9 es el cv_promedio (según tu return)
            cv_obtenidos = resultados[9] 
            
            print(f"{rpm_test} RPM\t|\t{cv_obtenidos:.0f} CV")
"""