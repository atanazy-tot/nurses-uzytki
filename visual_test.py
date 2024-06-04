from src.visualisation.parse_vacation import parse_vacation
from src.visualisation.schedule_graph import plot_week_schedule, plot_nurse_schedule
import pandas as pd

# Read the data into a DataFrame
# Data has to come as output from neos_output_parser.py
df = pd.read_csv("results/archiv/timetables/test_timetable.csv", sep=';', header=None)
df = df.iloc[2:]
df = df.reset_index(drop=True)
df = df.set_index(df.columns[0])
df = df.fillna(0).astype(int)
column_names = [f"Day_{k}_Shift_{j}" for k in range(1, 29) for j in range(1, 4)]
df.columns = column_names

vacation_data = parse_vacation('data/test_instance_last_shift.csv')
vacation_data.columns = column_names


# Plot schedules for each week
for week in range(1, 5):
    plot_week_schedule(df, week, vacation_data)

# Plot schedule for individual nurse
nurse_id = 11
plot_nurse_schedule(df, nurse_id, vacation_data)