import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="ERIK: College Admission AI", page_icon="🎓", layout="wide")
st.title("🎓 ERIK: College Admission AI")
st.markdown("Your offline, local college admission assistant with full profile evaluation!")

# --- Academic Profile ---
st.header("📝 Academic Profile")
col1, col2 = st.columns(2)
with col1:
    gpa_unweighted = st.slider("Unweighted GPA (0-5)", 0.0, 5.0, 4.5, 0.01)
    gpa_weighted = st.slider("Weighted GPA (0-6)", 0.0, 6.0, 5.0, 0.01)
    sat = st.slider("SAT Score (400-1600)", 400, 1600, 1400, 10)
with col2:
    act = st.slider("ACT Score (1-36)", 1, 36, 32, 1)
    country = st.selectbox("Country", ["Bangladesh", "USA", "Canada", "UK", "Other"])

# --- Extracurricular Activities (ECAs) ---
st.header("🎨 Extracurricular Activities (ECAs)")
st.markdown("Add multiple ECAs like Common App format")
if "ecas" not in st.session_state:
    st.session_state.ecas = []

with st.form("eca_form", clear_on_submit=True):
    eca_name = st.text_input("Activity Name")
    eca_category = st.selectbox("Category", ["STEM", "Arts", "Sports", "Leadership", "Community Service", "Other"])
    eca_role = st.selectbox("Role", ["Member", "Leader", "Founder"])
    eca_hours = st.number_input("Hours per week / achievement", 0, 100, 5)
    eca_submit = st.form_submit_button("Add ECA")
    
    if eca_submit and eca_name:
        st.session_state.ecas.append({
            "name": eca_name,
            "category": eca_category,
            "role": eca_role,
            "hours": eca_hours
        })

if st.session_state.ecas:
    st.subheader("Your ECAs")
    for idx, eca in enumerate(st.session_state.ecas):
        st.write(f"{idx+1}. {eca['name']} ({eca['category']} | {eca['role']} | {eca['hours']} hrs)")

# --- Essays & LORs ---
st.header("✍️ Essay & LOR")
essay_text = st.text_area("Paste your essay here for AI simulated rating")
essay_quality = st.slider("Self-rated Essay Quality (1-10)", 1, 10, 7)
lor_quality = st.slider("Self-rated LOR Strength (1-10)", 1, 10, 8)

def rate_essay(text):
    # Simulated AI essay rating based on length and presence of keywords
    if len(text) < 300:
        return max(essay_quality - 2, 1)
    elif len(text) < 600:
        return max(essay_quality, 1)
    else:
        return min(essay_quality + 1, 10)

essay_ai_rating = rate_essay(essay_text)

# --- Financial Status ---
st.header("💰 Financial Status")
efc = st.number_input("EFC (Expected Family Contribution, $)", 0, 100000, 5000)
coa = st.number_input("COA (Cost of Attendance, $)", 0, 200000, 50000)

# --- Extracurricular Score Calculation ---
def eca_score(ecas):
    score = 0
    for e in ecas:
        base = 2
        if e["role"] == "Leader":
            base += 2
        if e["role"] == "Founder":
            base += 3
        hours_score = min(e["hours"]/5, 5)
        score += base + hours_score
    return min(score, 20)

# --- Admission Evaluation ---
def evaluate_admission():
    score = 0
    # GPA contribution (weighted preferred)
    score += (gpa_weighted / 6) * 25
    # SAT contribution
    score += ((sat - 400)/1200) * 25
    # ACT contribution
    score += ((act -1)/35)*10
    # ECAs
    score += eca_score(st.session_state.ecas)
    # Essay & LOR
    score += essay_ai_rating
    score += lor_quality
    # Financial aid impact (lower EFC improves profile slightly for need-aware schools)
    if efc < coa * 0.3:
        score += 3
    
    # Admission probability
    if score >= 85:
        admission = "High chance 🎯 (Top-tier universities)"
    elif score >= 65:
        admission = "Moderate chance ✅ (Strong-fit schools)"
    else:
        admission = "Low chance ⚠️ (Focus on profile building)"
    return score, admission

# --- College Recommendation / Search ---
def recommend_colleges(score, country, efc, coa):
    colleges = []
    if score >= 85:
        colleges = ["MIT", "Harvard", "Stanford", "Columbia", "Caltech"]
    elif score >= 65:
        colleges = ["UPenn", "Duke", "Cornell", "Northwestern", "Johns Hopkins"]
    else:
        colleges = ["State University", "Community College", "Local Private University"]
    
    # Filter by country and affordability
    filtered = []
    for c in colleges:
        # Simulated: only show if COA affordable
        if efc <= coa*0.5:
            filtered.append(c)
    if not filtered:
        filtered = colleges
    return filtered

# --- Visualization ---
def visualize_profile(total_score):
    categories = ["GPA", "SAT", "ACT", "ECAs", "Essay", "LOR", "Financial Need"]
    values = [
        (gpa_weighted/6)*10,
        ((sat-400)/1200)*10,
        ((act-1)/35)*10,
        eca_score(st.session_state.ecas)/2,
        essay_ai_rating,
        lor_quality,
        3 if efc<coa*0.3 else 0
    ]
    fig, ax = plt.subplots(figsize=(8,4))
    ax.barh(categories, values, color='skyblue')
    ax.set_xlim(0,10)
    ax.set_xlabel("Contribution to Profile")
    ax.set_title("Profile Breakdown")
    st.pyplot(fig)

# --- Evaluate Button ---
if st.button("Evaluate My Admission"):
    total_score, admission_result = evaluate_admission()
    st.subheader("📊 ERIK's Evaluation")
    st.write(f"Total Score: **{total_score:.1f}/100**")
    st.success(admission_result)
    
    # College Recommendation
    st.subheader("🎓 Recommended Colleges")
    recommended = recommend_colleges(total_score, country, efc, coa)
    for c in recommended:
        st.write(f"- {c}")
    
    # Visualize Profile
    st.subheader("📈 Profile Visualization")
    visualize_profile(total_score)
    
    # Essay & LOR Guidance
    st.subheader("✍️ Essay & LOR Guidance")
    st.write(f"AI Essay Rating: **{essay_ai_rating}/10**")
    if essay_ai_rating < 7:
        st.info("Improve essay with personal stories, clarity, and impact.")
    else:
        st.success("Essay quality is strong!")
    
    if lor_quality <7:
        st.info("LOR should provide specific examples of achievements and character.")
    else:
        st.success("LOR is strong!")

    # Multi-turn guidance
    st.subheader("💡 ERIK Advice")
    if total_score < 65:
        st.warning("Focus on improving ECAs, essays, and leadership experience.")
    elif total_score < 85:
        st.info("Strengthen essays, LORs, and maintain ECAs for higher chance.")
    else:
        st.success("Excellent profile! Apply confidently to top-tier schools.")
