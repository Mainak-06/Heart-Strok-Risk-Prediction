import datetime

import joblib
import pandas as pd
import streamlit as st

# ==================================================================
# Page setup
# ==================================================================
st.set_page_config(
    page_title="Heart Stroke Prediction by Mainak",
    page_icon="🫀",
    layout="centered",
    initial_sidebar_state="expanded",
)

def html(s: str) -> None:
    """Render HTML safely (no blank lines or indentation that Markdown could misread)."""
    cleaned = "\n".join(line.strip() for line in s.strip().splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


html("""
<style>
:root {
  --cyan:#00E5FF; --mag:#FF2BD6; --vio:#8B5CF6;
  --ok:#2CFFA0; --bad:#FF3D6E; --warn:#FFC857;
  --ink:#E6EDFF; --mute:#9FB0D6;
  --glass:rgba(255,255,255,.05); --edge:rgba(255,255,255,.14);
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, 'Courier New', monospace;
}

/* ---------- background: aurora glow + faint grid ---------- */
.stApp {
  background:
    radial-gradient(900px 520px at 8% -8%, rgba(139,92,246,.38), transparent 62%),
    radial-gradient(800px 520px at 100% 6%, rgba(255,43,214,.24), transparent 62%),
    radial-gradient(1000px 640px at 50% 118%, rgba(0,229,255,.20), transparent 62%),
    #070B1A;
  background-attachment: fixed;
}
.stApp::before {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(0,229,255,.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,.045) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: radial-gradient(ellipse at 50% 30%, #000 20%, transparent 78%);
  -webkit-mask-image: radial-gradient(ellipse at 50% 30%, #000 20%, transparent 78%);
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; max-width: 880px; position: relative; z-index: 1; }
::selection { background: rgba(0,229,255,.35); }

/* ---------- sidebar: frosted glass ---------- */
section[data-testid="stSidebar"] {
  background: rgba(10,16,38,.62);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  backdrop-filter: blur(20px) saturate(140%);
  border-right: 1px solid rgba(0,229,255,.28);
  box-shadow: 8px 0 40px rgba(0,229,255,.06);
}
.side-title { font-family:var(--mono); font-weight:700; font-size:.95rem; letter-spacing:.12em;
  text-transform:uppercase; color:var(--cyan); text-shadow:0 0 12px rgba(0,229,255,.55); margin:0 0 .25rem 0; }

/* ---------- hero ---------- */
.hero { position:relative; padding:1.8rem 2rem 1.5rem 2rem; border-radius:22px; margin-bottom:1.2rem;
  background: linear-gradient(135deg, rgba(139,92,246,.30), rgba(0,229,255,.10) 55%, rgba(255,43,214,.16));
  border:1px solid rgba(255,255,255,.18);
  -webkit-backdrop-filter: blur(18px); backdrop-filter: blur(18px);
  box-shadow: 0 10px 40px rgba(0,0,0,.5), 0 0 40px rgba(139,92,246,.25), inset 0 1px 0 rgba(255,255,255,.25);
  overflow:hidden; }
.hero::after { content:""; position:absolute; top:-60%; left:-30%; width:60%; height:220%;
  background: linear-gradient(100deg, transparent, rgba(255,255,255,.10), transparent);
  transform: rotate(8deg); animation: sheen 7s ease-in-out infinite; pointer-events:none; }
@keyframes sheen { 0%,100% { left:-40%; } 50% { left:95%; } }
.hero .hero-title { margin:0 0 .35rem 0; padding:0; font-size:2rem; font-weight:800; letter-spacing:.01em; line-height:1.2;
  color:#FFFFFF; background:linear-gradient(90deg,#FFFFFF 0%, var(--cyan) 45%, var(--mag) 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  filter: drop-shadow(0 0 14px rgba(0,229,255,.35)); }
.hero p { margin:0 0 .9rem 0; color:var(--mute); font-size:.98rem; }
.chips { display:flex; flex-wrap:wrap; gap:.5rem; }
.chip { font-family:var(--mono); font-size:.72rem; letter-spacing:.06em; text-transform:uppercase;
  color:var(--cyan); padding:.28rem .7rem; border-radius:99px;
  background:rgba(0,229,255,.08); border:1px solid rgba(0,229,255,.35);
  box-shadow: 0 0 12px rgba(0,229,255,.18); }
.chip.m { color:#FF8AEA; background:rgba(255,43,214,.09); border-color:rgba(255,43,214,.4); box-shadow:0 0 12px rgba(255,43,214,.2); }

/* ---------- form card ---------- */
div[data-testid="stForm"] {
  background: var(--glass); border:1px solid var(--edge); border-radius:22px; padding:1.1rem 1.3rem 1.3rem 1.3rem;
  -webkit-backdrop-filter: blur(16px); backdrop-filter: blur(16px);
  box-shadow: 0 10px 36px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.14);
}
.group-title { font-family:var(--mono); font-weight:700; font-size:.82rem; letter-spacing:.14em; text-transform:uppercase;
  color:var(--cyan); text-shadow:0 0 10px rgba(0,229,255,.5);
  margin:1.1rem 0 .3rem 0; padding-bottom:.35rem;
  border-bottom:1px solid transparent;
  border-image: linear-gradient(90deg, rgba(0,229,255,.7), rgba(255,43,214,.45), transparent) 1; }

/* ---------- inputs ---------- */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {
  background: rgba(255,255,255,.055) !important; border:1px solid rgba(0,229,255,.22) !important;
  border-radius:12px !important; transition: border-color .2s ease, box-shadow .2s ease; }
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover { border-color: rgba(0,229,255,.6) !important; }
div[data-baseweb="select"] > div:focus-within, div[data-baseweb="input"] > div:focus-within {
  border-color: var(--cyan) !important; box-shadow: 0 0 0 1px var(--cyan), 0 0 18px rgba(0,229,255,.35) !important; }

/* ---------- tabs ---------- */
div[data-baseweb="tab-list"] { gap:.35rem; background:rgba(255,255,255,.04); padding:.3rem; border-radius:14px;
  border:1px solid var(--edge); -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }
button[data-baseweb="tab"] { border-radius:10px; transition: background .2s ease; }
button[data-baseweb="tab"]:hover { background:rgba(0,229,255,.10); }
button[data-baseweb="tab"][aria-selected="true"] { background:rgba(0,229,255,.14); }
div[data-baseweb="tab-highlight"] { height:3px !important; border-radius:3px;
  background: linear-gradient(90deg, var(--cyan), var(--mag)) !important; box-shadow: 0 0 14px var(--cyan); }
div[data-baseweb="tab-border"] { background: transparent !important; }

/* ---------- buttons ---------- */
div[data-testid="stFormSubmitButton"] > button {
  width:100%; border:0; border-radius:14px; padding:.75rem 1rem;
  background: linear-gradient(90deg, var(--cyan), var(--vio) 55%, var(--mag));
  box-shadow: 0 0 22px rgba(0,229,255,.45), 0 6px 24px rgba(139,92,246,.4), inset 0 1px 0 rgba(255,255,255,.5);
  transition: transform .15s ease, box-shadow .2s ease, filter .2s ease; }
div[data-testid="stFormSubmitButton"] > button p { color:#050816 !important; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
div[data-testid="stFormSubmitButton"] > button:hover { transform: translateY(-2px); filter: brightness(1.12);
  box-shadow: 0 0 34px rgba(0,229,255,.7), 0 10px 30px rgba(255,43,214,.45), inset 0 1px 0 rgba(255,255,255,.6); }
div[data-testid="stFormSubmitButton"] > button:active { transform: translateY(0) scale(.99); }

section[data-testid="stSidebar"] .stButton > button, .stDownloadButton > button {
  width:100%; border-radius:12px; font-weight:600; color:var(--ink);
  background: rgba(255,255,255,.06); border:1px solid rgba(0,229,255,.35);
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
  transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease, background .2s ease; }
section[data-testid="stSidebar"] .stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-1px); border-color: var(--cyan); background: rgba(0,229,255,.12);
  box-shadow: 0 0 18px rgba(0,229,255,.4); color:#FFFFFF; }

/* ---------- alerts, expanders ---------- */
div[data-testid="stAlert"] { border-radius:14px; border:1px solid var(--edge);
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); }
div[data-testid="stExpander"] { background:var(--glass); border:1px solid var(--edge) !important; border-radius:16px;
  -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }

/* ---------- verdict ---------- */
.verdict { padding:1.25rem 1.5rem; border-radius:20px; margin:.4rem 0 .8rem 0; border:1px solid;
  -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px); }
.verdict.high { background:linear-gradient(135deg, rgba(255,61,110,.20), rgba(255,61,110,.05));
  border-color:rgba(255,61,110,.65); box-shadow:0 0 30px rgba(255,61,110,.28), inset 0 1px 0 rgba(255,255,255,.14);
  animation: pulseRed 2.6s ease-in-out infinite; }
.verdict.low { background:linear-gradient(135deg, rgba(44,255,160,.18), rgba(44,255,160,.04));
  border-color:rgba(44,255,160,.6); box-shadow:0 0 30px rgba(44,255,160,.22), inset 0 1px 0 rgba(255,255,255,.14); }
@keyframes pulseRed { 0%,100% { box-shadow:0 0 22px rgba(255,61,110,.22), inset 0 1px 0 rgba(255,255,255,.14); }
  50% { box-shadow:0 0 42px rgba(255,61,110,.45), inset 0 1px 0 rgba(255,255,255,.14); } }
.verdict .vt { margin:0 0 .3rem 0; font-size:1.4rem; font-weight:800; padding:0; line-height:1.3; }
.verdict.high .vt { color:#FF7A99; text-shadow:0 0 16px rgba(255,61,110,.6); }
.verdict.low .vt  { color:var(--ok); text-shadow:0 0 16px rgba(44,255,160,.55); }
.verdict p { margin:0; color:var(--ink); opacity:.85; }

/* ---------- gauge ---------- */
.gauge-box { background:var(--glass); border:1px solid var(--edge); border-radius:20px; padding:.7rem .6rem .3rem .6rem;
  text-align:center; -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
  box-shadow: 0 8px 30px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.14); }
.gauge-cap { color:var(--mute); font-size:.8rem; margin:0 0 .5rem 0; }

/* ---------- flags ---------- */
.flag { background:var(--glass); border:1px solid var(--edge); border-left:5px solid; border-radius:12px;
  padding:.65rem 1rem; margin-bottom:.5rem; color:var(--ink); font-size:.93rem;
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); }
.flag.warn  { border-left-color:var(--warn); box-shadow:-6px 0 18px -8px rgba(255,200,87,.6); }
.flag.alert { border-left-color:var(--bad);  box-shadow:-6px 0 18px -8px rgba(255,61,110,.7); }
.flag.ok    { border-left-color:var(--ok);   box-shadow:-6px 0 18px -8px rgba(44,255,160,.6); }

/* ---------- range bars ---------- */
.rb { background:var(--glass); border:1px solid var(--edge); border-radius:16px; padding:.85rem 1.1rem; margin-bottom:.75rem;
  -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); box-shadow: inset 0 1px 0 rgba(255,255,255,.1); }
.rb-head { display:flex; justify-content:space-between; color:var(--ink); font-weight:600; font-size:.93rem; }
.rb-head span:last-child { font-family:var(--mono); color:var(--cyan); text-shadow:0 0 10px rgba(0,229,255,.5); }
.rb-track { position:relative; display:flex; height:12px; border-radius:99px; margin:.8rem 0 .4rem 0; }
.rb-segs { display:flex; width:100%; height:100%; border-radius:99px; overflow:hidden; }
.rb-seg { height:100%; opacity:.88; }
.rb-marker { position:absolute; top:-5px; width:4px; height:22px; background:#FFFFFF; border-radius:2px;
  box-shadow:0 0 8px #FFFFFF, 0 0 18px var(--cyan); }
.rb-tick { position:absolute; top:-3px; width:2px; height:18px; background:var(--cyan); box-shadow:0 0 8px var(--cyan); }
.rb-legend { color:var(--mute); font-size:.78rem; }

@media (prefers-reduced-motion: reduce) { .hero::after, .verdict.high { animation:none; } }
</style>
""")


# ==================================================================
# Load saved model, scaler, and expected columns (unchanged logic)
# ==================================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load("knn_heart_model.PKL")
    scaler = joblib.load("heart_scaler.PKL")
    expected_columns = joblib.load("heart_columns.PKL")

    # If it was saved as a method reference, call it to get the actual list
    if callable(expected_columns):
        expected_columns = expected_columns()
    return model, scaler, list(expected_columns)


try:
    model, scaler, expected_columns = load_artifacts()
except FileNotFoundError as e:
    st.error(
        f"Model file not found: **{e.filename}**. Keep `knn_heart_model.pkl`, "
        "`heart_scaler.pkl` and `heart_columns.pkl` in the same folder as `app.py`."
    )
    st.stop()


# ==================================================================
# Prediction pipeline (same steps as your original code)
# ==================================================================
def run_model(v: dict):
    # Create a raw input dictionary
    raw_input = {
        'Age': v["age"],
        'RestingBP': v["resting_bp"],
        'Cholesterol': v["cholesterol"],
        'FastingBS': v["fasting_bs"],
        'MaxHR': v["max_hr"],
        'Oldpeak': v["oldpeak"],
        'Sex_' + v["sex"]: 1,
        'ChestPainType_' + v["chest_pain"]: 1,
        'RestingECG_' + v["resting_ecg"]: 1,
        'ExerciseAngina_' + v["exercise_angina"]: 1,
        'ST_Slope_' + v["st_slope"]: 1,
    }

    # Create input dataframe
    input_df = pd.DataFrame([raw_input])

    # Fill in missing columns with 0s
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder columns to match training order
    input_df = input_df[expected_columns]

    # Numerical columns that need scaling
    numerical_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

    # Scale the input safely
    try:
        input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])
        scaled_input = input_df
    except ValueError:
        # Fallback if scaler was fitted on the entire dataframe
        scaled_input = scaler.transform(input_df)

    # Make prediction
    prediction = int(model.predict(scaled_input)[0])

    # Extra info only: share of nearest neighbours voting "disease"
    risk_pct = None
    try:
        risk_pct = float(model.predict_proba(scaled_input)[0][1]) * 100
    except Exception:
        pass
    return prediction, risk_pct


