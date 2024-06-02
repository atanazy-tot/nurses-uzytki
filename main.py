"""
Main file
"""

from src.input_parser import generate_dat, employer_demands
from src.neos_output_parser import get_variables_from_neos, create_timetable

input_path = 'data/test_instance.csv'
output_path = 'neos_output_2_variant1.txt'
N, J, K = generate_dat(input_path, 'model/dat_files/first_data.dat')
time, empl_demands = employer_demands(input_path, J, K)

Variables = get_variables_from_neos(output_path)
create_timetable(Variables, N, J, K, 'results/archiv/timetable_neos_output_2_variant1.csv', empl_demands)