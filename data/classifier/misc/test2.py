"""
Some testing stuff
"""
cases = pd.read_csv(cases_filename)
print(f"loaded file {cases_filename}")

cases = cases[['year', 'state_code', 'dist_code', 'court_no', 'type_name', 'purpose_name', 'disp_name', 'date_of_filing', 'date_of_decision']]

print(cases.columns)
## Cleaning the data

# remove all the invalid dates - done
# merge with disp_key.csv
# filter all the ones with bail in them
# make a 'bail' category

# transform the dates into year, month and day - easy to do
# transform the judge_position string into number matrix
# try to transform the mail female columns as well

# loading disp_key_name.csv

# removing all the invalid entries (where date of decision is not a valid/real date)
# also removing all the date of decisions = ""
cases = cases[(cases["date_of_decision"] < dt.datetime.now()) & 
(cases["date_of_decision"] >= cases["date_of_filing"])]

cases = pd.merge(cases, disp, how='left', on=['year', 'disp_name'])

# filtering all cases where judgement is bail related
cases = cases[cases['disp_name_s'].isin(bail_strings)]

# removing NaN values
cases = cases[cases['purpose_name'].notna()]

# setting the bail column
cases['bail'] = 0
cases.loc[cases['disp_name_s'] == "bail granted", ['bail']] = 1

# transforming the dates
cases['filing_year'] = cases['date_of_filing'].dt.year
cases['filing_month'] = cases['date_of_filing'].dt.month
cases['filing_day'] = cases['date_of_filing'].dt.day

cases['decision_year'] = cases['date_of_decision'].dt.year
cases['decision_month'] = cases['date_of_decision'].dt.month
cases['decision_day'] = cases['date_of_decision'].dt.day

cases.drop(['year', 'date_of_filing', 'date_of_decision', 'disp_name', 'disp_name_s', 'count'], axis=1, inplace=True)