# ==================================================================
# Input state, presets and labels
# ==================================================================
DEFAULTS = dict(
    age=40, sex="M", chest_pain="ATA", resting_bp=120, cholesterol=200,
    fasting_bs=0, resting_ecg="Normal", max_hr=150, exercise_angina="N",
    oldpeak=1.0, st_slope="Up",
)
PRESETS = {
    "Healthy example": dict(
        age=29, sex="F", chest_pain="ATA", resting_bp=110, cholesterol=180,
        fasting_bs=0, resting_ecg="Normal", max_hr=175, exercise_angina="N",
        oldpeak=0.0, st_slope="Up",
    ),
    "High-risk example": dict(
        age=62, sex="M", chest_pain="ASY", resting_bp=150, cholesterol=280,
        fasting_bs=1, resting_ecg="ST", max_hr=105, exercise_angina="Y",
        oldpeak=2.5, st_slope="Flat",
    ),
    "Reset": DEFAULTS,
}

for k, val in DEFAULTS.items():
    st.session_state.setdefault(k, val)
st.session_state.setdefault("last", None)
st.session_state.setdefault("history", [])


def apply_preset(name: str) -> None:
    for k, val in PRESETS[name].items():
        st.session_state[k] = val
    st.session_state["last"] = None  # don't show an old result next to new values
    st.toast(f"{name} loaded" if name != "Reset" else "Form reset")


