import base64
import json
import os
import time
from io import BytesIO
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

# ---------- Configuración de la página ----------
st.set_page_config(
    page_title="Corporación Indusegur Perú S.A.C.",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLOR_FONDO = "#0E1117"
AMARILLO = "#FFC800"
def bloque_html(html, alto):
    """Muestra HTML con JavaScript dentro de un marco (st.iframe en Streamlit nuevo)."""
    html = html.strip()
    if hasattr(st, "iframe"):
        st.iframe(html, height=alto)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=alto)

@st.cache_data
def a_base64(ruta, blur=0, oscuro=0.0, version=0):
    img = Image.open(ruta).convert("RGB")
    img.thumbnail((1920, 1080))
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    if oscuro:
        img = ImageEnhance.Brightness(img).enhance(1 - oscuro)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=78)
    return base64.b64encode(buf.getvalue()).decode()


# ---------- Quitar la barra superior y el botón "Deploy/Desplegar" ----------
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap');

  [data-testid="stMainBlockContainer"] h1 {
      font-family: 'Instrument Serif', 'Cormorant Garamond', Georgia, serif !important;
      font-weight: 400 !important;
      font-size: clamp(2.6rem, 3.4vw, 4.2rem) !important;
      line-height: 1.05 !important;
      letter-spacing: 0 !important;
  }
  [data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stToolbarActions"],
  [data-testid="stAppDeployButton"],
  [data-testid="stMainMenu"],
  [data-testid="stDecoration"],
  [data-testid="stStatusWidget"],
  #MainMenu, footer { display: none !important; }

  html, body { overflow-x: hidden; }
  .block-container { padding-top: 1.2rem; }
</style>
""", unsafe_allow_html=True)


# ---------- Portada ----------
def archivo_base64(ruta):
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()


if "entrado" not in st.session_state:
    st.session_state.entrado = False

if not st.session_state.entrado:
    logo_b64 = archivo_base64("logo_completo.png")
    # Imagen de fondo difuminada y un poco oscurecida
    # blur = cuánto se difumina (0 = nada). oscuro = 0 a 1 (más alto = más oscura)
    fondo_b64 = a_base64("static/fondo.jpg", blur=1.5, oscuro=0.35)

    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600&display=swap');

          /* Todo en una sola vista: sin scroll y sin barra superior */
          html, body,
          [data-testid="stApp"],
          [data-testid="stAppViewContainer"],
          [data-testid="stMain"] { overflow: hidden !important; background: transparent !important; }
          [data-testid="stHeader"] { display: none !important; }

          [data-testid="stMainBlockContainer"] {
              padding: 0 !important; max-width: none !important;
          }

          /* Fondo a pantalla completa */
          .fondo-portada {
              position: fixed; inset: 0; z-index: -2;
              background-size: cover; background-position: center;
              background-repeat: no-repeat;
          }
          .velo {
              position: fixed; inset: 0; z-index: -1; pointer-events: none;
              background: radial-gradient(ellipse at center,
                          rgba(0,0,0,.30) 0%, rgba(0,0,0,.65) 100%);
          }

          /* Grupo central: logo + título + botón, centrados en la pantalla */
          .st-key-portada {
              position: fixed; inset: 0;
              display: flex !important; flex-direction: column;
              align-items: center; justify-content: center;
              gap: 1rem !important; z-index: 1;
          }
          /* Cada elemento (logo+título, botón) se ajusta a su contenido y se centra */
          .st-key-portada > [data-testid="stElementContainer"] {
              width: auto !important;
              display: flex !important; justify-content: center;
          }
          .st-key-portada [data-testid="stMarkdownContainer"] {
              display: flex; flex-direction: column; align-items: center;
              width: auto !important;
          }
          .st-key-portada [data-testid="stMarkdownContainer"] > div { margin: 0 auto; }

          /* Logo en tarjeta blanca, recortado para que no sobre espacio blanco */
          .logo-izq img {
              width: clamp(170px, 14vw, 300px);
              aspect-ratio: 2.6 / 1; object-fit: cover;
              background: #fff; padding: 12px 16px; box-sizing: border-box;
              border-radius: 14px;
              box-shadow: 0 10px 40px rgba(0,0,0,.55);
          }

          /* Título resaltado */
          .titulo-portada {
              font-family: 'Instrument Serif', 'Cormorant Garamond', Georgia, serif;
              font-size: clamp(32px, 3.6vw, 80px);
              font-weight: 400; line-height: 1.05; color: #fff;
              margin: 0; text-align: center;
              white-space: nowrap; width: max-content; padding-bottom: .12em;
              text-shadow: 0 2px 6px rgba(0,0,0,.9), 0 4px 40px rgba(0,0,0,.8);
          }

          /* Botón centrado, con fondo oscuro para resaltar sobre la imagen */
          .st-key-btn_entrar { width: min(340px, 80vw) !important; }
          .st-key-btn_entrar .stButton { width: 100% !important; }
          .st-key-btn_entrar button {
              width: 100% !important;
              background: rgba(0,0,0,.45) !important;
              backdrop-filter: blur(8px);
              border: 2px solid #FFC800 !important;
              border-radius: 999px;
              padding: 0.7rem 2.4rem;
              font-weight: 600; letter-spacing: .15em;
              box-shadow:
                  0 0 8px rgba(255,200,0,.9),
                  0 0 22px rgba(255,200,0,.55),
                  inset 0 0 12px rgba(255,200,0,.35);
              transition: box-shadow .25s ease, transform .25s ease;
          }
          .st-key-btn_entrar button p { color: #ffffff !important; }
          .st-key-btn_entrar button:hover,
          .st-key-btn_entrar button:focus,
          .st-key-btn_entrar button:active {
              background: rgba(0,0,0,.6) !important;
              border-color: #FFC800 !important;
              box-shadow:
                  0 0 12px rgba(255,200,0,1),
                  0 0 34px rgba(255,200,0,.8),
                  inset 0 0 16px rgba(255,200,0,.5);
              transform: translateY(-2px);
          }

          /* Animaciones */
          @keyframes aparecer {
              from { opacity: 0; transform: translateY(24px); }
              to   { opacity: 1; transform: none; }
          }
          @keyframes escribir {
              from { -webkit-mask-size: 0% 100%;   mask-size: 0% 100%; }
              to   { -webkit-mask-size: 120% 100%; mask-size: 120% 100%; }
          }
          .logo-izq { animation: aparecer 1.2s ease-out .3s both; }
          .titulo-portada {
              -webkit-mask-image: linear-gradient(90deg, #000 85%, transparent 100%);
              mask-image: linear-gradient(90deg, #000 85%, transparent 100%);
              -webkit-mask-repeat: no-repeat;   mask-repeat: no-repeat;
              -webkit-mask-position: left center; mask-position: left center;
              -webkit-mask-size: 120% 100%;     mask-size: 120% 100%;
              animation: escribir 2s steps(20, end) .8s both;
          }
          .st-key-btn_entrar { animation: aparecer 1.2s ease-out 3s both; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="fondo-portada" style="background-image:url(data:image/jpeg;base64,{fondo_b64})"></div>
        <div class="velo"></div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="portada"):
        st.markdown(
            f"""
            <div class="logo-izq"><img src="data:image/png;base64,{logo_b64}"></div>
            <div class="titulo-portada">Aplicación Dashboard</div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Entrar", key="btn_entrar"):
            st.markdown(
                """
                <style>
                @keyframes salirPortada { to { opacity: 0; } }
                .st-key-portada { animation: salirPortada 0.8s ease-in forwards; }
                </style>
                """,
                unsafe_allow_html=True,
            )
            time.sleep(0.8)
            st.session_state.entrado = True
            st.session_state.recien_entrado = True
            st.rerun()

    st.stop()


# ---------- Aparición difuminada (cada vez que cambias de sección) ----------
def transicion_suave(clave):
    recien = st.session_state.pop("recien_entrado", False)
    cambio = st.session_state.get("ultima_seccion") != clave
    st.session_state.ultima_seccion = clave

    if not (recien or cambio):
        return  # al mover filtros no se repite la animación

    # Nombre distinto en cada transición: así el navegador reinicia la animación
    st.session_state.n_anim = st.session_state.get("n_anim", 0) + 1
    n = st.session_state.n_anim

    lateral = ""
    if recien:  # el lateral solo entra al venir de la portada
        lateral = f"""
        @keyframes lateral{n} {{
            from {{ opacity: 0; transform: translate3d(-24px, 0, 0); filter: blur(20px); }}
            to   {{ opacity: 1; transform: translate3d(0, 0, 0); filter: blur(0); }}
        }}
        [data-testid="stSidebarContent"] {{
            animation: lateral{n} 1.2s ease-out both;
        }}
        """

    st.markdown(
        f"""
        <style>
        @keyframes pagina{n} {{
            from {{ opacity: 0; transform: translate3d(0, 40px, 0); filter: blur(12px); }}
            to   {{ opacity: 1; transform: translate3d(0, 0, 0); filter: blur(0); }}
        }}
        [data-testid="stMainBlockContainer"] {{
            animation: pagina{n} 1.4s ease-out both;
        }}
        {lateral}
        </style>
        """,
        unsafe_allow_html=True,
    )
# ---------- Fin portada ----------

# =====================================================================
#  NUEVO DASHBOARD: BAJA ROTACIÓN DE INVENTARIOS (4 OBJETIVOS)
#  Todo se lee del Excel. Si cambias un número en el Excel y guardas,
#  la web se actualiza sola al recargar la página.
# =====================================================================
import openpyxl
import plotly.graph_objects as go

ARCHIVO_EXCEL = "Elaborado para Dashboard.xlsx"

# ---------- Colores ----------
PALETA = ["#FFC800", "#FF8A00", "#E5484D", "#3B82F6", "#22C55E",
          "#A855F7", "#14B8A6", "#94A3B8", "#F472B6"]
px.defaults.color_discrete_sequence = PALETA
COLOR_ESC = {"As-Is": "#E5484D", "Estándar": "#94A3B8", "To-Be": AMARILLO}
ORDEN_MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
               "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]


# ---------- Lectura del Excel ----------
@st.cache_data
def cargar_libro(version):
    """Lee todas las hojas y guarda cada celda con valor: {'OBJ2': {'K2': ...}}."""
    wb = openpyxl.load_workbook(ARCHIVO_EXCEL, data_only=True)
    libro = {}
    for ws in wb.worksheets:
        libro[ws.title.strip()] = {
            c.coordinate: c.value for fila in ws.iter_rows() for c in fila if c.value is not None
        }
    return libro


LIBRO = cargar_libro(os.path.getmtime(ARCHIVO_EXCEL))


def celda(hoja, ref, defecto=None):
    return LIBRO.get(hoja, {}).get(ref, defecto)


def numero(hoja, ref):
    try:
        return float(str(celda(hoja, ref)).replace(",", "."))
    except (TypeError, ValueError):
        return None


def tabla(hoja, fila_ini, fila_fin, columnas):
    """Arma una tabla. columnas = {"Nombre": "Letra"}. La 1.ª columna no puede estar vacía."""
    filas = []
    for f in range(fila_ini, fila_fin + 1):
        fila = {nombre: celda(hoja, f"{letra}{f}") for nombre, letra in columnas.items()}
        if fila[next(iter(columnas))] is not None:
            filas.append(fila)
    df = pd.DataFrame(filas)
    if "Mes" in df.columns:
        df["Mes"] = df["Mes"].astype(str).str.strip().str.capitalize()
    return df


def texto(valor, unidad):
    if valor is None:
        return "—"
    return f"{valor * 100:.1f}%" if unidad == "%" else f"{valor:.1f} días"


# ---------- Resumen de los 4 objetivos (ubicación de cada dato en el Excel) ----------
P = "Planteamiento"
OBJETIVOS = [
    {
        "n": 1, "corto": "Pronóstico de la demanda", "unidad": "%", "mejor": "mayor",
        "indicador": "Exactitud del pronóstico (FA = 1 − MAPE)",
        "herramienta": celda(P, "P9"), "motivo": celda(P, "J9"), "causa": celda(P, "L9"),
        "objetivo": celda("OBJ1", "C9"),
        "as_is": numero("OBJ1", "D53"), "estandar": numero("OBJ1", "D54"), "to_be": numero("OBJ1", "D55"),
        "conclusion": celda("OBJ1", "C72"), "recomendacion": celda("OBJ1", "C73"),
    },
    {
"n": 2, "corto": "Modelo EOQ", "unidad": "días", "mejor": "menor",        "indicador": "Duración del inventario (días)",
        "herramienta": celda(P, "P13"), "motivo": celda(P, "J13"), "causa": celda(P, "L13"),
        "objetivo": celda("OBJ2", "K2"),
        "as_is": numero("OBJ2", "L84"), "estandar": numero("OBJ2", "F28"), "to_be": numero("OBJ2", "P84"),
        "conclusion": celda(P, "AF13"), "recomendacion": celda(P, "AI13"),
    },
    {
        "n": 3, "corto": "Exactitud de inventarios", "unidad": "%", "mejor": "mayor",
        "indicador": "Confiabilidad del inventario (1 − % error)",
        "herramienta": celda(P, "P17"), "motivo": celda(P, "J17"), "causa": celda(P, "L17"),
        "objetivo": celda(P, "R17"),
        "as_is": numero("OBJ3", "P52"), "estandar": numero("OBJ3", "M76"), "to_be": numero("OBJ3", "P223"),
        "conclusion": celda(P, "AF17"), "recomendacion": celda(P, "AI17"),
    },
    {
        "n": 4, "corto": "Cumplimiento de pedidos", "unidad": "%", "mejor": "mayor",
        "indicador": "Cumplimiento de pedidos (%)",
        "herramienta": "Programación de despachos (regla EDD)",
        "motivo": celda("OBJ4", "C2"), "causa": celda("OBJ4", "C3"),
        "objetivo": celda("OBJ4", "G1"),
        "as_is": numero("OBJ4", "D90"), "estandar": numero("OBJ4", "L67"), "to_be": numero("OBJ4", "F90"),
        "conclusion": celda("OBJ4", "B92"), "recomendacion": celda("OBJ4", "B56"),
    },
]

for o in OBJETIVOS:
    a, s, t = o["as_is"], o["estandar"], o["to_be"]
    o["cumple"] = (t >= s) if o["mejor"] == "mayor" else (t <= s)
    o["cierre"] = (t - a) / (s - a) * 100 if s != a else 100.0  # % de la brecha que se cerró


# ---------- Gráficos reutilizables ----------
def escala(valores, unidad):
    return [v * 100 for v in valores] if unidad == "%" else list(valores)


def grafico_tres_barras(o, alto=300):
    esc = ["As-Is", "Estándar", "To-Be"]
    vals = escala([o["as_is"], o["estandar"], o["to_be"]], o["unidad"])
    sufijo = "%" if o["unidad"] == "%" else " d"
    fig = go.Figure(go.Bar(
        x=esc, y=vals, marker_color=[COLOR_ESC[e] for e in esc],
        text=[f"{v:.1f}{sufijo}" for v in vals], textposition="outside",
    ))
    fig.update_layout(height=alto, margin=dict(l=10, r=10, t=30, b=10), showlegend=False,
                      yaxis=dict(range=[0, max(vals) * 1.25], title=o["unidad"]))
    return fig


def grafico_medidor(o):
    a, s, t = escala([o["as_is"], o["estandar"], o["to_be"]], o["unidad"])
    tope = 100 if o["unidad"] == "%" else max(a, s, t) * 1.3
    sube_bien = o["mejor"] == "mayor"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=t,
        number={"suffix": "%" if o["unidad"] == "%" else " días", "valueformat": ".1f"},
        delta={"reference": a, "valueformat": ".1f",
               "increasing": {"color": "#22C55E" if sube_bien else "#E5484D"},
               "decreasing": {"color": "#E5484D" if sube_bien else "#22C55E"}},
        gauge={"axis": {"range": [0, tope]}, "bar": {"color": AMARILLO},
               "steps": [{"range": [0, a], "color": "#3A1F24"}],
               "threshold": {"line": {"color": "#FFFFFF", "width": 4}, "value": s}},
        title={"text": "To-Be vs. As-Is (línea blanca = estándar)", "font": {"size": 14}},
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=60, b=10))
    return fig


