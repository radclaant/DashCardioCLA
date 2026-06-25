import streamlit as st
import pandas as pd
import numpy as np
from copy import deepcopy
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import base64

# ─────────────────────────────────────────────
# CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PGP Cardio | Dashboard",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CONTRASEÑA
# ─────────────────────────────────────────────
PASSWORD = "ASD123asd"

# ─────────────────────────────────────────────
# URL LOGO
# ─────────────────────────────────────────────
LOGO_URL = "assets/Logotipo.png"

# ─────────────────────────────────────────────
# CUPS HOMÓLOGO DICT — RESPALDO (solo si no se carga Nota Técnica)
# ADVERTENCIA: Estos códigos son de EJEMPLO y probablemente NO
# coinciden con los CUPS Homologo reales de tu Nota Técnica PGP.
# SIEMPRE carga el archivo de Nota Técnica para resultados correctos.
# ─────────────────────────────────────────────
CUPS_HOMOLOGO_RESPALDO = {
    890901: {"descripcion": "ELECTROCARDIOGRAMA", "codalias": "EKG001", "tipo": "DIAGNÓSTICO", "valor": 45000, "tope": 4},
    890902: {"descripcion": "ECOCARDIOGRAMA TRANSTORÁCICO", "codalias": "ECO001", "tipo": "DIAGNÓSTICO", "valor": 280000, "tope": 2},
    890903: {"descripcion": "HOLTER DE RITMO 24 HORAS", "codalias": "HOL001", "tipo": "DIAGNÓSTICO", "valor": 195000, "tope": 2},
    890904: {"descripcion": "PRUEBA DE ESFUERZO", "codalias": "PRE001", "tipo": "DIAGNÓSTICO", "valor": 210000, "tope": 1},
    890905: {"descripcion": "CATETERISMO CARDIACO DIAGNÓSTICO", "codalias": "CAT001", "tipo": "HEMODINAMIA", "valor": 1850000, "tope": 1},
    890906: {"descripcion": "ANGIOPLASTIA CORONARIA", "codalias": "ANG001", "tipo": "HEMODINAMIA", "valor": 4500000, "tope": 1},
    890907: {"descripcion": "IMPLANTE DE STENT CORONARIO", "codalias": "STN001", "tipo": "HEMODINAMIA", "valor": 5200000, "tope": 1},
    890908: {"descripcion": "ABLACIÓN POR RADIOFRECUENCIA", "codalias": "ABL001", "tipo": "ELECTROFISIOLOGÍA", "valor": 3800000, "tope": 1},
    890909: {"descripcion": "IMPLANTE DE MARCAPASOS UNICAMERAL", "codalias": "MPC001", "tipo": "ELECTROFISIOLOGÍA", "valor": 6500000, "tope": 1},
    890910: {"descripcion": "IMPLANTE DE MARCAPASOS BICAMERAL", "codalias": "MPC002", "tipo": "ELECTROFISIOLOGÍA", "valor": 8200000, "tope": 1},
    890911: {"descripcion": "CARDIOVERSIÓN ELÉCTRICA", "codalias": "CVE001", "tipo": "ELECTROFISIOLOGÍA", "valor": 750000, "tope": 2},
    890912: {"descripcion": "REVASCULARIZACIÓN MIOCÁRDICA (CX)", "codalias": "REV001", "tipo": "CX CARDIOVASCULAR", "valor": 18500000, "tope": 1},
    890913: {"descripcion": "REEMPLAZO VALVULAR AÓRTICO", "codalias": "VAL001", "tipo": "CX CARDIOVASCULAR", "valor": 22000000, "tope": 1},
    890914: {"descripcion": "REEMPLAZO VALVULAR MITRAL", "codalias": "VAL002", "tipo": "CX CARDIOVASCULAR", "valor": 21500000, "tope": 1},
    890915: {"descripcion": "PERICARDIECTOMÍA", "codalias": "PER001", "tipo": "CX CARDIOVASCULAR", "valor": 15000000, "tope": 1},
    890916: {"descripcion": "CONSULTA CARDIOLOGÍA PRIMERA VEZ", "codalias": "CON001", "tipo": "CONSULTA", "valor": 85000, "tope": 6},
    890917: {"descripcion": "CONSULTA CARDIOLOGÍA CONTROL", "codalias": "CON002", "tipo": "CONSULTA", "valor": 65000, "tope": 12},
    890918: {"descripcion": "ECOCARDIOGRAMA TRANSESOFÁGICO", "codalias": "ECO002", "tipo": "DIAGNÓSTICO", "valor": 420000, "tope": 1},
    890919: {"descripcion": "MONITOREO AMBULATORIO PRESIÓN ARTERIAL", "codalias": "MAP001", "tipo": "DIAGNÓSTICO", "valor": 120000, "tope": 2},
    890920: {"descripcion": "ANGIOTOMOGRAFÍA CORONARIA", "codalias": "ATC001", "tipo": "DIAGNÓSTICO", "valor": 980000, "tope": 1},
}

