from parse_vacation import parse_vacation
from src.visualisation.schedule_graph import plot_week_schedule
import pandas as pd

# Read the data into a DataFrame
df = pd.read_csv("results/archiv/timetable_neos_output_2_variant1.csv", sep=';', header=None)
df = df.iloc[2:]
df = df.reset_index(drop=True)
df = df.set_index(df.columns[0])
df = df.fillna(0).astype(int)
nurses_total_hours = df.iloc[:-2, -1].tolist()
df = df.iloc[:, :-1]
column_names = [f"Day_{k}_Shift_{j}" for k in range(1, 29) for j in range(1, 4)]
df.columns = column_names

vacation_data = parse_vacation('data/test_instance.csv')
vacation_data.columns = column_names


# Plot schedules for each week
for week in range(1, 5):
    plot_week_schedule(df, week, vacation_data, 'employer')