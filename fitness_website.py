import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# =========================================================
# 1. THE DATA PIPELINE (Cloud Sheets Configuration)
# =========================================================
# Establish a secure connection to your cloud data sheet
conn = st.connection("gsheets", type=GSheetsConnection)

def save_lead_to_cloud(name, email, goal):
    """Safely appends a new biometric profile to the Google Sheet dataset."""
    try:
        # Read the current live sheet data safely (ttl=0 ensures no cached/stale data)
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
    except Exception:
        # If the sheet is completely blank and has no columns yet, start fresh
        existing_data = pd.DataFrame(columns=["Name", "Email", "Goal", "Date"])

    # Clean the incoming parameters
    email_clean = email.strip().lower()
    name_clean = name.strip()

    # Check for duplicate entries in the data frame array
    if not existing_data.empty and email_clean in existing_data["Email"].values:
        return False, "This email address is already registered on our client roster!"

    # Create a new data frame row matching the exact schema
    new_lead = pd.DataFrame([{
        "Name": name_clean,
        "Email": email_clean,
        "Goal": goal,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    # Concatenate the new data row to our existing master table
    updated_df = pd.concat([existing_data, new_lead], ignore_index=True)
    
    try:
        # Push the updated master table back to the cloud sheet node
        conn.update(worksheet="Sheet1", data=updated_df)
        return True, "Success"
    except Exception as e:
        return False, "An error occurred connecting to the cloud storage layer."


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

    # Execute Data Analyst Logic
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
        # Trigger the cloud data pipeline process
        success, message = save_lead_to_cloud(name_input, email_input, goal_selection)
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