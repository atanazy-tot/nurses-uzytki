import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np


# Function to plot a week schedule
def plot_week_schedule(df, week, vacation_df):
    fig, ax = plt.subplots(figsize=(15, 10))

    # Select data for the specified week
    start_col = (week - 1) * 21
    end_col = start_col + 21
    week_data = df.iloc[:, start_col:end_col]

    # Plot the nurse schedules
    for i, nurse in enumerate(week_data.index[:-2]):  # Exclude 'Required' and 'Available' rows
        for j, shift in enumerate(week_data.columns):
            if week_data.loc[nurse, shift] == 1:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='blue'))
            elif vacation_df.loc[nurse, shift] == 1:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='orange'))
            else:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='white'))
    # Annotate required and available nurses at the bottom
    for j, shift in enumerate(week_data.columns):
        ax.text(j + 0.5, len(week_data.index) - 2 + 0.5, str(week_data.loc['Nurses_on_shift', shift]), ha='center',
                va='center', color='red', fontsize=12)
        ax.text(j + 0.5, len(week_data.index) - 1 + 0.5, str(week_data.loc['Demanded_nurses', shift]), ha='center',
                va='center', color='green', fontsize=12)

    # Adjusting ticks and labels
    ax.set_xticks(np.arange(0, len(week_data.columns), 3))
    ax.set_xticklabels([f'Day {d + 1}' for d in range(7)])
    ax.xaxis.set_tick_params(labeltop=True, labelbottom=False)

    ax.set_yticks(np.arange(len(week_data.index)))
    ax.set_yticklabels(week_data.index)

    # Grid and lines
    ax.set_xticks(np.arange(len(week_data.columns)), minor=True)
    ax.set_yticks(np.arange(len(week_data.index)), minor=True)
    # Add thin grey lines to separate nurses and shifts
    for j in range(len(week_data.index)):
        ax.axhline(y=j, color='grey', linestyle='-', linewidth=0.5)
    for j in range(len(week_data.columns)):
        ax.axvline(x=j, color='grey', linestyle='-', linewidth=0.5)
    # Draw vertical lines for days
    for i in range(7):
        if i != 5:
            ax.axvline(x=i * 3, color='black', linewidth=1.5)
    # Mark Saturday start
    ax.axvline(x=15, color='fuchsia', linestyle='-', linewidth=5)
    # Mark summary info
    ax.axhline(y=15, color='black', linestyle='-', linewidth=1.5)

    # Create offset transform by 60 points in x direction
    dx = 60 / 72.
    dy = 0 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)

    # apply offset transform to all x ticklabels.
    for label in ax.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    # Create offset transform by -15 points in y direction
    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)

    # apply offset transform to all y ticklabels.
    for label in ax.yaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    ax.set_xlim(0, len(week_data.columns))
    ax.set_ylim(0, len(week_data.index))

    # Set plot title
    plt.title(f'Week {week} Nurse Schedule')
    plt.gca().invert_yaxis()  # To invert y-axis so Nurse 1 is at the top
    plt.show()


def plot_nurse_schedule(df, employee_id, vacation_df):
    nurse_name = f'Nurse_{employee_id}'

    if nurse_name not in df.index:
        raise ValueError(f"Nurse with ID {employee_id} not found in the dataset.")

    fig, axes = plt.subplots(4, 1, figsize=(15, 10), sharex=True)
    fig.suptitle(f'Schedule for {nurse_name}', fontsize=16)

    total_hours = 0
    weekly_hours = []
    shift_length = 8
    total_shifts = 0

    for week in range(4):
        start_col = week * 21
        end_col = start_col + 21
        week_data = df.iloc[:, start_col:end_col]
        vacation_week_data = vacation_df.iloc[:, start_col:end_col]

        ax = axes[week]
        nurse_schedule = week_data.loc[nurse_name]
        vacation_schedule = vacation_week_data.loc[nurse_name]

        # Plot nurse's shifts and vacations
        for j, shift in enumerate(nurse_schedule.index):
            if nurse_schedule[shift] == 1:
                ax.add_patch(plt.Rectangle((j, 0), 1, 1, color='blue'))
                total_hours += shift_length
                total_shifts += 1
            if vacation_schedule[shift] == 1:
                ax.add_patch(plt.Rectangle((j, 0), 1, 1, color='orange'))

        # Set labels and grid, remove y ticks and labels
        ax.set_yticks([])
        ax.set_yticklabels([])

        # Adjusting ticks and labels
        ax.set_xticks(np.arange(0, len(week_data.columns), 3))
        ax.set_xticklabels([f'Day {d + 1}' for d in range(7)])
        ax.set_xlim(0, len(week_data.columns))

        # Create offset transform by 60 points in x direction
        dx = 60 / 72.
        dy = 0 / 72.
        offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)

        # apply offset transform to all x ticklabels.
        for label in ax.xaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset)

        # Add thin grey lines to separate shifts
        for j in range(len(week_data.columns)):
            ax.axvline(x=j, color='grey', linestyle='-', linewidth=0.5)

        # Mark Saturday start
        ax.axvline(x=15, color='fuchsia', linestyle='-', linewidth=5)

        # Draw vertical lines for days
        for i in range(7):
            if i != 5:
                ax.axvline(x=i * 3, color='black', linewidth=1.5)

        weekly_hours.append(total_hours - sum(weekly_hours))

        # Add text for weekly hours
        ax.text(-1, 0.5, f'Week {week + 1}\nHours: {weekly_hours[week]}',
                ha='left', va='center', fontsize=12, bbox=dict(facecolor='white', alpha=1))

    # Add subtitle for total shifts
    fig.text(0.5, 0.92, f'Total of {total_shifts} shifts', ha='center', fontsize=14)

    plt.tight_layout(rect=[0, 0.03, 1, 0.90])
    plt.show()