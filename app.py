import streamlit as st
import google.generativeai as genai
import json
import re

st.set_page_config(
    page_title="ARIA Membresías",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --canary: #F5E642;
    --canary-dark: #D4C800;
    --ink: #0F0F0F;
    --ink-soft: #2A2A2A;
    --surface: #F9F8F2;
    --surface-2: #EFEDE3;
    --surface-3: #E4E1D4;
    --accent: #1A1A2E;
    --green: #1DB954;
    --red: #E53E3E;
    --muted: #6B6860;
    --border: #D8D5C8;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--surface) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: 3px solid var(--canary);
}

[data-testid="stSidebar"] * {
    color: #F0EDDE !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--canary) !important;
}

.stCheckbox label {
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] .stCheckbox label {
    color: #D0CDBE !important;
}

[data-testid="stSidebar"] .stCheckbox label p {
    color: #D0CDBE !important;
}

.main-header {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--ink);
    line-height: 1.05;
    letter-spacing: -0.03em;
}

.main-header span {
    background: var(--canary);
    padding: 0 6px;
    display: inline-block;
}

.subtitle {
    font-size: 1rem;
    color: var(--muted);
    font-weight: 300;
    margin-top: 0.4rem;
    margin-bottom: 1.5rem;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
    margin-top: 1.2rem;
}

.filter-group {
    border-top: 1px solid #2E2E2E;
    padding-top: 0.7rem;
    margin-top: 0.7rem;
}

.result-card {
    background: white;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--canary);
}

.result-card:hover {
    border-color: var(--canary-dark);
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.2rem;
}

.card-url {
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 0.8rem;
    word-break: break-all;
}

.card-url a {
    color: #1a73e8;
    text-decoration: none;
}

.card-section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 0.25rem;
    margin-top: 0.7rem;
}

.card-text {
    font-size: 0.88rem;
    color: var(--ink-soft);
    line-height: 1.55;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.4rem;
}

.badge {
    font-size: 0.72rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'DM Sans', sans-serif;
}

