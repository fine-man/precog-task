# calculate the average time of decision per district for all cases 2010 - 2018

import pandas as pd
import datetime as dt

# take as input
start_year = 2010
end_year = 2018
disposed_after_end_year=0
group_list = ['year', 'state_code', 'dist_code']
column_list = ['cases_per_judge']

def get_group_type(group_list):
    if len(group_list) == 1:
        return "state"
    elif len(group_list) == 2:
        return "district"
    elif len(group_type) == 3:
        return "court"
    else:
        return "cases"

def get_column_name(column_list):
    if len(column_list) == 1:
        return column_list[0]
    else:
        return "agg"

group_type = get_group_type(group_list[1:])
merge_on = group_list[1:]
merged_filepath = f"temps/{group_type}_agg_{start_year}_{end_year}.csv"

def count_judges(start_year=2010, end_year=2018, groupby=['year', 'state_code', 'dist_code']):
    # read the judges_clean.csv file
    # filter all the active judges in {year}
    # merge this with district csv file
    # group by district and count number of entries

    group_list = groupby

    # get the type of grouping
    group_type = get_group_type(group_list)

    # reading and setting up the judges dataframe
    judges = pd.read_csv("../judges_clean.csv")

    save_filepath = f"temps/{group_type}_judges_count_{start_year}_{end_year}.csv"

    # changing the type of all date columns
    date_columns = ['start_date', 'end_date']
    for column_name in date_columns:
        judges[column_name] = pd.to_datetime(judges[column_name], errors='coerce',
                                            infer_datetime_format=True)

    # filtering out all the judges who were active anywhere in the range[start_year, end_year]
    judges.loc[judges["end_date"].isna(), "end_date"] = dt.datetime.now()
    judges = judges[judges["start_date"] <= pd.to_datetime(f"{end_year}-12-31")]
    judges = judges[judges["end_date"] >= pd.to_datetime(f"{start_year}-01-01")]
    judges["active"] = 1

    # counting the number of judges per state
    judges = judges[group_list + ["active"]].groupby(group_list).agg(judges_count=("active", "sum"))

    # saving the judges count file
    judges["judges_count"].to_csv(save_filepath) 
    print(f"Number of judges per {group_type} ({start_year}-{end_year}) has been written to {save_filepath}")

def aggregate_cases(year, cases, max_year, disposed_after_end_year=0, groupby=['year', 'state_code', 'dist_code']):
    # filter out all the invalid entries
    # make colums for pending, solved, total
    # filter in all the cases which are of women domestic violence
    # groupby [state_code, dist_code] and then aggregate
    # save to a file
    cases_df = cases.copy(deep=True)
    
    group_list = groupby

    # get the type of grouping
    group_type = get_group_type(group_list[1:])

    # required filepaths
    save_filepath = f"cases_agg/{group_type}_agg_{year}.csv"

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases_df = cases_df[((cases_df["date_of_decision"] < dt.datetime.now()) & 
    (cases_df["date_of_decision"] >= cases_df["date_of_filing"]))
    | (cases_df["date_of_decision"].isna())]

    # condition to check if "date_of_decision" > max_year should be considered pending
    if not disposed_after_end_year:
        cases_df.loc[cases_df["date_of_decision"] > pd.to_datetime(f"{max_year}-12-31"), 
        "date_of_decision"] = pd.to_datetime("")

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

    final_df.to_csv(save_filepath)
    print(f"the {group_type} wise aggregate of {year} cases has been written to {save_filepath}")
    del cases_df
    del final_df

