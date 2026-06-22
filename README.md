# Simulador Módem Wi-Fi — Simulación de Eventos Discretos

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.58-red.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/plotly-6.8-blueviolet.svg)](https://plotly.com)

Aplicación interactiva para el **dimensionamiento de un Módem Wi-Fi** mediante simulación de eventos discretos. Modela una línea de espera con un servidor (el AP) y cola finita en bytes, utilizando datos de tráfico real capturados en horario pico (18:25–18:30).

## Requisitos

- Python 3.10 o superior
- `streamlit` ≥ 1.58
- `plotly` ≥ 6.8

## Instalación y Ejecución

```bash
# 1. Ubicarse en el directorio del proyecto
cd "/home/goya/Escritorio/Facultad/4TO AÑO/Simulación/app"

# 2. Crear un entorno virtual (recomendado para evitar conflictos)
python3 -m venv venv

# 3. Activar el entorno virtual
source venv/bin/activate              # Linux / macOS (bash/zsh)
source venv/bin/activate.fish         # Linux (fish shell)
# .\venv\Scripts\activate            # Windows (PowerShell)

# 4. Instalar dependencias
pip install streamlit plotly

# 5. Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá en el navegador en `http://localhost:8501`.

## Cómo Usar la Aplicación

### Barra Lateral (Controles)

| Control | Rango | Defecto | Descripción |
|---|---|---|---|
| **CB** — Capacidad del Buffer | 1000 – 50000 bytes | 10000 | Tamaño máximo del buffer del Módem |
| **AB** — Ancho de Banda | 10 – 500 bytes/μs | 100 | Tasa de servicio del AP |

### Área Principal (Resultados)

Al presionar **"Iniciar Simulación"** se muestran tres tarjetas y un gráfico:

1. **Porcentaje de Pérdida (%PP)** — Paquetes descartados por buffer lleno.  
   - Verde si ≤ 1.0% (cumple el objetivo de calidad).  
   - Rojo si > 1.0% (excede el objetivo).

2. **Utilización del Equipo (UAP)** — Porcentaje del tiempo que el AP estuvo transmitiendo.

3. **Pico de Ocupación del Buffer** — Máxima cantidad de bytes acumulados en el buffer durante la simulación. Sirve para ver si el buffer dimensionado estuvo cerca de desbordarse.

4. **Gráfico de Estabilización** — Evolución del %PP acumulado vs. paquetes procesados (CTP 0–1000). Interactivo (zoom, pan, hover).

## Motor de Simulación

### Metodología: Next-Event Time Advance

El reloj `T` salta asimétricamente hacia el evento más próximo (Llegada o Salida), sin usar incrementos de tiempo fijo Δt.

### Variables del Modelo

| Variable | Descripción |
|---|---|
| `CB` | Capacidad del buffer (bytes) — variable de control |
| `AB` | Ancho de banda (bytes/μs) — variable de control |
| `TEL` | Tiempo entre llegadas (Weibull, 3 parámetros) |
| `TAM` | Tamaño del paquete (distribución empírica bimodal, Monte Carlo) |
| `OB(t)` | Ocupación del buffer en el instante t |
| `CTP` | Cantidad total de paquetes procesados |
| `CPP` | Cantidad de paquetes perdidos |
| `%PP` | `(CPP / CTP) × 100` |
| `UAP` | `(Σ TSᵢ / T_total) × 100` |

### Generadores de Variables Aleatorias

**Tiempo Entre Llegadas** — Transformada Inversa Weibull (3 parámetros):

```
TEL_i = 2.0 + 553469.134 × (-ln(1 - r_i))^(1/0.842551)
```

Parámetros obtenidos del ajuste sobre datos reales:
- Forma (α): 0.842551
- Escala (β): 553469.134 μs
- Localización (γ): 2.0 μs

**Tamaño del Paquete** — Método de Monte Carlo sobre distribución empírica.

Los tamaños de paquete reales no siguen ninguna distribución teórica conocida (son **bimodales**: dos picos en ~66 bytes para ACKs/control y ~1460 bytes para datos). Se utiliza una tabla de frecuencias acumuladas construida a partir de la muestra real de 2000 paquetes. El algoritmo genera un número pseudoaleatorio r_i y asigna directamente el tamaño correspondiente de la tabla.

### Generador de Números Pseudoaleatorios (LCG)

Se utiliza un **Algoritmo Congruencial Lineal** con los siguientes parámetros:

| Parámetro | Valor |
|---|---|
| Semilla X₀ | 17 |
| Multiplicador a | 1.664.525 |
| Incremento c | 1.013.904.223 |
| Módulo m | 2³² = 4.294.967.296 |

Los 2000 números generados pasan las 6 pruebas estadísticas (Medias, Varianza, χ², K-S, Corridas arriba/abajo, Corridas sobre la media) con α = 0.05.

## Diseño Experimental

El objetivo es **determinar la capacidad de buffer y ancho de banda mínimos** que necesita un Módem para soportar el tráfico capturado manteniendo %PP ≤ 1%.

| Escenario | CB | AB | Resultado esperado |
|---|---|---|---|
| Módem mínimo | 1000–2000 | 10 | %PP > 1% — no cumple |
| Módem justo | 2000–5000 | 10–50 | %PP ≤ 1% — cumple |
| Módem seguro | ≥ 5000 | cualquier | %PP ≈ 0% — cumple sobradamente |

## Diseño Visual

Interfaz oscura inspirada en [Linear](https://linear.app):

| Token | Color | Uso |
|---|---|---|
| Canvas | `#010102` | Fondo de página |
| Surface | `#1a1b1e` | Tarjetas y sidebar |
| Hairline | `#23252a` | Bordes de 1px |
| Primary | `#5e6ad2` | Botón principal |
| Ink | `#f7f8f8` | Texto principal |
| Ink Subtle | `#8a8f98` | Texto secundario |
| Success | `#27a644` | %PP dentro del objetivo |
| Error | `#e5484d` | %PP fuera del objetivo |

## Estructura del Proyecto

```
app/
├── app.py          # Aplicación completa
├── README.md       # Documentación
├── STACK.md        # Especificación técnica original
├── spec/
│   ├── DESIGN.md   # Guía de diseño Linear
│   └── SKILL.md    # Skill de frontend
└── docs/
    ├── diagrama_flujo_simulacion.drawio
    ├── GOAT SIMULATOR 3-3.pdf   # Trabajo práctico completo
    └── Lineamientos Actividad N° 2 .pdf
```
