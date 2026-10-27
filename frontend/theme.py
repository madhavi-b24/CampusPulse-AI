"""
theme.py — Shared soft-lavender UI theme for the whole app.

Call `apply_theme()` right after `st.set_page_config(...)` on every page.
Optional helpers: `page_header(...)` for a consistent titled hero,
and `hero(...)` for the landing banner.
"""
import streamlit as st


# ── Palette ─────────────────────────────────────────────────────────────
LAVENDER_BG_1 = "#f7f4ff"
LAVENDER_BG_2 = "#efe9ff"
ACCENT        = "#7c3aed"   # violet
ACCENT_SOFT   = "#a78bfa"
ACCENT_TINT   = "#ede9fe"
INK           = "#2e1065"   # deep indigo for headings
BORDER        = "#e4dcff"


def apply_theme():
    """Inject the global stylesheet. Safe to call once per page."""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ============ GLOBAL ============ */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    [data-testid="stAppViewContainer"] {{
        background: #ffffff;
    }}
    .block-container {{
        padding-top: 2.2rem;
        padding-left: 2.4rem;
        padding-right: 2.4rem;
        max-width: 1250px;
    }}
    header[data-testid="stHeader"] {{
        background: transparent;
        box-shadow: none;
        border: none;
    }}
    #MainMenu {{ visibility: visible; }}
    footer {{ visibility: hidden; }}

    /* ============ TYPOGRAPHY ============ */
    h1 {{
        color: {INK};
        font-weight: 800;
        letter-spacing: -0.02em;
        font-size: 2.3rem;
    }}
    h2 {{ color: {INK}; font-weight: 700; letter-spacing:-0.01em; font-size: 1.65rem; }}
    h3 {{ color: {INK}; font-weight: 600; font-size: 1.3rem; }}
    p, span, label, li {{ color: #3f3d56; }}

    html[data-theme="dark"] h1,
    html[data-theme="dark"] h2,
    html[data-theme="dark"] h3 {{ color: #ede9fe; }}
    html[data-theme="dark"] p,
    html[data-theme="dark"] span,
    html[data-theme="dark"] label,
    html[data-theme="dark"] li {{ color: #cbd5e1; }}

    /* ============ SIDEBAR ============ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #f3eeff 0%, #ece5ff 100%);
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] > div {{ padding-top: 0.4rem; }}

    /* Branded header above the nav */
    [data-testid="stSidebarNav"]::before {{
        content: "✨ Feedback Intelligence";
        display: block;
        margin: 6px 12px 12px 12px;
        padding: 11px 14px;
        font-size: 0.95rem;
        font-weight: 700;
        color: white;
        letter-spacing: -0.01em;
        border-radius: 12px;
        background: linear-gradient(135deg, {ACCENT} 0%, #6d28d9 100%);
        box-shadow: 0 6px 16px rgba(124,58,237,.22);
    }}

    /* ---- Nav items as soft pills ---- */
    [data-testid="stSidebarNav"] ul {{ padding: 0 10px; }}
    [data-testid="stSidebarNav"] li {{ margin: 4px 0; list-style: none; }}
    [data-testid="stSidebarNav"] li a {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 13px;
        border-radius: 11px;
        background: rgba(255,255,255,0.55);
        border: 1px solid transparent;
        transition: all .16s ease;
    }}
    [data-testid="stSidebarNav"] li a span {{
        color: #4b3f6b;
        font-weight: 600;
        font-size: 0.92rem;
    }}
    [data-testid="stSidebarNav"] li a:hover {{
        background: {ACCENT_TINT};
        border-color: {BORDER};
    }}
    /* Active page — soft lavender tint, violet text, accent bar */
    [data-testid="stSidebarNav"] li a[aria-current="page"] {{
        background: {ACCENT_TINT};
        border-color: {ACCENT_SOFT};
        box-shadow: inset 3px 0 0 {ACCENT};
    }}
    [data-testid="stSidebarNav"] li a[aria-current="page"] span {{
        color: {ACCENT};
        font-weight: 700;
    }}

    /* Emoji chips per nav item (order: Home, Login, Upload, Dashboard,
       Themes, Sentiment, Bias, Recommendations, Reasoning) */
    [data-testid="stSidebarNav"] li:nth-child(1) a span::before {{ content:"🏠  "; }}
    [data-testid="stSidebarNav"] li:nth-child(2) a span::before {{ content:"🔐  "; }}
    [data-testid="stSidebarNav"] li:nth-child(3) a span::before {{ content:"📤  "; }}
    [data-testid="stSidebarNav"] li:nth-child(4) a span::before {{ content:"📊  "; }}
    [data-testid="stSidebarNav"] li:nth-child(5) a span::before {{ content:"💡  "; }}
    [data-testid="stSidebarNav"] li:nth-child(6) a span::before {{ content:"😊  "; }}
    [data-testid="stSidebarNav"] li:nth-child(7) a span::before {{ content:"⚖️  "; }}
    [data-testid="stSidebarNav"] li:nth-child(8) a span::before {{ content:"✨  "; }}
    [data-testid="stSidebarNav"] li:nth-child(9) a span::before {{ content:"🧠  "; }}

    /* ============ BUTTONS ============ */
    .stButton > button {{
        border-radius: 12px;
        border: 1px solid {ACCENT_SOFT};
        background: linear-gradient(135deg, {ACCENT} 0%, #6d28d9 100%);
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.1rem;
        transition: all .18s ease;
        box-shadow: 0 4px 12px rgba(124,58,237,.22);
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(124,58,237,.32);
        border-color: {ACCENT};
    }}
    .stButton > button:active {{ transform: translateY(0); }}
    .stDownloadButton > button {{
        border-radius: 12px; font-weight: 600;
        border: 1px solid {ACCENT_SOFT}; color: {INK}; background: {ACCENT_TINT};
    }}

    /* ============ INPUTS ============ */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {{
        border-radius: 10px; border: 1px solid {BORDER}; background: rgba(255,255,255,.9);
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {ACCENT_SOFT}; box-shadow: 0 0 0 3px {ACCENT_TINT};
    }}
    div[data-baseweb="select"] > div {{
        border-radius: 10px; border: 1px solid {BORDER}; background: rgba(255,255,255,.9);
    }}
    [data-testid="stFileUploader"] section {{
        border-radius: 14px; border: 1.5px dashed {ACCENT_SOFT}; background: rgba(255,255,255,.55);
    }}

    /* ============ METRIC CARDS ============ */
    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,0.9);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(91,33,182,.07);
        transition: all .18s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(124,58,237,.16);
        border-color: {ACCENT_SOFT};
    }}
    div[data-testid="stMetric"] label {{ font-size: 0.95rem; font-weight: 600; color:#6b7280; }}
    div[data-testid="stMetricValue"] {{ color: {INK}; font-size: 2rem; font-weight: 800; }}

    /* ============ CONTAINERS / EXPANDERS / TABS ============ */
    div[data-testid="stDataFrame"] {{ border-radius: 12px; border: 1px solid {BORDER}; overflow: hidden; }}
    details {{ border-radius: 14px; border: 1px solid {BORDER}; background: rgba(255,255,255,.75); }}
    summary {{ font-weight: 600; color: {INK}; }}
    [data-testid="stExpander"] {{ border-radius: 14px; }}

    .stTabs [role="tab"] {{ border-radius: 10px; font-weight: 600; }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {ACCENT} 0%, #6d28d9 100%); color: white;
    }}

    /* Bordered containers (st.container(border=True)) */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 16px !important;
        border: 1px solid {BORDER} !important;
        background: rgba(255,255,255,0.82);
        box-shadow: 0 4px 14px rgba(91,33,182,.06);
    }}

    /* ============ ALERTS ============ */
    .stAlert {{ border-radius: 14px; border: 1px solid {BORDER}; }}

    /* Plotly chart card */
    [data-testid="stPlotlyChart"] {{
        background: rgba(255,255,255,0.9);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 4px 14px rgba(91,33,182,.06);
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-thumb {{ background: {ACCENT_SOFT}; border-radius: 8px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Consistent gradient page title with optional subtitle."""
    st.markdown(f"""
    <div style="margin: 4px 0 18px 0;">
      <h1 style="margin-bottom:2px;
                 background: linear-gradient(135deg, {ACCENT} 0%, #6d28d9 55%, {INK} 100%);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        {icon} {title}
      </h1>
      {f'<p style="color:#6b7280; font-size:1.02rem; margin-top:0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def hero(title: str, subtitle: str):
    """Big landing banner for the home page."""
    st.markdown(f"""
    <div style="
        border-radius: 22px;
        padding: 40px 44px;
        margin: 4px 0 26px 0;
        background: linear-gradient(135deg, {ACCENT} 0%, #6d28d9 50%, #4c1d95 100%);
        box-shadow: 0 18px 42px rgba(124,58,237,.30);
        color: white;">
      <div style="font-size: 2.2rem; font-weight: 800; letter-spacing:-0.02em; line-height:1.15;">
        {title}
      </div>
      <div style="font-size: 1.08rem; opacity:.92; margin-top: 10px; max-width: 720px;">
        {subtitle}
      </div>
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon: str, title: str, desc: str):
    """Return HTML for a single feature card (compose several in one markdown)."""
    return (
        f"<div style='background:rgba(255,255,255,0.9); border:1px solid {BORDER}; "
        f"border-radius:16px; padding:18px 20px; box-shadow:0 4px 14px rgba(91,33,182,.06); height:100%;'>"
        f"<div style='font-size:1.7rem'>{icon}</div>"
        f"<div style='font-weight:700; color:{INK}; margin:6px 0 4px 0;'>{title}</div>"
        f"<div style='color:#6b7280; font-size:0.92rem;'>{desc}</div>"
        f"</div>"
    )
