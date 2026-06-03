import streamlit as st
import requests
from datetime import datetime

# =========================================================
# 1. THE DATA PIPELINE (Direct Web Entry Protocol)
# =========================================================

# Your verified custom Google Form submission endpoint
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdrFuod7p5mI9aAo5CJSU5JzM21HLiFJ-N-SwQou6hO4QQe3A/formResponse"

def save_lead_to_cloud_direct(name, email, goal):
    """Safely streams intake data straight to the Google ecosystem via web payloads."""
    # Your verified form field parameter entry keys
    payload = {
        "entry.1425746167": name.strip(),         # Full Name Entry ID
        "entry.1131361775": email.strip().lower(), # Email Address Entry ID
        "entry.3775637": goal                      # Athletic Target Entry ID
    }
    
    try:
        # Fire a secure, standalone HTTP POST request straight to the form server endpoint
        response = requests.post(FORM_URL, data=payload)
        if response.status_code == 200:
            return True, "Success"
        else:
            return False, "Cloud pipeline rejected data packet transaction."
    except Exception:
        return False, "Failed to establish handshake with cloud web target."


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

# --- CORE SERVICES ---
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

    # Activity multiplier dictionary
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active (1-3 days/wk)": 1.375,
        "Moderately Active (3-5 days/wk)": 1.55,
        "Heavy Athlete Training": 1.725
    }

    # Execute Calculations
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    tdee = int(bmr * activity_multipliers[activity])
    
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

# --- REGISTRATION INTAKE FORM ---
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
        # Trigger the clean, unified web payload pipeline
        success, message = save_lead_to_cloud_direct(name_input, email_input, goal_selection)
        if success:
            st.success(f"Success! Thank you {name_input}, your training goals have been securely logged.")
        else:
            st.error(message)

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