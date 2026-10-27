# frontend/pages/7_Agent_Reasoning.py - Live Multi-Agent "Why" Trace
import streamlit as st
import requests

# Check auth
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.switch_page("pages/0_Login.py")

st.set_page_config(page_title="Agent Reasoning", page_icon="🧠", layout="wide")

from theme import apply_theme
apply_theme()

API_URL = "http://localhost:8000/api/v1"

# Visual identity for each agent in the pipeline
AGENT_STYLES = {
    "preprocessing":  ("🧹", "#6366f1", "Preprocessing"),
    "embedding":      ("🧬", "#8b5cf6", "Embedding"),
    "sentiment":      ("😊", "#ec4899", "Sentiment"),
    "theme":          ("🔍", "#06b6d4", "Theme Discovery"),
    "bias":           ("⚖️", "#f59e0b", "Bias Detection"),
    "recommendation": ("✨", "#10b981", "Recommendation"),
}
PIPELINE_ORDER = ["preprocessing", "embedding", "sentiment", "theme", "bias", "recommendation"]

st.markdown("<h2>🧠 Agent Reasoning — Live 'Why' Trace</h2>", unsafe_allow_html=True)
st.markdown("Watch every agent's chain of thought as feedback flows through the multi-agent pipeline.")

# Pipeline flow banner
flow_html = "<div style='display:flex; align-items:center; flex-wrap:wrap; gap:6px; margin:8px 0 20px 0;'>"
for i, key in enumerate(PIPELINE_ORDER):
    emoji, color, label = AGENT_STYLES[key]
    flow_html += (
        f"<span style='background:{color}22; border:1px solid {color}; color:{color}; "
        f"padding:6px 12px; border-radius:20px; font-size:13px; font-weight:600;'>{emoji} {label}</span>"
    )
    if i < len(PIPELINE_ORDER) - 1:
        flow_html += "<span style='color:#6b7280;'>→</span>"
flow_html += "</div>"
st.markdown(flow_html, unsafe_allow_html=True)

# --- Job selector ---------------------------------------------------------
col_sel, col_refresh = st.columns([4, 1])

recent_jobs = []
try:
    jr = requests.get(f"{API_URL}/jobs/recent", timeout=10)
    if jr.status_code == 200:
        recent_jobs = jr.json().get("jobs", [])
except Exception:
    pass

session_job = st.session_state.get("job_id")
options = list(dict.fromkeys(([session_job] if session_job else []) + recent_jobs))

with col_sel:
    if options:
        selected_job = st.selectbox(
            "Select a job to inspect",
            options,
            format_func=lambda j: f"{j[:8]}…  (current)" if j == session_job else f"{j[:8]}…"
        )
    else:
        selected_job = st.text_input("Enter a Job ID", value=session_job or "")

with col_refresh:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

if not selected_job:
    st.info("📭 No job selected yet. Upload feedback first, then return here to see the reasoning trace.")
    st.stop()

# --- Fetch reasoning ------------------------------------------------------
try:
    resp = requests.get(f"{API_URL}/jobs/{selected_job}/reasoning", timeout=15)
    if resp.status_code != 200:
        st.warning("⏳ No reasoning captured yet for this job. The pipeline may still be running — hit Refresh.")
        st.stop()
    data = resp.json()
except Exception as e:
    st.error(f"❌ Error loading reasoning: {e}")
    st.stop()

feedbacks = data.get("feedbacks", [])
if not feedbacks:
    st.warning("⏳ Reasoning steps are being generated. Click 🔄 Refresh in a moment.")
    st.stop()

# --- Summary metrics ------------------------------------------------------
m1, m2, m3 = st.columns(3)
m1.metric("Feedback Items Traced", data.get("total_feedbacks", 0))
m2.metric("Total Reasoning Steps", data.get("total_steps", 0))
agents_seen = {s["agent_name"] for fb in feedbacks for s in fb["steps"]}
m3.metric("Agents Involved", len(agents_seen))

st.markdown("---")

# --- Pick ONE feedback to inspect -----------------------------------------
# Rendering every feedback's full trace at once means hundreds of HTML blocks,
# which makes the Streamlit session unresponsive. Inspect one at a time instead.
def _fb_label(i: int) -> str:
    t = feedbacks[i].get("text") or "(text unavailable)"
    preview = t[:70] + ("…" if len(t) > 70 else "")
    return f"#{i + 1} — {preview}"

sel_idx = st.selectbox(
    "Select a feedback item to inspect its reasoning chain",
    range(len(feedbacks)),
    format_func=_fb_label,
)

fb = feedbacks[sel_idx]
text = fb.get("text") or "(text unavailable)"
st.markdown(f"**Original feedback:** _{text}_")

# Build the entire timeline as a SINGLE HTML string (one render call).
cards = []
for step in fb["steps"]:
    key = step["agent_name"]
    emoji, color, label = AGENT_STYLES.get(key, ("🤖", "#9ca3af", key.title()))
    action = step.get("action") or ""
    observation = step.get("observation") or ""
    cards.append(
        f"<div style='border-left:4px solid {color}; background:{color}11; "
        f"padding:10px 14px; border-radius:8px; margin-bottom:8px;'>"
        f"<div style='color:{color}; font-weight:700; font-size:13px; margin-bottom:2px;'>"
        f"{emoji} {label}"
        + (f" <span style='color:#9ca3af; font-weight:500;'>· {action}</span>" if action else "")
        + "</div>"
        f"<div style='color:#e5e7eb; font-size:14px;'>{step.get('thought','')}</div>"
        + (f"<div style='color:#9ca3af; font-size:12px; margin-top:4px;'>↳ {observation}</div>" if observation else "")
        + "</div>"
    )
st.markdown(f"<div style='margin-top:10px'>{''.join(cards)}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("🧠 Each step is a real agent thought recorded during processing — proof the agents reason independently and hand off.")
