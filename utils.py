# utils.py
from datetime import datetime, timedelta

def calculate_streak(completed_dates):
    """
    Calculates the current consecutive streak (in days) for a habit.
    Assumes completed_dates are sorted and in 'YYYY-MM-DD' format.
    """
    if not completed_dates:
        return 0

    # Convert date strings to datetime.date objects for easier comparison
    # Use set to ensure uniqueness, then sort
    unique_sorted_dates = sorted(list(set(completed_dates)))
    dt_dates = [datetime.strptime(d, '%Y-%m-%d').date() for d in unique_sorted_dates]

    if not dt_dates: # Should not happen if completed_dates was not empty, but good defensive programming
        return 0

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    current_streak = 0
    # Check if the habit was completed today or yesterday to determine if a streak is active
    if dt_dates[-1] == today:
        current_streak = 1
        current_date = today
    elif dt_dates[-1] == yesterday:
        current_streak = 1
        current_date = yesterday
    else:
        # If not completed today or yesterday, no current streak
        return 0

    # Iterate backwards through the sorted unique dates
    # Check if each preceding date is exactly one day before the current date
    for i in range(len(dt_dates) - 2, -1, -1): # Start from second to last date, go down to 0
        if dt_dates[i] == current_date - timedelta(days=1):
            current_streak += 1
            current_date = dt_dates[i] # Move to the previous date in the streak
        else:
            # A gap is found, the streak is broken
            break

    return current_streak

# (Future functions like XP calculation, badge logic will go here)