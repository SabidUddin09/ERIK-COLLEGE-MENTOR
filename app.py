import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="ERIK: College Admission AI", page_icon="🎓", layout="wide")
st.title("🎓 ERIK: College Admission AI")
st.markdown("Your **local college admission assistant**. Fill out your profile and get advice!")

# --- User Profile ---
st.header("📝 Your Profile")

with st.expander("Academic Details"):
    gpa = st.slider("High School GPA (0-5 scale)", 0.0, 5.0, 4.5, 0.01)
    sat = st.slider("SAT Score (400-1600)", 400, 1600, 1400, 10)
    act = st.slider("ACT Score (1-36, optional)", 1, 36, 32, 1)

with st.expander("Extracurriculars"):
    activities = st.number_input("Number of Significant Activities", 0, 20, 5)
    leadership = st.checkbox("Leadership Roles?")
    research = st.checkbox("Research / Publication Experience?")
    community_service = st.number_input("Hours of Community Service", 0, 500, 50)

with st.expander("Essays & LORs"):
    essay_quality = st.slider("Self-rated Essay Quality (1-10)", 1, 10, 7)
    lor_quality = st.slider("Self-rated LOR Strength (1-10)", 1, 10, 8)

# --- Admission Evaluation Logic ---
def evaluate_admission(gpa, sat, act, activities, research, leadership, community_service, essay_quality, lor_quality):
    score = 0
    # GPA
    score += (gpa / 5) * 25
    # SAT
    score += ((sat - 400) / 1200) * 25
    # ACT (optional)
    score += ((act - 1) / 35) * 10
    # Activities
    score += min(activities * 1.5, 15)
    # Leadership
    if leadership:
        score += 5
    # Research
    if research:
        score += 5
    # Community Service
    score += min(community_service / 20, 10)
    # Essay
    score += essay_quality
    # LOR
    score += lor_quality

    # Determine admission probability
    if score >= 85:
        admission = "High chance 🎯 (Top-tier universities)"
    elif score >= 65:
        admission = "Moderate chance ✅ (Strong-fit schools)"
    else:
        admission = "Low chance ⚠️ (Focus on profile building)"
    
    return score, admission

# --- College Recommendation Logic ---
def recommend_colleges(score):
    if score >= 85:
        colleges = ["MIT", "Harvard", "Stanford", "Columbia", "Caltech"]
    elif score >= 65:
        colleges = ["UPenn", "Duke", "Cornell", "Northwestern", "Johns Hopkins"]
    else:
        colleges = ["State University", "Community College", "Local Private University"]
    return colleges

# --- Evaluate Button ---
if st.button("Evaluate My Admission"):
    total_score, result = evaluate_admission(gpa, sat, act, activities, research, leadership, community_service, essay_quality, lor_quality)
    
    st.subheader("📊 ERIK's Evaluation")
    st.success(result)
    st.write(f"Total Profile Score: **{total_score:.1f}/100**")
    
    # College Recommendations
    st.subheader("🎓 Suggested Colleges")
    colleges = recommend_colleges(total_score)
    for c in colleges:
        st.write(f"- {c}")

    # Profile Visualization
    st.subheader("📈 Profile Visualization")
    categories = ["GPA", "SAT", "ACT", "Activities", "Leadership", "Research", "Community Service", "Essay", "LOR"]
    values = [
        (gpa / 5) * 10,
        ((sat - 400) / 1200) * 10,
        ((act - 1) / 35) * 10,
        min(activities * 1.5 / 1.5, 10),
        5 if leadership else 0,
        5 if research else 0,
        min(community_service / 20, 10),
        essay_quality,
        lor_quality
    ]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(categories, values, color='skyblue')
    ax.set_xlim(0, 10)
    ax.set_xlabel("Score Contribution")
    st.pyplot(fig)

    # Essay & LOR Guidance
    st.subheader("✍️ Essay & LOR Guidance")
    if essay_quality < 7:
        st.info("Improve essay quality by adding personal stories, challenges, and impact.")
    else:
        st.success("Your essay is strong. Maintain clarity and originality.")
    
    if lor_quality < 7:
        st.info("Ask recommenders to provide specific examples of achievements and character.")
    else:
        st.success("Your LORs are strong.")