.badge-type-academica { background: #EBF8FF; color: #1A6B99; border: 1px solid #BEE3F8; }
.badge-type-profesional { background: #F0FFF4; color: #22543D; border: 1px solid #9AE6B4; }
.badge-type-comercial { background: #FFFBEB; color: #7B4F12; border: 1px solid #F6D860; }
.badge-type-comunidad { background: #FAF5FF; color: #553C9A; border: 1px solid #D6BCFA; }
.badge-region { background: #F7FAFC; color: #2D3748; border: 1px solid #CBD5E0; }
.badge-access { background: #F0FFF4; color: #276749; border: 1px solid #9AE6B4; }

.stars {
    font-size: 1rem;
    color: var(--canary-dark);
    letter-spacing: 1px;
}

.stars-empty { color: #D8D5C8; }

.search-btn {
    background: var(--canary) !important;
    color: var(--ink) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    padding: 0.6rem 2rem !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    width: 100% !important;
    margin-top: 1rem !important;
}

.stButton > button {
    background: var(--canary) !important;
    color: var(--ink) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    border: 2px solid var(--ink) !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.15s !important;
}

.stButton > button:hover {
    background: var(--ink) !important;
    color: var(--canary) !important;
}

.divider-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem 0 1rem;
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.divider-label::before,
.divider-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.status-bar {
    background: var(--ink);
    color: var(--canary);
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    letter-spacing: 0.06em;
    margin-bottom: 1.2rem;
    display: inline-block;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--muted);
    font-size: 0.95rem;
}

.empty-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    display: block;
}

.filter-counter {
    background: var(--canary);
    color: var(--ink);
    font-size: 0.65rem;
    font-weight: 700;
    padding: 1px 7px;
    border-radius: 10px;
    margin-left: 6px;
    vertical-align: middle;
}

.verified-badge {
    display: inline-block;
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
}
.verified-ok { background: #F0FFF4; color: #276749; border: 1px solid #9AE6B4; }
.verified-no { background: #FFF5F5; color: #9B2C2C; border: 1px solid #FEB2B2; }
.verified-unk { background: #F7FAFC; color: #4A5568; border: 1px solid #CBD5E0; }

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #D0CDBE !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 ARIA\n### Membresías Gratuitas")
    st.markdown("---")

    api_key = st.text_input("API Key Gemini", type="password", placeholder="AIza...")

    st.markdown('<div class="section-label">Número de resultados</div>', unsafe_allow_html=True)
    num_results = st.slider("", min_value=3, max_value=20, value=8, label_visibility="collapsed")

    # ── FILTROS SIEMPRE VISIBLES ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌎 Región prioritaria")
    with st.container():
        reg_norteamerica = st.checkbox("Norteamérica (EE.UU. / Canadá)", value=True)
        reg_europa = st.checkbox("Europa Occidental, Central y Norte", value=True)
        reg_latam = st.checkbox("América Latina y el Caribe", value=True)

    st.markdown("---")
    st.markdown("### 📚 Tipo de membresía")
    with st.container():
        tipo_academica = st.checkbox("Académica / Institucional", value=True)
        tipo_profesional = st.checkbox("Profesiones y Oficios", value=True)
        tipo_comercial = st.checkbox("Comercial / Herramientas", value=True)
        tipo_comunidad = st.checkbox("Comunidad y Redes", value=True)

    st.markdown("---")
    st.markdown("### 👤 Audiencia objetivo")
    with st.container():
        aud_instituciones = st.checkbox("Instituciones / Universidades", value=True)
        aud_investigadores = st.checkbox("Investigadores / Académicos", value=True)
        aud_docentes = st.checkbox("Docentes / Profesores", value=True)
        aud_posgrado = st.checkbox("Estudiantes de Posgrado", value=True)
        aud_licenciatura = st.checkbox("Estudiantes de Licenciatura", value=True)
        aud_directivos = st.checkbox("Directivos / Administradores", value=True)
        aud_bibliotecarios = st.checkbox("Bibliotecarios / Gestores", value=True)

    st.markdown("---")
    st.markdown("### 🔓 Condición de gratuidad")
    with st.container():
        cond_total = st.checkbox("Gratuidad total", value=True)
        cond_edu = st.checkbox("Student Tier (.edu / dominio univ.)", value=True)
        cond_grant = st.checkbox("Grant-Based Free Tier", value=True)
        cond_sandbox = st.checkbox("Institutional Sandbox", value=True)
        cond_alumni = st.checkbox("Año de Gracia / Alumni Launchpad", value=True)
        cond_cert = st.checkbox("Gratuidad por Certificación", value=True)
        cond_beta = st.checkbox("Acceso Beta Tester", value=True)
        cond_prueba = st.checkbox("Prueba Institucional 12 meses", value=True)

    st.markdown("---")
    st.markdown("### 🔐 Método de acceso")
    with st.container():
        acc_sso = st.checkbox("SSO Institucional / IP Whitelist", value=True)
        acc_edu = st.checkbox("Dominio .edu verificado", value=True)
        acc_invitacion = st.checkbox("Invitación / Aprobación previa", value=True)
        acc_personal = st.checkbox("Cuenta personal validada", value=True)

# ── Main content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    ARIA<br><span>Membresías</span><br>Gratuitas
</div>
<div class="subtitle">Inteligencia de recursos académicos y profesionales — acceso sin costo</div>
""", unsafe_allow_html=True)

topic_col, btn_col = st.columns([4, 1])
with topic_col:
    topic = st.text_input(
        "Tema o dominio de búsqueda",
        placeholder="Ej: software de análisis estadístico, gestión de referencias, diseño curricular...",
        label_visibility="visible"
    )
with btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    buscar = st.button("🔍 Buscar", use_container_width=True)


def build_filters_summary():
    regiones, tipos, audiencias, condiciones, accesos = [], [], [], [], []
    if reg_norteamerica: regiones.append("Norteamérica (EE.UU. y Canadá)")
    if reg_europa: regiones.append("Europa Occidental, Central y Norte")
    if reg_latam: regiones.append("América Latina y el Caribe")
    if tipo_academica: tipos.append("Académica/Institucional")
    if tipo_profesional: tipos.append("Profesiones y Oficios")
    if tipo_comercial: tipos.append("Comercial/Herramientas")
    if tipo_comunidad: tipos.append("Comunidad y Redes")
    if aud_instituciones: audiencias.append("Instituciones y Universidades")
    if aud_investigadores: audiencias.append("Investigadores y Académicos")
    if aud_docentes: audiencias.append("Docentes y Profesores")
    if aud_posgrado: audiencias.append("Estudiantes de Posgrado")
    if aud_licenciatura: audiencias.append("Estudiantes de Licenciatura")
    if aud_directivos: audiencias.append("Directivos y Administradores Universitarios")
    if aud_bibliotecarios: audiencias.append("Bibliotecarios y Gestores de Repositorios")
    if cond_total: condiciones.append("Gratuidad total")
    if cond_edu: condiciones.append("Student Tier (.edu o dominio universitario)")
    if cond_grant: condiciones.append("Grant-Based Free Tier")
    if cond_sandbox: condiciones.append("Institutional Sandbox")
    if cond_alumni: condiciones.append("Año de Gracia / Alumni Launchpad")
    if cond_cert: condiciones.append("Gratuidad por certificación o cursos completados")
    if cond_beta: condiciones.append("Acceso Beta Tester")
    if cond_prueba: condiciones.append("Prueba institucional de 12 meses")
    if acc_sso: accesos.append("SSO Institucional o IP Whitelisting")
    if acc_edu: accesos.append("Dominio .edu verificado")
    if acc_invitacion: accesos.append("Invitación o aprobación previa")
    if acc_personal: accesos.append("Cuenta personal con validación de perfil")
    return regiones, tipos, audiencias, condiciones, accesos


def build_prompt(topic, regiones, tipos, audiencias, condiciones, accesos, n):
    return f"""Eres un agente especializado en inteligencia de recursos académicos y profesionales. Tu función es identificar, evaluar y catalogar plataformas web que ofrecen membresías, suscripciones o accesos institucionales COMPLETAMENTE GRATUITOS para el sector educativo y de investigación.

TEMA DE BÚSQUEDA: {topic if topic else "herramientas y recursos académicos generales"}

OBJETIVO: Encuentra exactamente {n} páginas web que ofrezcan membresías académicas o institucionales GRATUITAS (sin costo alguno, periodo mínimo 12 meses o 1 año) para el tema indicado.

REGIONES PRIORITARIAS (busca SOLO en estas):
{chr(10).join(f"- {r}" for r in regiones) if regiones else "- Sin filtro regional (busca en todas)"}

TIPOS DE MEMBRESÍA A BUSCAR:
{chr(10).join(f"- {t}" for t in tipos) if tipos else "- Todos los tipos"}

AUDIENCIAS OBJETIVO:
{chr(10).join(f"- {a}" for a in audiencias) if audiencias else "- Todas las audiencias"}

CONDICIONES DE GRATUIDAD ACEPTABLES (al menos una debe cumplirse):
{chr(10).join(f"- {c}" for c in condiciones) if condiciones else "- Cualquier condición de gratuidad"}

MÉTODOS DE ACCESO ACEPTABLES:
{chr(10).join(f"- {a}" for a in accesos) if accesos else "- Cualquier método de acceso"}

REGLAS OBLIGATORIAS:
1. Solo membresías COMPLETAMENTE GRATUITAS. Excluye cualquier opción de pago.
2. El período de acceso gratuito debe ser de 12 meses o 1 año como mínimo.
3. Excluye plataformas de: Asia Oriental/Pacífico, Asia del Sur/Central, África, Medio Oriente.
4. Excluye organismos multilaterales: ONU, UNESCO, FMI, BM, OCDE, OMS, OEA y equivalentes.
5. Prioriza plataformas con poca visibilidad sobre las ampliamente conocidas.
6. Nunca inventes URLs. Si no puedes verificar un dato, usa "Sin verificar".
7. No incluyas contenido detrás de login previo que no sea descubrible públicamente.
8. Ordena los resultados de mayor a menor puntuación (5 a 1).

FORMATO DE RESPUESTA: Responde ÚNICAMENTE con un array JSON válido, sin texto adicional, sin bloques de código markdown, sin comillas extras. El array debe tener exactamente {n} objetos con esta estructura:

[
  {{
    "nombre": "Nombre oficial de la plataforma",
    "url": "https://url-directa-a-pagina-de-membresia.com",
    "para_quien_es_gratis": "Descripción exacta del perfil que califica (ej: investigadores con email .edu en instituciones acreditadas de EE.UU.)",
    "condicion_gratuidad": "Tipo específico de gratuidad que aplica",
    "metodo_acceso": "Método de acceso requerido",
    "beneficios": ["Beneficio concreto 1", "Beneficio concreto 2", "Beneficio concreto 3", "Beneficio concreto 4"],
    "tipo_membresia": "Académica|Profesional|Comercial|Comunidad",
    "region": "Norteamérica|Europa|América Latina|Global",
    "puntuacion": 4,
    "url_verificada": true,
    "duracion": "12 meses / 1 año / Indefinida mientras seas estudiante"
  }}
]"""


def render_stars(score):
    filled = "★" * score
    empty = "☆" * (5 - score)
    return f'<span class="stars">{filled}</span><span class="stars stars-empty">{empty}</span>'


def render_type_badge(tipo):
    tipo_lower = tipo.lower() if tipo else ""
    if "académic" in tipo_lower or "institucional" in tipo_lower:
        return f'<span class="badge badge-type-academica">{tipo}</span>'
    elif "profesion" in tipo_lower or "oficio" in tipo_lower:
        return f'<span class="badge badge-type-profesional">{tipo}</span>'
    elif "comercial" in tipo_lower or "herramienta" in tipo_lower:
        return f'<span class="badge badge-type-comercial">{tipo}</span>'
    else:
        return f'<span class="badge badge-type-comunidad">{tipo}</span>'


def render_results(results):
    for i, r in enumerate(results):
        score = r.get("puntuacion", 3)
        verified = r.get("url_verificada", None)
        if verified is True:
            ver_html = '<span class="verified-badge verified-ok">✓ URL verificada</span>'
        elif verified is False:
            ver_html = '<span class="verified-badge verified-no">⚠ Sin verificar</span>'
        else:
            ver_html = '<span class="verified-badge verified-unk">? Por verificar</span>'

        url = r.get("url", "#")
        nombre = r.get("nombre", "Sin nombre")
        beneficios = r.get("beneficios", [])
        bene_html = "".join(f"<li>{b}</li>" for b in beneficios)

        tipo_badge = render_type_badge(r.get("tipo_membresia", ""))
        region = r.get("region", "")
        condicion = r.get("condicion_gratuidad", "")
        metodo = r.get("metodo_acceso", "")
        para_quien = r.get("para_quien_es_gratis", "")
        duracion = r.get("duracion", "12 meses")

        st.markdown(f"""
        <div class="result-card">
            <div class="card-title">
                #{i+1} — {nombre}
                {ver_html}
            </div>
            <div class="card-url"><a href="{url}" target="_blank">{url}</a></div>
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:0.6rem;">
                {render_stars(score)}
                {tipo_badge}
                <span class="badge badge-region">{region}</span>
                <span class="badge badge-access">🕐 {duracion}</span>
            </div>
            <div class="card-section-title">Para quién es gratis</div>
            <div class="card-text">{para_quien}</div>
            <div class="card-section-title">Condición de gratuidad</div>
            <div class="card-text">{condicion}</div>
            <div class="card-section-title">Método de acceso</div>
            <div class="card-text">{metodo}</div>
            <div class="card-section-title">Beneficios principales</div>
            <div class="card-text"><ul style="margin:0; padding-left:1.2rem;">{bene_html}</ul></div>
        </div>
        """, unsafe_allow_html=True)


# ── Search execution ──────────────────────────────────────────────────────────
if buscar:
    if not api_key:
        st.error("Ingresa tu API Key de Gemini en el panel lateral.")
    else:
        regiones, tipos, audiencias, condiciones, accesos = build_filters_summary()
        if not regiones:
            st.warning("Selecciona al menos una región.")
        elif not condiciones:
            st.warning("Selecciona al menos una condición de gratuidad.")
        else:
            prompt = build_prompt(topic, regiones, tipos, audiencias, condiciones, accesos, num_results)
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")

                with st.spinner("Buscando membresías gratuitas..."):
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.3,
                            max_output_tokens=8192,
                        )
                    )

                raw = response.text.strip()
                raw = re.sub(r"```json\s*", "", raw)
                raw = re.sub(r"```\s*", "", raw)
                raw = raw.strip()

                try:
                    results = json.loads(raw)
                    if not isinstance(results, list):
                        results = [results]
                except json.JSONDecodeError:
                    match = re.search(r"\[.*\]", raw, re.DOTALL)
                    if match:
                        results = json.loads(match.group())
                    else:
                        st.error("Error al procesar la respuesta. Intenta de nuevo.")
                        st.code(raw[:500])
                        st.stop()

                st.markdown(f'<div class="status-bar">✦ {len(results)} membresías gratuitas encontradas</div>', unsafe_allow_html=True)
                render_results(results)

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-icon">◈</span>
        Configura los filtros en el panel lateral y escribe un tema para comenzar.<br>
        <span style="font-size:0.82rem; color:#9E9B90;">Los filtros siempre están visibles — ajústalos antes de cada búsqueda.</span>
    </div>
    """, unsafe_allow_html=True)
