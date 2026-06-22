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
    return 2.0 + 553469.134 * (-math.log(1.0 - r)) ** (1.0 / 0.842551)


def correr_simulacion(cb: int, ab: float):
    lcg = LCG(semilla=17)

    T = 0.0
    TPLL = 0.0
    TPS = float("inf")
    OB = 0
    estado_AP = "Ocioso"
    CPP = 0
    CTP = 0
    buffer_FIFO: list[int] = []
    tiempo_total_servicio = 0.0
    tam_actual = 0
    max_ob = 0

    historial_ctp: list[int] = []
    historial_pp: list[float] = []

    while CTP < 1000:
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
                buffer_FIFO.append(tam)
                if estado_AP == "Ocioso":
                    estado_AP = "Transmitiendo"
                    tam_actual = buffer_FIFO.pop(0)
                    TS = tam_actual / ab
                    tiempo_total_servicio += TS
                    TPS = T + TS
            else:
                CPP += 1
        else:
            T = TPS
            OB -= tam_actual

            if len(buffer_FIFO) > 0:
                tam_actual = buffer_FIFO.pop(0)
                TS = tam_actual / ab
                tiempo_total_servicio += TS
                TPS = T + TS
            else:
                estado_AP = "Ocioso"
                TPS = float("inf")

        if CTP > 0:
            pp_temp = (CPP / CTP) * 100.0
            historial_ctp.append(CTP)
            historial_pp.append(pp_temp)

    pp_final = (CPP / CTP) * 100.0 if CTP > 0 else 0.0
    uap_final = (tiempo_total_servicio / T) * 100.0 if T > 0 else 0.0

    return pp_final, uap_final, max_ob, historial_ctp, historial_pp


with st.sidebar:
    st.markdown(
        "<div style='color:#f7f8f8; font-size:22px; font-weight:500; letter-spacing:-0.4px; margin-bottom:24px;'>Controles</div>",
        unsafe_allow_html=True,
    )

    CB = st.number_input(
        "CB — Capacidad del Buffer (bytes)",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        format="%d",
    )

    AB = st.number_input(
        "AB — Ancho de Banda (bytes/μs)",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
        format="%d",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    iniciar = st.button("Iniciar Simulación", type="primary")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#8a8f98; font-size:12px; border-top:1px solid #23252a; padding-top:16px;'>Motor: Evento-a-Evento · Weibull TEL · Monte Carlo TAM · 1000 paquetes</div>",
        unsafe_allow_html=True,
    )

if "sim_run" not in st.session_state:
    st.session_state.sim_run = False
    st.session_state.pp_final = 0.0
    st.session_state.uap_final = 0.0
    st.session_state.max_ob = 0
    st.session_state.historial_ctp = []
    st.session_state.historial_pp = []

if iniciar:
    with st.spinner("Ejecutando simulación..."):
        pp_final, uap_final, max_ob, hist_ctp, hist_pp = correr_simulacion(CB, AB)
    st.session_state.sim_run = True
    st.session_state.pp_final = pp_final
    st.session_state.uap_final = uap_final
    st.session_state.max_ob = max_ob
    st.session_state.historial_ctp = hist_ctp
    st.session_state.historial_pp = hist_pp

if st.session_state.sim_run:
    pp = st.session_state.pp_final
    uap = st.session_state.uap_final
    max_ob = st.session_state.max_ob

    col1, col2 = st.columns(2)

    with col1:
        pp_color = "metric-green" if pp <= 1.0 else "metric-red"
        pp_label = "Cumple objetivo (≤1.0%)" if pp <= 1.0 else "Excede objetivo (>1.0%)"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Porcentaje de Pérdida (%PP)</div>
                <div class="metric-value {pp_color}">{pp:.2f}%</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">{pp_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Utilización del Equipo (UAP)</div>
                <div class="metric-value metric-blue">{uap:.2f}%</div>
                <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Tiempo transmitiendo / Tiempo total</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    utilizacion_pct = (100 * max_ob) / CB if CB > 0 else 0
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Pico de Ocupación del Buffer</div>
            <div class="metric-value metric-blue">{max_ob} / {CB} bytes</div>
            <div style="color:#8a8f98; font-size:13px; margin-top:8px;">Máximo uso del buffer durante la simulación ({utilizacion_pct:.1f}%)</div>
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
            range=[0, 1000],
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

else:
    st.markdown(
        "<div class='placeholder-text'>Ajusta los parámetros en la barra lateral y presiona <strong>Iniciar Simulación</strong>.</div>",
        unsafe_allow_html=True,
    )