SEX = {"M": "Male", "F": "Female"}
CHEST = {"ATA": "ATA - Atypical angina", "NAP": "NAP - Non-anginal pain",
         "TA": "TA - Typical angina", "ASY": "ASY - No symptoms"}
ECG = {"Normal": "Normal", "ST": "ST-T wave abnormality", "LVH": "Left ventricular hypertrophy"}
SLOPE = {"Up": "Upsloping", "Flat": "Flat", "Down": "Downsloping"}
YN01 = {0: "No", 1: "Yes"}
YN = {"Y": "Yes", "N": "No"}


# ==================================================================
# Visual helpers
# ==================================================================
def gauge_svg(pct: float, color: str) -> str:
    arc = 251.33  # length of the half circle with radius 80
    fill = max(0.0, min(pct, 100.0)) / 100 * arc
    return f"""
    <svg viewBox="0 0 200 124" width="100%" style="max-width:300px">
      <defs>
        <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="3.2" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.10)"
            stroke-width="14" stroke-linecap="round"/>
      <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="{color}"
            stroke-width="14" stroke-linecap="round" filter="url(#glow)"
            stroke-dasharray="{fill:.1f} {arc}"/>
      <text x="100" y="90" text-anchor="middle" font-size="32" font-weight="800"
            fill="#E6EDFF" style="font-family:ui-monospace,Menlo,Consolas,monospace">{pct:.0f}%</text>
      <text x="20" y="118" text-anchor="middle" font-size="9" fill="#9FB0D6">0</text>
      <text x="180" y="118" text-anchor="middle" font-size="9" fill="#9FB0D6">100</text>
    </svg>"""


