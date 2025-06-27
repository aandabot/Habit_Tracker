# main.py
import streamlit as st
from data_manager import load_habits, save_habits, add_habit, mark_completed, delete_habit
from plotting_utils import create_habit_completion_bar_chart, create_habit_heatmap
from utils import calculate_streak
from datetime import datetime

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="HabitPRO", initial_sidebar_state="expanded")

# --- Custom CSS for a more "Royal" look (subtle dark theme enhancements) ---
# You can expand on this with more colors, fonts, shadows etc.
st.markdown("""
<style>
    /* General body styling */
    body {
        font-family: 'Georgia', serif; /* A more classic font */
        color: #E0E0E0; /* Lighter text for dark background */
        background-color: #1A1A2E; /* Dark blue/purple background */
    }

    /* Main title */
    .st-emotion-cache-18jvaq.eqr7zpz0 { /* Target Streamlit's h1/title */
        color: #FFD700; /* Gold color for main title */
        text-align: center;
        font-size: 3.5em;
        padding-bottom: 20px;
        border-bottom: 2px solid #FFD700;
        margin-bottom: 30px;
    }

    /* Subheaders */
    h2, h3, h4 {
        color: #ADD8E6; /* Light blue for subheaders */
        border-bottom: 1px solid #33334A; /* Subtle separator */
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    /* Expander styling */
    .st-emotion-cache-q8sptp.e1exp3v10 { /* Target expander header */
        background-color: #2C2C42; /* Slightly lighter background for expanders */
        border-radius: 8px;
        padding: 10px 20px;
        margin-bottom: 10px;
        color: #FFD700; /* Gold text for expander titles */
        font-weight: bold;
    }

    /* Sidebar styling */
    .st-emotion-cache-1ldf02.eczjsme4 { /* Target sidebar background */
        background-color: #2C2C42; /* Darker sidebar */
        padding: 20px;
        border-right: 1px solid #33334A;
    }
    .st-emotion-cache-1ldf02.eczjsme4 h2 { /* Sidebar subheaders */
        color: #FFD700; /* Gold */
        border-bottom: 1px solid #FFD700;
    }

    /* Buttons */
    .st-emotion-cache-7ym5gk.ef3psqc11 { /* Target all buttons */
        background-color: #4CAF50; /* Green for action buttons */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 15px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .st-emotion-cache-7ym5gk.ef3psqc11:hover {
        background-color: #45a049;
    }

    /* Specific delete button (red) */
    .st-emotion-cache-7ym5gk.ef3psqc11[data-testid="stButton-primary"] { /* This targets primary buttons, might need adjustment */
        background-color: #F44336; /* Red for delete */
    }
    .st-emotion-cache-7ym5gk.ef3psqc11[data-testid="stButton-primary"]:hover {
        background-color: #D32F2F;
    }


    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        font-weight: bold;
    }
    .stAlert.info { background-color: #2196F3; color: white; }
    .stAlert.success { background-color: #4CAF50; color: white; }
    .stAlert.warning { background-color: #FFC107; color: #333; }
    .stAlert.error { background-color: #F44336; color: white; }

    /* Metrics */
    .st-emotion-cache-1c1j55r.e16fv1u3 { /* Target metric label */
        color: #ADD8E6; /* Light blue label */
        font-size: 0.9em;
    }
    .st-emotion-cache-1btdzba.e16fv1u3 { /* Target metric value */
        color: #FFD700; /* Gold value */
        font-size: 1.5em;
        font-weight: bold;
    }

</style>
""", unsafe_allow_html=True)


st.title("💪 HabitPRO")
st.markdown("### Elevate your consistency, visualize your progress, and master your habits!")


# --- Load Habit Data ---
habits = load_habits()

# --- Sidebar for Habit Management ---
st.sidebar.header("👑 Manage Your Habits")

with st.sidebar.expander("➕ Add New Habit", expanded=False):
    new_habit_name = st.text_input("Enter Habit Name:", key="sidebar_new_habit_input_text")
    if st.button("Add Habit", key="sidebar_add_habit_button"):
        if new_habit_name:
            if add_habit(habits, new_habit_name.strip()):
                save_habits(habits)
                st.sidebar.success(f"Habit '{new_habit_name.strip()}' added!")
                st.rerun()
            else:
                st.sidebar.info(f"Habit '{new_habit_name.strip()}' already exists.")
        else:
            st.sidebar.warning("Please enter a habit name.")

st.sidebar.markdown("---")
st.sidebar.subheader("Your Royal Habits")

if not habits:
    st.sidebar.info("No habits added yet. Use the 'Add New Habit' section above to get started!")
else:
    for habit in habits:
        st.sidebar.markdown(f"**{habit.name}**")
        col_mark, col_delete = st.sidebar.columns(2)

        with col_mark:
            if st.button(f"✅ Complete", key=f"sidebar_complete_{habit.name}"):
                if mark_completed(habit):
                    save_habits(habits)
                    st.sidebar.success(f"'{habit.name}' marked complete for today!")
                    st.rerun()
                else:
                    st.sidebar.info(f"'{habit.name}' already complete for today.")

        with col_delete:
            if st.button(f"🗑️ Delete", key=f"sidebar_delete_{habit.name}"):
                if delete_habit(habits, habit.name):
                    save_habits(habits)
                    st.sidebar.warning(f"Habit '{habit.name}' deleted!")
                    st.rerun()
                else:
                    st.sidebar.error(f"Could not delete habit '{habit.name}'.")
        st.sidebar.markdown("---") # Separator between habits in sidebar

# --- Main Content Area for Overview & Charts ---
st.subheader("Your Habit Dashboard")

if not habits:
    st.info("No habits added yet. Use the sidebar to add your first habit!")
else:
    st.markdown("#### Current Streaks & Status")
    habit_cols = st.columns(len(habits))
    for i, habit in enumerate(habits):
        with habit_cols[i % len(habit_cols)]: # Distribute metrics evenly
            streak = calculate_streak(habit.completed_dates)
            st.metric(label=f"{habit.name}", value=f"{streak} days", delta="🔥 Streak")
    st.markdown("---")

    st.subheader("📊 Your Progress Visualized")

    # Section for Bar Chart (Total Completions)
    st.markdown("#### Total Completions Overview")
    bar_chart_fig = create_habit_completion_bar_chart(habits)
    st.pyplot(bar_chart_fig)

    st.markdown("---") # Separator between chart types

    # Section for Calendar Heatmaps (Daily Activity)
    st.markdown("#### Daily Activity Heatmaps")

    habit_names_for_heatmap = [h.name for h in habits]
    selected_habit_name = st.selectbox(
        "Select a habit to view its daily activity heatmap:",
        habit_names_for_heatmap,
        key="heatmap_habit_selector"
    )

    selected_habit = next((h for h in habits if h.name == selected_habit_name), None)

    if selected_habit:
        all_years_with_data = sorted(list(set([datetime.strptime(d, '%Y-%m-%d').year for d in selected_habit.completed_dates])))
        current_year = datetime.now().year

        if current_year not in all_years_with_data:
            all_years_with_data.append(current_year)
            all_years_with_data.sort(reverse=True)

        try:
            default_year_index = all_years_with_data.index(current_year)
        except ValueError:
            default_year_index = 0

        selected_year = st.selectbox(
            "Select Year for Heatmap:",
            options=all_years_with_data,
            index=default_year_index,
            key="heatmap_year_selector"
        )

        heatmap_fig = create_habit_heatmap(selected_habit.completed_dates, selected_habit.name, year=selected_year)
        st.pyplot(heatmap_fig)