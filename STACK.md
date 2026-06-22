## 1. Arquitectura y Tecnologías Core
*   **Lenguaje de Programación:** Python 3.x
*   **Framework de Interfaz Gráfica (Frontend):** Streamlit. 
*   **Librería de Visualización de Datos:** Plotly (para gráficos interactivos) o Altair.
*   **Objetivo de la Interfaz:** Implementar una "Simulación Visual Interactiva" que permita la modificación dinámica de los parámetros de control y la visualización de resultados en tiempo real tras la ejecución.

## 2. Requisitos de la Interfaz de Usuario (Layout en Streamlit)
La aplicación de Streamlit debe estar estructurada de la siguiente manera:

### A. Barra Lateral (Sidebar) - Controles de Usuario
Debe contener los controles interactivos para las variables de decisión (variables de control):
*   **Slider / Number Input para `CB`:** Capacidad del Buffer (en bytes). Rango sugerido: 5000 a 50000 bytes.
*   **Slider / Number Input para `AB`:** Ancho de Banda o tasa de servicio (en bytes/$\mu$s). Rango sugerido: 10 a 500.
*   **Botón de Acción:** Un botón principal llamado "Iniciar Simulación" que dispare la ejecución del código backend (la lógica de Evento a Evento).

### B. Área Principal (Main Page) - Resultados
Al finalizar la corrida de los 1000 paquetes, el área principal debe mostrar:
1.  **Tarjetas de Métricas (KPI Cards):** Usando `st.metric()` para mostrar los resultados finales:
    *   **Porcentaje de Pérdida (%PP):** Mostrar el valor final. *Regla visual:* Si `%PP <= 1.0%`, mostrarlo en verde o como éxito (cumple el objetivo del estudio). Si es mayor, en rojo.
    *   **Utilización del Equipo (UAP):** Mostrar el porcentaje del tiempo que el Módem estuvo transmitiendo.
2.  **Gráfica de Estabilización (Obligatorio):**
    *   Usar Plotly (`st.plotly_chart()`) para graficar la evolución del Porcentaje de Pérdida (`%PP`) a lo largo de la simulación.
    *   **Eje X:** Cantidad Total de Paquetes (`CTP`), de 0 a 1000.
    *   **Eje Y:** Porcentaje de pérdida acumulado en ese instante.
    *   *Propósito:* Demostrar visualmente que el sistema alcanzó el estado estable antes de finalizar la corrida.

## 3. Integración Backend-Frontend
*   El motor del simulador (la lógica del bucle `while` de Evento a Evento) debe estar encapsulado en una función, por ejemplo `correr_simulacion(cb, ab)`.
*   Esta función debe devolver no solo los KPI finales (`%PP` y `UAP`), sino también dos listas/arrays (`historial_ctp` e `historial_pp`) que se usarán para alimentar la gráfica de Plotly.
*   Asegurar que la simulación se ejecute de manera local y rápida sin bloquear el hilo principal de Streamlit.