def range_bar(title, value, unit, lo, hi, zones, tick=None, tick_label=""):
    """zones: list of (start, end, colour, label). Draws a track with a marker at `value`."""
    span = hi - lo
    segs = "".join(
        f'<div class="rb-seg" style="width:{(b - a) / span * 100:.2f}%;background:{c}"></div>'
        for a, b, c, _ in zones
    )
    pos = max(0.0, min((value - lo) / span * 100, 100.0))
    tick_html = ""
    if tick is not None:
        tpos = max(0.0, min((tick - lo) / span * 100, 100.0))
        tick_html = f'<div class="rb-tick" style="left:{tpos:.2f}%"></div>'
    legend = " &nbsp;|&nbsp; ".join(label for *_, label in zones)
    if tick_label:
        legend += f" &nbsp;|&nbsp; teal tick: {tick_label}"
    html(f"""
    <div class="rb">
      <div class="rb-head"><span>{title}</span><span>{value} {unit}</span></div>
      <div class="rb-track"><div class="rb-segs">{segs}</div><div class="rb-marker" style="left:calc({pos:.2f}% - 2px)"></div>{tick_html}</div>
      <div class="rb-legend">{legend}</div>
    </div>""")


GREEN, AMBER, RED = "#19D68F", "#FFC857", "#FF3D6E"


