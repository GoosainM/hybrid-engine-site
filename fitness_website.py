import streamlit as st
import sqlite3
from datetime import datetime

# =========================================================
# 1. THE DATA BASEMENT (Backend Storage Setup)
# =========================================================
def init_database():
    """Creates a local secure file to store our fitness leads."""
    connection = sqlite3.connect("fitness.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL UNIQUE,
            fitness_goal TEXT NOT NULL,
            submission_date TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

init_database()

# =========================================================
# 2. THE VISUAL STOREFRONT (Frontend Layout)
# =========================================================
st.set_page_config(page_title="Coach Matthews | Performance Specialist", page_icon="⚡", layout="centered")

# --- HERO AREA ---
st.title("Coach Matthews | Performance Specialist")
st.subheader("Build the Hybrid Engine")
st.write(
    "Engineering elite physical output. Stop guessing your variables. "
    "Get structured, metrics-focused training blocks designed to balance raw compound strength "
    "with high-intensity metabolic thresholds and progressive cardiovascular running engines."
)
st.markdown("---")

# --- CORE SERVICES (Tier 2: Style 1) ---
st.header("Training Pillars")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏃‍♂️ Hybrid Engine & Endurance")
    st.write(
        "Designed for athletes who refuse to compromise. Learn to build a powerful aerobic base "
        "and running economy while maintaining functional mass and peak strength levels."
    )

with col2:
    st.markdown("### ⚡ Specific Event Prep & Conditioning")
    st.write(
        "High-output, metabolic conditioning engineered for specific competitive simulation "
        "(including 10-week beginner Hyrox training protocols). Maximize your work capacity under fatigue."
    )

st.markdown("---")

# --- INTERACTIVE FITNESS CALCULATOR ---
st.header("📊 Calculate Your Baseline Metrics")
st.write("Use our internal data engine to estimate your total daily energy expenditure and performance macros.")

with st.expander("Open Interactive Macro Calculator", expanded=False):
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    
    with calc_col1:
        age = st.number_input("Age", min_value=15, max_value=80, value=31, step=1)
        weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=85, step=1)
    
    with calc_col2:
        height = st.number_input("Height (cm)", min_value=120, max_value=220, value=180, step=1)
        fitness_target = st.selectbox("Your Target Goal", ["Performance Muscle Gain", "Maintenance / Conditioning", "Fat Loss / Cutting"])
        
    with calc_col3:
        activity = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active (1-3 days/wk)", "Moderately Active (3-5 days/wk)", "Heavy Athlete Training"]
        )

    # Activity multiplier dictionary (Mifflin-St Jeor Constants)
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active (1-3 days/wk)": 1.375,
        "Moderately Active (3-5 days/wk)": 1.55,
        "Heavy Athlete Training": 1.725
    }

    # Execute Data Analyst Logic (Mifflin-St Jeor Formula)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    tdee = int(bmr * activity_multipliers[activity])
    
    # Target distribution math based on selected fitness objective
    if fitness_target == "Performance Muscle Gain":
        target_calories = tdee + 300
        protein = weight * 2.2  
    elif fitness_target == "Fat Loss / Cutting":
        target_calories = tdee - 500
        protein = weight * 2.4  
    else:
        target_calories = tdee
        protein = weight * 2.0

    st.markdown("#### Your Estimated Performance Baseline:")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="Target Daily Energy Intake", value=f"{target_calories} kcal")
    with res_col2:
        st.metric(label="Daily Protein Target", value=f"{int(protein)}g")
        
    st.caption("Note: These are initial mathematical models. True coaching blends biometric feedback with adaptive weekly tracking adjustments.")

st.markdown("---")

# --- REGISTRATION INTAKE FORM (Tier 3: Example A) ---
st.header("Submit Your Biometric Profile")
st.write("Fill out your details below to lock in your initial fitness consultation or receive elite training updates.")

with st.form(key="intake_form", clear_on_submit=True):
    name_input = st.text_input("Full Name*", placeholder="e.g. John Doe")
    email_input = st.text_input("Email Address*", placeholder="e.g. john@example.com")
    
    goal_selection = st.selectbox(
        "What is your primary athletic target?*",
        [
            "Hybrid Engine (Strength + Endurance)",
            "Specific Event / Hyrox Prep",
            "Newsletter & Dynamic Workout Updates"
        ]
    )
    
    submit_btn = st.form_submit_button(label="Submit Biometric Profile")

if submit_btn:
    if not name_input or not email_input:
        st.error("Please fill out both your name and email to proceed.")
    else:
        try:
            conn = sqlite3.connect("fitness.db")
            curr = conn.cursor()
            curr.execute(
                "INSERT INTO registrations (client_name, client_email, fitness_goal, submission_date) VALUES (?, ?, ?, ?)",
                (name_input.strip(), email_input.strip().lower(), goal_selection, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()
            st.success(f"Success! Thank you {name_input}, your training goals have been securely logged.")
        except sqlite3.IntegrityError:
            st.error("This email address is already registered on our client roster!")
        except Exception as e:
            st.error("An internal system error occurred saving your data.")

st.markdown("---")

# --- LINKS & CONNECTIVITY FOOTER ---
st.header("Follow the Engine")
st.write("Connect across my active channels for visual workout execution breakdowns and performance tips.")

s_col1, s_col2, s_col3 = st.columns(3)
with s_col1:
    st.markdown("[💼 LinkedIn](https://linkedin.com)")
with s_col2:
    st.markdown("[📸 Instagram](https://instagram.com)")
with s_col3:
    st.markdown("[💻 GitHub Portfolio](https://github.com)")

st.caption("© 2026 Coach Matthews Performance. All client datasets are sandboxed and structurally isolated locally.")