def merge(start_year, end_year, groupby=['state_code', 'dist_code']):
    # start with each year
    # combine the dataframes
    group_list = groupby

    # setting the type of grouping
    group_type = get_group_type(group_list)

    # required filepaths
    filepath = f"cases_agg/{group_type}_agg_{start_year}.csv"
    save_filepath = f"temps/{group_type}_agg_{start_year}_{end_year}.csv"

    # reading the initial data frame
    df = pd.read_csv(filepath)
    print(f"loaded {filepath}")

    # concatinating all the data frames
    for year in range(start_year + 1, end_year + 1):
        filepath = f"cases_agg/{group_type}_agg_{year}.csv"
        df_2 = pd.read_csv(filepath)
        print(f"loaded {filepath}")

        df = pd.concat([df, df_2], axis=0) 

        print(f"concated {filepath}")
    
    # grouping and aggregating
    df = df[group_list + ["pending_cases", "solved_cases",
    "total_cases", "total_days"]].groupby(group_list).agg(
    pending_cases=('pending_cases', 'sum'), solved_cases=('solved_cases', 'sum'),
    total_cases=('total_cases', 'sum'), total_days=('total_days', 'sum'))

    # calculating again after final grouping has been done
    df["mean_disposition_days"] = df["total_days"]/df["solved_cases"]
    df["case_pendency_rate"] = df["pending_cases"]/df["total_cases"]
    df["case_disposition_rate"] = df["solved_cases"]/df["total_cases"]

    # saving to the file
    df.to_csv(save_filepath)
    print(f"All {group_type}-wise attributes has been saved to {save_filepath}")

def merge_with_judges(start_year, end_year, groupby=['state_code', 'dist_code']):
    # merge the attribute file with the judges file
 
    group_list = groupby

    # get the type of grouping
    group_type = get_group_type(group_list)

    # required filepaths
    cases_filepath = f"temps/{group_type}_agg_{start_year}_{end_year}.csv"
    judge_filepath = f"temps/{group_type}_judges_count_{start_year}_{end_year}.csv"
    save_filepath = f"temps/{group_type}_agg_{start_year}_{end_year}.csv" 

    # reading the required csv files
    cases_merge = pd.read_csv(cases_filepath)
    judge_count = pd.read_csv(judge_filepath)

    # merge the judge count with the attributes dataframe
    merged = pd.merge(cases_merge, judge_count, on=group_list)
    merged["cases_per_judge"] = merged["total_cases"]/merged["judges_count"]

    # saving the final dataframe
    merged.to_csv(save_filepath, index=False)
    print(f"saved the {group_type}-wise attributes file combined with judge-count to {save_filepath}")

def data_map(filepath, column_list, merge_on=['state_code', 'dist_code']):
    merge_list = merge_on

    # set the type of merge
    merge_type = get_group_type(merge_list)
    
    # get the column name by which to name the save_filepath
    column_name = get_column_name(column_list)

    # read all the relevant files
    df = pd.read_csv(filepath)
    names_df = pd.read_csv(f"../processed/{merge_type}_key.csv")
    map_unique_id = pd.read_csv(f"../processed/{merge_type}_unique_id.csv")

    # merge the file with names and then unique map id
    df = pd.merge(df, names_df, how='left', on=merge_list)
    data_map_df = pd.merge(df, map_unique_id, on=[f"{merge_type}_name"])
    
    # saving the final csv file
    save_filepath = f"./csv-files/{merge_type}_{column_name}_map_{start_year}_{end_year}.csv"
    data_map_df[["Name", "Unique-ID"] + column_list].to_csv(save_filepath, index=False)
    print(f"{column_name} data map has been saved to {save_filepath}")

def process(year):
    cases = pd.read_csv(f'../cases/cases_{year}.csv')
    print(f'cases_{year}.csv has been loaded')

    cases = cases[["ddl_case_id", "year", "state_code", "dist_code", "court_no",
                   "date_of_filing", "date_of_decision"]]

    cases["date_of_filing"] = pd.to_datetime(cases["date_of_filing"],
                                             infer_datetime_format=True,
                                             errors='coerce')

    cases["date_of_decision"] = pd.to_datetime(cases["date_of_decision"],
                                             infer_datetime_format=True,
                                             errors='coerce')
    
    aggregate_cases(year, cases, end_year, groupby=group_list)
    del cases

# process the data for each year separately
years = [year for year in range(start_year, end_year + 1)]

for year in years:
    process(year)

# merge the data for all the years
count_judges(start_year, end_year, groupby=group_list[1:])
merge(start_year, end_year, groupby=group_list[1:])
merge_with_judges(start_year, end_year, groupby=group_list[1:])
#data_map(merged_filepath, column_list, merge_on=group_list[1:])
