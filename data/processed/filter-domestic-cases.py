# filter all the domestic violence cases from acts_sections.csv
import pandas as pd

# list of women domestic violence cases dataframes
wdv_cases = []

# retrieving all the act numbers related to women domestic violence
df = pd.read_csv("domestic_acts.csv")
acts = list(df['act'])
acts = [int(act) for act in acts]
del df

# setting all the parameters for acts_sections.csv
dtypes = {'ddl_judge_id': 'object', 'act' : 'float64'}
chunksize = 10 ** 6
filename = "../acts_sections.csv"
usecols = ['ddl_case_id', 'act']

# remove the empty rows
# choose all the rows for which act is in acts list
# append the dataframe to wdv_cases list
with pd.read_csv(filename, chunksize=chunksize, usecols=usecols, dtype=dtypes) as reader:
    for chunk in reader:
        chunk = chunk[(chunk['act'].notna()) & (chunk['ddl_case_id'].notna())]
        chunk = chunk[chunk['act'].isin(acts)]
        wdv_cases.append(chunk['ddl_case_id'])
        print(len(wdv_cases))

domestic_cases = pd.concat(wdv_cases)
domestic_cases.to_csv("domestic_cases_id.csv", index=False)
