import pandas as pd


def parse_vacation(data_file_path):
    # Read the CSV file
    df = pd.read_csv(data_file_path, delimiter=';', header=None)

    # Find the index where "vacation" appears
    try:
        vacation_index = df[df[0].str.contains("vacation")].index[0]
    except IndexError:
        print("Vacation data not found in the file.")
        exit()

    # Find the index where the next section starts
    next_section_index = df[df[0].str.contains("preferred_companions")].index[0]

    # Extract the vacation data
    vacation_data = df.iloc[vacation_index + 1:next_section_index, :]

    # Create a DataFrame to hold the parsed vacation data
    vacation_df = pd.DataFrame(index=[f"Nurse_{i}" for i in range(1, 16)], columns=range(1, 85))

    # Fill the DataFrame with 1s where the nurse has vacation
    for _, row in vacation_data.iterrows():
        nurse_id = int(row[0])
        vacation_day = int(row[1])
        vacation_df.loc[f"Nurse_{nurse_id}", vacation_day * 3 - 2:vacation_day * 3] = 1

    # Fill NaNs with 0s
    vacation_df = vacation_df.infer_objects(copy=False).fillna(0)

    # Convert DataFrame to integer type
    vacation_df = vacation_df.astype(int)
    return vacation_df