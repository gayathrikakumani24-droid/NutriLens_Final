#app.py
"""
NutriLens — Streamlit Frontend (app.py)
Theme: Dark green / cream / gold ("NutriLens AI" landing style)
Run with:  streamlit run app.py
Requires the FastAPI backend (main.py) running at http://localhost:8000
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ── Config ─────────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="NutriLens AI",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme colors ─────────────────────────────────────────────────────────────
DARK_GREEN   = "#1b2f1f"
DARKER_GREEN = "#14241a"
CREAM        = "#f4efe6"
GOLD         = "#e0a458"
TEXT_LIGHT   = "#f4efe6"
TEXT_DARK    = "#2b2b28"
MUTED        = "#9aa79c"

# ── Global CSS injection ──────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {{
        font-family: 'Inter', sans-serif;
    }}

    /* Main app background */
    .stApp {{
        background-color: {CREAM};
        color: {TEXT_DARK};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {DARK_GREEN};
    }}
    section[data-testid="stSidebar"] * {{
        color: {TEXT_LIGHT} !important;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background-color: {DARKER_GREEN};
        color: {TEXT_LIGHT};
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        text-align: left;
        font-weight: 500;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        border-color: {GOLD};
        color: {GOLD};
    }}

    /* Headings */
    h1, h2, h3 {{
        font-family: 'Playfair Display', serif;
        color: {TEXT_DARK};
        font-weight: 700;
    }}

    /* Accent text */
    .accent {{
        color: {GOLD};
    }}

    /* Primary buttons */
    .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {{
        background-color: {DARK_GREEN};
        color: {CREAM};
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
    }}
    .stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {{
        background-color: {GOLD};
        color: {DARK_GREEN};
    }}

    /* Secondary buttons */
    .stButton button[kind="secondary"], .stFormSubmitButton button[kind="secondary"] {{
        background-color: #ffffff;
        color: {TEXT_DARK};
        border: 1px solid #d8d2c4;
        border-radius: 10px;
        font-weight: 500;
    }}

    /* Inputs */
    .stTextInput > div > div > input, .stSelectbox div[data-baseweb="select"] > div {{
        background-color: #ffffff;
        border: 1px solid #d8d2c4;
        border-radius: 8px;
        color: {TEXT_DARK};
    }}

    /* Cards / feature boxes */
    .feature-card {{
        background-color: {DARKER_GREEN};
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: {TEXT_LIGHT};
    }}
    .feature-card .title {{
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 2px;
    }}
    .feature-card .desc {{
        font-size: 0.85rem;
        color: {MUTED};
    }}

    /* Pill tags */
    .pill {{
        display: inline-block;
        background-color: rgba(224,164,88,0.15);
        color: {GOLD};
        border: 1px solid {GOLD};
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        margin-right: 6px;
        margin-top: 8px;
    }}

    /* Metric cards */
    div[data-testid="stMetric"] {{
        background-color: #ffffff;
        border: 1px solid #e6e0d4;
        border-radius: 12px;
        padding: 12px 16px;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e6e0d4;
    }}

    /* Divider */
    hr {{
        border-color: #e0dac9;
    }}

    /* Card-like containers */
    .nl-panel {{
        background-color: #ffffff;
        border: 1px solid #e6e0d4;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
    }}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────────────
for key, default in {
    "logged_in": False,
    "username": "",
    "page": "analyze",
    "last_analysis": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Helpers ────────────────────────────────────────────────────────────────

DISEASE_OPTIONS = ["None", "Diabetes", "Hypertension", "Obesity"]

STATUS_COLOR = {"safe": "🟢", "caution": "🟡", "danger": "🔴"}


def api_post(endpoint: str, **kwargs):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", **kwargs)
        r.raise_for_status()
        return r.json(), None
    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, detail
    except Exception as e:
        return None, str(e)


def api_get(endpoint: str, **kwargs):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", **kwargs)
        r.raise_for_status()
        return r.json(), None
    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, detail
    except Exception as e:
        return None, str(e)


def nutrition_card(label, value, unit=""):
    st.metric(label=label, value=f"{value} {unit}".strip())


# ══════════════════════════════════════════════════════════════════════════
# AUTH PAGES (Landing-style split layout)
# ══════════════════════════════════════════════════════════════════════════

FEATURES = [
    ("📷", "Vision AI", "Detect food from any photo automatically"),
    ("📊", "FNDDS Database", "Verified nutrient data for 10,000+ foods"),
    ("🩺", "Medical AI", "Personalized for diabetes, hypertension & more"),
    ("⚖️", "Portion Vision", "Estimate serving size directly from image"),
]


def render_left_panel():
    st.markdown(f"""
    <div style="background-color:{DARK_GREEN}; padding:2.5rem; border-radius:18px; height:100%; color:{TEXT_LIGHT};">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:2.2rem;">
            <span style="font-size:1.6rem;">🥑</span>
            <span style="font-family:'Playfair Display', serif; font-size:1.4rem; font-weight:800;">
                Nutri<span style="color:{GOLD};">Lens</span> AI
            </span>
        </div>
        <h1 style="font-family:'Playfair Display', serif; color:{TEXT_LIGHT}; font-size:2.4rem; line-height:1.25; margin-bottom:1rem;">
            Upload any food photo —
            <span style="color:{GOLD};">know every nutrient instantly.</span>
        </h1>
        <p style="color:{MUTED}; font-size:0.95rem; margin-bottom:1.8rem;">
            Indian, Asian, or global — understand every calorie, macro, and micronutrient in your plate.
        </p>
    """, unsafe_allow_html=True)

    for icon, title, desc in FEATURES:
        st.markdown(f"""
        <div class="feature-card">
            <div class="title">{icon}&nbsp;&nbsp;{title}</div>
            <div class="desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="margin-top:1rem;">
            <span class="pill">FNDDS Verified</span>
            <span class="pill">Medical AI</span>
            <span class="pill">Indian Foods</span>
            <span class="pill">Free to use</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_login():
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        render_left_panel()

    with col_right:
        st.markdown("<div style='padding:1rem 2rem;'>", unsafe_allow_html=True)

        tab1, tab2 = st.columns(2)
        with tab1:
            if st.button("Sign In", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
        with tab2:
            if st.button("Create Account", use_container_width=True, type="secondary"):
                st.session_state.page = "register"
                st.rerun()

        st.markdown("### Welcome back")
        st.caption("Sign in to continue your nutrition journey")

        with st.form("login_form"):
            username = st.text_input("USERNAME", placeholder="Your username")
            password = st.text_input("PASSWORD", type="password", placeholder="••••••••••")
            submitted = st.form_submit_button("Sign In  →", type="primary", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                data, err = api_post(
                    "/api/auth/login",
                    json={"username": username, "password": password},
                )
                if err:
                    st.error(f"Login failed: {err}")
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(data.get("message", "Logged in!"))
                    st.rerun()

        st.markdown(
            "<p style='text-align:center; color:#9aa79c; margin-top:1rem;'>"
            "Don't have an account? "
            f"<a href='#' style='color:{GOLD}; font-weight:600;'>Create one</a></p>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


def page_register():
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        render_left_panel()

    with col_right:
        st.markdown("<div style='padding:1rem 2rem;'>", unsafe_allow_html=True)

        tab1, tab2 = st.columns(2)
        with tab1:
            if st.button("Sign In", use_container_width=True, type="secondary"):
                st.session_state.page = "login"
                st.rerun()
        with tab2:
            if st.button("Create Account", use_container_width=True, type="primary"):
                st.session_state.page = "register"
                st.rerun()

        st.markdown("### Create account")
        st.caption("Start your nutrition journey for free")

        with st.form("register_form"):
            username = st.text_input("USERNAME", placeholder="Choose a username")
            password = st.text_input("PASSWORD", type="password", placeholder="••••••••••")
            password2 = st.text_input("CONFIRM PASSWORD", type="password", placeholder="••••••••••")
            submitted = st.form_submit_button("Create Account  →", type="primary", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields.")
            elif password != password2:
                st.error("Passwords do not match.")
            else:
                data, err = api_post(
                    "/api/auth/register",
                    json={"username": username, "password": password},
                )
                if err:
                    st.error(f"Registration failed: {err}")
                else:
                    st.success(data.get("message", "Registered! Please log in."))
                    st.session_state.page = "login"
                    st.rerun()

        st.markdown(
            "<p style='font-size:0.78rem; color:#9aa79c; text-align:center; margin-top:0.8rem;'>"
            "By creating an account you agree to our Terms of Service and Privacy Policy.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; color:#9aa79c; margin-top:0.6rem;'>"
            "Already have an account? "
            f"<a href='#' style='color:{GOLD}; font-weight:600;'>Sign in</a></p>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# ANALYZE PAGE
# ══════════════════════════════════════════════════════════════════════════

def page_analyze():
    st.markdown(f"<h1>🔍 Analyze <span class='accent'>Food</span></h1>", unsafe_allow_html=True)
    st.write(f"Logged in as **{st.session_state.username}**")

    # ── Upload & Settings ──────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        uploaded_file = st.file_uploader(
            "Upload a food photo",
            type=["jpg", "jpeg", "png", "webp", "jfif"],
            help="Snap or upload a photo of your meal.",
        )
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded image", use_column_width=True)

    with col_right:
        disease = st.selectbox(
            "Do you have a medical condition?",
            DISEASE_OPTIONS,
            help="We'll tailor dietary advice to your condition.",
        )
        analyze_btn = st.button("🔬 Analyze", type="primary", use_container_width=True)

    if not uploaded_file:
        st.info("Please upload a food image to begin analysis.")
        return

    # ── Run Analysis ───────────────────────────────────────────────────────
    if analyze_btn:
        with st.spinner("Analysing your meal…"):
            file_bytes = uploaded_file.getvalue()
            files = {"file": (uploaded_file.name, BytesIO(file_bytes), uploaded_file.type)}
            data_form = {"disease": disease, "username": st.session_state.username}
            result, err = api_post("/api/analyze", files=files, data=data_form)

        if err:
            st.error(f"Analysis failed: {err}")
            return

        st.session_state.last_analysis = result
        st.session_state.last_disease = disease

    # ── Display Results ────────────────────────────────────────────────────
    result = st.session_state.get("last_analysis")
    disease = st.session_state.get("last_disease", "None")

    if not result:
        return

    per_food = result.get("per_food_data", [])
    if not per_food:
        st.warning("No food items detected.")
        return

    st.markdown("---")
    st.subheader(f"Detected {result.get('count', len(per_food))} food item(s)")

    # Tab per food item
    tab_labels = [f"{fd['emoji']} {fd['label'].title()}" for fd in per_food]
    tabs = st.tabs(tab_labels) if len(per_food) > 1 else [st.container()]

    for tab, fd in zip(tabs, per_food):
        with tab:
            _render_food_item(fd, disease)

    # ── Log a Meal ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📝 Log a Meal")
    if per_food:
        food_options = [f["label"].title() for f in per_food]
        selected_idx = st.selectbox("Select food to log", range(len(food_options)),
                                    format_func=lambda i: food_options[i])
        fd_to_log = per_food[selected_idx]
        nut = fd_to_log["nutrition"]

        if st.button("✅ Log this meal", type="primary"):
            payload = {
                "username":  st.session_state.username,
                "food_name": fd_to_log["label"],
                "caption":   fd_to_log["caption"],
                "calories":  nut["calories"],
                "protein":   nut["protein"],
                "carbs":     nut["carbs"],
                "fat":       nut["fat"],
                "portion":   fd_to_log["detected_portion"],
            }
            log_result, err = api_post("/api/meals/log", json=payload)
            if err:
                st.error(f"Logging failed: {err}")
            else:
                st.success("Meal logged successfully! 🎉")


def _render_food_item(fd: dict, disease: str):
    """Render nutrition card + AI recommendation for a single food."""
    status_icon = STATUS_COLOR.get(fd.get("status", "safe"), "🟢")
    st.markdown(f"### {fd['emoji']} {fd['label'].title()}  {status_icon}")
    st.caption(f"Confidence: {fd['confidence']:.0%} | Caption: {fd['caption']}")

    # Tags
    tags = fd.get("tags", [])
    if tags:
        tag_html = " ".join(
            f"<span style='background:#{'4caf50' if t['color']=='green' else 'ff9800' if t['color']=='yellow' else 'f44336'};color:white;padding:2px 8px;border-radius:12px;font-size:0.8em;margin-right:4px'>{t['label']}</span>"
            for t in tags
        )
        st.markdown(tag_html, unsafe_allow_html=True)

    st.markdown("")

    # Portion slider with live rescaling
    base_portion  = fd.get("base_portion", 100)
    init_portion  = fd.get("detected_portion", base_portion)
    base_nut      = fd.get("base_nutrition", fd.get("nutrition", {}))

    portion = st.slider(
        "Adjust portion (g)",
        min_value=25, max_value=500,
        value=int(init_portion), step=25,
        key=f"portion_{fd['index']}",
    )

    # Fetch scaled nutrition from API
    scaled_nut, err = api_get(
        "/api/scale",
        params={
            "base_calories":    base_nut.get("calories", 0),
            "base_protein":     base_nut.get("protein", 0),
            "base_carbs":       base_nut.get("carbs", 0),
            "base_fat":         base_nut.get("fat", 0),
            "base_portion":     base_nut.get("portion", base_portion),
            "current_portion":  portion,
            "disease":          disease,
            "food_name":        fd["label"],
        },
    )
    if err or not scaled_nut:
        scaled_nut = fd["nutrition"]  # fallback

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🔥 Calories",  f"{scaled_nut['calories']} kcal")
    with c2: st.metric("💪 Protein",   f"{scaled_nut['protein']} g")
    with c3: st.metric("🌾 Carbs",     f"{scaled_nut['carbs']} g")
    with c4: st.metric("🧈 Fat",       f"{scaled_nut['fat']} g")

    # Macro donut chart
    macro_fig = go.Figure(go.Pie(
        labels=["Protein", "Carbs", "Fat"],
        values=[scaled_nut["protein"], scaled_nut["carbs"], scaled_nut["fat"]],
        hole=0.55,
        marker_colors=[GOLD, DARK_GREEN, "#c97b4a"],
        textinfo="label+percent",
    ))
    macro_fig.update_layout(
        showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=220,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(macro_fig, use_container_width=True, key=f"pie_{fd['index']}")

    # AI Recommendation
    with st.expander("🤖 AI Dietary Recommendation", expanded=True):
        st.write(fd.get("ai_rec", "No recommendation available."))


# ══════════════════════════════════════════════════════════════════════════
# HISTORY PAGE
# ══════════════════════════════════════════════════════════════════════════

def page_history():
    st.markdown(f"<h1>📋 Meal <span class='accent'>History</span></h1>", unsafe_allow_html=True)
    username = st.session_state.username

    data, err = api_get(f"/api/meals/history/{username}")
    if err:
        st.error(f"Could not load history: {err}")
        return
    if not data:
        st.info("No meals logged yet. Go analyse some food! 🍴")
        return

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp", ascending=False)

    st.markdown("<div class='nl-panel'>", unsafe_allow_html=True)
    st.dataframe(
        df[["emoji", "food_name", "calories", "protein", "carbs", "fat", "portion", "timestamp"]].rename(
            columns={"emoji": "", "food_name": "Food", "calories": "Calories (kcal)",
                     "protein": "Protein (g)", "carbs": "Carbs (g)", "fat": "Fat (g)",
                     "portion": "Portion (g)", "timestamp": "Time"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# ANALYTICS PAGE
# ══════════════════════════════════════════════════════════════════════════

def page_analytics():
    st.markdown(f"<h1>📊 Nutrition <span class='accent'>Analytics</span></h1>", unsafe_allow_html=True)
    username = st.session_state.username
    disease  = st.selectbox("Filter by condition", DISEASE_OPTIONS, key="analytics_disease")

    data, err = api_get(f"/api/meals/analytics/{username}", params={"disease": disease})
    if err:
        st.error(f"Could not load analytics: {err}")
        return
    if not data or data.get("empty"):
        st.info("No data yet — log some meals first!")
        return

    stats = data["stats"]

    # ── KPI row ────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("🍽️ Total Meals",   stats["total_meals"])
    k2.metric("🔥 Avg Calories",  f"{stats['avg_calories']} kcal")
    k3.metric("💪 Avg Protein",   f"{stats['avg_protein']} g")
    k4.metric("🌾 Avg Carbs",     f"{stats['avg_carbs']} g")
    k5.metric("🧈 Avg Fat",       f"{stats['avg_fat']} g")
    k6.metric("❤️ Health Score",  f"{stats['health_score']} / 100")

    st.markdown("---")

    # ── Charts ─────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗓️ Calorie Trend (last 7 meals)")
        calorie_df = pd.DataFrame(data["calorie_trend"])
        if not calorie_df.empty:
            fig = px.bar(calorie_df, x="day", y="calories",
                         color_discrete_sequence=[GOLD],
                         labels={"day": "Day", "calories": "Calories (kcal)"})
            fig.update_layout(showlegend=False, margin=dict(t=10, b=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🥧 Macro Distribution (all time)")
        macros = data["macros"]
        fig2 = go.Figure(go.Pie(
            labels=["Carbs", "Protein", "Fat"],
            values=[macros["carbs"], macros["protein"], macros["fat"]],
            hole=0.5,
            marker_colors=[DARK_GREEN, GOLD, "#c97b4a"],
        ))
        fig2.update_layout(margin=dict(t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Daily trend line ───────────────────────────────────────────────────
    st.subheader("📈 Daily Nutrition Trend")
    daily_df = pd.DataFrame(data["daily_trend"])
    if not daily_df.empty:
        fig3 = px.line(daily_df, x="date", y=["calories", "protein", "carbs", "fat"],
                       labels={"value": "Amount", "variable": "Nutrient", "date": "Date"},
                       color_discrete_map={"calories": "#c0392b", "protein": GOLD,
                                           "carbs": DARK_GREEN, "fat": "#c97b4a"})
        fig3.update_layout(margin=dict(t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)

    # ── Top foods & recent meals ───────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏆 Top Foods")
        top_df = pd.DataFrame(data["top_foods"])
        if not top_df.empty:
            fig4 = px.bar(top_df, x="count", y="food", orientation="h",
                          color_discrete_sequence=[DARK_GREEN],
                          labels={"count": "Times logged", "food": "Food"})
            fig4.update_layout(showlegend=False, margin=dict(t=10, b=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig4, use_container_width=True)

    with col4:
        st.subheader("🕐 Recent Meals")
        recent = data.get("recent_meals", [])
        for meal in recent:
            icon  = STATUS_COLOR.get(meal.get("status", "safe"), "🟢")
            emoji = meal.get("emoji", "🍽️")
            name  = meal.get("food_name", "Unknown").title()
            cal   = meal.get("calories", 0)
            ts    = meal.get("timestamp", "")[:16].replace("T", " ")
            st.markdown(
                f"{icon} {emoji} **{name}** — {cal} kcal  <small style='color:grey'>{ts}</small>",
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════
# WEEKLY INSIGHT PAGE
# ══════════════════════════════════════════════════════════════════════════

def page_weekly_insight():
    st.markdown(f"<h1>🗓️ Weekly <span class='accent'>Insight</span></h1>", unsafe_allow_html=True)
    st.write("Get a personalised weekly diet recommendation based on your logged meals.")

    if st.button("✨ Generate Weekly Insight", type="primary"):
        with st.spinner("Generating insight…"):
            result, err = api_post(
                "/api/meals/weekly-insight",
                json={"username": st.session_state.username},
            )
        if err:
            st.error(f"Could not generate insight: {err}")
        else:
            st.success("Here's your personalised weekly insight:")
            st.markdown("<div class='nl-panel'>", unsafe_allow_html=True)
            st.write(result.get("insight", "No insight returned."))
            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR NAV
# ══════════════════════════════════════════════════════════════════════════

def sidebar_nav():
    with st.sidebar:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:0.5rem;">
            <span style="font-size:1.6rem;">🥑</span>
            <span style="font-family:'Playfair Display', serif; font-size:1.3rem; font-weight:800; color:{TEXT_LIGHT};">
                Nutri<span style="color:{GOLD};">Lens</span> AI
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='color:{GOLD}; font-weight:600;'>{st.session_state.username}</p>", unsafe_allow_html=True)
        st.markdown("---")
        pages = {
            "🔍 Analyze":        "analyze",
            "📋 History":        "history",
            "📊 Analytics":      "analytics",
            "🗓️ Weekly Insight": "weekly",
        }
        for label, key in pages.items():
            if st.button(label, use_container_width=True):
                st.session_state.page = key
                st.rerun()
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username  = ""
            st.session_state.page      = "login"
            st.session_state.last_analysis = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════

def main():
    if not st.session_state.logged_in:
        if st.session_state.page == "register":
            page_register()
        else:
            page_login()
        return

    sidebar_nav()

    page = st.session_state.page
    if page == "analyze":
        page_analyze()
    elif page == "history":
        page_history()
    elif page == "analytics":
        page_analytics()
    elif page == "weekly":
        page_weekly_insight()
    else:
        page_analyze()


if __name__ == "__main__":
    main()