def health_flags(v: dict):
    flags = []
    if v["resting_bp"] >= 140:
        flags.append(("alert", "Resting blood pressure is 140 or higher, which is generally considered high."))
    elif v["resting_bp"] >= 120:
        flags.append(("warn", "Resting blood pressure is slightly raised (120 to 139)."))
    if v["cholesterol"] >= 240:
        flags.append(("alert", "Cholesterol is 240 mg/dL or higher, which is generally considered high."))
    elif v["cholesterol"] >= 200:
        flags.append(("warn", "Cholesterol is borderline (200 to 239 mg/dL)."))
    if v["fasting_bs"] == 1:
        flags.append(("warn", "Fasting blood sugar above 120 mg/dL can be an early sign of diabetes."))
    if v["exercise_angina"] == "Y":
        flags.append(("alert", "Chest pain during exercise is worth discussing with a doctor."))
    if v["oldpeak"] >= 2.0:
        flags.append(("alert", "An ST depression of 2.0 or more can point to reduced blood flow to the heart."))
    elif v["oldpeak"] >= 1.0:
        flags.append(("warn", "ST depression between 1.0 and 2.0 is worth keeping an eye on."))
    if v["max_hr"] < 0.6 * (220 - v["age"]):
        flags.append(("warn", "Your max heart rate is under 60% of the age-predicted maximum (220 minus age)."))
    if not flags:
        flags.append(("ok", "None of your blood pressure, cholesterol, sugar or exercise values fall in a flagged range."))
    return flags


def build_report(v: dict, prediction: int, risk_pct) -> str:
    lines = [
        "HEART DISEASE RISK REPORT",
        f"Generated: {datetime.datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"Result: {'HIGH risk' if prediction == 1 else 'LOW risk'}",
    ]
    if risk_pct is not None:
        lines.append(f"Similar patients with heart disease: {risk_pct:.0f}%")
    lines += [
        "",
        "Inputs",
        f"  Age: {v['age']}",
        f"  Sex: {SEX[v['sex']]}",
        f"  Chest pain type: {CHEST[v['chest_pain']]}",
        f"  Resting BP: {v['resting_bp']} mm Hg",
        f"  Cholesterol: {v['cholesterol']} mg/dL",
        f"  Fasting blood sugar > 120: {YN01[v['fasting_bs']]}",
        f"  Resting ECG: {ECG[v['resting_ecg']]}",
        f"  Max heart rate: {v['max_hr']}",
        f"  Exercise angina: {YN[v['exercise_angina']]}",
        f"  Oldpeak: {v['oldpeak']}",
        f"  ST slope: {SLOPE[v['st_slope']]}",
        "",
        "Notes",
    ]
    lines += [f"  - {text}" for _, text in health_flags(v)]
    lines += ["", "This is an estimate from a machine learning model, not a medical diagnosis."]
    return "\n".join(lines)


