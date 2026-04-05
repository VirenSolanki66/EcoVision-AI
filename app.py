import streamlit as st
import random
import time
from PIL import Image
from utils import predict_image

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoVision AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg-main:    #C8DFC8;
    --bg-mid:     #B5D4B5;
    --bg-deep:    #9EC49E;
    --accent:     #3A7D44;
    --accent-light: #5A9E62;
    --accent-dark:  #235C2A;
    --amber:      #D4813A;
    --red:        #B83232;
    --text:       #1A2E1A;
    --text-mid:   #2E472E;
    --text-muted: #5A7A5A;
    --border:     rgba(58,125,68,0.20);
    --border-mid: rgba(58,125,68,0.30);
    --card-bg:    rgba(240,250,240,0.55);
    --card-bg-strong: rgba(240,250,240,0.78);
    --shadow:     0 4px 24px rgba(35,92,42,0.10);
    --shadow-md:  0 8px 32px rgba(35,92,42,0.14);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(150deg, #C8DFC8 0%, #B5D4B5 45%, #9EC49E 100%) !important;
    min-height: 100vh;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(200,223,200,0.97) 0%, rgba(158,196,158,0.97) 100%) !important;
    border-right: 1px solid var(--border-mid) !important;
    backdrop-filter: blur(12px);
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: var(--text) !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--card-bg-strong) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    box-shadow: var(--shadow) !important;
    backdrop-filter: blur(8px);
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.78rem !important; letter-spacing: 1px; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: var(--accent-dark) !important; font-weight: 800 !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--card-bg-strong) !important;
    border: 2px dashed var(--accent-light) !important;
    border-radius: 18px !important;
    transition: border-color 0.2s;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%) !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 14px rgba(0,121,107,0.30) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,121,107,0.40) !important;
}

/* Progress bar */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent-dark), var(--accent-light)) !important;
    border-radius: 99px !important;
}

/* Chat input */
.stChatInput > div {
    background: var(--card-bg-strong) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 14px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(180,215,180,0.55) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(8px);
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    border-radius: 9px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-light)) !important;
    color: #fff !important;
    border-radius: 9px !important;
    box-shadow: 0 2px 10px rgba(0,121,107,0.25) !important;
}

/* ─── Custom components ─── */

.glass-card {
    background: var(--card-bg-strong);
    border: 1px solid var(--border-mid);
    border-radius: 20px;
    padding: 22px 26px;
    margin-bottom: 16px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
}
.glass-card-accent {
    border-left: 4px solid var(--accent);
}

.hero-header {
    text-align: center;
    padding: 32px 0 10px 0;
}
.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1A3A1A 0%, #3A7D44 55%, #5A9E62 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 6px;
}

.slogan-bar {
    background: linear-gradient(90deg, rgba(200,223,200,0.75), rgba(181,212,181,0.85), rgba(200,223,200,0.75));
    border: 1px solid var(--border-mid);
    border-radius: 14px;
    padding: 14px 28px;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: var(--accent-dark);
    letter-spacing: 2px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(8px);
}

.result-big {
    font-family: 'Inter', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--accent-dark);
    line-height: 1.1;
}

.conf-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-muted);
    letter-spacing: 2.5px;
    margin-bottom: 7px;
    text-transform: uppercase;
}

.tip-box {
    background: linear-gradient(135deg, rgba(220,238,220,0.80) 0%, rgba(181,212,181,0.60) 100%);
    border: 1px solid var(--border-mid);
    border-radius: 14px;
    padding: 16px 20px;
    font-style: italic;
    color: var(--text-mid);
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: var(--shadow);
}

.score-badge {
    background: linear-gradient(135deg, var(--accent-dark) 0%, var(--accent) 50%, var(--accent-light) 100%);
    color: #fff;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 1.6rem;
    border-radius: 14px;
    padding: 14px 24px;
    display: inline-block;
    min-width: 100px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(26,92,66,0.30);
}

.badge-recyclable {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,121,107,0.12);
    border: 1.5px solid var(--accent);
    color: var(--accent-dark);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 6px 16px;
    border-radius: 99px;
}
.badge-nonrecyclable {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(198,40,40,0.10);
    border: 1.5px solid #C62828;
    color: #C62828;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 6px 16px;
    border-radius: 99px;
}

