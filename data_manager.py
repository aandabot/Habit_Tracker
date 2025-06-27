# data_manager.py
import json
from datetime import datetime

# Define the file where your habit data will be stored
DATA_FILE = 'habits_data.json'

class Habit:
    """Represents a single habit with its name and completion dates."""
    def __init__(self, name, completed_dates=None):
        self.name = name
        # Ensure completed_dates is a list, default to empty list if None
        self.completed_dates = completed_dates if completed_dates is not None else []

    def to_dict(self):
        """Converts a Habit object into a dictionary for JSON serialization."""
        return {"name": self.name, "completed_dates": self.completed_dates}

    @staticmethod
    def from_dict(data):
        """Creates a Habit object from a dictionary (for JSON deserialization)."""
        return Habit(data["name"], data["completed_dates"])

def load_habits():
    """
    Loads all habit data from the DATA_FILE.
    Returns a list of Habit objects. Handles file not found or corrupted JSON.
    """
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Deserialize each dictionary back into a Habit object
            return [Habit.from_dict(h_data) for h_data in data]
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is corrupted, return an empty list
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No existing habits_data.json found or file is empty/corrupted. Starting fresh.")
        return []

def save_habits(habits):
    """
    Saves the current list of Habit objects to the DATA_FILE.
    Serializes Habit objects into dictionaries before saving.
    """
    # Convert Habit objects to dictionaries for JSON serialization
    data_to_save = [h.to_dict() for h in habits]
    try:
        with open(DATA_FILE, 'w') as f:
            # Use indent=4 for pretty-printing the JSON file, makes it readable
            json.dump(data_to_save, f, indent=4)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Habits saved successfully.")
    except IOError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error saving habits: {e}")

def add_habit(habits_list, name):
    """
    Adds a new habit to the list if a habit with the same name doesn't already exist.
    Modifies the provided habits_list in place.
    Returns True if added, False if already exists.
    """
    # Check if a habit with the same name already exists (case-insensitive for robustness)
    if not any(h.name.lower() == name.lower() for h in habits_list):
        habits_list.append(Habit(name))
        return True
    return False

def mark_completed(habit_obj):
    """
    Marks a given habit as completed for the current day.
    Adds today's date to the habit's completed_dates list if not already present.
    Returns True if marked, False if already marked today.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in habit_obj.completed_dates:
        habit_obj.completed_dates.append(today)
        # Keep dates sorted for easier streak calculation and display
        habit_obj.completed_dates.sort()
        return True
    return False

def delete_habit(habits_list, habit_name_to_delete):
    """
    Deletes a habit from the list of habits.
    Modifies the provided habits_list in place.
    Returns True if deleted, False if habit not found.
    """
    initial_length = len(habits_list)
    # Create a new list excluding the habit to be deleted and assign it back
    # to the slice of the original list to modify it in place.
    habits_list[:] = [h for h in habits_list if h.name.lower() != habit_name_to_delete.lower()]
    return len(habits_list) < initial_length # True if length changed (habit was removed)

# You can add edit_habit here later, similar to delete_habit
# def edit_habit(habits_list, old_name, new_name):
#     for h in habits_list:
#         if h.name.lower() == old_name.lower():
#             h.name = new_name
#             return True
#     return False