import streamlit as st
import json
import random
import math

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ankim-Card & Calc",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open("data/flashcards.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
categories = data["categories"]

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;700&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --cream:    #F5F0E8;
    --cream2:   #EDE6D6;
    --green:    #2D5A3D;
    --green2:   #3D7A52;
    --green3:   #4E9A68;
    --green-lt: #C8DDD1;
    --brown:    #6B4F3A;
    --brown-lt: #C4A882;
    --text:     #2C2416;
    --text2:    #5C4A32;
    --white:    #FEFCF8;
    --shadow:   0 4px 20px rgba(45,90,61,0.12);
    --shadow2:  0 8px 32px rgba(45,90,61,0.18);
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    background-color: var(--cream);
    color: var(--text);
}

.stApp {
    background: linear-gradient(160deg, var(--cream) 0%, var(--cream2) 100%);
    min-height: 100vh;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 760px; }

/* ── TYPOGRAPHY ── */
h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: var(--green);
}

/* ── HEADER ── */
.site-header {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    border-bottom: 2px solid var(--green-lt);
    margin-bottom: 2rem;
}
.site-header .logo {
    font-size: 2.6rem;
    font-family: 'Playfair Display', serif;
    color: var(--green);
    letter-spacing: -1px;
    line-height: 1.1;
}
.site-header .logo span {
    color: var(--brown);
}
.site-header .tagline {
    font-size: 0.85rem;
    color: var(--text2);
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
    font-style: italic;
}

/* ── NAV TABS ── */
.nav-row {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin: 1.2rem 0 0;
}
.nav-btn {
    padding: 0.5rem 1.8rem;
    border-radius: 50px;
    font-family: 'Lato', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.04em;
    cursor: pointer;
    border: 2px solid var(--green);
    transition: all 0.2s;
}
.nav-btn.active {
    background: var(--green);
    color: var(--white);
}
.nav-btn.inactive {
    background: transparent;
    color: var(--green);
}

/* ── CATEGORY CARDS ── */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.2rem;
    margin-top: 1.5rem;
}
.cat-card {
    background: var(--white);
    border: 1.5px solid var(--green-lt);
    border-radius: 16px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}
.cat-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow2);
}
.cat-card .cat-icon { font-size: 2.4rem; margin-bottom: 0.6rem; }
.cat-card .cat-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--green);
    margin-bottom: 0.4rem;
}
.cat-card .cat-desc {
    font-size: 0.78rem;
    color: var(--text2);
    line-height: 1.5;
    margin-bottom: 1rem;
}
.cat-card .cat-count {
    font-size: 0.75rem;
    color: var(--green3);
    font-weight: 700;
    margin-bottom: 0.8rem;
}

/* ── FLASHCARD ── */
.flashcard-wrap {
    perspective: 1200px;
    width: 100%;
    max-width: 600px;
    height: 280px;
    margin: 1.5rem auto;
    cursor: pointer;
}
.flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.55s cubic-bezier(0.4, 0, 0.2, 1);
}
.flashcard-inner.flipped {
    transform: rotateY(180deg);
}
.flashcard-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    box-sizing: border-box;
    text-align: center;
}
.flashcard-front {
    background: var(--white);
    border: 2px solid var(--green-lt);
    box-shadow: var(--shadow2);
}
.flashcard-back {
    background: var(--green);
    border: 2px solid var(--green2);
    box-shadow: var(--shadow2);
    transform: rotateY(180deg);
}
.flashcard-front .label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brown-lt);
    margin-bottom: 0.8rem;
}
.flashcard-front .question {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: var(--text);
    line-height: 1.6;
}
.flashcard-front .hint {
    position: absolute;
    bottom: 1rem;
    font-size: 0.72rem;
    color: var(--brown-lt);
    font-style: italic;
}
.flashcard-back .label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 0.8rem;
}
.flashcard-back .answer {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    color: var(--white);
    line-height: 1.6;
    font-weight: 600;
}

/* ── PROGRESS BAR ── */
.progress-wrap {
    margin: 0.5rem 0 1rem;
}
.progress-label {
    font-size: 0.78rem;
    color: var(--text2);
    margin-bottom: 0.3rem;
    display: flex;
    justify-content: space-between;
}
.progress-bar-bg {
    background: var(--green-lt);
    border-radius: 50px;
    height: 8px;
    overflow: hidden;
}
.progress-bar-fill {
    background: linear-gradient(90deg, var(--green2), var(--green3));
    height: 100%;
    border-radius: 50px;
    transition: width 0.4s ease;
}

