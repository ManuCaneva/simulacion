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
# 1. Clonar el repositorio
git clone <url-del-repo>
cd <repo-directory>

# 2. Crear un entorno virtual (recomendado)
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
|---|---|---|---|---|
| **CB** — Capacidad del Buffer | 100 – 100.000 bytes | 2000 | Tamaño máximo del buffer del Módem |
| **AB** — Ancho de Banda | 1 – 100.000 bytes/μs | 10 | Tasa de servicio del AP |
| **Semilla LCG** (X₀) | 1 – 100.000 | 17 | Semilla del generador de números pseudoaleatorios |
| **Máx. paquetes (CTP)** | 100 – 50.000 | 2000 | Cantidad máxima de paquetes a generar |
| **Limitar por tiempo** | checkbox | activado | Habilita límite de tiempo de simulación (por defecto 5 min) |
| **Tiempo máximo** | 1 – 60 min | 5 | Ventana de simulación (solo si el checkbox está activo) |

### Área Principal (Resultados)

Al presionar **"Iniciar Simulación"** se muestran ocho tarjetas de indicadores y dos gráficos interactivos:

**Fila 1 — Indicadores principales (3 columnas):**

1. **CTP — Cantidad Total de Paquetes** — Paquetes que llegaron al sistema.
2. **CPP — Paquetes Perdidos** — Paquetes descartados por buffer lleno.
3. **%PP — Porcentaje de Pérdida** — `(CPP / CTP) × 100`.
   - Verde si ≤ 1.0% (cumple el objetivo de calidad).
   - Rojo si > 1.0% (excede el objetivo).

**Fila 2 — Indicadores secundarios (3 columnas):**

4. **UAP — Utilización del AP** — Porcentaje del tiempo que el AP estuvo transmitiendo.
5. **PTO — Porcentaje Tiempo Ocioso** — `100% - UAP`.
6. **T. Espera Prom. en Buffer** — Tiempo promedio que cada paquete esperó antes de ser transmitido.

**Fila 3 — Indicadores adicionales (2 columnas):**

7. **Pico de Ocupación del Buffer** — Máxima cantidad de bytes acumulados en el buffer durante la simulación.
8. **Tiempo Máximo de Espera Registrado** — Peor caso de espera en el buffer.

**Gráficos:**

- **Estabilización del %PP** — Evolución del %PP acumulado vs. CTP. Permite observar a partir de cuántos paquetes el porcentaje se estabiliza.
- **Evolución de la Ocupación del Buffer (OB)** — OB vs. tiempo (segundos), con línea punteja roja indicando CB.

## Motor de Simulación

### Metodología: Next-Event Time Advance

El reloj `T` salta asimétricamente hacia el evento más próximo (Llegada o Salida), sin usar incrementos de tiempo fijo Δt.

### Variables del Modelo

| Variable | Descripción |
|---|---|
| `CB` | Capacidad del buffer (bytes) — variable de control |
| `AB` | Ancho de banda (bytes/μs) — variable de control |
| `X₀` | Semilla del LCG — variable de control |
| `TEL` | Tiempo entre llegadas (Weibull, 3 parámetros) |
| `TAM` | Tamaño del paquete (distribución empírica bimodal, Monte Carlo) |
| `OB(t)` | Ocupación del buffer en el instante t |
| `CTP` | Cantidad total de paquetes procesados |
| `CPP` | Cantidad de paquetes perdidos |
| `%PP` | `(CPP / CTP) × 100` |
| `UAP` | `(Σ TSᵢ / T_total) × 100` |
| `PTO` | `100% - UAP` — tiempo ocioso del AP |
| `T. Espera Prom.` | Promedio de `(T_transmisión - T_llegada)` para cada paquete transmitido |

### Generadores de Variables Aleatorias

**Tiempo Entre Llegadas** — Transformada Inversa Weibull (3 parámetros):

```
TEL_i = 2.0 + 137108.2 × (-ln(1 - r_i))^(1/0.842551)
```

Parámetros obtenidos del ajuste sobre datos reales (2000 paquetes en 5 min → TEL medio ≈ 150 ms):
- Forma (α): 0.842551
- Escala (β): 137108.2 μs
- Localización (γ): 2.0 μs

**Tamaño del Paquete** — Método de Monte Carlo sobre distribución empírica.

Los tamaños de paquete reales no siguen ninguna distribución teórica conocida (son **bimodales**: dos picos en ~66 bytes para ACKs/control y ~1460 bytes para datos). Se utiliza una tabla de frecuencias acumuladas construida a partir de la muestra real de 2000 paquetes. El algoritmo genera un número pseudoaleatorio r_i y asigna directamente el tamaño correspondiente de la tabla.

### Generador de Números Pseudoaleatorios (LCG)

Se utiliza un **Algoritmo Congruencial Lineal** con los siguientes parámetros:

| Parámetro | Valor |
|---|---|
| Semilla X₀ | 17 (configurable desde el sidebar) |
| Multiplicador a | 1.664.525 |
| Incremento c | 1.013.904.223 |
| Módulo m | 2³² = 4.294.967.296 |

Los 2000 números generados pasan las 6 pruebas estadísticas (Medias, Varianza, χ², K-S, Corridas arriba/abajo, Corridas sobre la media) con α = 0.05.

## Diseño Experimental

El objetivo es **determinar la capacidad de buffer y ancho de banda mínimos** que necesita un Módem para soportar el tráfico capturado manteniendo %PP ≤ 1%.

Con los controles del sidebar se pueden explorar estos escenarios:

| Escenario | CB | AB | %PP | ¿Cumple? |
|---|---|---|---|---|
| Módem mínimo (paquetes grandes > CB) | 1000 | 10 | ~44% | ❌ |
| Módem justo (límite) | 2000 | 10 | ~0.25% | ✅ |
| Módem sobrado | 5000 | 10 | ~0% | ✅ |

> **Nota:** Los datos capturados en hora pico (18:25–18:30) ya incluyen todo el tráfico de la facultad. Con ~6.7 paquetes/s promedio, el AP está ocioso >99% del tiempo. La pérdida de paquetes se debe exclusivamente a que el tamaño del paquete supera la capacidad del buffer (CB), no a congestión por exceso de tráfico.

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
