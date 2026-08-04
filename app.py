"""
Passos Mágicos — Preditor de Risco de Defasagem
Streamlit App | PosTech Datathon Fase 5
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64
import plotly.graph_objects as go

# ── Configuração ───────────────────────────────────────────────────────────────
LOGO_PATH = "logo_passos_magicos.png"

st.set_page_config(
    page_title="Passos Mágicos • Risco de Defasagem",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def get_logo_base64(path: str):
    """Lê o arquivo da logo e devolve a string base64 para embutir em HTML."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


logo_b64 = get_logo_base64(LOGO_PATH)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #f8fafc; }

/* Header */
.hero {
    background: linear-gradient(135deg, #ffffff 0%, #eaf3fb 100%);
    border: 1px solid #d7e6f5;
    border-radius: 16px;
    padding: 2rem 2rem 1.8rem;
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(4,104,176,0.06) 0%, transparent 60%);
}
.hero h1 { color: #0468B0; font-size: 2rem; font-weight: 800; margin: 0 0 0.3rem; letter-spacing: -0.5px; }
.hero p  { color: #373435; opacity: 0.75; font-size: 0.95rem; margin: 0; }

/* Cards de resultado */
.result-card {
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    margin-bottom: 1rem;
    border: 2px solid transparent;
}
.card-alto   { background: linear-gradient(135deg, #fff0f0, #ffe4e4); border-color: #E84855; }
.card-medio  { background: linear-gradient(135deg, #fffbf0, #fff3d4); border-color: #F9A11B; }
.card-baixo  { background: linear-gradient(135deg, #f0fff8, #d4f7eb); border-color: #43AA8B; }

.result-emoji  { font-size: 3.5rem; line-height: 1; margin-bottom: 0.3rem; }
.result-label  { font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
                 letter-spacing: 1.5px; color: #666; margin-bottom: 0.2rem; }
.result-nivel  { font-size: 1.8rem; font-weight: 800; margin-bottom: 0.2rem; }
.result-prob   { font-size: 3.8rem; font-weight: 800; line-height: 1; }
.result-sub    { font-size: 0.8rem; color: #888; margin-top: 0.3rem; }
.result-rec    { background: rgba(255,255,255,0.7); border-radius: 10px; padding: 0.8rem 1rem;
                 font-size: 0.85rem; color: #444; margin-top: 1rem; text-align: left; }

/* Banner de resultado horizontal */
.result-banner {
    display: flex;
    align-items: center;
    gap: 1.8rem;
    border-radius: 16px;
    padding: 1.3rem 1.8rem;
    margin-bottom: 1.2rem;
    border: 2px solid transparent;
    flex-wrap: wrap;
}
.rb-left { display: flex; align-items: center; gap: 0.9rem; flex-shrink: 0; }
.rb-emoji { font-size: 2.8rem; line-height: 1; }
.rb-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
            letter-spacing: 1px; color: #666; }
.rb-nivel { font-size: 1.4rem; font-weight: 800; }
.rb-prob { font-size: 2.8rem; font-weight: 800; line-height: 1; flex-shrink: 0; }
.rb-prob-sub { font-size: 0.7rem; font-weight: 500; color: #888; margin-top: 0.15rem; }
.rb-rec { flex: 1 1 260px; font-size: 0.85rem; color: #444;
          background: rgba(255,255,255,0.65); border-radius: 10px; padding: 0.7rem 1rem; }
.rb-metrics { display: flex; gap: 0.7rem; flex-shrink: 0; align-items: stretch; }
.rb-metric { background: white; border-radius: 12px; padding: 0.6rem 1rem;
             text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.07); min-width: 92px; }
.rb-metric .val { font-size: 1.35rem; font-weight: 800; }
.rb-metric .lbl { font-size: 0.68rem; color: #888; font-weight: 500; margin-top: 0.1rem; }

/* Indicador bar */
.ind-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1rem 1.3rem 0.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.ind-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 2rem;
}
.ind-row { display: flex; align-items: center; margin-bottom: 0.9rem; gap: 0.7rem; }
.ind-label { font-size: 0.8rem; font-weight: 700; color: #334155; width: 40px; flex-shrink: 0; }
.ind-bar-wrap { flex: 1; background: #eef2f6; border-radius: 99px; height: 12px; }
.ind-bar { height: 12px; border-radius: 99px; transition: width 0.5s ease; }
.ind-val { font-size: 0.85rem; font-weight: 800; color: #1e293b; width: 32px; text-align: right; flex-shrink: 0; }

/* Badges Pedra */
.pedra-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.pedra-agata    { background:#fee2e2; color:#b91c1c; }
.pedra-quartzo  { background:#fef9c3; color:#854d0e; }
.pedra-topazio  { background:#dbeafe; color:#1e40af; }
.pedra-ametista { background:#f3e8ff; color:#7e22ce; }

/* Seção */
.section-title {
    font-size: 1rem; font-weight: 700; color: #1e293b;
    margin: 1.2rem 0 0.7rem; padding-left: 0.5rem;
    border-left: 3px solid #0468B0;
}

/* Sidebar */
section[data-testid="stSidebar"] { background: #1e293b !important; }
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] { }
section[data-testid="stSidebar"] h3 { color: #FBAE31 !important; font-size: 0.9rem !important; }

/* Logo na sidebar */
.sidebar-logo-wrap {
    background: #ffffff;
    border-radius: 14px;
    padding: 0.7rem;
    display: flex;
    justify-content: center;
    margin-bottom: 0.8rem;
}
.sidebar-logo-wrap img { width: 100px; height: 100px; object-fit: contain; }

/* Métrica simples */
.mini-metric {
    background: white;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.mini-metric .val { font-size: 1.6rem; font-weight: 800; }
.mini-metric .lbl { font-size: 0.72rem; color: #888; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── Carregar modelo ────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    if os.path.exists('modelo_risco_defasagem.pkl'):
        model    = joblib.load('modelo_risco_defasagem.pkl')
        features = joblib.load('features_modelo.pkl') if os.path.exists('features_modelo.pkl') else None
        return model, features
    return None, None

model, feature_names = load_model()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    if logo_b64:
        st.markdown(f"""
        <div class="sidebar-logo-wrap">
            <img src="data:image/png;base64,{logo_b64}" alt="Passos Mágicos">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 🌟 Passos Mágicos")

    st.markdown("##### Preencha os indicadores do aluno")
    st.markdown("---")

    st.markdown("**Desempenho**")
    IDA = st.slider("IDA — Desempenho Acadêmico", 0.0, 10.0, 6.0, 0.1)
    MAT = st.slider("Matemática",  0.0, 10.0, 6.0, 0.1)
    POR = st.slider("Português",   0.0, 10.0, 6.0, 0.1)

    st.markdown("**Engajamento & Comportamento**")
    IEG = st.slider("IEG — Engajamento",    0.0, 10.0, 7.0, 0.1)
    IPV = st.slider("IPV — Ponto de Virada", 0.0, 10.0, 7.0, 0.1)

    st.markdown("**Aspectos Pessoais**")
    IAA = st.slider("IAA — Autoavaliação",  0.0, 10.0, 7.0, 0.1)
    IPS = st.slider("IPS — Psicossocial",   0.0, 10.0, 6.5, 0.1)
    IPP = st.slider("IPP — Psicopedagógico",0.0, 10.0, 6.5, 0.1)

    st.markdown("**Adequação**")
    IAN = st.slider("IAN — Adequação de Nível", 0.0, 10.0, 6.5, 0.1)

    st.markdown("---")
    st.caption("Dados de referência: PEDE 2022–2024")

# ── Features ───────────────────────────────────────────────────────────────────
GAP_IAA_IDA   = IAA - IDA
IEG_IDA_MEDIO = (IEG + IDA) / 2
IPS_IDA_RATIO = IPS / (IDA + 0.01)

input_data = {
    'IAA': IAA, 'IEG': IEG, 'IPS': IPS, 'IPP': IPP,
    'IDA': IDA, 'IPV': IPV, 'IAN': IAN, 'MAT': MAT, 'POR': POR,
    'GAP_IAA_IDA': GAP_IAA_IDA,
    'IEG_IDA_MEDIO': IEG_IDA_MEDIO,
    'IPS_IDA_RATIO': IPS_IDA_RATIO
}

if feature_names:
    input_df = pd.DataFrame([[input_data.get(f, np.nan) for f in feature_names]], columns=feature_names)
else:
    input_df = pd.DataFrame([input_data])

# ── Calcular predição ──────────────────────────────────────────────────────────
if model:
    prob_risco = float(model.predict_proba(input_df)[0][1])
else:
    # Demo sem modelo: usar heurística simples
    prob_risco = max(0.0, min(1.0, 1 - (IDA * 0.3 + IEG * 0.2 + IAN * 0.3 + IPS * 0.1 + IAA * 0.1) / 10))

if prob_risco >= 0.70:
    nivel, emoji_risk, card_cls, cor_hex, cor_rgba = "ALTO",   "🔴", "card-alto",  "#E84855", "rgba(232,72,85,0.2)"
    recomendacao = "⚡ Intervenção imediata recomendada. Acionar equipe psicopedagógica e revisar plano individual de estudos."
elif prob_risco >= 0.40:
    nivel, emoji_risk, card_cls, cor_hex, cor_rgba = "MÉDIO",  "🟡", "card-medio", "#F9A11B", "rgba(249,161,27,0.2)"
    recomendacao = "📅 Monitoramento próximo recomendado. Agendar reunião de acompanhamento nas próximas 2 semanas."
else:
    nivel, emoji_risk, card_cls, cor_hex, cor_rgba = "BAIXO",  "🟢", "card-baixo", "#43AA8B", "rgba(67,170,139,0.2)"
    recomendacao = "✅ Aluno no caminho certo. Manter acompanhamento regular e incentivar continuidade."

# Classificação INDE estimado
INDE_est = (IDA * 0.35 + IEG * 0.25 + IAA * 0.1 + IPS * 0.1 + IPV * 0.1 + IAN * 0.1)
if   INDE_est >= 8.0: pedra, pedra_cls = "Ametista", "pedra-ametista"
elif INDE_est >= 6.5: pedra, pedra_cls = "Topázio",  "pedra-topazio"
elif INDE_est >= 5.0: pedra, pedra_cls = "Quartzo",  "pedra-quartzo"
else:                 pedra, pedra_cls = "Ágata",    "pedra-agata"


def bar_color_for(val):
    if val >= 7:
        return '#43AA8B'
    elif val >= 5:
        return '#F9A11B'
    return '#E84855'


# ── Principais fatores de risco ────────────────────────────────────────────────
# Usa a importância real do modelo quando disponível; senão, os pesos da heurística.
NOMES_FATORES = {
    'IAN': 'Adequação de nível', 'IDA': 'Desempenho', 'IEG': 'Engajamento',
    'IPS': 'Psicossocial', 'IAA': 'Autoavaliação', 'IPP': 'Psicopedagógico',
    'IPV': 'Ponto de virada'
}
pesos_fatores = None
if model and hasattr(model, "named_steps") and "model" in model.named_steps:
    base_model = model.named_steps["model"]
    if hasattr(base_model, "feature_importances_") and feature_names:
        importancias = dict(zip(feature_names, base_model.feature_importances_))
        candidatos = {k: importancias.get(k, 0) for k in NOMES_FATORES if k in importancias}
        if sum(candidatos.values()) > 0:
            pesos_fatores = candidatos

if not pesos_fatores:
    pesos_fatores = {'IAN': 0.30, 'IDA': 0.30, 'IEG': 0.20, 'IPS': 0.10, 'IAA': 0.10}

soma_pesos = sum(pesos_fatores.values()) or 1
pesos_fatores = {k: v / soma_pesos for k, v in pesos_fatores.items()}

contrib = {k: pesos_fatores[k] * max(0.0, 10 - input_data[k]) for k in pesos_fatores}
soma_contrib = sum(contrib.values())
contrib_pct = {k: (v / soma_contrib * 100 if soma_contrib > 0 else 0) for k, v in contrib.items()}
fatores_ordenados = sorted(contrib_pct.items(), key=lambda x: x[1])

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Passos Mágicos</h1>
    <p>Preditor de Risco de Defasagem Educacional • PosTech Datathon Fase 5</p>
</div>
""", unsafe_allow_html=True)

# ── BANNER DE RESULTADO (horizontal, bem visível) ─────────────────────────────
st.markdown(f"""
<div class="result-banner {card_cls}">
    <div class="rb-left">
        <div class="rb-emoji">{emoji_risk}</div>
        <div>
            <div class="rb-label">Risco de Defasagem</div>
            <div class="rb-nivel" style="color:{cor_hex}">{nivel}</div>
        </div>
    </div>
    <div>
        <div class="rb-prob" style="color:{cor_hex}">{prob_risco:.0%}</div>
        <div class="rb-prob-sub">probabilidade estimada</div>
    </div>
    <div class="rb-rec">{recomendacao}</div>
    <div class="rb-metrics">
        <div class="rb-metric">
            <div class="val" style="color:{cor_hex}">{INDE_est:.1f}</div>
            <div class="lbl">INDE estimado</div>
        </div>
        <div class="rb-metric">
            <div class="val">{GAP_IAA_IDA:+.1f}</div>
            <div class="lbl">Gap IAA−IDA</div>
        </div>
        <div class="rb-metric">
            <span class="pedra-badge {pedra_cls}">{pedra}</span>
            <div class="lbl">Classificação</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LINHA 1: Radar (menor) + Principais fatores de risco ──────────────────────
col_radar, col_fatores = st.columns([1, 1], gap="medium")

with col_radar:
    st.markdown('<div class="section-title">Perfil vs Média Geral</div>', unsafe_allow_html=True)

    MEDIAS_REF = {'IAA': 7.67, 'IEG': 8.26, 'IPS': 6.12,
                  'IPP': 6.98, 'IDA': 7.15, 'IPV': 7.71, 'IAN': 6.71}
    # Ordem lógica: desempenho -> engajamento -> pessoal -> adequação
    ind_radar  = ['IDA', 'IEG', 'IPV', 'IAA', 'IPS', 'IPP', 'IAN']
    vals_aluno = [input_data[i] for i in ind_radar] + [input_data[ind_radar[0]]]
    vals_ref   = [MEDIAS_REF[i] for i in ind_radar] + [MEDIAS_REF[ind_radar[0]]]
    cats       = ind_radar + [ind_radar[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_ref, theta=cats, fill='toself',
        name='Média geral',
        line=dict(color='#cbd5e1', width=1.5),
        fillcolor='rgba(148,163,184,0.10)',
        hovertemplate='%{theta}: %{r:.1f}<extra>Média geral</extra>'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_aluno, theta=cats, fill='toself',
        name='Este aluno',
        line=dict(color=cor_hex, width=3),
        fillcolor=cor_rgba,
        marker=dict(size=6, color=cor_hex),
        hovertemplate='%{theta}: %{r:.1f}<extra>Este aluno</extra>'
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True, range=[0, 10],
                tickvals=[0, 5, 10], tickfont=dict(size=9, color='#94a3b8'),
                gridcolor='#eef2f6', linecolor='#eef2f6'
            ),
            angularaxis=dict(tickfont=dict(size=11, color='#1e293b'), gridcolor='#eef2f6')
        ),
        showlegend=True,
        legend=dict(orientation='h', y=-0.08, x=0.5, xanchor='center', font=dict(size=11)),
        height=320,
        margin=dict(t=10, b=20, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

with col_fatores:
    st.markdown('<div class="section-title">Principais fatores de risco</div>', unsafe_allow_html=True)

    fig_fatores = go.Figure(go.Bar(
        x=[v for _, v in fatores_ordenados],
        y=[NOMES_FATORES.get(k, k) for k, _ in fatores_ordenados],
        orientation='h',
        marker=dict(color=[bar_color_for(input_data[k]) for k, _ in fatores_ordenados]),
        text=[f"{v:.0f}%" for _, v in fatores_ordenados],
        textposition='outside',
        cliponaxis=False,
        hovertemplate='%{y}: %{x:.0f}%<extra></extra>'
    ))
    max_x = max([v for _, v in fatores_ordenados] + [10])
    fig_fatores.update_layout(
        height=320,
        margin=dict(t=10, b=10, l=5, r=35),
        xaxis=dict(visible=False, range=[0, max_x * 1.3]),
        yaxis=dict(tickfont=dict(size=12, color='#334155')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.45
    )
    st.plotly_chart(fig_fatores, use_container_width=True, config={'displayModeBar': False})
    st.caption("Quanto cada indicador contribui para o risco estimado deste aluno.")

# ── LINHA 2: Indicadores (grid) + Alertas ─────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
col_bars, col_alerts = st.columns([1.6, 1], gap="medium")

with col_bars:
    st.markdown('<div class="section-title">Indicadores do Aluno</div>', unsafe_allow_html=True)

    indicadores_info = [
        ('IDA', IDA,  'Desempenho Acadêmico'),
        ('IEG', IEG,  'Engajamento'),
        ('IAA', IAA,  'Autoavaliação'),
        ('IPS', IPS,  'Psicossocial'),
        ('IPV', IPV,  'Ponto de Virada'),
        ('IAN', IAN,  'Adequação de Nível'),
        ('IPP', IPP,  'Psicopedagógico'),
        ('Mat', MAT,  'Matemática'),
        ('Por', POR,  'Português'),
    ]

    rows_html = ""
    for sigla, val, nome in indicadores_info:
        pct = val / 10 * 100
        color = bar_color_for(val)
        rows_html += (
            f'<div class="ind-row" title="{nome}">'
            f'<div class="ind-label">{sigla}</div>'
            f'<div class="ind-bar-wrap">'
            f'<div class="ind-bar" style="width:{pct}%;background:{color}"></div>'
            f'</div>'
            f'<div class="ind-val">{val:.1f}</div>'
            f'</div>'
        )

    st.markdown(f"<div class='ind-card ind-grid'>{rows_html}</div>", unsafe_allow_html=True)

    # Legenda de cores
    st.markdown("""
    <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.6rem; display:flex; gap:1rem;">
        <span><span style="color:#43AA8B">■</span> ≥ 7.0 Bom</span>
        <span><span style="color:#F9A11B">■</span> 5–7 Atenção</span>
        <span><span style="color:#E84855">■</span> < 5 Crítico</span>
    </div>
    """, unsafe_allow_html=True)

with col_alerts:
    st.markdown('<div class="section-title">⚠️ Alertas</div>', unsafe_allow_html=True)
    alertas = []
    if IDA < 5:  alertas.append("IDA crítico — desempenho abaixo de 5")
    if IEG < 6:  alertas.append("IEG baixo — engajamento comprometido")
    if IAN < 5:  alertas.append("IAN crítico — defasagem de nível severa")
    if IPS < 5:  alertas.append("IPS baixo — vulnerabilidade psicossocial")
    if GAP_IAA_IDA > 2: alertas.append("Autopercepção muito acima do real (+2)")
    if GAP_IAA_IDA < -2: alertas.append("Aluno subestima demais sua capacidade")

    if alertas:
        for a in alertas:
            st.markdown(f"<div style='background:#fff0f0;border-left:3px solid #E84855;"
                        f"padding:0.6rem 0.8rem;border-radius:6px;font-size:0.82rem;"
                        f"margin-bottom:0.4rem;'>🚨 {a}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background:#f0fff8;border-left:3px solid #43AA8B;"
                    "padding:0.6rem 0.8rem;border-radius:6px;font-size:0.82rem;'>"
                    "✅ Nenhum alerta crítico identificado</div>", unsafe_allow_html=True)

    # Comparação rápida (movida para cá, ao lado dos alertas)
    st.markdown('<div class="section-title">Aluno vs Média</div>', unsafe_allow_html=True)
    df_comp = pd.DataFrame({
        'Indicador': ind_radar,
        'Aluno': [input_data[i] for i in ind_radar],
        'Média': [MEDIAS_REF[i] for i in ind_radar],
        'Δ': [round(input_data[i] - MEDIAS_REF[i], 1) for i in ind_radar]
    })

    def fmt_delta(v):
        return f"{'▲' if v > 0 else '▼' if v < 0 else '='} {abs(v):.1f}"

    df_comp['Δ'] = df_comp['Δ'].apply(fmt_delta)
    st.dataframe(df_comp, use_container_width=True, hide_index=True, height=250)

# ── Rodapé ─────────────────────────────────────────────────────────────────────
if not model:
    st.info("💡 **Modo demonstração** — Execute o notebook para treinar e salvar o modelo real (`modelo_risco_defasagem.pkl`). Os valores atuais são estimativas heurísticas.", icon="ℹ️")

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.8rem; padding-bottom:1rem;">
    🌟 Associação Passos Mágicos &nbsp;•&nbsp; PosTech Datathon Fase 5 &nbsp;•&nbsp;
    <a href="https://passosmagicos.org.br" target="_blank" style="color:#FBAE31;">passosmagicos.org.br</a>
</div>
""", unsafe_allow_html=True)
