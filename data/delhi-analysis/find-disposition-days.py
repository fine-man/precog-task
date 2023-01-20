# find the disposition days for all state cases and store them to days.csv
import pandas as pd

state_code = 26 # state code for 
filename = "../processed/state_26_cases.csv"

state_cases = pd.read_csv(filename)
print(f"loaded {filename}")

# remove all the pending cases
state_cases = state_cases[state_cases['date_of_decision'].notna()]
date_columns = ['date_of_filing', 'date_of_decision']

for column_name in date_columns:
    state_cases[column_name] = pd.to_datetime(state_cases[column_name], errors='coerce')

state_cases['disposition_days'] = state_cases['date_of_decision'] - state_cases['date_of_filing']
state_cases['disposition_days'] = state_cases['disposition_days'].dt.days

save_filename = f"./csv-files/days_{state_code}.csv"
state_cases['disposition_days'].to_csv(save_filename, index=False)
print(f"saved dispositon days for all cases of state with code {state_code} to {save_filename}")
