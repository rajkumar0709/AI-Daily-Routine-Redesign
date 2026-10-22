
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Daily Routine Redesign",
    page_icon="📅",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #F5F7FC;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg, #4338CA, #7C3AED);
    padding: 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 34px;
}

.hero p {
    color: #EDE9FE;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E5E7EB;
}

div.stButton > button {
    background: #4F46E5;
    color: white;
    border-radius: 10px;
    min-height: 48px;
    border: none;
    font-weight: 600;
}

div.stButton > button:hover {
    background: #3730A3;
    color: white;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HELPER FUNCTIONS ----------------
def to_datetime(time_value):
    return datetime.combine(datetime.today().date(), time_value)


def add_minutes(time_value, minutes):
    return to_datetime(time_value) + timedelta(minutes=minutes)


def show_time(value):
    # Always display time in AM/PM format
    return value.strftime("%I:%M %p").lstrip("0")


def add_activity(schedule, start, end, activity):
    if end > start:
        schedule.append({
            "Time": f"{show_time(start)} - {show_time(end)}",
            "Activity": activity
        })


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>📅 AI-Powered Daily Routine Redesign</h1>
    <p>Your personal productivity planner for a balanced,
    organized and healthier day.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- USER INPUTS ----------------
left, right = st.columns(2, gap="large")

with left:
    st.subheader("👤 Your Details")

    name = st.text_input(
        "Your name",
        value="Student"
    )

    wake_up = st.time_input(
        "Wake-up time",
        value=datetime.strptime("06:00", "%H:%M").time()
    )

    college_start = st.time_input(
        "College start time",
        value=datetime.strptime("09:00", "%H:%M").time()
    )

    college_end = st.time_input(
        "College end time",
        value=datetime.strptime("16:00", "%H:%M").time()
    )


with right:
    st.subheader("🎯 Your Daily Goals")

    study_hours = st.slider(
        "Daily self-study goal (hours)",
        min_value=1,
        max_value=6,
        value=2
    )

    sleep_hours = st.slider(
        "Target sleep duration (hours)",
        min_value=6,
        max_value=9,
        value=8
    )

    exercise = st.selectbox(
        "Daily exercise",
        [
            "30 minutes",
            "45 minutes",
            "60 minutes",
            "No exercise"
        ]
    )

    exercise_minutes = {
        "30 minutes": 30,
        "45 minutes": 45,
        "60 minutes": 60,
        "No exercise": 0
    }[exercise]


generate = st.button(
    "✨ Generate My Daily Routine",
    use_container_width=True
)


# ---------------- GENERATE ROUTINE ----------------
if generate:

    if not name.strip():
        st.error("Please enter your name.")

    elif college_end <= college_start:
        st.error("College end time must be after college start time.")

    elif wake_up >= college_start:
        st.error("Wake-up time must be before college starts.")

    else:
        wake_dt = to_datetime(wake_up)
        college_start_dt = to_datetime(college_start)
        college_end_dt = to_datetime(college_end)

        schedule = []

        # 1. Wake up
        add_activity(
            schedule,
            wake_dt,
            add_minutes(wake_up, 15),
            "Wake up, freshen up and drink water"
        )

        # 2. Exercise
        exercise_start = add_minutes(wake_up, 15)
        exercise_end = add_minutes(
            wake_up, 15 + exercise_minutes
        )

        if exercise_minutes > 0:
            add_activity(
                schedule,
                exercise_start,
                exercise_end,
                f"Exercise and physical activity ({exercise})"
            )

        # 3. Morning preparation
        preparation_start = exercise_end

        add_activity(
            schedule,
            preparation_start,
            college_start_dt,
            "Breakfast, get ready and travel to college"
        )

        # 4. College
        add_activity(
            schedule,
            college_start_dt,
            college_end_dt,
            "College classes and learning"
        )

        # 5. Rest after college
        rest_start = college_end_dt
        rest_end = rest_start + timedelta(minutes=30)

        add_activity(
            schedule,
            rest_start,
            rest_end,
            "Relax, freshen up and have a snack"
        )

        # 6. Self-study
        study_start = rest_end
        study_end = study_start + timedelta(hours=study_hours)

        add_activity(
            schedule,
            study_start,
            study_end,
            f"Focused self-study ({study_hours} hours)"
        )

        # 7. Dinner
        dinner_start = study_end
        dinner_end = dinner_start + timedelta(minutes=45)

        add_activity(
            schedule,
            dinner_start,
            dinner_end,
            "Dinner and family time"
        )

        # 8. Bedtime based on wake-up time and sleep goal
        bedtime = wake_dt - timedelta(hours=sleep_hours)

        # If bedtime is earlier than wake-up time on the same
        # date, show it as the previous evening.
        bedtime_label = show_time(bedtime)

        schedule.append({
            "Time": bedtime_label,
            "Activity": f"Planned bedtime for {sleep_hours} hours of sleep"
        })

        # Save generated result across Streamlit reruns
        st.session_state["routine"] = schedule
        st.session_state["student_name"] = name.strip()
        st.session_state["study_hours"] = study_hours
        st.session_state["sleep_hours"] = sleep_hours
        st.session_state["exercise"] = exercise


# ---------------- DISPLAY RESULTS ----------------
if "routine" in st.session_state:

    st.divider()

    st.header(
        f"🌟 Hello, {st.session_state['student_name']}!"
    )

    st.write("Your suggested daily routine is ready.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Study Goal",
            f"{st.session_state['study_hours']} hours"
        )

    with col2:
        st.metric(
            "😴 Sleep Goal",
            f"{st.session_state['sleep_hours']} hours"
        )

    with col3:
        st.metric(
            "💪 Exercise",
            st.session_state["exercise"]
        )

    st.subheader("🗓️ Your Redesigned Daily Timetable")

    df = pd.DataFrame(st.session_state["routine"])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Download timetable
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download My Timetable",
        data=csv_data,
        file_name="my_daily_routine.csv",
        mime="text/csv"
    )

    # Recommendations
    st.subheader("💡 Smart Recommendations")

    st.success(
        "📌 Follow a consistent daily schedule to build good habits."
    )

    st.info(
        "📚 Divide your study into focused sessions and take "
        "short breaks to maintain concentration."
    )

    st.info(
        "🥗 Balance college, meals, personal time, exercise "
        "and adequate sleep."
    )

    if st.session_state["sleep_hours"] < 7:
        st.warning(
            "Consider allowing more time for sleep. "
            "Most adults need at least 7 hours."
        )

    st.caption(
        "Prototype note: recommendations are rule-based, "
        "not generated by a trained AI model."
    )

else:
    st.markdown("""
    <div style="
        background:white;
        padding:24px;
        border-radius:16px;
        border:1px solid #E5E7EB;
        margin-top:20px;
    ">
        <h3>✨ What this application does</h3>
        <p>📚 Creates a personalized daily timetable</p>
        <p>⏰ Helps organize college and study time</p>
        <p>💪 Includes exercise and sleep goals</p>
        <p>📥 Allows timetable download as a CSV file</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "VAC Mini Project | AI-Powered Daily Routine Redesign"
)