.label-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(0,121,107,0.10);
    border: 1px solid var(--border-mid);
    color: var(--accent-dark);
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 5px 14px;
    border-radius: 99px;
    margin: 4px 4px 4px 0;
}

.chat-bubble-user {
    background: linear-gradient(135deg, var(--accent-dark), var(--accent));
    color: #fff;
    border-radius: 18px 18px 6px 18px;
    padding: 12px 18px;
    margin: 8px 0;
    font-size: 0.92rem;
    text-align: right;
    box-shadow: var(--shadow);
}
.chat-bubble-bot {
    background: var(--card-bg-strong);
    border: 1px solid var(--border-mid);
    color: var(--text);
    border-radius: 18px 18px 18px 6px;
    padding: 12px 18px;
    margin: 8px 0;
    font-size: 0.92rem;
    box-shadow: var(--shadow);
}

.divider {
    border: none;
    border-top: 1px solid var(--border-mid);
    margin: 18px 0;
}

.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 12px;
}

.stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--card-bg-strong);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.9rem;
    color: var(--text);
    box-shadow: var(--shadow);
}

.empty-state {
    background: var(--card-bg-strong);
    border: 1.5px dashed var(--border-mid);
    border-radius: 20px;
    padding: 56px 28px;
    text-align: center;
    box-shadow: var(--shadow);
}

/* Warning / info override */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--border-mid) !important;
}

