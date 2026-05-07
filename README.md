# Simulador_Motor_Otto_2.0
Abstract: Simulador interactivo 0D de motores termodinámicos (Ciclo Otto) con física realista: convección de Woschni, combustión de Wiebe, flujo de Saint-Venant y fricción de Chen-Flynn. Creado con Python y Streamlit. Cuenta con un catalogo de coches y otras funciones (combustible, aceite...) ademásd de sliders para comparar gráficas.


# Simulador Termodinámico de Motores Otto 0D (Banco de Pruebas Virtual)
Este proyecto es un simulador interactivo de motores de combustión interna basado en modelos termodinámicos de cero dimensiones (0D). Ha evolucionado de un modelo adiabático ideal a un motor virtual riguroso que incorpora pérdidas térmicas, fricción mecánica, dinámica de fluidos compresibles y límites cinéticos.
El simulador cuenta con una interfaz web analítica construida en Streamlit que permite modificar la geometría y los parámetros operativos en tiempo real, ofreciendo telemetría detallada del comportamiento interno del motor.

# ⚙️ Arquitectura Física y Termodinámica (Backend)
El núcleo matemático (Ciclo_Otto_Motor_Mathematica.py) ha sido reescrito para abandonar las suposiciones ideales y enfrentar el motor a las leyes físicas reales. Las principales implementaciones incluyen:
  - Cinética de Combustión (Modelo de Wiebe): La inyección de energía ya no es instantánea. Se utiliza la función de Wiebe para simular el frente de llama progresivo, modelando la fracción de masa quemada en forma de curva "S", lo que optimiza el cálculo del torque al coincidir con el ángulo de biela correcto.
  - Transferencia de Calor Transitoria (Correlación de Woschni): Se aplica el Primer Principio de la Termodinámica evaluando las pérdidas por convección hacia las paredes del cilindro y la culata en cada paso de tiempo, reduciendo drásticamente los picos irreales de presión y temperatura.
  - Dinámica de Fluidos (Barré de Saint-Venant): El flujo de admisión y escape no es libre. Se evalúa el caudal másico compresible a través de las válvulas, contemplando el límite sónico (estrangulamiento o choked flow) y generando el bucle negativo de bombeo en el diagrama P-V.
  - Pérdidas Mecánicas (Modelo de Chen-Flynn): Separación del torque indicado y el torque al freno. Calcula la Presión Media Efectiva de Fricción (PMEF) evaluando el arrastre de accesorios, la carga sobre los cojinetes y el rozamiento hidrodinámico de los anillos según la viscosidad del aceite seleccionado.
  - Predicción de Detonación (Integral de Livengood-Wu): Sistema de seguridad algorítmico que rastrea el retraso de autoignición mediante la ecuación de Arrhenius. Si las condiciones de presión y temperatura superan el octanaje antes de quemar la mezcla, el motor sufre pre-detonación (picado de biela) y se detiene.
  - Disociación Térmica y Calor Específico Variable: El $C_v$ del aire se adapta dinámicamente. A partir de los 2000 K, se simula el muro térmico por disociación molecular, impidiendo que el cilindro alcance temperaturas termodinámicamente imposibles.

# 📊 Interfaz y Telemetría (Frontend)
La interfaz gráfica (Simulador_motor_a_combustion.py) actúa como un banco de pruebas interactivo:
  - Renderizado de Cinemática en Vivo: Animación del conjunto pistón-biela-cigüeñal adaptando dinámicamente los fotogramas por segundo a las RPM calculadas.
  - Escudo de Seguridad (Fail-Safe): Si el usuario somete el motor a condiciones destructivas (ej. exceso de presión de turbo a bajas RPM) y la integral de Livengood-Wu detona el motor, la interfaz intercepta el fallo. Muestra una alerta crítica y estabiliza los gráficos con un "electrocardiograma plano" (cayendo a cero), evitando el colapso del sistema.
  - Análisis Multicilíndrico: El código calcula el ciclo termodinámico de un cilindro y lo superpone matemáticamente según el orden de encendido y la arquitectura del bloque (ej. V8, Bóxer 6, 4 en línea), entregando la potencia y el torque promedio suavizado al volante motor.
  - Comparativa de Combustibles (Gasolina vs. Hidrógeno): Modificación en tiempo real de la cinética química para comparar el rendimiento de ambos combustibles bajo las mismas condiciones geométricas y de sobrealimentación.

# 🚀 Requisitos e Instalación
Para ejecutar este simulador en local, es necesario contar con Python instalado y las siguientes librerías detalladas en el archivo requirements.txt:
  - 1. Instalar las dependencias a través de la terminal:
    Bash
      pip install -r requirements.txt
  - 2. Lanzar el servidor local de Streamlit:
    Bash
      streamlit run Simulador_motor_a_combustion.py