# ─────────────────────────────────────────────
# CSS CUSTOM
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #151922 100%);
        border-right: 1px solid #2d3748;
    }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2a3a 0%, #1a2332 100%);
        border: 1px solid #2d4a6e;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0,100,200,0.15);
    }
    [data-testid="metric-container"] label {
        color: #7ecbf7 !important;
        font-size: 0.78rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 700;
    }
    .membrete-title { font-size: 1.5rem; font-weight: 800; color: #ffffff; margin: 0; }
    .membrete-subtitle { font-size: 0.82rem; color: #7ecbf7; margin: 2px 0 0 0; }
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1f2e; border-radius: 10px; padding: 4px; gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent; color: #9eb8d4; border-radius: 8px;
        font-weight: 600; font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e4080 0%, #1565c0 100%) !important;
        color: #ffffff !important;
    }
    .dataframe { font-size: 0.82rem !important; }
    .stButton button {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        color: white; border: none; border-radius: 8px;
        font-weight: 600; width: 100%;
    }
    .badge-pending {
        background: #1a2744; border: 1px dashed #4a6fa5;
        border-radius: 10px; padding: 60px 30px; text-align: center; color: #7ecbf7;
    }
    .warning-hallucinated {
        background: linear-gradient(135deg, #3d2a00, #4a3200);
        border: 1px solid #ff8f00; border-radius: 10px;
        padding: 12px 18px; color: #ffd54f; font-size: 0.82rem; margin: 10px 0;
    }
    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #7ecbf7;
        border-left: 3px solid #1565c0; padding-left: 10px; margin: 20px 0 12px 0;
    }
    .login-wrapper {
        max-width: 420px; margin: 80px auto;
        background: linear-gradient(135deg, #1a1f2e, #141920);
        border: 1px solid #2d4a6e; border-radius: 16px;
        padding: 40px; box-shadow: 0 8px 32px rgba(0,50,150,0.25);
    }
    .nota-tecnica-box {
        background: linear-gradient(135deg, #1a2744, #0d1b2a);
        border: 1px solid #1565c0; border-radius: 10px;
        padding: 14px 16px; margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def login_screen():
    st.markdown("""
    <div class="login-wrapper">
        <div style="text-align:center; margin-bottom:28px;">
            <div style="font-size:3rem;">🫀</div>
            <h2 style="color:#fff; margin:8px 0 4px 0; font-size:1.4rem; font-weight:800;">PGP Cardiovascular</h2>
            <p style="color:#7ecbf7; font-size:0.82rem; margin:0;">Sistema de Reportes | EPS SURA</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("###")
        pwd = st.text_input("🔒 Contraseña", type="password", placeholder="Ingresa tu contraseña...")
        if st.button("Ingresar →", use_container_width=True):
            if pwd == PASSWORD:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta. Intenta de nuevo.")


# ─────────────────────────────────────────────
# MEMBRETE
# ─────────────────────────────────────────────
def render_membrete():
    col_logo, col_text, col_fecha = st.columns([1, 5, 2])
    with col_logo:
        try:
            st.image(LOGO_URL, width=100)
        except Exception:
            st.markdown("🫀")
    with col_text:
        st.markdown("""
        <div style="padding-top:6px;">
            <p class="membrete-title">PGP Cardiovascular — EPS SURA</p>
            <p class="membrete-subtitle">Sistema de Monitoreo y Reportes de Prestaciones | Programa de Gestión de Patología</p>
        </div>
        """, unsafe_allow_html=True)
    with col_fecha:
        st.markdown(f"""
        <div style="text-align:right; padding-top:10px; color:#7ecbf7; font-size:0.80rem;">
            📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
            <span style="color:#9eb8d4;">Sesión activa</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #1e3a5f; margin:12px 0 18px 0;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FORMATEO
# ─────────────────────────────────────────────
def fmt_money(v):
    try:
        return f"$ {v:,.0f}".replace(",", ".")
    except Exception:
        return str(v)

def fmt_num(v):
    try:
        return f"{int(v):,}".replace(",", ".")
    except Exception:
        return str(v)


# ─────────────────────────────────────────────
# LEER NOTA TÉCNICA (igual que cardiopgp.py)
# ─────────────────────────────────────────────
def leer_nota_tecnica(uploaded_file):
    """
    Replica exactamente la lógica de cardiopgp.py para construir
    cups_homologo_dict desde el Excel de Nota Técnica.
    """
    try:
        # Leer el Excel — detectar hoja "Procedimientos "
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = None
        for s in xls.sheet_names:
            if "procedimiento" in s.lower():
                sheet_name = s
                break

        if sheet_name is None:
            # Si no encuentra por nombre, usar la primera hoja
            sheet_name = xls.sheet_names[0]
            st.warning(f"⚠️ No se encontró hoja 'Procedimientos'. Se usará: '{sheet_name}'")

        df_notatec = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=1)

        # Detectar columnas esperadas (pueden variar de nombre)
        col_cups = None
        col_desc = None
        col_codalias = None
        col_tipo = None
        col_tarifa = None
        col_frecuencia = None

        for c in df_notatec.columns:
            cl = c.lower().strip()
            if "cups" in cl and "homolog" in cl:
                col_cups = c
            elif "prestacion_desc" in cl or ("prestacion" in cl and "desc" in cl):
                col_desc = c
            elif "codigo_prestacion_op" in cl or ("codigo" in cl and "op" in cl):
                col_codalias = c
            elif "agrup" in cl and "salud" in cl:
                col_tipo = c
            elif "tarifa" in cl:
                col_tarifa = c
            elif "frecuencia" in cl or ("fren" in cl and "mes" in cl):
                col_frecuencia = c

        # Si no encontró por nombre exacto, intentar por posición/parcial
        if col_cups is None:
            for c in df_notatec.columns:
                if "cups" in c.lower():
                    col_cups = c
                    break
        if col_desc is None:
            for c in df_notatec.columns:
                if "desc" in c.lower() and "prest" in c.lower():
                    col_desc = c
                    break
        if col_tipo is None:
            for c in df_notatec.columns:
                if "agrup" in c.lower():
                    col_tipo = c
                    break
        if col_tarifa is None:
            for c in df_notatec.columns:
                if "tarifa" in c.lower() or "valor" in c.lower():
                    col_tarifa = c
                    break
        if col_frecuencia is None:
            for c in df_notatec.columns:
                if "frec" in c.lower() or "tope" in c.lower():
                    col_frecuencia = c
                    break

        # Validar columnas críticas
        if col_cups is None:
            st.error("❌ No se encontró columna 'Cups Homologo' en la Nota Técnica.")
            st.markdown(f"**Columnas disponibles:** `{list(df_notatec.columns)}`")
            return None, df_notatec

        # Construir dict — misma lógica que cardiopgp.py
        cups_homologo_dict = {}
        errores = 0
        for index, row in df_notatec.iterrows():
            try:
                key = row[col_cups]
                # Convertir a numérico si viene como string
                if pd.notna(key):
                    key = pd.to_numeric(key, errors='coerce')
                    if pd.notna(key):
                        key = int(key)
                        cups_homologo_dict[key] = {
                            'descripcion': str(row[col_desc]) if col_desc and pd.notna(row.get(col_desc)) else "",
                            'codalias': str(row[col_codalias]) if col_codalias and pd.notna(row.get(col_codalias)) else "",
                            'tipo': str(row[col_tipo]) if col_tipo and pd.notna(row.get(col_tipo)) else "",
                            'valor': float(row[col_tarifa]) if col_tarifa and pd.notna(row.get(col_tarifa)) else 0,
                            'tope': float(row[col_frecuencia]) if col_frecuencia and pd.notna(row.get(col_frecuencia)) else 0,
                        }
            except Exception:
                errores += 1

        if errores > 0:
            st.warning(f"⚠️ {errores} filas de la Nota Técnica no se pudieron procesar.")

        return cups_homologo_dict, df_notatec

    except Exception as e:
        st.error(f"❌ Error leyendo Nota Técnica: {e}")
        return None, None


# ─────────────────────────────────────────────
# PROCESAMIENTO — REPLICA EXACTA DE cardiopgp.py
# ─────────────────────────────────────────────
def procesar_ghips(df_raw, cups_homologo_dict):
    """
    Replica exactamente la lógica de limpieza de cardiopgp.py.
    Recibe cups_homologo_dict como parámetro (ya sea del Excel o del respaldo).
    """
    df = deepcopy(df_raw)

    # ── Detectar columnas ──
    fecha_col = None
    for c in df.columns:
        if "fecha" in c.lower() and "activ" in c.lower():
            fecha_col = c
            break
    if fecha_col is None:
        for c in df.columns:
            if "fecha" in c.lower():
                fecha_col = c
                break

    aseg_col = None
    for c in df.columns:
        if "aseguradora" in c.lower():
            aseg_col = c
            break

    cod_col = None
    for c in df.columns:
        if "codactividad" in c.lower() or "vcodactividad" in c.lower() or "cod_actividad" in c.lower():
            cod_col = c
            break

    id_col = None
    for c in df.columns:
        if "identif" in c.lower():
            id_col = c
            break

    # ── PASO 1: Filtrar por Aseguradora (MATCH EXACTO) ──
    if aseg_col:
        df_sura = df[df[aseg_col] == 'EPS  SURAMERICANA S.A'].copy()
    else:
        df_sura = df.copy()

    # ── Convertir fecha ──
    if fecha_col:
        df_sura[fecha_col] = pd.to_datetime(df_sura[fecha_col], errors="coerce")

    # ── PASO 2: Filtrar por CUPS homologados ──
    unique_cups_homologo_values = list(cups_homologo_dict.keys())

    if cod_col:
        df_sura['vCodActividad_numeric'] = pd.to_numeric(df_sura[cod_col], errors='coerce')
        df_sura = df_sura[
            df_sura['vCodActividad_numeric'].isin(unique_cups_homologo_values) &
            df_sura['vCodActividad_numeric'].notna()
        ].copy()

        # ── PASO 3: Merge con atributos ──
        cups_attributes_df = pd.DataFrame.from_dict(cups_homologo_dict, orient='index')
        cups_attributes_df = cups_attributes_df.reset_index().rename(columns={'index': 'vCodActividad_numeric'})

        df_sura = pd.merge(
            df_sura,
            cups_attributes_df,
            left_on='vCodActividad_numeric',
            right_on='vCodActividad_numeric',
            how='left'
        )
        df_sura = df_sura.drop(columns=['vCodActividad_numeric'])
    else:
        st.error("❌ No se encontró columna 'vCodActividad' en el archivo.")
        return df.head(0), fecha_col, aseg_col, cod_col, id_col

    return df_sura, fecha_col, aseg_col, cod_col, id_col


def agrupar_por_cups(df, fecha_col, id_col, cod_col):
    """Group by exacto de cardiopgp.py: [vCodActividad, descripcion, Mes]"""
    if fecha_col and fecha_col in df.columns:
        df.loc[:, 'Mes'] = df[fecha_col].dt.to_period('M')
    else:
        df.loc[:, 'Mes'] = "SIN MES"

    grp_cols = ['descripcion', 'Mes']
    if cod_col and cod_col in df.columns:
        grp_cols = [cod_col] + grp_cols

    agg_dict = {
        'total_valor': ('valor', 'sum'),
        'conteo_cups': ('valor', 'count'),
        'valor_unitario': ('valor', 'first'),
        'tope_redondeado': ('tope', lambda x: np.ceil(x.iloc[0]) if len(x) > 0 else 0),
    }
    if id_col and id_col in df.columns:
        agg_dict['cantidad_usuarios_diferentes'] = (id_col, lambda x: x.nunique())

    grouped = df.groupby(grp_cols).agg(**agg_dict).reset_index()

    grouped['porcentaje_tope'] = np.where(
        grouped['tope_redondeado'] > 0,
        (grouped['conteo_cups'] / grouped['tope_redondeado'] * 100).round(1),
        0.0
    )

    sort_cols = ['Mes']
    if cod_col and cod_col in grouped.columns:
        sort_cols.append(cod_col)
    sort_cols.append('descripcion')
    grouped = grouped.sort_values(by=sort_cols)

    return grouped


# ─────────────────────────────────────────────
# TAB 1: REPORTES GHIPS
# ─────────────────────────────────────────────
def tab_ghips():
    st.markdown("<div class='section-title'>📂 Cargar Archivos</div>", unsafe_allow_html=True)

    # ── CARGA DE NOTA TÉCNICA ──
    st.sidebar.markdown("""
    <div class="nota-tecnica-box">
        <div style="font-size:1.2rem;">📝</div>
        <p style="color:#7ecbf7; font-weight:700; font-size:0.85rem; margin:4px 0 2px 0;">NOTA TÉCNICA PGP</p>
        <p style="color:#9eb8d4; font-size:0.72rem; margin:0;">Archivo Excel con los CUPS homologados del PGP Cardiovascular</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_nota = st.sidebar.file_uploader(
        "📝 Nota Técnica (.xlsx)",
        type=["xlsx", "xls"],
        key="nota_file",
    )

    cups_dict = None
    df_notatec_raw = None
    usando_respaldo = False

    if uploaded_nota is not None:
        cups_dict, df_notatec_raw = leer_nota_tecnica(uploaded_nota)
        if cups_dict is not None:
            st.sidebar.success(f"✅ {len(cups_dict)} CUPS cargados desde Nota Técnica")
    else:
        # Usar respaldo
        cups_dict = CUPS_HOMOLOGO_RESPALDO
        usando_respaldo = True
        st.sidebar.warning(f"⚠️ Usando {len(cups_dict)} CUPS de respaldo (ejemplo)")

    # ── CARGA DE FACTURACIÓN ──
    st.sidebar.markdown("---")
    uploaded = st.sidebar.file_uploader(
        "📁 Facturación Grabada (.csv / .xlsx)",
        type=["csv", "xlsx", "xls"],
        key="ghips_file",
    )

    if uploaded is None:
        st.info("👆 Carga ambos archivos en el panel izquierdo para comenzar.")
        if usando_respaldo:
            st.markdown("""
            <div style="background:#3d2a00; border:1px solid #ff8f00; border-radius:12px; padding:20px; margin-top:16px;">
                <p style="color:#ffd54f; font-weight:700; font-size:0.9rem; margin:0 0 8px 0;">⚠️ IMPORTANTE — Nota Técnica no cargada</p>
                <p style="color:#ffcc80; font-size:0.82rem; line-height:1.6; margin:0;">
                    Los CUPS del dict de respaldo (<code>890901</code>-<code>890920</code>) son <strong>códigos de ejemplo</strong>
                    y muy probablemente <strong>NO coinciden</strong> con los CUPS Homologo reales de tu Nota Técnica PGP Cardiovascular.<br><br>
                    Por eso el dashboard muestra 0 resultados: los códigos de tu archivo (ej: <code>901107</code>, <code>907106</code>, <code>890701</code>)
                    no están en el dict de ejemplo.<br><br>
                    <strong>👉 Carga el archivo "NOTA TECNICA AMBULATORIA PGP CARDIO.xlsx"</strong> para que el sistema lea los CUPS Homologo reales.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#1a1f2e; border:1px dashed #2d4a6e; border-radius:12px; padding:30px; text-align:center; color:#7ecbf7; margin-top:20px;">
            <div style="font-size:2.5rem;">📊</div>
            <p style="font-size:1rem; font-weight:600; margin:10px 0 4px 0;">Sin datos cargados</p>
            <p style="font-size:0.82rem; color:#9eb8d4;">Se necesitan 2 archivos:</p>
            <p style="font-size:0.78rem; color:#6a8aaa; margin-top:8px;">
                1️⃣ Nota Técnica PGP Cardio (.xlsx)<br>
                2️⃣ Facturación Grabada (.csv o .xlsx)
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Leer archivo de facturación
    try:
        if uploaded.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded, encoding="latin-1")
        else:
            df_raw = pd.read_excel(uploaded)
        st.sidebar.success(f"✅ {len(df_raw):,} filas cargadas")
    except Exception as e:
        st.error(f"Error leyendo archivo: {e}")
        return

    # ── DIAGNÓSTICO PRE-PROCESAMIENTO ──
    # Detectar columna de código
    cod_col_detect = None
    for c in df_raw.columns:
        if "codactividad" in c.lower() or "vcodactividad" in c.lower():
            cod_col_detect = c
            break

    # Mostrar diagnóstico si se usa respaldo
    if usando_respaldo and cod_col_detect:
        cups_en_archivo = set(pd.to_numeric(df_raw[cod_col_detect], errors='coerce').dropna().unique())
        cups_en_dict = set(cups_dict.keys())
        interseccion = cups_en_archivo & cups_en_dict

        with st.expander("🔍 Diagnóstico: ¿Por qué no hay resultados?", expanded=True):
            st.markdown("""
            <div style="background:#3d0a0a; border:1px solid #c62828; border-radius:10px; padding:16px; margin-bottom:12px;">
                <p style="color:#ff8a80; font-weight:700; font-size:0.95rem; margin:0 0 6px 0;">🔴 Los CUPS de tu archivo NO coinciden con el dict de respaldo</p>
                <p style="color:#ffcdd2; font-size:0.82rem; margin:0;">
                    El dict de respaldo tiene códigos de ejemplo (890901-890920) que no corresponden
                    a los CUPS Homologo reales de la Nota Técnica PGP Cardiovascular.
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("CUPS en archivo", fmt_num(len(cups_en_archivo)))
            c2.metric("CUPS en dict respaldo", fmt_num(len(cups_en_dict)))
            c3.metric("Coincidencias", fmt_num(len(interseccion)))

            st.markdown("**Ejemplo de CUPS en tu archivo (primeros 20):**")
            muestra_cups = sorted(cups_en_archivo)[:20]
            st.code(", ".join([str(int(c)) for c in muestra_cups]))

            st.markdown("**CUPS en el dict de respaldo:**")
            st.code(", ".join([str(c) for c in sorted(cups_en_dict)]))

            st.markdown("""
            <div style="background:#0d3d17; border:1px solid #2e7d32; border-radius:10px; padding:16px;">
                <p style="color:#a5d6a7; font-weight:700; margin:0 0 6px 0;">✅ Solución: Carga la Nota Técnica</p>
                <p style="color:#c8e6c9; font-size:0.82rem; margin:0;">
                    Sube el archivo <strong>"NOTA TECNICA AMBULATORIA PGP CARDIO.xlsx"</strong> en el panel izquierdo.
                    El sistema leerá la columna <code>Cups Homologo</code> y construirá el diccionario correcto
                    con los códigos reales del PGP.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # No continuar si no hay intersección
        if len(interseccion) == 0:
            return

    # ── PROCESAMIENTO ──
    df, fecha_col, aseg_col, cod_col, id_col = procesar_ghips(df_raw, cups_dict)

    # Log del procesamiento
    with st.expander("🔍 Log de procesamiento", expanded=False):
        st.markdown(f"- **Filas originales:** {len(df_raw):,}")
        # Contar SURA
        aseg_col_tmp = None
        for c in df_raw.columns:
            if "aseguradora" in c.lower():
                aseg_col_tmp = c
                break
        if aseg_col_tmp:
            n_sura = (df_raw[aseg_col_tmp] == 'EPS  SURAMERICANA S.A').sum()
            st.markdown(f"- **Filas EPS SURAMERICANA S.A:** {n_sura:,}")
        st.markdown(f"- **Filas después de filtro CUPS PGP:** {len(df):,}")
        st.markdown(f"- **CUPS homologados en Nota Técnica:** {len(cups_dict)}")
        st.markdown(f"- **Columna fecha:** `{fecha_col}`")
        st.markdown(f"- **Columna Aseguradora:** `{aseg_col}`")
        st.markdown(f"- **Columna vCodActividad:** `{cod_col}`")
        st.markdown(f"- **Columna Identificacion:** `{id_col}`")
        if not usando_respaldo and df_notatec_raw is not None:
            st.markdown(f"- **Fuente CUPS:** ✅ Nota Técnica cargada ({len(cups_dict)} códigos)")
        else:
            st.markdown(f"- **Fuente CUPS:** ⚠️ Dict de respaldo ({len(cups_dict)} códigos de ejemplo)")

    if df.empty:
        st.warning("⚠️ Sin registros después del procesamiento.")
        if usando_respaldo:
            st.markdown("""
            <div style="background:#3d2a00; border:1px solid #ff8f00; border-radius:10px; padding:16px;">
                <p style="color:#ffd54f; font-weight:700;">👉 Carga la Nota Técnica PGP Cardio (.xlsx) para usar los CUPS Homologo reales.</p>
            </div>
            """, unsafe_allow_html=True)
        return

    # ── FILTROS SIDEBAR ──
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Filtros de Fecha")
    fecha_modo = st.sidebar.radio("Filtrar por", ["Mes", "Año", "Rango"], horizontal=True)

    if fecha_col and fecha_col in df.columns and df[fecha_col].notna().any():
        min_fecha = df[fecha_col].min()
        max_fecha = df[fecha_col].max()

        if fecha_modo == "Mes":
            meses_disp = sorted(df[fecha_col].dt.to_period("M").dropna().unique().astype(str).tolist(), reverse=True)
            sel_mes = st.sidebar.multiselect("Mes(es)", meses_disp, default=meses_disp[:1])
            if sel_mes:
                df = df[df[fecha_col].dt.to_period("M").astype(str).isin(sel_mes)]
        elif fecha_modo == "Año":
            anios = sorted(df[fecha_col].dt.year.dropna().unique().astype(int).tolist(), reverse=True)
            sel_anio = st.sidebar.multiselect("Año(s)", anios, default=[anios[0]] if anios else [])
            if sel_anio:
                df = df[df[fecha_col].dt.year.isin(sel_anio)]
        else:
            f_ini = st.sidebar.date_input("Desde", min_fecha.date() if not pd.isna(min_fecha) else datetime.today())
            f_fin = st.sidebar.date_input("Hasta", max_fecha.date() if not pd.isna(max_fecha) else datetime.today())
            df = df[(df[fecha_col].dt.date >= f_ini) & (df[fecha_col].dt.date <= f_fin)]
    else:
        st.sidebar.info("Sin columna de fecha detectada")

    st.sidebar.markdown("### 🏥 Tipo de Procedimiento")
    tipos_disp = sorted(df["tipo"].dropna().unique().tolist()) if "tipo" in df.columns else []
    sel_tipo = st.sidebar.multiselect("Tipo(s)", tipos_disp, default=tipos_disp)
    if sel_tipo and "tipo" in df.columns:
        df = df[df["tipo"].isin(sel_tipo)]

    st.sidebar.markdown("### 🔎 Filtro por CUPS")
    descripciones_disp = sorted(df["descripcion"].dropna().unique().tolist()) if "descripcion" in df.columns else []
    sel_desc = st.sidebar.multiselect("Procedimiento(s)", descripciones_disp, default=[])
    if sel_desc and "descripcion" in df.columns:
        df = df[df["descripcion"].isin(sel_desc)]

    if df.empty:
        st.warning("⚠️ Sin datos para los filtros seleccionados.")
        return

    # ── KPIs ──
    total_valor = df["valor"].sum() if "valor" in df.columns else 0
    total_cups = len(df)
    total_pacientes = df[id_col].nunique() if id_col and id_col in df.columns else 0
    tipos_unicos = df["tipo"].nunique() if "tipo" in df.columns else 0
    cups_unicos = df[cod_col].nunique() if cod_col and cod_col in df.columns else 0

    st.markdown("<div class='section-title'>📊 Totales del Período</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👥 Pacientes", fmt_num(total_pacientes))
    c2.metric("💰 Valor Total", fmt_money(total_valor))
    c3.metric("🧾 Total CUPS", fmt_num(total_cups))
    c4.metric("🏷️ Tipos", fmt_num(tipos_unicos))
    c5.metric("📋 CUPS Dif.", fmt_num(cups_unicos))

    if usando_respaldo:
        st.markdown("""
        <div style="background:#3d2a00; border:1px solid #ff8f00; border-radius:8px; padding:10px 14px; margin-bottom:16px;">
            <span style="color:#ffd54f; font-size:0.8rem;">⚠️ Usando CUPS de respaldo. Carga la Nota Técnica para datos reales.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── GRÁFICAS ──
    st.markdown("<div class='section-title'>📈 Visualizaciones</div>", unsafe_allow_html=True)
    gcol1, gcol2 = st.columns(2)

    with gcol1:
        if "tipo" in df.columns and "valor" in df.columns:
            df_tipo = df.groupby("tipo")["valor"].sum().reset_index().sort_values("valor", ascending=False)
            fig1 = px.bar(
                df_tipo, x="tipo", y="valor", color="tipo",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                title="💰 Valor por Tipo",
                template="plotly_dark",
            )
            fig1.update_traces(hovertemplate="<b>%{x}</b><br>Valor: $%{y:,.0f}<extra></extra>")
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,17,23,0.8)",
                showlegend=False, title_font_color="#7ecbf7", xaxis_tickangle=-30,
            )
            st.plotly_chart(fig1, use_container_width=True)

    with gcol2:
        if "tipo" in df.columns:
            df_donut = df.groupby("tipo").size().reset_index(name="cantidad")
            fig2 = px.pie(
                df_donut, names="tipo", values="cantidad", hole=0.5,
                color_discrete_sequence=px.colors.sequential.Blues_r,
                title="🧾 Distribución CUPS por Tipo", template="plotly_dark",
            )
            fig2.update_traces(hovertemplate="<b>%{label}</b><br>CUPS: %{value}<br>%{percent}<extra></extra>")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font_color="#7ecbf7")
            st.plotly_chart(fig2, use_container_width=True)

    if "descripcion" in df.columns and "valor" in df.columns:
        df_top = df.groupby("descripcion").agg(total_valor=("valor", "sum"), conteo=("valor", "count")).reset_index().sort_values("total_valor", ascending=True).tail(10)
        fig_top = px.bar(
            df_top, x="total_valor", y="descripcion", orientation="h",
            color="total_valor", color_continuous_scale=px.colors.sequential.Blues,
            title="🏆 Top 10 Procedimientos por Valor", template="plotly_dark",
        )
        fig_top.update_traces(hovertemplate="<b>%{y}</b><br>Valor: $%{x:,.0f}<extra></extra>")
        fig_top.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,17,23,0.8)",
            showlegend=False, title_font_color="#7ecbf7", coloraxis_showscale=False,
        )
        st.plotly_chart(fig_top, use_container_width=True)

    if fecha_col and fecha_col in df.columns and df[fecha_col].notna().any():
        df["_mes"] = df[fecha_col].dt.to_period("M").astype(str)
        df_evol = df.groupby("_mes").agg(total_val=("valor", "sum"), total_cups=("valor", "count")).reset_index().sort_values("_mes")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_evol["_mes"], y=df_evol["total_val"], name="Valor ($)",
            marker_color="#1565c0", hovertemplate="<b>%{x}</b><br>Valor: $%{y:,.0f}<extra></extra>",
        ))
        fig3.add_trace(go.Scatter(
            x=df_evol["_mes"], y=df_evol["total_cups"], name="N° CUPS", yaxis="y2",
            line=dict(color="#7ecbf7", width=2.5), mode="lines+markers",
            hovertemplate="<b>%{x}</b><br>CUPS: %{y}<extra></extra>",
        ))
        fig3.update_layout(
            title="📅 Evolución Mensual", template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,17,23,0.8)",
            title_font_color="#7ecbf7",
            yaxis=dict(title="Valor ($)", tickformat="$,.0f"),
            yaxis2=dict(title="N° CUPS", overlaying="y", side="right", showgrid=False),
            legend=dict(bgcolor="rgba(0,0,0,0.3)"), hovermode="x unified",
        )
        st.plotly_chart(fig3, use_container_width=True)
        df.drop(columns=["_mes"], inplace=True, errors="ignore")

    st.markdown("---")

    # ── ALERTAS TOPES ──
    st.markdown("<div class='section-title'>🚦 Control de Topes por CUPS</div>", unsafe_allow_html=True)
    grouped = agrupar_por_cups(df.copy(), fecha_col, id_col, cod_col)

    def clasificar(pct):
        if pct >= 90: return "🔴 MÁS CRÍTICO"
        elif pct >= 70: return "🟡 ALERTA"
        else: return "🟢 NORMAL"

    grouped["estado"] = grouped["porcentaje_tope"].apply(clasificar)

    n_critico = (grouped["porcentaje_tope"] >= 90).sum()
    n_alerta = ((grouped["porcentaje_tope"] >= 70) & (grouped["porcentaje_tope"] < 90)).sum()
    n_ok = (grouped["porcentaje_tope"] < 70).sum()

    ac1, ac2, ac3 = st.columns(3)
    ac1.metric("🔴 Crítico (≥90%)", int(n_critico))
    ac2.metric("🟡 Alerta (70-89%)", int(n_alerta))
    ac3.metric("🟢 Normal (<70%)", int(n_ok))

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(grouped["porcentaje_tope"].max()) if not grouped.empty else 0,
        title={"text": "% Tope Máximo", "font": {"color": "#7ecbf7"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#7ecbf7"},
            "bar": {"color": "#1565c0"},
            "steps": [
                {"range": [0, 70], "color": "#0d3d17"},
                {"range": [70, 90], "color": "#4a3200"},
                {"range": [90, 100], "color": "#3d0a0a"},
            ],
            "threshold": {"line": {"color": "#ff1744", "width": 3}, "thickness": 0.75, "value": 90},
        },
        number={"suffix": "%", "font": {"color": "#ffffff"}},
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#7ecbf7", height=220)

    col_g, col_tbl = st.columns([1, 2])
    with col_g:
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col_tbl:
        st.markdown("**Top 5 CUPS con mayor % de tope:**")
        top_cols = []
        if cod_col and cod_col in grouped.columns:
            top_cols.append(cod_col)
        top_cols.extend(["descripcion", "conteo_cups", "tope_redondeado", "porcentaje_tope", "estado"])
        top_topes = grouped.nlargest(5, "porcentaje_tope")[top_cols]
        rename_top = {"descripcion": "Descripción", "conteo_cups": "Realizados", "tope_redondeado": "Tope", "porcentaje_tope": "% Tope", "estado": "Estado"}
        if cod_col and cod_col in top_topes.columns:
            rename_top[cod_col] = "Código CUPS"
        st.dataframe(top_topes.rename(columns=rename_top), use_container_width=True, hide_index=True)

    with st.expander("📋 Detalle completo de topes (Resumen Mensual)"):
        show_cols = []
        if cod_col and cod_col in grouped.columns:
            show_cols.append(cod_col)
        for c in ["descripcion", "tipo", "Mes", "valor_unitario", "total_valor", "conteo_cups", "cantidad_usuarios_diferentes", "tope_redondeado", "porcentaje_tope", "estado"]:
            if c in grouped.columns:
                show_cols.append(c)
        df_show = grouped[show_cols].copy()
        rename_map = {
            "descripcion": "Descripción", "tipo": "Tipo", "Mes": "Mes",
            "valor_unitario": "Valor Unit.", "total_valor": "Valor Total",
            "conteo_cups": "CUPS Realiz.", "cantidad_usuarios_diferentes": "Pac. Únicos",
            "tope_redondeado": "Tope Mensual", "porcentaje_tope": "% del Tope", "estado": "Estado",
        }
        if cod_col and cod_col in df_show.columns:
            rename_map[cod_col] = "Código CUPS"
        df_show.rename(columns=rename_map, inplace=True)

        def colorear(row):
            pct = row.get("% del Tope", 0)
            if pct >= 90: return ["background-color: #3d0a0a"] * len(row)
            elif pct >= 70: return ["background-color: #3d2a00"] * len(row)
            return [""] * len(row)

        st.dataframe(df_show.style.apply(colorear, axis=1), use_container_width=True, hide_index=True)
        csv_buf = io.StringIO()
        df_show.to_csv(csv_buf, index=False, encoding="utf-8-sig")
        st.download_button("⬇️ Descargar Resumen Mensual (.csv)", csv_buf.getvalue(), file_name="resumen_mensual_cups.csv", mime="text/csv")

    st.markdown("---")

    # ── LISTADO COMPLETO ──
    st.markdown("<div class='section-title'>🔍 Listado Completo de Registros</div>", unsafe_allow_html=True)
    buscar_cups = st.text_input("🔎 Buscar por descripción, código, tipo o identificación", placeholder="ej: ecocardiograma, 890902...")

    df_listado = df.copy()
    if buscar_cups:
        mask = (
            df_listado["descripcion"].str.contains(buscar_cups, case=False, na=False) |
            df_listado["tipo"].str.contains(buscar_cups, case=False, na=False)
        )
        if cod_col and cod_col in df_listado.columns:
            mask = mask | df_listado[cod_col].astype(str).str.contains(buscar_cups, case=False, na=False)
        if id_col and id_col in df_listado.columns:
            mask = mask | df_listado[id_col].astype(str).str.contains(buscar_cups, case=False, na=False)
        df_listado = df_listado[mask]

    if not df_listado.empty:
        cols_mostrar = []
        if fecha_col and fecha_col in df_listado.columns:
            cols_mostrar.append(fecha_col)
        if id_col and id_col in df_listado.columns:
            cols_mostrar.append(id_col)
        if cod_col and cod_col in df_listado.columns:
            cols_mostrar.append(cod_col)
        for c in ["descripcion", "codalias", "tipo", "valor", "tope"]:
            if c in df_listado.columns:
                cols_mostrar.append(c)

        st.markdown(f"Mostrando **{len(df_listado):,}** de **{len(df):,}** registros")
        st.dataframe(df_listado[cols_mostrar].head(1000), use_container_width=True, hide_index=True)
        if len(df_listado) > 1000:
            st.info(f"ℹ️ Mostrando primeros 1,000 de {len(df_listado):,}")

        csv_buf2 = io.StringIO()
        df_listado[cols_mostrar].to_csv(csv_buf2, index=False, encoding="utf-8-sig")
        st.download_button("⬇️ Descargar Listado Completo (.csv)", csv_buf2.getvalue(), file_name="listado_completo_cups_pgp.csv", mime="text/csv")
    else:
        st.info("Sin registros para el filtro aplicado.")


# ─────────────────────────────────────────────
# TAB 2: REPORTES SALUDWEB
# ─────────────────────────────────────────────
def tab_saludweb():
    st.markdown("""
    <div class="badge-pending">
        <div style="font-size:3rem;">🚧</div>
        <h3 style="color:#7ecbf7; margin:12px 0 8px 0;">Pestaña en Desarrollo</h3>
        <p style="color:#9eb8d4; font-size:0.9rem;">Reportes SaludWeb — Próximamente disponible</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 3: INDICADORES
# ─────────────────────────────────────────────
def tab_indicadores():
    st.markdown("""
    <div class="warning-hallucinated">
        ⚠️ <strong>ADVERTENCIA:</strong> Los datos de esta sección son <strong>ilustrativos</strong> para demostración.
        No representan información real. Pendiente de integración con fuentes de datos reales.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📊 Indicadores PGP Cardiovascular — Demo</div>", unsafe_allow_html=True)

    indicadores = [
        {"codigo": "1.8.C", "nombre": "Oportunidad procedimientos diagnósticos", "descripcion": "Procedimientos ambulatorios realizados en ≤30 días desde la autorización", "numerador": 412, "denominador": 450, "meta": "> 90%", "periodicidad": "Mensual", "responsable": "EPS", "agrupador": "Electrofisiología / Hemodinamia / Cx"},
        {"codigo": "1.8.C", "nombre": "Oportunidad consulta especialista", "descripcion": "Consultas especializadas realizadas antes de 30 días", "numerador": 387, "denominador": 400, "meta": "> 95%", "periodicidad": "Mensual", "responsable": "EPS", "agrupador": "Consulta Especializada"},
        {"codigo": "1.8.R", "nombre": "Rehospitalizaciones", "descripcion": "% rehospitalizaciones ≤15 días post-alta", "numerador": 8, "denominador": 320, "meta": "< 5%", "periodicidad": "Mensual", "responsable": "IPS", "agrupador": "Hospitalización"},
        {"codigo": "1.8.R", "nombre": "Reintervenciones quirúrgicas", "descripcion": "Pacientes reintervenidos en Cx cardiovascular ≤30 días", "numerador": 3, "denominador": 95, "meta": "< 10", "periodicidad": "Mensual", "responsable": "IPS", "agrupador": "Cx Cardiovascular"},
        {"codigo": "1.8.G", "nombre": "% Ejecución nota técnica", "descripcion": "Valor ejecutado vs. valor proyectado del mes", "numerador": 98500000, "denominador": 100000000, "meta": "95–105%", "periodicidad": "Mensual", "responsable": "EPS", "agrupador": "Financiero"},
    ]

    for ind in indicadores:
        pct = round(ind["numerador"] / ind["denominador"] * 100, 1) if ind["denominador"] > 0 else 0
        if ">" in ind["meta"]:
            meta_val = float(ind["meta"].replace(">", "").replace("%", "").strip())
            ok = pct >= meta_val
        elif "<" in ind["meta"] and "%" in ind["meta"]:
            meta_val = float(ind["meta"].replace("<", "").replace("%", "").strip())
            ok = pct < meta_val
        else:
            ok = True
        color = "#2e7d32" if ok else "#c62828"
        icono = "✅" if ok else "❌"

        with st.expander(f"{icono} [{ind['codigo']}] {ind['nombre']} — **{pct}%**"):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"**Descripción:** {ind['descripcion']}")
                st.markdown(f"**Agrupador:** {ind['agrupador']} | **Responsable:** {ind['responsable']}")
            with c2:
                st.metric("Meta", ind["meta"])
            with c3:
                st.metric("Resultado", f"{pct}%", delta=f"{'✅ Cumple' if ok else '❌ No cumple'}")
            fig_bar = go.Figure(go.Bar(x=[pct], y=[""], orientation="h", marker_color=color))
            fig_bar.update_layout(xaxis=dict(range=[0, max(110, pct + 5)], ticksuffix="%"), height=50, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)
            col_n, col_d = st.columns(2)
            col_n.metric("Numerador", fmt_num(ind["numerador"]))
            col_d.metric("Denominador", fmt_num(ind["denominador"]))

    st.markdown("""
    <div class="warning-hallucinated">
        ⚠️ <strong>DATOS SINTÉTICOS:</strong> Integración con fuentes reales pendiente.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 4: INFORMACIÓN
# ─────────────────────────────────────────────
def tab_info():
    st.markdown("<div class='section-title'>ℹ️ Información del Sistema</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style="background:#1a1f2e; border:1px solid #2d4a6e; border-radius:12px; padding:24px; margin-bottom:16px;">
            <h3 style="color:#7ecbf7; margin-top:0;">🫀 ¿Para qué sirve?</h3>
            <p style="color:#d0e4f7; font-size:0.9rem; line-height:1.7;">
                Monitoreo y análisis del <strong>Programa de Gestión de Patología Cardiovascular</strong> de <strong>EPS SURA</strong>.
                Control de topes CUPS, seguimiento de facturación e indicadores de calidad.
            </p>
            <hr style="border-color:#2d4a6e;">
            <h4 style="color:#7ecbf7;">📌 Módulos</h4>
            <ul style="color:#d0e4f7; font-size:0.88rem; line-height:1.9;">
                <li><strong>Reportes GHIPS:</strong> Facturación grabada, topes CUPS, listado de códigos.</li>
                <li><strong>Reportes SaludWeb:</strong> 🚧 En desarrollo.</li>
                <li><strong>Indicadores:</strong> Oportunidad, rehospitalizaciones, ejecución financiera.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#1a1f2e; border:1px solid #2d4a6e; border-radius:12px; padding:24px;">
            <h4 style="color:#7ecbf7; margin-top:0;">📁 Archivos requeridos</h4>
            <table style="width:100%; border-collapse:collapse; font-size:0.83rem; color:#d0e4f7;">
                <tr style="border-bottom:1px solid #2d4a6e; color:#7ecbf7;">
                    <th style="padding:8px; text-align:left;">Archivo</th>
                    <th style="padding:8px; text-align:left;">Descripción</th>
                </tr>
                <tr style="border-bottom:1px solid #1a2744;">
                    <td style="padding:8px;"><code>NOTA TECNICA...xlsx</code></td>
                    <td style="padding:8px;">Excel con hoja "Procedimientos ", columna "Cups Homologo", "Tarifa", "FRENCUENCIA MES"</td>
                </tr>
                <tr style="border-bottom:1px solid #1a2744;">
                    <td style="padding:8px;"><code>Facturación (.csv/.xlsx)</code></td>
                    <td style="padding:8px;">Archivo GHIPS con columnas: fechaActividad, Aseguradora (= 'EPS  SURAMERICANA S.A'), vCodActividad, Identificacion</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#1a1f2e; border:1px solid #2d4a6e; border-radius:12px; padding:24px; text-align:center;">
            <div style="font-size:2.5rem;">👨‍💻</div>
            <h4 style="color:#7ecbf7; margin:10px 0 4px 0;">Equipo de Datos</h4>
            <p style="color:#9eb8d4; font-size:0.80rem;"Antonio Narvaez</p>
            <hr style="border-color:#2d4a6e; margin:16px 0;">
            <p style="color:#7ecbf7; font-size:0.78rem;">Analista de Datos</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#1a1f2e; border:1px solid #2d4a6e; border-radius:12px; padding:24px;">
            <h4 style="color:#7ecbf7; margin-top:0;">📋 Versión</h4>
            <table style="width:100%; font-size:0.82rem; color:#d0e4f7;">
                <tr><td style="padding:5px; color:#7ecbf7;">Versión</td><td style="padding:5px;">1.2.0</td></tr>
                <tr><td style="padding:5px; color:#7ecbf7;">Framework</td><td style="padding:5px;">Streamlit</td></tr>
                <tr><td style="padding:5px; color:#7ecbf7;">Motor</td><td style="padding:5px;">Pandas / Plotly</td></tr>
                <tr><td style="padding:5px; color:#7ecbf7;">Licencia</td><td style="padding:5px;">Interno CLINICA LA ASUNCION</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_screen()
        return

    render_membrete()

    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:10px 0 4px 0;">
            <span style="font-size:1.6rem;">🫀</span>
            <p style="color:#7ecbf7; font-weight:700; font-size:0.88rem; margin:4px 0 0 0;">PGP Cardiovascular</p>
            <p style="color:#6a8aaa; font-size:0.72rem; margin:2px 0 0 0;">EPS SURA</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### ⚙️ Panel de Carga")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Reportes GHIPS", "🌐 Reportes SaludWeb", "📊 Indicadores", "ℹ️ Información",
    ])
    with tab1: tab_ghips()
    with tab2: tab_saludweb()
    with tab3: tab_indicadores()
    with tab4: tab_info()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
    st.sidebar.markdown("""
    <div style="color:#4a6a8a; font-size:0.70rem; text-align:center; padding-top:10px;">
        PGP Cardio v1.2 · EPS SURA
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()