/* ── SCORE BADGE ── */
.score-badges {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 0.5rem 0;
}
.badge {
    padding: 0.3rem 1rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 700;
}
.badge-ingat { background: #D4EDDA; color: #155724; }
.badge-lupa  { background: #F8D7DA; color: #721C24; }

/* ── RESULT SCREEN ── */
.result-box {
    background: var(--white);
    border: 1.5px solid var(--green-lt);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: var(--shadow2);
    margin-top: 1rem;
}
.result-box .result-emoji { font-size: 4rem; margin-bottom: 0.5rem; }
.result-box .result-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: var(--green);
    margin-bottom: 0.3rem;
}
.result-box .result-score {
    font-size: 3rem;
    font-weight: 700;
    color: var(--green2);
    margin: 0.5rem 0;
}
.result-box .result-sub { font-size: 0.9rem; color: var(--text2); }

/* ── KALKULATOR ── */
.calc-card {
    background: var(--white);
    border: 1.5px solid var(--green-lt);
    border-radius: 20px;
    padding: 1.8rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.5rem;
}
.calc-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: var(--green);
    margin-bottom: 0.3rem;
}
.calc-formula {
    background: var(--cream2);
    border-left: 4px solid var(--green3);
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    font-size: 0.88rem;
    color: var(--text2);
    margin-bottom: 1.2rem;
    font-family: 'Georgia', serif;
    font-style: italic;
}
.result-output {
    background: linear-gradient(135deg, var(--green) 0%, var(--green2) 100%);
    color: var(--white);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    margin-top: 1rem;
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
}
.result-output small {
    display: block;
    font-family: 'Lato', sans-serif;
    font-size: 0.75rem;
    opacity: 0.75;
    margin-bottom: 0.2rem;
}

