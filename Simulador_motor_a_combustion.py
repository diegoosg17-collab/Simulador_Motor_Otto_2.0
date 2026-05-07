# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 00:08:09 2026

@author: diego
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import tempfile
import os

import Ciclo_Otto_Motor_Mathematica as sim_motor

if "Motor Genérico (Por defecto)" in sim_motor.base_datos_coches:
    pass

st.set_page_config(page_title="Telemetría - Banco de Pruebas", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.header("⚙️ Panel de Control")
    with st.expander("🚗 Vehículo y Geometría", expanded=True):
        coche_seleccionado = st.selectbox("Modelo de coche", options=list(sim_motor.base_datos_coches.keys()))
        if coche_seleccionado == "Motor Genérico (Por defecto)":
            st.markdown("---")
            st.markdown("**Modificar Geometría:**")
            def reset_geometria():
                st.session_state.cil_gen = 4; st.session_state.biela_gen = 0.140
                st.session_state.diam_gen = 0.086; st.session_state.carr_gen = 0.086
            if 'cil_gen' not in st.session_state: reset_geometria()
            st.button("🔄 Restablecer Valores Originales", on_click=reset_geometria, use_container_width=True)
            
            cil_val = st.slider("Cilindros", 1, 12, key="cil_gen", step=1)
            biela_val = st.slider("L. Biela (m)", 0.100, 0.200, key="biela_gen", step=0.001)
            diametro_val = st.slider("Diámetro Cilindro / Bore (m)", 0.050, 0.150, key="diam_gen", step=0.001)
            carrera_val = st.slider("Carrera / Stroke (m)", 0.050, 0.150, key="carr_gen", step=0.001)
            
            sim_motor.base_datos_coches[coche_seleccionado]["cilindros"] = cil_val
            sim_motor.base_datos_coches[coche_seleccionado]["l"] = biela_val
            sim_motor.base_datos_coches[coche_seleccionado]["ancho_cilindro"] = diametro_val
            sim_motor.base_datos_coches[coche_seleccionado]["r"] = carrera_val / 2.0 
    
    with st.expander("🔧 Mecánica y Lubricación", expanded=True):
        descripciones_aceite = {
            "Mobil 1 (0W-40)": "Mobil 1 0W-40 (Equilibrado)",
            "Castrol EDGE (5W-30)": "Castrol EDGE 5W-30 (Estándar)",
            "Liqui Moly (10W-60)": "Liqui Moly 10W-60 (Más viscoso / Denso)",
            "Petronas Syntium (0W-20)": "Petronas Syntium 0W-20 (Más líquido / Fluido)"
        }
        aceite_seleccionado = st.selectbox("Tipo de Aceite", options=list(sim_motor.aceites_motor.keys()), format_func=lambda x: descripciones_aceite.get(x, x))
        turbo_activado = st.checkbox("Activar Turbo", value=True)

    with st.expander("🏎️ Conducción", expanded=True):
        acelerador_val = st.slider("Acelerador %", min_value=10.0, max_value=100.0, value=10.0, step=1.0)
        tipo_combustible_val = st.selectbox("Tipo de Combustible", options=["normal", "carreras"])
        comparar_h2 = st.checkbox("🌱 Comparativa con Hidrógeno", value=False)

coche_datos = sim_motor.base_datos_coches[coche_seleccionado]
if len(coche_datos["rpm_ref"]) >= 7: rpm_max = coche_datos["rpm_ref"][-3] 
else: rpm_max = coche_datos["rpm_ref"][-2]

rpm_automatica = 800.0 + ((acelerador_val - 10.0) / 90.0) * (rpm_max - 800.0)

with st.spinner('Procesando fluidos y cinemática...'):
    # 1. PASADA ORIGINAL (GASOLINA)
    resultados = sim_motor.simular_ciclo_motor(
        coche_elegido=coche_seleccionado, activar_turbo=turbo_activado, porcentaje_acelerador=acelerador_val,
        tipo_combustible=tipo_combustible_val, aceite=aceite_seleccionado, rpm_inicial=rpm_automatica,
        es_hidrogeno=False
    )
    th, pos, vel, acc, temp, pres, fza, trq, vol, cv_promedio, rpm_final = resultados

    # --- ESCUDO SALVAVIDAS: CONTROL DE DETONACIÓN (GASOLINA) ---
    if len(th) == 0:
        st.error("💥 ¡El motor ha gripado! La pre-detonación ha reventado los cilindros.")
        # Fabricamos el "electrocardiograma plano" para que Streamlit no se cuelgue
        th = np.linspace(0, 4 * np.pi, 360).tolist()
        pos = [0.0] * 360; vel = [0.0] * 360; acc = [0.0] * 360
        fza = [0.0] * 360; trq = [0.0] * 360; vol = [0.0005] * 360
        temp = [300.0] * 360       # Cae a temperatura ambiente
        pres = [101325.0] * 360    # Cae a presión atmosférica
        cv_promedio = 0.0; rpm_final = 0.0
    
    # Pasamos a grados para la gráfica
    th_grados = [angulo * (180 / np.pi) for angulo in th]

    # 2. SEGUNDA PASADA (HIDRÓGENO)
    if comparar_h2:
        resultados_h2 = sim_motor.simular_ciclo_motor(
            coche_elegido=coche_seleccionado, activar_turbo=turbo_activado, porcentaje_acelerador=acelerador_val,
            tipo_combustible=tipo_combustible_val, aceite=aceite_seleccionado, rpm_inicial=rpm_automatica,
            es_hidrogeno=True
        )
        th_h2, pos_h2, vel_h2, acc_h2, temp_h2, pres_h2, fza_h2, trq_h2, vol_h2, cv_h2, rpm_final_h2 = resultados_h2

        # --- ESCUDO SALVAVIDAS: CONTROL DE DETONACIÓN (HIDRÓGENO) ---
        if len(th_h2) == 0:
            st.error("💥 ¡El motor de Hidrógeno ha reventado!")
            # Fabricamos el "electrocardiograma plano" para el hidrógeno
            th_h2 = np.linspace(0, 4 * np.pi, 360).tolist()
            pos_h2 = [0.0] * 360; vel_h2 = [0.0] * 360; acc_h2 = [0.0] * 360
            fza_h2 = [0.0] * 360; trq_h2 = [0.0] * 360; vol_h2 = [0.0005] * 360
            temp_h2 = [300.0] * 360; pres_h2 = [101325.0] * 360
            cv_h2 = 0.0; rpm_final_h2 = 0.0
            
        th_grados_h2 = [angulo * (180 / np.pi) for angulo in th_h2]

# Guardado en memoria Fantasma
ciclo_nuevo = {'th_grados': th_grados, 'pos': pos, 'vel': vel, 'acc': acc, 'pres': pres, 'temp': temp, 'fza': fza, 'trq': trq, 'vol': vol}
if 'ciclo_actual' in st.session_state: st.session_state.ciclo_anterior = st.session_state.ciclo_actual
st.session_state.ciclo_actual = ciclo_nuevo

st.title("Telemetría - Banco de Pruebas Motor Otto 2D")
st.markdown("---")
col_dibujo, col_metricas = st.columns([1, 2])

with col_dibujo:
    coche_geo = sim_motor.base_datos_coches[coche_seleccionado]
    r, l, ancho = coche_geo["r"], coche_geo["l"], coche_geo["ancho_cilindro"]
    techo = r + l + 0.02

    # Extraemos la información visual de 720º para la animación
    indices_animacion = np.linspace(0, len(th)-1, 40, dtype=int)
    th_anim, pos_anim, temp_anim = [th[i] for i in indices_animacion], [pos[i] for i in indices_animacion], [temp[i] for i in indices_animacion]

    fig_motor, ax_motor = plt.subplots(figsize=(4, 5))
    ax_motor.set_aspect('equal'); ax_motor.axis('off')
    ax_motor.set_xlim(-0.1, 0.1); ax_motor.set_ylim(-0.05, techo + 0.05)

    ax_motor.plot([-ancho/2, -ancho/2], [0, techo], 'k-', lw=3)
    ax_motor.plot([ancho/2, ancho/2], [0, techo], 'k-', lw=3)
    ax_motor.plot([-ancho/2, ancho/2], [techo, techo], 'k-', lw=5)
    ax_motor.plot(0, 0, 'ko', markersize=8)

    bujia, = ax_motor.plot([0], [techo], marker='v', color='white', markersize=8, markeredgecolor='black', zorder=5)
    piston_draw = patches.Rectangle((-ancho/2 + 0.002, pos_anim[0] - 0.02), ancho - 0.004, 0.02, color='gray', ec='black')
    ax_motor.add_patch(piston_draw)
    biela_draw, = ax_motor.plot([], [], color='#e67e22', lw=4)
    ciguenal_draw, = ax_motor.plot([], [], 'k-', lw=4)

    def animar(i):
        pos_y = pos_anim[i]
        piston_draw.set_y(pos_y - 0.02)
        
        # EL ARREGLO: Ya está en radianes y va de 0 a 4*pi (720º). ¡No hay que convertir nada!
        angulo_rad = th_anim[i] 
        c_x, c_y = r * np.sin(angulo_rad), r * np.cos(angulo_rad)
        
        biela_draw.set_data([c_x, 0], [c_y, pos_y - 0.02])
        ciguenal_draw.set_data([0, c_x], [0, c_y])
        
        # ¡Magia 4 Tiempos! La temperatura en la segunda vuelta es de 300K, por lo que la bujía no saltará
        if temp_anim[i] > 1000: 
            bujia.set_color('#ffaa00'); bujia.set_markersize(16)     
        else: 
            bujia.set_color('white'); bujia.set_markersize(8)      
        return piston_draw, biela_draw, ciguenal_draw, bujia

    ani = FuncAnimation(fig_motor, animar, frames=len(th_anim), blit=True)
    fps_dinamico = int(10 + ((acelerador_val - 10) / 90) * 30)
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile: ruta_temporal = tmpfile.name
    ani.save(ruta_temporal, writer='pillow', fps=fps_dinamico)
    st.image(ruta_temporal); os.remove(ruta_temporal); plt.close(fig_motor)

with col_metricas:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Comprobamos si el botón de H2 está activado
    if comparar_h2:
        html_potencia = f"""
        <div style='text-align: center;'>
            <h3 style='color: #7f8c8d; font-weight: bold; margin-bottom: -15px;'>Modelo: {coche_seleccionado}</h3>
            <h1 style='color: #2ecc71; font-size: 38px; margin-bottom: -10px;'>Gasolina: {cv_promedio:.1f} CV</h1>
            <h1 style='color: #39FF14; font-size: 38px; margin-bottom: -15px;'>Hidrógeno: {cv_h2:.1f} CV</h1>
            <h2 style='color: #3498db; font-size: 36px;'>Régimen: {rpm_final:.0f} RPM</h2>
        </div>
        """
    else:
        # Tu diseño original intacto
        html_potencia = f"""
        <div style='text-align: center;'>
            <h3 style='color: #7f8c8d; font-weight: bold; margin-bottom: -15px;'>Modelo: {coche_seleccionado}</h3>
            <h1 style='color: #2ecc71; font-size: 54px; margin-bottom: -15px;'>Potencia: {cv_promedio:.1f} CV</h1>
            <h2 style='color: #3498db; font-size: 36px;'>Régimen: {rpm_final:.0f} RPM</h2>
        </div>
        """
    st.markdown(html_potencia, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Análisis Telemetrico (Estado Actual vs Variación Anterior)")

plt.style.use('seaborn-v0_8-darkgrid')
fig_graf, axs = plt.subplots(4, 2, figsize=(16, 14))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# Añadir x_h2=None, y_h2=None al final de los parámetros
def plot_comparativa(ax, x_act, y_act, color_act, titulo, xlabel, ylabel, ref_key_x, ref_key_y, x_h2=None, y_h2=None):
    # Añadimos la comprobación: and ref_key_x in st.session_state.ciclo_anterior
    if 'ciclo_anterior' in st.session_state and st.session_state.ciclo_anterior and ref_key_x in st.session_state.ciclo_anterior:
        ax.plot(st.session_state.ciclo_anterior[ref_key_x], st.session_state.ciclo_anterior[ref_key_y], color='gray', linestyle='--', linewidth=2, alpha=0.5, label='Ajuste Anterior')
    # Cambiar 'Actual' por 'Gasolina' si se está comparando
    ax.plot(x_act, y_act, color=color_act, linestyle='-', linewidth=2, label='Gasolina' if x_h2 is not None else 'Actual')
    
    # --- AÑADIR SOLO ESTAS DOS LÍNEAS AQUÍ ---
    if x_h2 is not None and y_h2 is not None:
        ax.plot(x_h2, y_h2, color='#39FF14', linestyle='-', linewidth=2, label='Hidrógeno (H2)')
    
    ax.set_title(titulo, fontweight='bold', fontsize=12); ax.set_xlabel(xlabel, fontsize=10); ax.set_ylabel(ylabel, fontsize=10, fontweight='bold')
    ax.legend(loc='upper right')

# --- LÍNEA CLAVE PARA LOS ARGUMENTOS DEL HIDRÓGENO ---
h2_args = lambda x, y: (x, y) if comparar_h2 else (None, None)

# --- LLAMADAS ACTUALIZADAS A LAS GRÁFICAS ---
plot_comparativa(axs[0, 0], th_grados, pos, 'b', "1. Posición del Pistón", "Ángulo Cigüeñal (Grados)", "Altura (m)", 'th_grados', 'pos', *h2_args(th_grados_h2, pos_h2) if comparar_h2 else (None, None))
plot_comparativa(axs[1, 0], th_grados, vel, 'g', "2. Velocidad", "Ángulo Cigüeñal (Grados)", "Velocidad (m/s)", 'th_grados', 'vel', *h2_args(th_grados_h2, vel_h2) if comparar_h2 else (None, None))
plot_comparativa(axs[2, 0], th_grados, acc, 'r', "3. Aceleración", "Ángulo Cigüeñal (Grados)", "Acel. (m/s²)", 'th_grados', 'acc', *h2_args(th_grados_h2, acc_h2) if comparar_h2 else (None, None))
plot_comparativa(axs[3, 0], th_grados, fza, 'k', "4. Fuerza Neta", "Ángulo Cigüeñal (Grados)", "Fuerza (N)", 'th_grados', 'fza', *h2_args(th_grados_h2, fza_h2) if comparar_h2 else (None, None))

axs[0, 1].set_title("5. Presión y Temperatura", fontweight='bold', fontsize=12); axs[0, 1].set_xlabel("Ángulo Cigüeñal (Grados)", fontsize=10)

# Escudo para la Presión (con la línea de Hidrógeno)
if 'ciclo_anterior' in st.session_state and st.session_state.ciclo_anterior and 'th_grados' in st.session_state.ciclo_anterior: 
    axs[0, 1].plot(st.session_state.ciclo_anterior['th_grados'], st.session_state.ciclo_anterior['pres'], color='gray', linestyle='--', alpha=0.5)
axs[0, 1].plot(th_grados, pres, color='purple', linewidth=2, label='Presión Gasolina'); axs[0, 1].set_ylabel("Presión (Pa)", color='purple', fontweight='bold')
if comparar_h2: axs[0, 1].plot(th_grados_h2, pres_h2, color='#39FF14', linewidth=2, label='Presión H2')

ax_temp = axs[0, 1].twinx()
# Escudo para la Temperatura (con la línea de Hidrógeno)
if 'ciclo_anterior' in st.session_state and st.session_state.ciclo_anterior and 'th_grados' in st.session_state.ciclo_anterior: 
    ax_temp.plot(st.session_state.ciclo_anterior['th_grados'], st.session_state.ciclo_anterior['temp'], color='gray', linestyle='--', alpha=0.5)
ax_temp.plot(th_grados, temp, color='orange', linewidth=2, label='Temp Gasolina'); ax_temp.set_ylabel("Temperatura (K)", color='orange', fontweight='bold')
if comparar_h2: ax_temp.plot(th_grados_h2, temp_h2, color='#A8FF98', linewidth=2, linestyle=':', label='Temp H2') # Un verde suave para distinguir

plot_comparativa(axs[1, 1], vol, pres, 'k', "6. Diagrama P-V", "Volumen Cilindro (m³)", "Presión (Pa)", 'vol', 'pres', *h2_args(vol_h2, pres_h2) if comparar_h2 else (None, None))
plot_comparativa(axs[2, 1], th_grados, trq, 'crimson', "7. Torque Motor por Cilindro", "Ángulo Cigüeñal (Grados)", "Torque (Nm)", 'th_grados', 'trq', *h2_args(th_grados_h2, trq_h2) if comparar_h2 else (None, None))
axs[3, 1].axis('off')
st.pyplot(fig_graf)


# =====================================================================
# COMO EJECUTAR EL PROGRAMA
# =====================================================================

# 1. Abrir Anaconda Prompt desde el menú de inicio de Windows.
# 2. Copiar y pegar esta ruta para ir a la carpeta y pulsa Enter:
#    cd C:\Users\diego\UPV\Primero_de_carrera\008_Calculo_II\Trabajo_poster\Programa_definitivo

# En caso de no tener instalado Streamlit, asegúrate de instalarlo dentro de Anaconda escribiendo esto y pulsando Enter:
# pip install streamlit             (Esperar a que se termine de descargar).

# 3. Escribir el comando siguiente y pulsa Enter:
#    streamlit run Simulador_motor_a_combustion.py