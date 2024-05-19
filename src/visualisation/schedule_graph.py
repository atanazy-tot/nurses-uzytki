import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np


# Function to plot a week schedule
def plot_week_schedule(df, week, vacation_data, variant):
    fig, ax = plt.subplots(figsize=(15, 10))

    # Select data for the specified week
    start_col = (week - 1) * 21
    end_col = start_col + 21
    week_data = df.iloc[:, start_col:end_col]

    if variant == "employer":
        # Plot the nurse schedules
        for i, nurse in enumerate(week_data.index[:-2]):  # Exclude 'Required' and 'Available' rows
            for j, shift in enumerate(week_data.columns):
                if week_data.loc[nurse, shift] == 1:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='blue'))
                elif vacation_data.loc[nurse, shift] == 1:
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

        # Create offset transform by 20 points in x direction
        dx = 60 / 72.
        dy = 0 / 72.
        offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)

        # apply offset transform to all x ticklabels.
        for label in ax.xaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset)

        # Create offset transform by 5 points in x direction
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
    elif variant == 'employee':
        pass
    else:
        raise ValueError(f'Invalid variant {variant}. Must be either "employee" or "employer"')