/* Image caption */
[data-testid="caption"] { color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
SLOGANS = [
    "♻️  Reduce. Reuse. Recycle.",
    "🌿  Go Green, Keep It Clean",
    "🌍  Waste Today, Shortage Tomorrow",
    "🌱  Every Scan Counts for the Planet",
    "💧  Small Actions, Big Impact",
    "🔋  Recharge the Earth, Not Just Your Phone",
]

ECO_TIPS = [
    "Carry a reusable bag — it takes 500 years for a plastic bag to decompose.",
    "Turn off the tap while brushing your teeth and save up to 8 litres per minute.",
    "Compost food scraps to cut household waste by up to 30%.",
    "Buy second-hand before buying new — fashion is the second-largest polluter.",
    "Use a bamboo toothbrush; plastic ones fill 50 million kg of landfill each year.",
    "Unplug chargers when idle — standby power wastes 10% of household electricity.",
    "Choose products with minimal or recyclable packaging when shopping.",
    "Plant one tree this year — a single tree absorbs ~22 kg of CO₂ annually.",
    "Opt for a reusable coffee cup — 500 billion disposable cups are used every year.",
    "Buy local produce to reduce food miles and support your community.",
]

RECYCLING_TIPS = {
    "cardboard":   ["Flatten before recycling to save space", "Remove all tape, staples, and labels", "Keep dry — wet cardboard cannot be recycled"],
    "glass":       ["Rinse bottles and jars before recycling", "Do not mix broken glass in regular bins", "Glass can be recycled indefinitely without quality loss"],
    "metal":       ["Crush cans to save bin space", "Rinse food residue from tins and cans", "Aluminium recycling saves 95% of energy vs virgin production"],
    "paper":       ["Shred confidential documents before recycling", "Avoid recycling waxed or heavily greasy paper", "Newspaper, office paper and magazines are all recyclable"],
    "plastic":     ["Check the resin code (1–7) printed on the bottom", "Rinse containers thoroughly before recycling", "Remove lids if made from a different plastic type"],
    "trash":       ["Separate recyclables before general disposal", "Consider composting the organic portion", "Contact your municipality for hazardous waste drop-off"],
    "biological":  ["Compost fruit and vegetable scraps at home", "Use a city green bin for cooked food and meat", "Avoid composting dairy or meat in a home composter"],
    "clothes":     ["Donate wearable clothes to charities or shelters", "Cut worn fabric into useful cleaning rags", "Look for textile recycling bins near you"],
    "shoes":       ["Donate usable shoes to local shelters or NGOs", "Some brands run take-back programmes", "Separate rubber soles for industrial recycling"],
    "batteries":   ["Never throw batteries in regular trash — toxic!", "Drop off at electronics stores or municipality points", "Rechargeable batteries significantly reduce waste"],
    "e-waste":     ["Bring to a certified e-waste recycling centre", "Wipe personal data before recycling any device", "Many manufacturers offer device take-back programmes"],
    "white-glass": ["Same rules as regular glass — rinse and recycle", "Keep separate from coloured glass if required locally", "Reuse jars for food storage before recycling"],
    "brown-glass": ["Rinse before placing in the glass bin", "Brown glass (usually beer/sauce bottles) is highly recyclable", "Check local guidelines for colour separation"],
    "green-glass": ["Rinse and recycle with the glass stream", "Most wine and olive oil bottles are green glass", "Reuse as decorative vases or planters before recycling"],
}

RECYCLABLE_CLASSES = {
    "cardboard", "glass", "metal", "paper", "plastic",
    "biological", "white-glass", "brown-glass", "green-glass",
}

CHATBOT_KB = {
    ("plastic", "reduce plastic", "plastic waste", "single use"):
        "🧴 Switch to reusable water bottles and bags. Buy in bulk to reduce packaging. Choose products in glass or cardboard instead of plastic whenever possible.",
    ("paper", "paper waste", "save paper"):
        "📄 Go digital where possible. Print double-sided. Use both sides of notebooks. Recycled paper requires 70% less energy to produce than virgin paper.",
    ("composting", "compost", "food waste", "organic", "kitchen waste"):
        "🌱 Composting converts kitchen scraps into nutrient-rich soil. Start with a simple bin. Fruits, vegetables, coffee grounds, and eggshells are all great inputs.",
    ("recycling", "how to recycle", "recycle", "sorting waste"):
        "♻️ Rinse containers before recycling, check your local guidelines, and separate by material type. When in doubt, check the resin code on the packaging.",
    ("energy", "electricity", "save energy", "power", "carbon"):
        "⚡ Switch to LED bulbs, unplug unused devices, use cold-water laundry cycles, and consider rooftop solar panels for long-term savings.",
    ("water", "save water", "water waste", "tap"):
        "💧 Fix dripping taps, take shorter showers, run the dishwasher only when full, and collect rainwater for watering plants.",
    ("e-waste", "electronics", "old phone", "old laptop", "gadget"):
        "📱 Drop electronics at certified e-waste centres. Many brands have take-back programmes. Never throw batteries or circuit boards in general waste.",
    ("clothes", "fashion", "textile", "clothing"):
        "👗 Buy second-hand first, mend before discarding, donate to charities, and look for fabric recycling bins in your area.",
    ("battery", "batteries", "lithium"):
        "🔋 Rechargeable batteries save money and reduce waste. Drop used batteries at collection points — they contain toxic heavy metals.",
    ("tip", "tips", "advice", "help", "eco", "green", "sustainable"):
        "🌍 Three quick wins: (1) carry a reusable bag everywhere, (2) say no to single-use cutlery and straws, (3) compost your kitchen scraps. Small habits, big impact!",
    ("hello", "hi", "hey", "greetings"):
        "👋 Hello! I'm EcoBot, your green assistant. Ask me about recycling, composting, reducing plastic, saving energy, or any sustainability topic!",
}

def chatbot_response(msg: str) -> str:
    msg_lower = msg.lower()
    for keys, reply in CHATBOT_KB.items():
        if any(k in msg_lower for k in keys):
            return reply
    return (
        "🤔 Great question! I'm best at topics like plastic reduction, paper recycling, "
        "composting, e-waste, energy saving, and water conservation. "
        "Try asking me about any of those — I'd love to help you go greener! 🌿"
    )

# ── Session state ──────────────────────────────────────────────────────────────
defaults = {
    "eco_score":    0,
    "waste_counts": {},
    "chat_history": [],
    "slogan_index": 0,
    "daily_tip":    random.choice(ECO_TIPS),
    "last_result":  None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:14px 0 10px 0;">
      <div style="font-size:2.4rem; margin-bottom:4px;">♻️</div>
      <div style="font-family:'Inter',sans-serif; font-size:1.3rem; font-weight:800;
        background:linear-gradient(135deg,#1A3A1A,#3A7D44,#5A9E62);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        EcoVision AI
      </div>
      <div style="font-size:0.7rem; color:#78909C; letter-spacing:2px; margin-top:2px;">
        WASTE INTELLIGENCE
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🏆 Eco Score</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="score-badge">🏆 {st.session_state.eco_score}</div>', unsafe_allow_html=True)
    st.caption("Earn +10 pts every time you correctly identify recyclable waste.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">💡 Daily Eco Tip</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tip-box">{st.session_state.daily_tip}</div>', unsafe_allow_html=True)
    if st.button("🎲 New Tip", use_container_width=True):
        st.session_state.daily_tip = random.choice(ECO_TIPS)
        st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Session Stats</div>', unsafe_allow_html=True)
    total_sess = sum(st.session_state.waste_counts.values())
    st.markdown(f"""
    <div class="stat-row">
      <span>Total Scans</span>
      <strong>{total_sess}</strong>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.waste_counts:
        top_cls = max(st.session_state.waste_counts, key=st.session_state.waste_counts.get)
        st.markdown(f"""
        <div class="stat-row">
          <span>Most Detected</span>
          <strong>{top_cls.title()}</strong>
        </div>
        """, unsafe_allow_html=True)
        rec_s = sum(v for k, v in st.session_state.waste_counts.items() if k in RECYCLABLE_CLASSES)
        rec_pct_s = rec_s / total_sess * 100 if total_sess else 0
        st.markdown(f"""
        <div class="stat-row">
          <span>Recycling Rate</span>
          <strong style="color:#3A7D44;">{rec_pct_s:.0f}%</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#78909C; font-size:0.75rem; padding-bottom:10px;">
      🌍 Building a greener planet<br>
      <strong style="color:#3A7D44;">EcoVision AI v3.0</strong>
    </div>
    """, unsafe_allow_html=True)

# ── Hero Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div class="hero-title">♻️ EcoVision AI</div>
  <div class="hero-sub">Smart Waste Detection &amp; Classification System</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

slogan = SLOGANS[st.session_state.slogan_index % len(SLOGANS)]
st.markdown(f'<div class="slogan-bar">{slogan}</div>', unsafe_allow_html=True)

col_slogan_btn, _ = st.columns([1, 6])
with col_slogan_btn:
    if st.button("▶ Next Slogan"):
        st.session_state.slogan_index += 1
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍  Classify Waste",
    "📷  Live Camera",
    "📊  Analytics",
    "🤖  Eco Chatbot",
])

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 1 — Classify Waste                                     ║
# ╚══════════════════════════════════════════════════════════════╝
with tab1:
    col_upload, col_result = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown('<div class="section-title">Upload an Image</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding:14px 20px; margin-bottom:14px;">
          <span style="font-size:0.88rem; color:#37474F;">
            📎 Upload a clear photo of the waste item. Supported formats: JPG, PNG, WEBP.
          </span>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drag & drop or click to browse",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.image(img, caption="Uploaded Image", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔍 Analyse Waste", use_container_width=True):
                progress_bar = st.progress(0)
                status_msg   = st.empty()
                steps = [
                    (20,  "⚙️ Preprocessing image…"),
                    (50,  "🧠 Running YOLOv8 model…"),
                    (80,  "📊 Ranking predictions…"),
                    (100, "✅ Done!"),
                ]
                for pct, msg in steps:
                    status_msg.markdown(
                        f'<span style="font-family:\'Space Mono\',monospace; font-size:0.8rem; color:#78909C;">{msg}</span>',
                        unsafe_allow_html=True
                    )
                    progress_bar.progress(pct)
                    time.sleep(0.25)

                top3 = predict_image(img)
                progress_bar.empty()
                status_msg.empty()

                st.session_state.last_result = top3
                top_label_l = top3[0][0].lower()
                top_conf    = top3[0][1]

                st.session_state.waste_counts[top_label_l] = (
                    st.session_state.waste_counts.get(top_label_l, 0) + 1
                )
                if top_conf >= 0.6 and top_label_l in RECYCLABLE_CLASSES:
                    st.session_state.eco_score += 10
                    st.toast("🌟 +10 Eco Score! Great recyclable find!", icon="🌱")

                st.rerun()

    with col_result:
        st.markdown('<div class="section-title">Classification Result</div>', unsafe_allow_html=True)

        if st.session_state.last_result:
            top3        = st.session_state.last_result
            top_label   = top3[0][0]
            top_conf    = top3[0][1]
            top_label_l = top_label.lower()
            recyclable  = top_label_l in RECYCLABLE_CLASSES

            # Primary result card
            if top_conf < 0.6:
                st.markdown("""
                <div class="glass-card" style="border-left:4px solid #F57F17;">
                  <div style="font-size:2.2rem; margin-bottom:8px;">⚠️</div>
                  <div class="result-big" style="color:#F57F17;">Mixed / Unclear</div>
                  <div style="color:#78909C; font-size:0.88rem; margin-top:10px; line-height:1.6;">
                    Confidence too low for reliable detection.<br>
                    Try a clearer, well-lit image.
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                badge_html = (
                    '<span class="badge-recyclable">♻️ RECYCLABLE</span>'
                    if recyclable else
                    '<span class="badge-nonrecyclable">🗑️ NON-RECYCLABLE</span>'
                )
                icon = "♻️" if recyclable else "🗑️"
                st.markdown(f"""
                <div class="glass-card glass-card-accent">
                  <div style="font-size:1.8rem; margin-bottom:6px;">{icon}</div>
                  <div class="result-big">{top_label.title()}</div>
                  <div style="margin-top:12px;">{badge_html}</div>
                </div>
                """, unsafe_allow_html=True)

            # Confidence bar
            st.markdown('<div class="conf-label">Top Prediction Confidence</div>', unsafe_allow_html=True)
            conf_color = "#3A7D44" if top_conf >= 0.6 else "#F57F17"
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:20px;">
              <div style="flex:1; background:rgba(0,121,107,0.12); border-radius:99px; height:14px; overflow:hidden; border:1px solid rgba(0,121,107,0.2);">
                <div style="width:{top_conf*100:.1f}%; height:100%;
                  background:linear-gradient(90deg,#235C2A,{conf_color});
                  border-radius:99px;"></div>
              </div>
              <span style="font-family:'Space Mono',monospace; font-size:0.92rem;
                color:{conf_color}; font-weight:700; min-width:58px; text-align:right;">{top_conf*100:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

            # Top-3 breakdown
            st.markdown('<div class="section-title">Top 3 Predictions</div>', unsafe_allow_html=True)
            rank_icons  = ["🥇", "🥈", "🥉"]
            rank_colors = ["#235C2A", "#3A7D44", "#5A9E62"]
            for rank, (lbl, prob) in enumerate(top3):
                st.markdown(f"""
                <div class="glass-card" style="padding:14px 18px; margin-bottom:10px;">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:0.92rem; font-weight:600; color:{'#1A3C38' if rank==0 else '#37474F'};">
                      {rank_icons[rank]} &nbsp;{lbl.title()}
                    </span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.82rem;
                      color:#78909C; font-weight:700;">{prob*100:.1f}%</span>
                  </div>
                  <div style="background:rgba(0,121,107,0.10); border-radius:99px; height:8px; overflow:hidden;">
                    <div style="width:{prob*100:.1f}%; height:100%;
                      background:{rank_colors[rank]}; border-radius:99px; opacity:{1 - rank*0.2:.1f};"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Recycling suggestions
            if top_conf >= 0.6:
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">♻️ Recycling Suggestions</div>', unsafe_allow_html=True)
                tips = RECYCLING_TIPS.get(
                    top_label_l,
                    [
                        "Separate this waste before disposal",
                        "Check your local municipality guidelines",
                        "When in doubt, ask your local waste authority",
                    ]
                )
                pills_html = "".join(f'<span class="label-pill">✔ {t}</span>' for t in tips)
                st.markdown(f'<div style="line-height:2.2;">{pills_html}</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="empty-state">
              <div style="font-size:4rem; margin-bottom:16px;">🌿</div>
              <div style="font-size:1.1rem; font-weight:600; color:#1A3C38; margin-bottom:8px;">
                Ready to Classify
              </div>
              <div style="color:#78909C; font-size:0.92rem; line-height:1.7;">
                Upload an image and click<br>
                <strong style="color:#3A7D44;">Analyse Waste</strong> to get started.
              </div>
            </div>
            """, unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 2 — Live Camera                                        ║
# ╚══════════════════════════════════════════════════════════════╝
with tab2:
    st.markdown('<div class="section-title">Live Camera Capture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="margin-bottom:18px;">
      📷 Point your camera at a waste item and capture a photo for instant classification.
      Works best in good lighting with the item clearly visible and centred.
    </div>
    """, unsafe_allow_html=True)

    cam_image = st.camera_input("Capture waste item", label_visibility="collapsed")

    if cam_image:
        cam_img = Image.open(cam_image).convert("RGB")
        col_c1, col_c2 = st.columns([1, 1], gap="large")

        with col_c1:
            st.image(cam_img, caption="Captured Frame", use_container_width=True)

        with col_c2:
            pb = st.progress(0)
            for p in [20, 50, 80, 100]:
                pb.progress(p)
                time.sleep(0.12)
            top3_cam = predict_image(cam_img)
            pb.empty()

            lbl_cam, conf_cam = top3_cam[0]
            lbl_cam_l  = lbl_cam.lower()
            rec_cam    = lbl_cam_l in RECYCLABLE_CLASSES

            st.session_state.waste_counts[lbl_cam_l] = (
                st.session_state.waste_counts.get(lbl_cam_l, 0) + 1
            )
            if conf_cam >= 0.6 and rec_cam:
                st.session_state.eco_score += 10
                st.toast("🌟 +10 Eco Score!", icon="🌱")

            if conf_cam < 0.6:
                st.warning("⚠️ Mixed or unclear waste detected. Try better lighting or a closer shot.")
            else:
                badge_html = (
                    '<span class="badge-recyclable">♻️ RECYCLABLE</span>'
                    if rec_cam else
                    '<span class="badge-nonrecyclable">🗑️ NON-RECYCLABLE</span>'
                )
                st.markdown(f"""
                <div class="glass-card glass-card-accent">
                  <div class="result-big">{lbl_cam.title()}</div>
                  <div style="margin-top:10px;">{badge_html}</div>
                </div>
                """, unsafe_allow_html=True)

            conf_color_c = "#3A7D44" if conf_cam >= 0.6 else "#F57F17"
            st.markdown(f"""
            <div class="conf-label" style="margin-top:12px;">CONFIDENCE</div>
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:18px;">
              <div style="flex:1; background:rgba(0,121,107,0.12); border-radius:99px; height:12px; overflow:hidden; border:1px solid rgba(0,121,107,0.2);">
                <div style="width:{conf_cam*100:.1f}%; height:100%;
                  background:linear-gradient(90deg,#235C2A,{conf_color_c}); border-radius:99px;"></div>
              </div>
              <span style="font-family:'Space Mono',monospace; font-size:0.88rem; font-weight:700; color:{conf_color_c};">
                {conf_cam*100:.1f}%
              </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-title">Top 3 Predictions</div>', unsafe_allow_html=True)
            rank_icons = ["🥇", "🥈", "🥉"]
            for rank, (l, p) in enumerate(top3_cam):
                st.markdown(f"""
                <div class="glass-card" style="padding:10px 16px; margin-bottom:8px;">
                  <div style="display:flex; justify-content:space-between;">
                    <span style="font-weight:600; font-size:0.88rem;">{rank_icons[rank]} {l.title()}</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#78909C;">{p*100:.1f}%</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 3 — Analytics Dashboard                                ║
# ╚══════════════════════════════════════════════════════════════╝
with tab3:
    st.markdown('<div class="section-title">Session Analytics Dashboard</div>', unsafe_allow_html=True)

    if st.session_state.waste_counts:
        counts      = st.session_state.waste_counts
        total_s     = sum(counts.values())
        rec_count   = sum(v for k, v in counts.items() if k in RECYCLABLE_CLASSES)
        non_rec     = total_s - rec_count
        rec_pct     = (rec_count / total_s * 100) if total_s else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Scans",     total_s)
        k2.metric("Recyclable ♻️",   rec_count)
        k3.metric("Non-Recyclable",  non_rec)
        k4.metric("Eco Score 🏆",    st.session_state.eco_score)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Recycling rate bar
        st.markdown('<div class="section-title">Recycling Rate</div>', unsafe_allow_html=True)
        rate_color = "#3A7D44" if rec_pct >= 50 else "#F57F17"
        st.markdown(f"""
        <div class="glass-card" style="padding:18px 24px;">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
            <span style="font-weight:600; color:#1A3C38;">♻️ Recyclable vs 🗑️ Non-Recyclable</span>
            <span style="font-family:'Space Mono',monospace; font-size:1.1rem; font-weight:700; color:{rate_color};">{rec_pct:.1f}%</span>
          </div>
          <div style="background:rgba(0,121,107,0.12); border-radius:99px; height:20px; overflow:hidden; border:1px solid rgba(0,121,107,0.15);">
            <div style="width:{rec_pct:.1f}%; height:100%;
              background:linear-gradient(90deg,#235C2A,#5A9E62); border-radius:99px;
              display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">
              <span style="font-size:0.7rem; color:rgba(255,255,255,0.9); font-weight:600;">{rec_pct:.0f}%</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_chart, col_breakdown = st.columns([3, 2], gap="large")

        with col_chart:
            st.markdown('<div class="section-title">Waste Type Distribution</div>', unsafe_allow_html=True)
            import pandas as pd
            df = pd.DataFrame(list(counts.items()), columns=["Waste Type", "Count"])
            df["Waste Type"] = df["Waste Type"].str.title()
            df = df.sort_values("Count", ascending=False)
            st.bar_chart(df.set_index("Waste Type"), color="#3A7D44", height=280)

        with col_breakdown:
            st.markdown('<div class="section-title">Class Breakdown</div>', unsafe_allow_html=True)
            for wtype, cnt in sorted(counts.items(), key=lambda x: -x[1]):
                pct = cnt / total_s * 100
                icon = "♻️" if wtype in RECYCLABLE_CLASSES else "🗑️"
                bar_c = "#3A7D44" if wtype in RECYCLABLE_CLASSES else "#C62828"
                st.markdown(f"""
                <div class="glass-card" style="padding:12px 16px; margin-bottom:8px;">
                  <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-size:0.88rem; font-weight:500;">{icon} {wtype.title()}</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.78rem;
                      color:#78909C;">{cnt} ({pct:.0f}%)</span>
                  </div>
                  <div style="background:rgba(0,121,107,0.10); border-radius:99px; height:7px; overflow:hidden;">
                    <div style="width:{pct:.0f}%; height:100%;
                      background:{bar_c}; border-radius:99px; opacity:0.75;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        if st.button("🗑️  Reset Analytics & Score", use_container_width=False):
            st.session_state.waste_counts = {}
            st.session_state.eco_score    = 0
            st.session_state.last_result  = None
            st.rerun()

    else:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:4rem; margin-bottom:16px;">📊</div>
          <div style="font-size:1.1rem; font-weight:600; color:#1A3C38; margin-bottom:8px;">
            No Data Yet
          </div>
          <div style="color:#78909C; font-size:0.92rem; line-height:1.7;">
            Start classifying waste in the
            <strong style="color:#3A7D44;">Classify Waste</strong> tab
            to see your analytics here.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 4 — Eco Chatbot                                        ║
# ╚══════════════════════════════════════════════════════════════╝
with tab4:
    st.markdown('<div class="section-title">🤖 EcoBot — Your Green Assistant</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="margin-bottom:16px;">
      Ask anything about recycling, composting, reducing plastic, saving energy, or eco-tips!<br>
      <small style="color:#78909C; margin-top:4px; display:block;">
        Try: "How do I reduce plastic?" &nbsp;·&nbsp; "Tips for composting" &nbsp;·&nbsp;
        "What about e-waste?" &nbsp;·&nbsp; "How to save water?"
      </small>
    </div>
    """, unsafe_allow_html=True)

    # Quick suggestion pills
    suggestions = [
        "♻️ How to recycle?",
        "🧴 Reduce plastic",
        "🌱 Composting tips",
        "⚡ Save energy",
        "💧 Save water",
        "📱 E-waste advice",
    ]
    pill_cols = st.columns(len(suggestions))
    for i, sugg in enumerate(suggestions):
        with pill_cols[i]:
            if st.button(sugg, key=f"sugg_{i}", use_container_width=True):
                st.session_state.chat_history.append(("user", sugg))
                st.session_state.chat_history.append(("bot", chatbot_response(sugg)))
                st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Chat history display
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center; padding:36px; color:#78909C; font-size:0.92rem; line-height:1.8;">
          🌿 Start the conversation with a quick suggestion above,<br>or type your question below.
        </div>
        """, unsafe_allow_html=True)
    else:
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-bubble-user">🧑 &nbsp;{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-bot">🤖 &nbsp;{msg}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Ask EcoBot anything…")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", chatbot_response(user_input)))
        st.rerun()

    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
