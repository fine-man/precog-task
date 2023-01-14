import pandas as pd

cases = pd.read_csv("state_total_cases_2010_2018.csv")
state_pop = pd.read_csv("../processed/state_population_key.csv")
df = pd.merge(cases, state_pop, how='left', on=['state_name'])
df['women_percentage'] = (df['total_cases'] * (10 ** 6))/df['women_population']
df = df.sort_values(by=['women_percentage'])
filename = "state_women_per_2010_2018.csv"
df[['state_name', 'women_percentage']].to_csv(filename, index=False)
print(f"wrote cases per women to {filename}")
del cases
del df

cases = pd.read_csv("state_women_per_2010_2018.csv")
state_id = pd.read_csv("../processed/state_unique_id.csv")
df = pd.merge(cases, state_id, how='left', on=['state_name'])
map_filename = "state_women_map_2010_2018.csv"
df[['Name', 'Unique-ID', 'women_percentage']].to_csv(map_filename, index=False)
print(f"wrote cases per women to {map_filename}")
