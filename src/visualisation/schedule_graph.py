import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data into a DataFrame
df = pd.read_csv("timetable_neos_output_2_variant1.csv", sep=';', header=None)
df = df.iloc[2:]
df = df.reset_index(drop=True)
df = df.set_index(df.columns[0])
df = df.fillna(0).astype(int)
nurses_total_hours = df.iloc[:-2, -1].tolist()
df = df.iloc[:, :-1]
column_names = [f"Day_{k}_Shift_{j}" for k in range(1, 29) for j in range(1, 4)]
df.columns = column_names


# Function to plot a week schedule
def plot_week_schedule(df, week):
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
            else:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='white', edgecolor='black'))

    # Annotate required and available nurses
    for j, shift in enumerate(week_data.columns):
        ax.text(j + 0.5, 15, str(week_data.loc['Nurses_on_shift', shift]), ha='center', va='center', color='green', fontsize=12)
        ax.text(j + 0.5, 16, str(week_data.loc['Demanded_nurses', shift]), ha='center', va='center', color='red',
                fontsize=12)

    # Set labels and grid
    ax.set_xticks(np.arange(len(week_data.columns)) + 0.5)
    ax.set_xticklabels([f'Day {d + 1}\nShift {s + 1}' for d in range(7) for s in range(3)], rotation=90)
    ax.set_yticks(np.arange(len(week_data.index)))
    ax.set_yticklabels(week_data.index)
    ax.grid(True)

    # Set plot title
    plt.title(f'Week {week} Nurse Schedule')
    plt.show()


# Plot schedules for each week
for week in range(1, 5):
    plot_week_schedule(df, week)