/* ── BUTTONS (override Streamlit) ── */
.stButton > button {
    background: var(--green) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover {
    background: var(--green2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(45,90,61,0.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── INGAT / LUPA buttons ── */
.btn-ingat > button {
    background: #2D7A4F !important;
}
.btn-lupa > button {
    background: #A0453A !important;
}
.btn-back > button {
    background: transparent !important;
    color: var(--green) !important;
    border: 1.5px solid var(--green) !important;
}

/* ── INPUT OVERRIDE ── */
.stNumberInput input, .stSelectbox select {
    background: var(--cream) !important;
    border: 1.5px solid var(--green-lt) !important;
    border-radius: 10px !important;
    font-family: 'Lato', sans-serif !important;
    color: var(--text) !important;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--green);
    margin-bottom: 0.2rem;
}
.section-sub {
    font-size: 0.85rem;
    color: var(--text2);
    margin-bottom: 1.5rem;
}

/* ── REVIEW LIST ── */
.review-item {
    background: #FFF8F5;
    border: 1.5px solid #F0CFC0;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    color: var(--text);
}
.review-item strong { color: var(--brown); }

/* ── DIVIDER ── */
.styled-hr {
    border: none;
    border-top: 1.5px solid var(--green-lt);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
def init_state():
    defaults = {
        "mode": "flashcard",          # "flashcard" | "kalkulator"
        "view": "menu",               # "menu" | "session" | "result"
        "category_id": None,
        "deck": [],
        "current_idx": 0,
        "flipped": False,
        "score_ingat": 0,
        "score_lupa": 0,
        "wrong_cards": [],
        "answered": False,
        "review_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── HELPER ──────────────────────────────────────────────────────────────────
def get_category(cat_id):
    return next((c for c in categories if c["id"] == cat_id), None)

def start_session(cat_id, shuffle=True, review_cards=None):
    cat = get_category(cat_id)
    deck = review_cards if review_cards else list(cat["cards"])
    if shuffle:
        random.shuffle(deck)
    st.session_state.category_id = cat_id
    st.session_state.deck = deck
    st.session_state.current_idx = 0
    st.session_state.flipped = False
    st.session_state.score_ingat = 0
    st.session_state.score_lupa = 0
    st.session_state.wrong_cards = []
    st.session_state.answered = False
    st.session_state.review_mode = bool(review_cards)
    st.session_state.view = "session"

def progress_html(current, total):
    pct = int((current / total) * 100) if total > 0 else 0
    return f"""
    <div class="progress-wrap">
        <div class="progress-label">
            <span>Kartu {current} dari {total}</span>
            <span>{pct}%</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%"></div>
        </div>
    </div>
    """

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
    <div class="logo">Ankim<span>-Card</span> &amp; Calc</div>
    <div class="tagline">Asisten Pintar Hafalan Reaksi &amp; Perhitungan Larutan AKA</div>
    <div class="nav-row">
        <span class="nav-btn {fc}" id="nav-flash">🃏 Flashcard</span>
        <span class="nav-btn {cc}" id="nav-calc">🧮 Kalkulator</span>
    </div>
</div>
""".format(
    fc="active" if st.session_state.mode == "flashcard" else "inactive",
    cc="active" if st.session_state.mode == "kalkulator" else "inactive"
), unsafe_allow_html=True)

col_f, col_c = st.columns(2)
with col_f:
    if st.button("🃏 Flashcard", key="nav_flash", use_container_width=True):
        st.session_state.mode = "flashcard"
        st.session_state.view = "menu"
        st.rerun()
with col_c:
    if st.button("🧮 Kalkulator", key="nav_calc", use_container_width=True):
        st.session_state.mode = "kalkulator"
        st.rerun()

st.markdown("<hr class='styled-hr'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FLASHCARD MODE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.mode == "flashcard":

    # ── MENU ──────────────────────────────────────────────────────────────────
    if st.session_state.view == "menu":
        st.markdown('<div class="section-title">Pilih Kategori</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Klik tombol "Mulai Belajar" untuk memulai sesi flashcard.</div>', unsafe_allow_html=True)

        for cat in categories:
            total = len(cat["cards"])
            with st.container():
                st.markdown(f"""
                <div class="cat-card">
                    <div class="cat-icon">{cat['icon']}</div>
                    <div class="cat-name">{cat['name']}</div>
                    <div class="cat-desc">{cat['description']}</div>
                    <div class="cat-count">📋 {total} kartu</div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button(f"🚀 Mulai Belajar", key=f"start_{cat['id']}", use_container_width=True):
                        start_session(cat["id"], shuffle=False)
                        st.rerun()
                with col2:
                    if st.button(f"🔀 Acak", key=f"shuffle_{cat['id']}", use_container_width=True):
                        start_session(cat["id"], shuffle=True)
                        st.rerun()

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── SESSION ───────────────────────────────────────────────────────────────
    elif st.session_state.view == "session":
        cat = get_category(st.session_state.category_id)
        deck = st.session_state.deck
        idx = st.session_state.current_idx
        total = len(deck)
        card = deck[idx]

        # Back button
        bcol, _ = st.columns([1, 3])
        with bcol:
            st.markdown('<div class="btn-back">', unsafe_allow_html=True)
            if st.button("← Ganti Kategori", key="back_btn"):
                st.session_state.view = "menu"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Title + progress
        label = "🔁 Sesi Ulang" if st.session_state.review_mode else cat["name"]
        st.markdown(f"<div style='text-align:center;font-family:Playfair Display,serif;font-size:1.2rem;color:var(--green);margin-bottom:0.3rem'>{cat['icon']} {label}</div>", unsafe_allow_html=True)
        st.markdown(progress_html(idx + 1, total), unsafe_allow_html=True)

        # Score badges
        st.markdown(f"""
        <div class="score-badges">
            <span class="badge badge-ingat">👍 Ingat: {st.session_state.score_ingat}</span>
            <span class="badge badge-lupa">❌ Lupa: {st.session_state.score_lupa}</span>
        </div>
        """, unsafe_allow_html=True)

        # Flashcard — use JS-driven flip via unique key
        flip_class = "flipped" if st.session_state.flipped else ""
        card_html = f"""
        <div class="flashcard-wrap" onclick="flipCard()">
            <div class="flashcard-inner {flip_class}" id="fc-inner">
                <div class="flashcard-face flashcard-front">
                    <div class="label">— Pertanyaan —</div>
                    <div class="question">{card['front']}</div>
                    <div class="hint">Ketuk kartu untuk melihat jawaban ↩</div>
                </div>
                <div class="flashcard-face flashcard-back">
                    <div class="label">— Jawaban —</div>
                    <div class="answer">{card['back']}</div>
                </div>
            </div>
        </div>
        <script>
        function flipCard() {{
            var el = document.getElementById('fc-inner');
            el.classList.toggle('flipped');
        }}
        </script>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        # Flip toggle button
        flip_label = "👁️ Lihat Jawaban" if not st.session_state.flipped else "🔁 Sembunyikan"
        if st.button(flip_label, key="flip_btn", use_container_width=True):
            st.session_state.flipped = not st.session_state.flipped
            st.rerun()

        # Answer buttons (always visible after flip toggle area)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="btn-lupa">', unsafe_allow_html=True)
            if st.button("❌ Lupa / Salah", key="lupa_btn", use_container_width=True):
                st.session_state.score_lupa += 1
                st.session_state.wrong_cards.append(card)
                st.session_state.flipped = False
                if idx + 1 >= total:
                    st.session_state.view = "result"
                else:
                    st.session_state.current_idx += 1
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="btn-ingat">', unsafe_allow_html=True)
            if st.button("👍 Ingat / Benar", key="ingat_btn", use_container_width=True):
                st.session_state.score_ingat += 1
                st.session_state.flipped = False
                if idx + 1 >= total:
                    st.session_state.view = "result"
                else:
                    st.session_state.current_idx += 1
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ── RESULT ────────────────────────────────────────────────────────────────
    elif st.session_state.view == "result":
        cat = get_category(st.session_state.category_id)
        total = st.session_state.score_ingat + st.session_state.score_lupa
        pct = int((st.session_state.score_ingat / total) * 100) if total > 0 else 0

        if pct == 100:
            emoji, title = "🏆", "Sempurna!"
        elif pct >= 70:
            emoji, title = "🌿", "Bagus!"
        elif pct >= 40:
            emoji, title = "📚", "Terus Belajar!"
        else:
            emoji, title = "💪", "Jangan Menyerah!"

        st.markdown(f"""
        <div class="result-box">
            <div class="result-emoji">{emoji}</div>
            <div class="result-title">{title}</div>
            <div class="result-score">{st.session_state.score_ingat}/{total}</div>
            <div class="result-sub">Kartu benar &nbsp;•&nbsp; Akurasi <strong>{pct}%</strong></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        wrong = st.session_state.wrong_cards
        if wrong:
            st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:var(--brown);margin:1rem 0 0.5rem'>📌 Kartu yang perlu diulang ({len(wrong)})</div>", unsafe_allow_html=True)
            for w in wrong:
                st.markdown(f'<div class="review-item">❓ {w["front"]}<br><strong>✅ {w["back"]}</strong></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔁 Ulangi Semua", use_container_width=True):
                start_session(st.session_state.category_id, shuffle=False)
                st.rerun()
        with c2:
            if wrong:
                if st.button(f"⚡ Ulang Salah ({len(wrong)})", use_container_width=True):
                    start_session(st.session_state.category_id, shuffle=True, review_cards=wrong)
                    st.rerun()
        with c3:
            if st.button("🏠 Menu Utama", use_container_width=True):
                st.session_state.view = "menu"
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# KALKULATOR MODE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "kalkulator":
    st.markdown('<div class="section-title">🧮 Kalkulator Kimia</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pilih jenis perhitungan di bawah ini.</div>', unsafe_allow_html=True)

    # ── PENGENCERAN ───────────────────────────────────────────────────────────
    with st.expander("🧪 Kalkulator Pengenceran Larutan", expanded=True):
        st.markdown('<div class="calc-formula">Rumus: C₁ × V₁ = C₂ × V₂ &nbsp;&nbsp;(C = konsentrasi, V = volume dalam mL)</div>', unsafe_allow_html=True)

        unit = st.selectbox("Satuan konsentrasi", ["M (Molar)", "N (Normal)", "% (Persen)", "ppm"], key="dil_unit")
        col1, col2 = st.columns(2)
        with col1:
            c1 = st.number_input("C₁ – Konsentrasi Awal", min_value=0.0, value=0.0, format="%.4f", key="dil_c1")
        with col2:
            c2 = st.number_input("C₂ – Konsentrasi Akhir", min_value=0.0, value=0.0, format="%.4f", key="dil_c2")
        v2 = st.number_input("V₂ – Volume Akhir (mL)", min_value=0.0, value=0.0, format="%.2f", key="dil_v2")

        if st.button("Hitung V₁", key="calc_dil"):
            if c1 > 0 and c2 > 0 and v2 > 0:
                v1 = (c2 * v2) / c1
                st.markdown(f"""
                <div class="result-output">
                    <small>📢 Hasil Akhir (V₁)</small>
                    {v1:.4f} mL
                </div>
                """, unsafe_allow_html=True)
                if v1 > v2:
                    st.warning("⚠️ V₁ > V₂ — Konsentrasi akhir lebih besar dari awal. Periksa kembali nilai Anda.")
            else:
                st.error("Isi semua kolom dengan nilai > 0.")

    # ── MOLARITAS ─────────────────────────────────────────────────────────────
    with st.expander("⚖️ Kalkulator Molaritas (M)", expanded=False):
        st.markdown('<div class="calc-formula">Rumus: M = massa (g) / [BM (g/mol) × Volume (L)]</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            massa_m = st.number_input("Massa zat (gram)", min_value=0.0, value=0.0, format="%.4f", key="mol_massa")
        with col2:
            bm = st.number_input("Berat Molekul / BM (g/mol)", min_value=0.0, value=0.0, format="%.4f", key="mol_bm")
        with col3:
            vol_m = st.number_input("Volume larutan (L)", min_value=0.0, value=0.0, format="%.4f", key="mol_vol")

        if st.button("Hitung Molaritas", key="calc_mol"):
            if massa_m > 0 and bm > 0 and vol_m > 0:
                M = massa_m / (bm * vol_m)
                st.markdown(f"""
                <div class="result-output">
                    <small>📢 Konsentrasi Molaritas (M)</small>
                    {M:.4f} mol/L
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Isi semua kolom dengan nilai > 0.")

    # ── NORMALITAS ────────────────────────────────────────────────────────────
    with st.expander("⚗️ Kalkulator Normalitas (N)", expanded=False):
        st.markdown('<div class="calc-formula">Rumus: N = massa (g) / [BE (g/grek) × Volume (L)]</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            massa_n = st.number_input("Massa zat (gram)", min_value=0.0, value=0.0, format="%.4f", key="norm_massa")
        with col2:
            be = st.number_input("Berat Ekuivalen / BE (g/grek)", min_value=0.0, value=0.0, format="%.4f", key="norm_be")
        with col3:
            vol_n = st.number_input("Volume larutan (L)", min_value=0.0, value=0.0, format="%.4f", key="norm_vol")

        if st.button("Hitung Normalitas", key="calc_norm"):
            if massa_n > 0 and be > 0 and vol_n > 0:
                N = massa_n / (be * vol_n)
                st.markdown(f"""
                <div class="result-output">
                    <small>📢 Konsentrasi Normalitas (N)</small>
                    {N:.4f} grek/L
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Isi semua kolom dengan nilai > 0.")

    # ── KONVERSI SATUAN ───────────────────────────────────────────────────────
    with st.expander("🔄 Konversi Satuan Konsentrasi", expanded=False):
        st.markdown('<div class="calc-formula">Konversi antar satuan konsentrasi yang umum dipakai di lab.</div>', unsafe_allow_html=True)

        conv_type = st.selectbox("Pilih konversi", [
            "ppm → mg/L",
            "mg/L → ppm",
            "% (b/v) → g/L",
            "g/L → % (b/v)",
            "mol/L → mg/L (butuh BM)",
            "mg/L → mol/L (butuh BM)",
        ], key="conv_type")

        val_in = st.number_input("Nilai input", min_value=0.0, value=0.0, format="%.6f", key="conv_val")

        bm_conv = None
        if "BM" in conv_type:
            bm_conv = st.number_input("Berat Molekul / BM (g/mol)", min_value=0.0, value=0.0, format="%.4f", key="conv_bm")

        if st.button("Konversi", key="calc_conv"):
            result = None
            unit_out = ""
            try:
                if conv_type == "ppm → mg/L":
                    result = val_in * 1.0
                    unit_out = "mg/L"
                    note = "(1 ppm ≈ 1 mg/L dalam larutan encer)"
                elif conv_type == "mg/L → ppm":
                    result = val_in * 1.0
                    unit_out = "ppm"
                    note = "(1 mg/L ≈ 1 ppm dalam larutan encer)"
                elif conv_type == "% (b/v) → g/L":
                    result = val_in * 10.0
                    unit_out = "g/L"
                    note = "(1% b/v = 10 g/L)"
                elif conv_type == "g/L → % (b/v)":
                    result = val_in / 10.0
                    unit_out = "%"
                    note = "(10 g/L = 1% b/v)"
                elif conv_type == "mol/L → mg/L (butuh BM)":
                    if bm_conv and bm_conv > 0:
                        result = val_in * bm_conv * 1000
                        unit_out = "mg/L"
                        note = f"(mol/L × BM × 1000)"
                    else:
                        st.error("Masukkan nilai BM > 0.")
                elif conv_type == "mg/L → mol/L (butuh BM)":
                    if bm_conv and bm_conv > 0:
                        result = val_in / (bm_conv * 1000)
                        unit_out = "mol/L"
                        note = f"(mg/L ÷ (BM × 1000))"
                    else:
                        st.error("Masukkan nilai BM > 0.")

                if result is not None:
                    st.markdown(f"""
                    <div class="result-output">
                        <small>📢 Hasil Konversi ({unit_out}) &nbsp;·&nbsp; {note}</small>
                        {result:.6f} {unit_out}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<hr class='styled-hr'>
<div style='text-align:center;font-size:0.78rem;color:var(--brown-lt);padding-bottom:1rem'>
    🌿 Ankim-Card &amp; Calc &nbsp;·&nbsp; Asisten Hafalan &amp; Perhitungan Kimia Analitik
</div>
""", unsafe_allow_html=True)