# ==================================================================
# Sidebar
# ==================================================================
with st.sidebar:
    html('<p class="side-title">Quick fill</p>')
    st.caption("Load sample values to try the app.")
    for name in PRESETS:
        st.button(name, on_click=apply_preset, args=(name,), key=f"preset_{name}")
    st.divider()
    html('<p class="side-title">About the model</p>')
    st.write("K-Nearest Neighbors classifier trained on clinical heart data. Test score: about 0.86.")
    st.warning("Student project. Not a medical device and not a diagnosis. See a doctor for medical advice.")
    st.caption("Built by Mainak")


# ==================================================================
# Header
# ==================================================================
# ==================================================================
# Header
# ==================================================================
# ==================================================================
# Header
# ==================================================================
# ==================================================================
# Header
# ==================================================================
# ==================================================================
# Header
# ==================================================================
html("""
<div class="hero">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.35rem;">
    <!-- Anatomical Heart Emoji with Color Presentation Force -->
    <span style="font-size: 2.2rem; filter: drop-shadow(0 0 12px rgba(255,61,110,0.8)); line-height: 1; flex-shrink: 0;">🫀&#xFE0F;</span>
    <div style="font-size: 2rem; font-weight: 800; letter-spacing: .01em; line-height: 1.2; background: linear-gradient(90deg,#FFFFFF 0%, var(--cyan) 45%, var(--mag) 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 14px rgba(0,229,255,.35);">Heart Stroke Prediction by Mainak</div>
  </div>
  <p>Provide the following details to check your heart stroke risk.</p>
  <div class="chips">
    <span class="chip">KNN model</span>
    <span class="chip m">Test score ≈ 0.86</span>
    <span class="chip">11 health inputs</span>
    <span class="chip m">Instant result</span>
  </div>
</div>
""")

tab_predict, tab_compare, tab_about = st.tabs(["Check my risk", "Compare with healthy ranges", "How it works"])

# ==================================================================
# TAB 1: inputs + result
# ==================================================================
with tab_predict:
    with st.form("risk_form"):
        html('<div class="group-title">About you</div>')
        c1, c2 = st.columns(2)
        with c1:
            st.slider("Age", 18, 100, key="age")
        with c2:
            st.selectbox("Sex", list(SEX), format_func=SEX.get, key="sex")

        html('<div class="group-title">Blood tests and vitals</div>')
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input("Resting blood pressure (mm Hg)", 80, 200, key="resting_bp")
        with c2:
            st.number_input("Cholesterol (mg/dL)", 100, 600, key="cholesterol")
        with c3:
            st.selectbox("Fasting blood sugar > 120 mg/dL", [0, 1], format_func=YN01.get, key="fasting_bs")

        html('<div class="group-title">Heart tests</div>')
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chest pain type", list(CHEST), format_func=CHEST.get, key="chest_pain")
            st.selectbox("Resting ECG", list(ECG), format_func=ECG.get, key="resting_ecg")
        with c2:
            st.selectbox("ST slope", list(SLOPE), format_func=SLOPE.get, key="st_slope")
            st.slider("Oldpeak (ST depression)", 0.0, 6.0, step=0.1, key="oldpeak")

        html('<div class="group-title">During exercise</div>')
        c1, c2 = st.columns(2)
        with c1:
            st.slider("Max heart rate", 60, 220, key="max_hr")
        with c2:
            st.selectbox("Exercise-induced angina", list(YN), format_func=YN.get, key="exercise_angina")

        submitted = st.form_submit_button("Predict")

    if submitted:
        values = {k: st.session_state[k] for k in DEFAULTS}
        prediction, risk_pct = run_model(values)
        st.session_state["last"] = dict(values=values, prediction=prediction, risk_pct=risk_pct)
        st.session_state["history"].append({
            "Time": f"{datetime.datetime.now():%H:%M:%S}",
            "Age": values["age"], "Sex": values["sex"],
            "BP": values["resting_bp"], "Chol": values["cholesterol"],
            "MaxHR": values["max_hr"], "Oldpeak": values["oldpeak"],
            "Result": "High risk" if prediction == 1 else "Low risk",
            "Similar patients with disease (%)": None if risk_pct is None else round(risk_pct),
        })

    last = st.session_state["last"]
    if last:
        v, prediction, risk_pct = last["values"], last["prediction"], last["risk_pct"]
        color = "#FF3D6E" if prediction == 1 else "#2CFFA0"

        left, right = st.columns([3, 2])
        with left:
            if prediction == 1:
                html("""
                <div class="verdict high"><div class="vt">⚠️ High Risk of Heart Disease</div>
                <p>Patients with values like yours were mostly diagnosed with heart disease.
                Please talk to a doctor for a proper check-up.</p></div>""")
            else:
                html("""
                <div class="verdict low"><div class="vt">✅ Low Risk of Heart Disease</div>
                <p>Patients with values like yours were mostly healthy.
                Keep up regular check-ups and a healthy lifestyle.</p></div>""")
        with right:
            if risk_pct is not None:
                html(f"""
                <div class="gauge-box">{gauge_svg(risk_pct, color)}
                <p class="gauge-cap">Share of the most similar patients who had heart disease</p></div>""")

        st.markdown("##### What stands out in your numbers")
        for level, text in health_flags(v):
            html(f'<div class="flag {level}">{text}</div>')
        st.caption("These notes use general health guidelines. They are separate from the model's prediction.")

        st.download_button(
            "Download report (.txt)",
            data=build_report(v, prediction, risk_pct),
            file_name="heart_risk_report.txt",
            mime="text/plain",
        )

        if len(st.session_state["history"]) > 0:
            with st.expander(f"Predictions this session ({len(st.session_state['history'])})"):
                hist = pd.DataFrame(st.session_state["history"])
                st.dataframe(hist, hide_index=True)
                st.download_button(
                    "Download history (.csv)",
                    data=hist.to_csv(index=False),
                    file_name="prediction_history.csv",
                    mime="text/csv",
                )
    else:
        st.info("Fill in the form and press **Predict**. Or use the Quick fill buttons in the sidebar to try sample patients.")

