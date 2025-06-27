# plotting_utils.py
import matplotlib.pyplot as plt
import calplot
import pandas as pd
from datetime import datetime, timedelta
import collections

def create_habit_completion_bar_chart(habits):
    """
    Generates a bar chart showing the total number of completions for each habit.
    Expects a list of Habit objects.
    Returns a matplotlib.figure.Figure object.
    """
    if not habits:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No habits to display chart yet.",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Habit Performance Overview")
        return fig

    habit_names = [h.name for h in habits]
    completion_counts = [len(h.completed_dates) for h in habits]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(habit_names, completion_counts, color='skyblue')

    ax.set_xlabel('Habit', fontsize=12)
    ax.set_ylabel('Total Days Completed', fontsize=12)
    ax.set_title('Habit Performance Overview', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}',
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    return fig

def create_habit_heatmap(completed_dates, habit_name, year=None):
    """
    Generates a calendar heatmap for a single habit's completion dates for a given year.
    Returns a matplotlib.figure.Figure object.
    """
    if not completed_dates:
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.text(0.5, 0.5, f"No daily activity data for '{habit_name}' yet.",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Calendar Heatmap for '{habit_name}'")
        plt.tight_layout()
        return fig

    date_counts = collections.Counter(completed_dates)
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in date_counts.keys()]
    counts = list(date_counts.values())
    daily_series = pd.Series(counts, index=dates)

    if year is None:
        target_year = daily_series.index.max().year if not daily_series.empty else datetime.now().year
    else:
        target_year = year

    yearly_series = daily_series[daily_series.index.year == target_year]

    if yearly_series.empty:
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.text(0.5, 0.5, f"No activity for '{habit_name}' in {target_year}.",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Calendar Heatmap for '{habit_name}' in {target_year}")
        plt.tight_layout()
        return fig

    fig_cal, axes_cal = calplot.calplot(
        yearly_series,
        edgecolor='black',
        linewidth=1,
        cmap='YlGn',
        figsize=(12, 6),
        suptitle=f"Daily Activity: '{habit_name}' in {target_year}",
        linecolor='white',
        yearlabels=True,
        monthlabels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        colorbar=True,
    )
    plt.tight_layout()
    return fig_cal