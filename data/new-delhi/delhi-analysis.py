# provide an analysis of New Delhi

# filter all the new delhi cases from al the years
# combine all these dataframes to make a combined dataframe
# now for each year, calculate all the attributes
# somehow combine all these dataframes

import pandas as pd
import datetime as dt

# take as input
start_year = 2010
end_year = 2018
disposed_after_end_year=0
group_list = ['year', 'state_code', 'dist_code']
column_list = ['case_pendency_rate']
state_code = 26 # state code for New Delhi

def aggregate_cases(year, cases):
    # filter all the cases according to year
    # make colums for pending, solved, total
    # groupby [state_code, dist_code] and then aggregate
    # return the resulting dataframe

    cases_df = cases.copy(deep=True)

    group_list = ['year', 'state_code', 'dist_code']
    
    filing_date = pd.to_datetime(f"{year}-01-01", infer_datetime_format=True)
    decision_date = pd.to_datetime(f"{year}-12-31", infer_datetime_format=True)

    # setting all the cases whose date_of_decision > year as pending
    cases_df.loc[cases_df["date_of_decision"] > decision_date, "date_of_decision"] = pd.to_datetime("")

    # selecting all the cases which were either filed/solved in that {year} or are pending
    cases_df = cases_df[(cases_df['date_of_filing'] >= filing_date) |
                        (cases_df['date_of_decision'] >= filing_date) |
                        (cases_df['date_of_decision'].isna())]

    cases_df['year'] = year

    # aggregate attributes
    cases_df["pending"] = cases_df["date_of_decision"].isna().apply(lambda x : 1 if x else 0)
    cases_df["solved"] = 1 - cases_df["pending"]
    cases_df["total"] = 1
    
    # calculating the number of disposition days, automatically set to 0 for pending cases
    cases_df["disposition_days"] = cases_df["date_of_decision"] - cases_df["date_of_filing"]
    cases_df["disposition_days"] = cases_df["disposition_days"].dt.days

    # grouping and aggregating
    final_df = cases_df[group_list + ["pending",
    "solved", "total", "disposition_days"]].groupby(group_list).agg(pending_cases=('pending', 'sum'),
    solved_cases=('solved', 'sum'), total_cases=('total', 'sum'), total_days=('disposition_days', 'sum'))

    final_df["mean_disposition_days"] = final_df["total_days"]/final_df["solved_cases"]
    final_df["case_pendency_rate"] = final_df["pending_cases"]/final_df["total_cases"]

    #final_df.to_csv(f"cases_agg/{group_type}_agg_{year}.csv")
    #print(f"the {group_type} wise aggregate of {year} cases has been written to cases_agg/{group_type}_agg_{year}.csv")
    del cases_df
    return final_df

def filter_by_state(year, state_code=state_code):
    cases = pd.read_csv(f'../cases/cases_{year}.csv')
    print(f'cases_{year}.csv has been loaded')

    # filtering all the new delhi cases
    cases = cases[cases['state_code'] == state_code]

    # filtering only the wanted columns
    cases = cases[["ddl_case_id", "year", "state_code", "dist_code", "court_no",
                   "date_of_filing", "date_of_decision"]]

    # changing the type of all date columns
    date_columns = ['date_of_filing', 'date_of_decision']
    for column_name in date_columns:
        cases[column_name] = pd.to_datetime(cases[column_name], errors='coerce')

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases = cases[((cases["date_of_decision"] < dt.datetime.now()) & 
    (cases["date_of_decision"] >= cases["date_of_filing"]))
    | (cases["date_of_decision"].isna())]

    num_cases = cases.shape[0]
    print(f"The number of new delhi in {year} are {num_cases}")
    return cases

def combine(state_code=state_code, start_year=start_year, end_year=end_year):
    # filter all the cases of a particular state from the years
    # return the combined dataframe
    
    state_cases_list = []
    # process the data for each year separately
    years = [year for year in range(start_year, end_year + 1)]
    for year in years:
        state_cases_list.append(filter_by_state(year))

    save_filepath = f"../processed/state_{state_code}_cases.csv"
    combined_df = pd.concat(state_cases_list)
    combined_df.to_csv(save_filepath, index=False)
    print(f"all the cases of state with code={state_code} has been saved to {save_filepath}")
    return combined_df

def group_by_year(state_code=state_code, start_year=start_year, end_year=end_year):
    # read the state csv file
    # change the type of date columns
    # aggregate all the years and add the df to a list
    # make a merge_df

    # reading the state csv file
    state_filepath = f"../processed/state_{state_code}_cases.csv" 
    df_list = []
    save_filepath = f"state_{state_code}_merged.csv"

    state_case_df = pd.read_csv(state_filepath)
    print(f"{state_filepath} loaded")

    # changing the type of all date columns
    date_columns = ['date_of_filing', 'date_of_decision']
    for column_name in date_columns:
        state_case_df[column_name] = pd.to_datetime(state_case_df[column_name], errors='coerce')

    # calculating the attribute values for all the different years
    years = [year for year in range(start_year, end_year + 1)]
    for year in years:
        print(year)
        df_list.append(aggregate_cases(year, state_case_df))

    merge_df = pd.concat(df_list)

    merge_df.to_csv(save_filepath)
    
#df = combine()
group_by_year()

#merge(start_year, end_year, groupby=group_list[1:])
#merge_with_name(merged_filepath, column_list, merge_on=group_list[1:])
#data_map(merged_filepath, column_list, merge_on=group_list[1:])