def linea_estandar(fig, valor, texto_linea="Estándar"):
    fig.add_hline(y=valor, line_dash="dash", line_color=COLOR_ESC["Estándar"],
                  annotation_text=texto_linea, annotation_position="top left")
    return fig


def filtrar_meses(df, meses):
    d = df[df["Mes"].isin(meses)].copy()
    d["Mes"] = pd.Categorical(d["Mes"], categories=ORDEN_MESES, ordered=True)
    return d.sort_values("Mes")


# ---------- Estilos de las tarjetas ----------
st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        background-color: #1A1D24;
        border-left: 5px solid #FFC800;
        padding: 12px 16px;
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
    .ficha {
        background-color: #1A1D24; border-radius: 8px; padding: 12px 14px;
        height: 100%; border-top: 3px solid #FFC800;
    }
    .ficha small { color: #9AA0A6; text-transform: uppercase; letter-spacing: 1px; font-size: 0.7rem; }
    .ficha p { margin: 4px 0 0 0; font-size: 0.95rem; }
    .etiqueta { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }
    .ok  { background: #14532D; color: #86EFAC; }
    .no  { background: #4C1D1D; color: #FCA5A5; }
    </style>
    """,
    unsafe_allow_html=True,
)


def ficha(titulo, contenido):
    st.markdown(f'<div class="ficha"><small>{titulo}</small><p>{contenido}</p></div>',
                unsafe_allow_html=True)


def etiqueta_cumple(o):
    if o["cumple"]:
        return '<span class="etiqueta ok">Cumple el estándar</span>'
    return '<span class="etiqueta no">Aún no llega al estándar</span>'

st.markdown("""
<style>
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0B0E14 0%, #10141C 100%) !important;
  border-right: 1px solid rgba(255,200,0,.22);
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  color: #E5484D !important; letter-spacing: .32em; text-transform: uppercase;
  font-size: .72rem !important; font-weight: 700;
}
/* Casco de la barra lateral más pequeño y centrado */
[data-testid="stSidebar"] [data-testid="stImage"] {
  display: flex; justify-content: center;
}
[data-testid="stSidebar"] [data-testid="stImage"] img {
  width: 90px !important; height: auto !important;
}
[data-testid="stSidebar"] [role="radiogroup"] { gap: 6px; counter-reset: idx; }
[data-testid="stSidebar"] [role="radiogroup"] > label {
  counter-increment: idx;
  display: flex; align-items: center; gap: 12px;
  padding: 9px 16px; margin: 0; cursor: pointer;
  background: rgba(255,255,255,.03);
  clip-path: polygon(14px 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%, 0 14px);
  transition: background .3s ease, transform .3s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child { display: none !important; }
[data-testid="stSidebar"] [role="radiogroup"] > label::before {
  content: "0" counter(idx); color: #FFC800; font-size: .72rem;
  letter-spacing: .12em; font-weight: 700;
}
[data-testid="stSidebar"] [role="radiogroup"] > label p {
  color: #D9D5CB !important; margin: 0; letter-spacing: .02em; transition: color .3s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] > label:hover {
  background: linear-gradient(90deg, rgba(229,72,77,.22), rgba(229,72,77,.05));
  transform: translateX(4px);
}
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
  background: linear-gradient(120deg, #FF7A7E 0%, #E5484D 45%, #B91C22 100%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.45);
  transform: translateX(6px);
}
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::before { color: #fff; }
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p { color: #fff !important; font-weight: 700; }
/* Circulito de la opción */
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child > div {
  border-color: #E5484D !important;
}
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) > div:first-child > div {
  background-color: #E5484D !important;
  border-color: #E5484D !important;
}
</style>
""", unsafe_allow_html=True)
# ---------- Barra lateral: logo e índice ----------
st.sidebar.image("logo.png")
st.sidebar.title("Indusegur Perú S.A.C.")
seccion = st.sidebar.radio(
    "Índice",
    ["Carátula", "Modelo EOQ", "RFID"],
)
transicion_suave(seccion)

# Filtro de meses (solo para los objetivos 2, 3 y 4)
meses_elegidos = ORDEN_MESES
if seccion in ("Modelo EOQ", "RFID"):
    with st.sidebar:
        st.divider()
        st.subheader("Filtros")
        desde, hasta = st.select_slider("Meses", options=ORDEN_MESES,
                                        value=(ORDEN_MESES[0], ORDEN_MESES[-1]))
        meses_elegidos = ORDEN_MESES[ORDEN_MESES.index(desde): ORDEN_MESES.index(hasta) + 1]


# ---------- Cabecera común de cada objetivo ----------
def cabecera_objetivo(o):
    st.title(o["corto"])
    st.markdown(etiqueta_cumple(o), unsafe_allow_html=True)
    st.caption(o["objetivo"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: ficha("Motivo", o["motivo"])
    with c2: ficha("Causa raíz", o["causa"])
    with c3: ficha("Herramienta", o["herramienta"])
    with c4: ficha("Indicador", o["indicador"])
    st.write("")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("As-Is (actual)", texto(o["as_is"], o["unidad"]))
    m2.metric("Estándar (meta)", texto(o["estandar"], o["unidad"]))
    dif = o["to_be"] - o["as_is"]
    dif_txt = f"{dif * 100:+.1f} pp" if o["unidad"] == "%" else f"{dif:+.1f} días"
    m3.metric("To-Be (con la mejora)", texto(o["to_be"], o["unidad"]), dif_txt,
              delta_color="normal" if o["mejor"] == "mayor" else "inverse")
    m4.metric("Brecha cerrada", f"{min(o['cierre'], 100):.0f}%")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("As-Is vs. Estándar vs. To-Be")
        st.plotly_chart(grafico_tres_barras(o), width="stretch", key=f"barras{o['n']}")
    with g2:
        st.subheader("Avance del indicador")
        st.plotly_chart(grafico_medidor(o), width="stretch", key=f"medidor{o['n']}")


def pie_objetivo(o):
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Conclusión")
        st.success(o["conclusion"] or "—")
    with c2:
        st.subheader("Recomendación" if o["n"] != 4 else "Propuesta")
        st.info(o["recomendacion"] or "—")


def ver_tabla(df, nombre):
    with st.expander("Ver los datos de esta tabla"):
        st.dataframe(df, width="stretch", hide_index=True)
        st.download_button("Descargar (CSV)", df.to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"{nombre}.csv", mime="text/csv", key=f"dl_{nombre}")


# ---------- Contenido según la opción elegida ----------
if seccion == "Carátula":
    # ----- Edita estos datos -----
    INSTITUCION = "Universidad Privada del Norte"
    FACULTAD = "Facultad de Ingeniería Industrial"
    CURSO = "Logística y Cadena de Suministro · Grupo 8"
    TITULO_1 = "Dashboard:"
    TITULO_2 = "Modelo EOQ y RFID"
    INTEGRANTES = [
        "ERIG JOHAN DIAZ PERALTA",
        "ARACELY FERNANDA RAMON ALANYA",
        "PIERINA NICOLLE GARAMENDI GALINDO",
        "CHRISTIAN PEREZ QUISPE",
    ]
    DOCENTE = "TU PAPÁ YA SABES QUIÉN"
    FECHA = "28 noviembre del 2026"
    # -----------------------------

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap');

.caratula-simple {
  min-height: 80vh; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center;
  gap: 3.2vh; color: #fff;
  font-family: 'Source Serif 4', Georgia, serif;
}
.caratula-simple .univ  { font-size: 2rem; font-weight: 800; color: #FFC800; text-transform: uppercase; letter-spacing: .05em; }
.caratula-simple .fac   { font-size: 1.4rem; font-weight: 600; margin-top: .3rem; }
.caratula-simple .curso { font-size: 1.2rem; font-style: italic; color: #C9CED6; margin-top: .2rem; }
.caratula-simple .t1    { font-size: 3.6rem; font-weight: 800; color: #FFC800; text-transform: uppercase; line-height: 1.05; }
.caratula-simple .t2    { font-size: 2.2rem; font-weight: 400; color: #E6E8EB; text-transform: uppercase; }
.caratula-simple .rotulo { font-size: 1rem; font-weight: 700; color: #FFC800; letter-spacing: .18em; text-transform: uppercase; margin-bottom: .6rem; }
.caratula-simple .nombres { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem 3rem; }
.caratula-simple .nombre  { font-size: 1.1rem; font-weight: 600; }
.caratula-simple .docente { font-size: 1.2rem; font-weight: 600; }
.caratula-simple .fecha   { font-size: 1.05rem; font-style: italic; color: #C9CED6; margin-top: .3rem; }
</style>
""", unsafe_allow_html=True)

    nombres_html = "".join(f'<div class="nombre">{n}</div>' for n in INTEGRANTES)
    st.markdown(
        '<div class="caratula-simple">'
        f'<div><div class="univ">{INSTITUCION}</div>'
        f'<div class="fac">{FACULTAD}</div>'
        f'<div class="curso">{CURSO}</div></div>'
        f'<div><div class="t1">{TITULO_1}</div>'
        f'<div class="t2">{TITULO_2}</div></div>'
        f'<div><div class="rotulo">Integrantes</div><div class="nombres">{nombres_html}</div></div>'
        f'<div><div class="rotulo">Docente</div><div class="docente">{DOCENTE}</div>'
        f'<div class="fecha">{FECHA}</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
elif seccion == "Modelo EOQ":
    o = OBJETIVOS[1]
    cabecera_objetivo(o)

    st.subheader("Duración del inventario por mes")
    dur = tabla("OBJ2", 72, 83, {"Mes": "F", "Duración actual (días)": "L",
                                 "Duración con EOQ (días)": "P", "Mejora (días)": "R"})
    dur = filtrar_meses(dur, meses_elegidos)
    fig = px.line(dur, x="Mes", y=["Duración actual (días)", "Duración con EOQ (días)"],
                  markers=True, labels={"value": "Días", "variable": "Escenario"},
                  color_discrete_sequence=[COLOR_ESC["As-Is"], COLOR_ESC["To-Be"]])
    linea_estandar(fig, o["estandar"], f"Estándar {o['estandar']:.0f} días")
    st.plotly_chart(fig, width="stretch")
    ver_tabla(dur, "duracion_inventario")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Lote actual vs. lote óptimo (EOQ)")
        lotes = pd.DataFrame({
            "Producto": ["Pintura", "Cintillo", "Llave"],
            "Lote actual": [numero("OBJ2", "G64"), numero("OBJ2", "K64"), numero("OBJ2", "O64")],
            "EOQ óptimo": [numero("OBJ2", "G65"), numero("OBJ2", "K65"), numero("OBJ2", "O65")],
        })
        fig = px.bar(lotes, x="Producto", y=["Lote actual", "EOQ óptimo"], barmode="group",
                     text_auto=True, labels={"value": "Unidades", "variable": ""},
                     color_discrete_sequence=[COLOR_ESC["As-Is"], COLOR_ESC["To-Be"]])
        st.plotly_chart(fig, width="stretch")
    with c2:
        st.subheader("Clasificación ABC")
        abc = tabla("OBJ2", 46, 48, {"Producto": "F", "Demanda": "I", "Costo (S/)": "L",
                                     "Valor anual (S/)": "O", "Clase": "R"})
        fig = px.pie(abc, names="Producto", values="Valor anual (S/)", hole=0.5)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, width="stretch")

    st.subheader("Impacto económico mensual: antes vs. después del EOQ")
    imp = tabla("OBJ2", 113, 124, {"Mes": "F", "Antes (S/)": "H", "Después (S/)": "K"})
    imp = filtrar_meses(imp, meses_elegidos)
    fig = px.bar(imp, x="Mes", y=["Antes (S/)", "Después (S/)"], barmode="group",
                 labels={"value": "Soles", "variable": ""},
                 color_discrete_sequence=[COLOR_ESC["As-Is"], COLOR_ESC["To-Be"]])
    st.plotly_chart(fig, width="stretch")
    pie_objetivo(o)

elif seccion == "RFID":
    o = OBJETIVOS[2]
    cabecera_objetivo(o)

    asis = tabla("OBJ3", 40, 51, {"Mes": "G", "Diferencia (S/)": "L", "Error": "N", "Confiabilidad": "P"})
    tobe = tabla("OBJ3", 211, 222, {"Mes": "G", "Diferencia (S/)": "L", "Error": "N", "Confiabilidad": "P"})
    asis["Escenario"], tobe["Escenario"] = "As-Is", "To-Be"
    ambos = filtrar_meses(pd.concat([asis, tobe]), meses_elegidos)
    ambos["Confiabilidad (%)"] = (ambos["Confiabilidad"].astype(float) * 100).round(1)
    ambos["Error (%)"] = (ambos["Error"].astype(float) * 100).round(1)

    st.subheader("Confiabilidad del inventario por mes")
    fig = px.line(ambos, x="Mes", y="Confiabilidad (%)", color="Escenario", markers=True,
                  color_discrete_map=COLOR_ESC)
    linea_estandar(fig, o["estandar"] * 100, f"Estándar {o['estandar'] * 100:.0f}%")
    st.plotly_chart(fig, width="stretch")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Diferencia entre físico y sistema (S/)")
        fig = px.bar(ambos, x="Mes", y="Diferencia (S/)", color="Escenario", barmode="group",
                     color_discrete_map=COLOR_ESC)
        st.plotly_chart(fig, width="stretch")
    with c2:
        st.subheader("Costo de implementación RFID")
        costos = tabla("OBJ3", 109, 113, {"Componente": "F", "Cantidad": "N",
                                          "Costo unitario (S/)": "O", "Costo total (S/)": "P"})
        fig = px.pie(costos, names="Componente", values="Costo total (S/)", hole=0.5)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Inversión total estimada: S/ {numero('OBJ3', 'P114'):,.0f}")
    ver_tabla(ambos.drop(columns=["Error", "Confiabilidad"]), "exactitud_inventarios")
    pie_objetivo(o)

elif seccion == "Objetivo 4":
    o = OBJETIVOS[3]
    cabecera_objetivo(o)

    cum = tabla("OBJ4", 70, 81, {"Mes": "B", "Programados": "C", "Retrasados As-Is": "D",
                                 "Cumplimiento As-Is": "E", "Retrasados To-Be": "F",
                                 "Cumplimiento To-Be": "H", "Impacto As-Is (S/)": "J",
                                 "Impacto To-Be (S/)": "K", "Ahorro (S/)": "L"})
    cum = filtrar_meses(cum, meses_elegidos)
    graf = cum.assign(**{"As-Is": cum["Cumplimiento As-Is"].astype(float) * 100,
                         "To-Be": cum["Cumplimiento To-Be"].astype(float) * 100})

    st.subheader("Cumplimiento de pedidos por mes")
    fig = px.line(graf, x="Mes", y=["As-Is", "To-Be"], markers=True,
                  labels={"value": "Cumplimiento (%)", "variable": "Escenario"},
                  color_discrete_map=COLOR_ESC)
    linea_estandar(fig, o["estandar"] * 100, f"Meta {o['estandar'] * 100:.0f}%")
    st.plotly_chart(fig, width="stretch")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Impacto económico por retrasos")
        fig = px.bar(cum, x="Mes", y=["Impacto As-Is (S/)", "Impacto To-Be (S/)"], barmode="group",
                     labels={"value": "Soles", "variable": ""},
                     color_discrete_sequence=[COLOR_ESC["As-Is"], COLOR_ESC["To-Be"]])
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Ahorro en los meses elegidos: S/ {cum['Ahorro (S/)'].astype(float).sum():,.0f}")
    with c2:
        st.subheader("Gráfico de control de retrasos (p)")
        ctrl = tabla("OBJ4", 30, 41, {"Mes": "B", "Proporción de retraso": "G",
                                      "LCS": "I", "LC": "K", "LCI": "M"})
        ctrl = filtrar_meses(ctrl, meses_elegidos)
        fig = px.line(ctrl, x="Mes", y=["Proporción de retraso", "LCS", "LC", "LCI"], markers=True,
                      labels={"value": "Proporción", "variable": ""},
                      color_discrete_sequence=[AMARILLO, "#E5484D", "#94A3B8", "#E5484D"])
        st.plotly_chart(fig, width="stretch")

    st.subheader("Plan de programación de despachos")
    plan = tabla("OBJ4", 60, 64, {"Actividad": "B", "Descripción": "E",
                                  "Responsable": "I", "Frecuencia": "K"})
    st.dataframe(plan, width="stretch", hide_index=True)
    ver_tabla(cum, "cumplimiento_pedidos")
    pie_objetivo(o)