# ==================================================================
# TAB 2: compare with healthy ranges
# ==================================================================
with tab_compare:
    src = st.session_state["last"]["values"] if st.session_state["last"] else {k: st.session_state[k] for k in DEFAULTS}
    st.caption(
        "Where your values sit against general reference ranges. "
        + ("Showing your last prediction." if st.session_state["last"] else "Showing the current form values.")
    )
    range_bar("Resting blood pressure", src["resting_bp"], "mm Hg", 80, 200,
              [(80, 120, GREEN, "under 120 normal"), (120, 140, AMBER, "120 to 139 raised"),
               (140, 200, RED, "140+ high")])
    range_bar("Cholesterol", src["cholesterol"], "mg/dL", 100, 600,
              [(100, 200, GREEN, "under 200 desirable"), (200, 240, AMBER, "200 to 239 borderline"),
               (240, 600, RED, "240+ high")])
    range_bar("Oldpeak (ST depression)", src["oldpeak"], "", 0, 6,
              [(0, 1, GREEN, "under 1.0"), (1, 2, AMBER, "1.0 to 1.9"), (2, 6, RED, "2.0+")])
    pm = 220 - src["age"]
    range_bar("Max heart rate", src["max_hr"], "bpm", 60, 220,
              [(60, 0.6 * pm, RED, "under 60% of predicted"), (0.6 * pm, 0.85 * pm, AMBER, "60 to 85%"),
               (0.85 * pm, 220, GREEN, "85%+")],
              tick=pm, tick_label=f"age-predicted max ({pm})")
    st.caption("Reference ranges are general guidelines for adults and are not personal medical advice.")

# ==================================================================
# TAB 3: how it works
# ==================================================================
with tab_about:
    st.markdown(
        """
**How the prediction is made**

1. Your answers are turned into the same columns the model was trained on (one-hot encoding for sex, chest pain, ECG, angina and ST slope).
2. Age, blood pressure, cholesterol, max heart rate and oldpeak are scaled with the saved scaler.
3. The K-Nearest Neighbors model finds the training patients most similar to you and predicts the group most of them belong to.

**The percentage on the gauge** is the share of those nearest patients who had heart disease. It is a similarity vote, not a medical probability.

**Limits to keep in mind**

- The model learned from one dataset and may not fit every person or population.
- It uses only the 11 inputs shown here.
- A score of about 0.86 means it is wrong for roughly 1 in 7 patients in testing.

This tool cannot diagnose anything. If you have symptoms such as chest pain, shortness of breath or dizziness, contact a doctor right away.
"""
    )
