import pandas as pd
from ..neos_output_parser import get_variables_from_neos
from .input_digester import get_section_data


def create_nurse_dict(n: int) -> dict:
    return {i: 0 for i in range(1, n + 1)}


def variables_dict_to_pandas(neos_output_path: str) -> pd.DataFrame:
    schedule = get_variables_from_neos(neos_output_path)

    data = [(*key, value) for key, value in schedule.items()]
    df = pd.DataFrame(data, columns=['nurse_id', 'shift', 'day', 'attendance'])

    return df


def establish_justice(nurse_dict: dict) -> dict:
    data = [(*key, value) for key, value in nurse_dict.items()]
    df = pd.DataFrame(data, columns=['nurse_id', 'feeling_points'])

    justice_dict = {'sum': df.feeling_points.sum(),
                    'min': df.feeling_points.min(),
                    'max': df.feeling_points.max(),
                    'mean': df.feeling_points.mean(),
                    'std': df.feeling_points.std()}

    return justice_dict


def weekend_justice(neos_output_path: str) -> dict:
    df = variables_dict_to_pandas(neos_output_path)

    weekend_df = df[(df['day'] % 7 == 6) | (df['day'] % 7 == 0)]

    weekend_shifts = weekend_df.groupby('nurse_id')['attendance'].sum().reset_index()
    weekend_shifts.columns = ['nurse_id', 'num_weekend_shifts']

    justice_dict = {'sum': weekend_shifts.num_weekend_shifts.sum(),
                    'min': weekend_shifts.num_weekend_shifts.min(),
                    'max': weekend_shifts.num_weekend_shifts.max(),
                    'mean': weekend_shifts.num_weekend_shifts.mean(),
                    'std': weekend_shifts.num_weekend_shifts.std()}

    return justice_dict


def company_justice(neos_output_path: str, data_input_path: str,
                    preferred: bool, num_nurses: int) -> dict:
    if preferred:
        section_name = 'preferred_companions'
    else:
        section_name = 'unpreferred_companions'

    selected_companions = get_section_data(data_input_path, section_name)
    df = variables_dict_to_pandas(neos_output_path)

    nurse_dict = create_nurse_dict(num_nurses)

    for pair in selected_companions:
        couple_df = df[(df['nurse_id'] == pair[0]) | (df['nurse_id'] == pair[1])]

        couples_aggregated = couple_df.groupby('shift', 'day')['attendance'].sum().reset_index()
        couples_aggregated.columns = ['shift', 'day', 'attendances']

        couples_filtered = couples_aggregated[(couples_aggregated['attendances'] == 2)]
        num_requests_fulfilled = couples_filtered.shape[0]
        nurse_dict[pair[0]] += num_requests_fulfilled

    return establish_justice(nurse_dict)


def shifts_justice(neos_output_path: str, data_input_path: str,
                   preferred: bool, num_nurses: int) -> dict:
    if preferred:
        section_name = 'preferred_shifts'
    else:
        section_name = 'unpreferred_shifts'

    selected_shifts = get_section_data(data_input_path, section_name)
    variables_dict = get_variables_from_neos(neos_output_path)

    nurse_dict = create_nurse_dict(num_nurses)

    for shift in selected_shifts:
        reordered_shift = (shift[0], shift[2], shift[1])
        if variables_dict[reordered_shift] == 1:
            nurse_dict[shift[0]] += 1

    return establish_justice(nurse_dict)


# jeszcze do sprawdzenia: jaka część funkcji celu odpowiada za wynik w jakim stopniu?
# może warto policzyć zadowolenie per zmiana? usuwanie niezadowolonych pielęgniarek? :)
# TODO: Wymęczyć podsumowanie na podstawie słowników; zamieścić to w głównym skrypcie
def generate_summary(neos_output_path: str, data_input_path: str, summary_output_path: str):
    pass

