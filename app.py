import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="Simulador Módem Wi-Fi",
    page_icon="📡",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background-color: #010102;
    }
    .stSidebar {
        background-color: #1a1b1e;
    }
    .stSidebar .stMarkdown, .stSidebar .stNumberInput label, .stSidebar .stSlider label {
        color: #d0d6e0 !important;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
    .stButton > button {
        background-color: #5e6ad2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        font-family: system-ui, -apple-system, sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: background-color 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #828fff !important;
    }
    .stButton > button:active {
        background-color: #5e69d1 !important;
    }
    .metric-card {
        background-color: #1a1b1e;
        border: 1px solid #23252a;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .metric-label {
        color: #8a8f98;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 14px;
        font-weight: 400;
        letter-spacing: -0.05px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 28px;
        font-weight: 600;
        letter-spacing: -0.6px;
        line-height: 1.2;
    }
    .metric-green { color: #27a644; }
    .metric-red { color: #e5484d; }
    .metric-blue { color: #f7f8f8; }
    .title-text {
        color: #f7f8f8;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 40px;
        font-weight: 600;
        letter-spacing: -1.0px;
        line-height: 1.15;
        margin-bottom: 8px;
    }
    .subtitle-text {
        color: #8a8f98;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 16px;
        font-weight: 400;
        letter-spacing: -0.05px;
        margin-bottom: 32px;
    }
    .divider {
        border: none;
        border-top: 1px solid #23252a;
        margin: 24px 0;
    }
    .kpi-row {
        display: flex;
        gap: 24px;
    }
    .placeholder-text {
        color: #8a8f98;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 16px;
        text-align: center;
        padding: 80px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">Simulador Módem Wi-Fi</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Simulación de Eventos Discretos — Línea de Espera con un Servidor</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


class LCG:
    def __init__(self, semilla: int = 17):
        self.x = semilla
        self.a = 1664525
        self.c = 1013904223
        self.m = 2 ** 32

    def next(self) -> float:
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m


TABLA_MONTECARLO = [
    (40, 0.0000), (54, 0.0324), (55, 0.0370), (56, 0.0417),
    (57, 0.0463), (58, 0.0509), (59, 0.0556), (60, 0.0648),
    (61, 0.0741), (62, 0.0833), (63, 0.0972), (64, 0.1111),
    (65, 0.1250), (66, 0.1528), (67, 0.1713), (68, 0.1852),
    (69, 0.1944), (70, 0.2037), (71, 0.2130), (72, 0.2222),
    (73, 0.2315), (74, 0.2407), (75, 0.2500), (76, 0.2593),
    (77, 0.2685), (78, 0.2778), (79, 0.2824), (80, 0.2870),
    (84, 0.2963), (88, 0.3009), (92, 0.3056), (96, 0.3102),
    (100, 0.3148), (110, 0.3241), (120, 0.3333), (130, 0.3426),
    (140, 0.3519), (150, 0.3611), (160, 0.3704), (180, 0.3796),
    (200, 0.3889), (220, 0.3981), (240, 0.4074), (260, 0.4167),
    (280, 0.4259), (300, 0.4352), (350, 0.4444), (400, 0.4537),
    (450, 0.4630), (500, 0.4722), (550, 0.4815), (600, 0.4907),
    (650, 0.5000), (700, 0.5093), (750, 0.5185), (800, 0.5278),
    (850, 0.5370), (900, 0.5463), (950, 0.5556), (1000, 0.5648),
    (1050, 0.5741), (1100, 0.5833), (1150, 0.5926), (1200, 0.6019),
    (1220, 0.6111), (1240, 0.6250), (1260, 0.6389), (1280, 0.6528),
    (1300, 0.6667), (1320, 0.6852), (1340, 0.7037), (1360, 0.7222),
    (1380, 0.7407), (1400, 0.7593), (1410, 0.7778), (1420, 0.7963),
    (1430, 0.8148), (1440, 0.8333), (1450, 0.8519), (1460, 0.8796),
    (1470, 0.8981), (1472, 0.9167), (1474, 0.9352), (1476, 0.9537),
    (1478, 0.9722), (1480, 0.9815), (1490, 0.9907), (1500, 0.9954),
    (1514, 1.0000),
]


def generar_tam_montecarlo(r: float) -> int:
    for tam, prob in TABLA_MONTECARLO:
        if r <= prob:
            return tam
    return 1514


def generar_tel_weibull(r: float) -> float:
    return 2.0 + 137108.2 * (-math.log(1.0 - r)) ** (1.0 / 0.842551)


def correr_simulacion(cb: int, ab: float, semilla: int = 17, max_paquetes: int = 2000, usar_tiempo_final: bool = True, tiempo_final_min: int = 5):
    lcg = LCG(semilla=semilla)
    TIEMPO_FINAL = tiempo_final_min * 60 * 1_000_000 if usar_tiempo_final else float("inf")

    T = 0.0
    TPLL = 0.0
    TPS = float("inf")
    OB = 0
    estado_AP = "Ocioso"
    CPP = 0
    CTP = 0
    buffer_FIFO: list[tuple[int, float]] = []
    tiempo_total_servicio = 0.0
    tam_actual = 0
    max_ob = 0

    tiempos_espera: list[float] = []
    historial_ctp: list[int] = []
    historial_pp: list[float] = []
    historial_t: list[float] = []
    historial_ob: list[int] = []

    while CTP < max_paquetes and T < TIEMPO_FINAL:
        if TPLL <= TPS:
            T = TPLL
            CTP += 1

            r_tel = lcg.next()
            r_tam = lcg.next()
            tel = generar_tel_weibull(r_tel)
            tam = generar_tam_montecarlo(r_tam)
            TPLL = T + tel

            if (OB + tam) <= cb:
                OB += tam
                if OB > max_ob:
                    max_ob = OB
                buffer_FIFO.append((tam, T))
                if estado_AP == "Ocioso":
                    estado_AP = "Transmitiendo"
                    tam_actual, llegada = buffer_FIFO.pop(0)
                    TS = tam_actual / ab
                    tiempo_total_servicio += TS
                    tiempos_espera.append(T - llegada)
                    TPS = T + TS
            else:
                CPP += 1
        else:
            T = TPS
            OB -= tam_actual

            if OB > 0:
                tam_actual, llegada = buffer_FIFO.pop(0)
                TS = tam_actual / ab
                tiempo_total_servicio += TS
                tiempos_espera.append(T - llegada)
                TPS = T + TS
            else:
                estado_AP = "Ocioso"
                TPS = float("inf")

        historial_t.append(T)
        historial_ob.append(OB)

        if CTP > 0:
            pp_temp = (CPP / CTP) * 100.0
            historial_ctp.append(CTP)
            historial_pp.append(pp_temp)

    pp_final = (CPP / CTP) * 100.0 if CTP > 0 else 0.0
    uap_final = (tiempo_total_servicio / T) * 100.0 if T > 0 else 0.0
    promedio_espera = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0.0
    max_espera = max(tiempos_espera) if tiempos_espera else 0.0

    return pp_final, uap_final, max_ob, historial_ctp, historial_pp, CTP, CPP, promedio_espera, max_espera, historial_t, historial_ob


with st.sidebar:
    st.markdown(
        "<div style='color:#f7f8f8; font-size:22px; font-weight:500; letter-spacing:-0.4px; margin-bottom:24px;'>Controles</div>",
        unsafe_allow_html=True,
    )

    CB = st.number_input(
        "CB — Capacidad del Buffer (bytes)",
        min_value=100,
        max_value=100000,
        value=2000,
        step=100,
        format="%d",
    )

    AB = st.number_input(
        "AB — Ancho de Banda (bytes/μs)",
        min_value=1,
        max_value=100000,
        value=10,
        step=1,
        format="%d",
    )

    SEMILLA = st.number_input(
        "Semilla LCG (X₀)",
        min_value=1,
        max_value=100000,
        value=17,
        step=1,
        format="%d",
    )

    st.markdown("---")

    MAX_PAQUETES = st.number_input(
        "Máximo de paquetes (CTP)",
        min_value=100,
        max_value=50000,
        value=2000,
        step=100,
        format="%d",
    )

    USAR_TIEMPO_FINAL = st.checkbox("Limitar por tiempo", value=True)

    TIEMPO_FINAL_MIN = 5
    if USAR_TIEMPO_FINAL:
        TIEMPO_FINAL_MIN = st.slider(
            "Tiempo máximo (min)",
            min_value=1,
            max_value=60,
            value=5,
            step=1,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    iniciar = st.button("Iniciar Simulación", type="primary")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#8a8f98; font-size:12px; border-top:1px solid #23252a; padding-top:16px;'>Motor: Evento-a-Evento · Weibull TEL · Monte Carlo TAM</div>",
        unsafe_allow_html=True,
    )

if "sim_run" not in st.session_state:
    st.session_state.sim_run = False
    st.session_state.pp_final = 0.0
    st.session_state.uap_final = 0.0
    st.session_state.max_ob = 0
    st.session_state.ctp = 0
    st.session_state.cpp = 0
    st.session_state.promedio_espera = 0.0
    st.session_state.max_espera = 0.0
    st.session_state.max_paquetes = 2000
    st.session_state.historial_ctp = []
    st.session_state.historial_pp = []
    st.session_state.historial_t = []
    st.session_state.historial_ob = []

if iniciar:
    with st.spinner("Ejecutando simulación..."):
        pp_final, uap_final, max_ob, hist_ctp, hist_pp, ctp, cpp, promedio_espera, max_espera, hist_t, hist_ob = correr_simulacion(CB, AB, SEMILLA, MAX_PAQUETES, USAR_TIEMPO_FINAL, TIEMPO_FINAL_MIN)
    st.session_state.sim_run = True
    st.session_state.pp_final = pp_final
    st.session_state.uap_final = uap_final
    st.session_state.max_ob = max_ob
    st.session_state.ctp = ctp
    st.session_state.cpp = cpp
    st.session_state.promedio_espera = promedio_espera
    st.session_state.max_espera = max_espera
    st.session_state.max_paquetes = MAX_PAQUETES
    st.session_state.historial_ctp = hist_ctp
    st.session_state.historial_pp = hist_pp
    st.session_state.historial_t = hist_t
    st.session_state.historial_ob = hist_ob

if st.session_state.sim_run:
    pp = st.session_state.pp_final
    uap = st.session_state.uap_final
    pto = 100.0 - uap
    max_ob = st.session_state.max_ob
    ctp = st.session_state.ctp
    cpp = st.session_state.cpp
    promedio_espera = st.session_state.promedio_espera
    max_espera = st.session_state.max_espera

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">CTP — Cantidad Total de Paquetes</div>
                <div class="metric-value metric-blue">{ctp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">CPP — Paquetes Perdidos</div>
                <div class="metric-value metric-blue">{cpp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        pp_color = "metric-green" if pp <= 1.0 else "metric-red"
        pp_label = "Cumple (≤1.0%)" if pp <= 1.0 else "Excede (>1.0%)"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">%PP — Porcentaje de Pérdida</div>
                <div class="metric-value {pp_color}">{pp:.2f}%</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">{pp_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">UAP — Utilización del AP</div>
                <div class="metric-value metric-blue">{uap:.2f}%</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Tiempo transmitiendo / Tiempo total</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">PTO — Porcentaje Tiempo Ocioso</div>
                <div class="metric-value metric-blue">{pto:.2f}%</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Tiempo ocioso / Tiempo total</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col6:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">T. Espera Prom. en Buffer</div>
                <div class="metric-value metric-blue">{promedio_espera / 1000:.2f} ms</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Promedio de espera antes de transmitir</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col7, col8 = st.columns(2)

    with col7:
        utilizacion_pct = (100 * max_ob) / CB if CB > 0 else 0
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Pico de Ocupación del Buffer</div>
                <div class="metric-value metric-blue">{max_ob} / {CB} bytes</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Máximo uso del buffer ({utilizacion_pct:.1f}% de CB)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col8:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Tiempo Máximo de Espera Registrado</div>
                <div class="metric-value metric-blue">{max_espera / 1000:.2f} ms</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Peor caso de espera en el buffer</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#d0d6e0; font-size:20px; font-weight:500; letter-spacing:-0.3px; margin-bottom:8px;'>Estabilización del %PP</div>",
        unsafe_allow_html=True,
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=st.session_state.historial_ctp,
            y=st.session_state.historial_pp,
            mode="lines",
            line=dict(color="#5e6ad2", width=2),
            hovertemplate="CTP: %{x}<br>%PP: %{y:.2f}%",
            name="%PP",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#010102",
        plot_bgcolor="#010102",
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis=dict(
            title=dict(text="CTP — Cantidad Total de Paquetes", font=dict(color="#8a8f98", size=13)),
            tickfont=dict(color="#8a8f98", size=12),
            gridcolor="#1a1b1e",
            range=[0, st.session_state.max_paquetes],
            dtick=100,
        ),
        yaxis=dict(
            title=dict(text="%PP — Porcentaje de Pérdida", font=dict(color="#8a8f98", size=13)),
            tickfont=dict(color="#8a8f98", size=12),
            gridcolor="#1a1b1e",
            zeroline=False,
        ),
        hovermode="x unified",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#d0d6e0; font-size:20px; font-weight:500; letter-spacing:-0.3px; margin-bottom:8px;'>Evolución de la Ocupación del Buffer (OB)</div>",
        unsafe_allow_html=True,
    )

    t_segundos = [t / 1_000_000 for t in st.session_state.historial_t]

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=t_segundos,
            y=st.session_state.historial_ob,
            mode="lines",
            line=dict(color="#5e6ad2", width=2),
            hovertemplate="Tiempo: %{x:.2f}s<br>OB: %{y} bytes",
            name="OB",
        )
    )
    fig2.add_hline(
        y=CB,
        line_dash="dash",
        line_color="#e5484d",
        line_width=1.5,
        annotation_text=f"CB = {CB} bytes",
        annotation_position="top right",
        annotation_font=dict(color="#e5484d", size=12),
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#010102",
        plot_bgcolor="#010102",
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis=dict(
            title=dict(text="Tiempo (s)", font=dict(color="#8a8f98", size=13)),
            tickfont=dict(color="#8a8f98", size=12),
            gridcolor="#1a1b1e",
        ),
        yaxis=dict(
            title=dict(text="Ocupación del Buffer (bytes)", font=dict(color="#8a8f98", size=13)),
            tickfont=dict(color="#8a8f98", size=12),
            gridcolor="#1a1b1e",
            zeroline=False,
            range=[0, max(CB, max_ob) * 1.1],
        ),
        hovermode="x unified",
        showlegend=False,
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.markdown(
        "<div class='placeholder-text'>Ajusta los parámetros en la barra lateral y presiona <strong>Iniciar Simulación</strong>.</div>",
        unsafe_allow_html=True,
    )
