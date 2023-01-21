# rank all the states

import pandas as pd
import datetime as dt

# take as input
start_year = 2010
end_year = 2018
disposed_after_end_year=0
column_name = "mean_disposition_days"

def judges_per_state(start_year=2010, end_year=2018):
    # read the judges_clean.csv file
    # filter all the active judges in {year}
    # merge this with district csv file
    # group by district and count number of entries

    # reading and setting up the judges dataframe
    judges = pd.read_csv("../judges_clean.csv")

    save_filepath = f"temps/judges_count_{start_year}_{end_year}.csv"

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
    judges = judges[["state_code", "active"]].groupby(["state_code"]).agg(judges_count=("active", "sum"))

    # saving the judges count file
    judges["judges_count"].to_csv(save_filepath) 
    print(f"Number of judges per state ({start_year}-{end_year}) has been written to {save_filepath}")

def aggregate_cases(year, cases, max_year, disposed_after_end_year=0):
    # filter out all the invalid entries
    # make colums for pending, solved, total
    # groupby [state_code, dist_code] and then aggregate
    # save to a file

    save_filepath = f"cases_agg/cases_agg_{year}.csv"
    cases_df = cases.copy(deep=True)

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases_df = cases_df[((cases_df["date_of_decision"] < dt.datetime.now()) &
                         (cases_df["date_of_decision"] >= cases_df["date_of_filing"])) |
                        (cases_df["date_of_decision"].isna())]

    if not disposed_after_end_year:
        cases_df.loc[cases_df["date_of_decision"] > pd.to_datetime(f"{max_year}-12-31"), 
        "date_of_decision"] = pd.to_datetime("")

    # setting values to some basic attributes
    cases_df["pending"] = cases_df["date_of_decision"].isna().apply(lambda x : 1 if x else 0)
    cases_df["solved"] = 1 - cases_df["pending"]
    cases_df["total"] = 1

    # calculating the disposition days of each case (is made 0 for pending cases)
    cases_df["disposition_days"] = cases_df["date_of_decision"] - cases_df["date_of_filing"]
    cases_df["disposition_days"] = cases_df["disposition_days"].dt.days

    # grouping by state code and aggregating attributes
    final_df = cases_df[["year", "state_code", "pending",
    "solved", "total", "disposition_days"]].groupby(["year", "state_code"]).agg(pending_cases=('pending', 'sum'),
    solved_cases=('solved', 'sum'), total_cases=('total', 'sum'), total_days=('disposition_days', 'sum'))

    # calculating the mean disposition days
    final_df["mean_disposition_days"] = final_df["total_days"]/final_df["solved_cases"]

    # saving the final aggregated df for this year
    final_df.to_csv(save_filepath)
    print(f"the aggregate of {year} cases has been written to {save_filepath}")
    del cases_df
    del final_df


def process(year):
    cases = pd.read_csv(f'../cases/cases_{year}.csv')
    print(f'cases_{year}.csv has been loaded')

    cases = cases[["ddl_case_id", "year", "state_code", "dist_code", "court_no",
                   "date_of_filing", "date_of_decision"]]

    # changing the type of date columns
    date_columns = ['date_of_filing', 'date_of_decision']
    for column_name in date_columns:
        cases[column_name] = pd.to_datetime(cases[column_name], errors='coerce')

    aggregate_cases(year, cases, end_year)
    del cases

def merge(start_year, end_year):
    # combine the dataframes of all the years into a single csv file

    # filepaths
    filepath = f"cases_agg/cases_agg_{start_year}.csv"
    save_filepath = f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv"

    df = pd.read_csv(filepath)
    print(f"loaded {filepath}")

    # merge each year
    for year in range(start_year + 1, end_year + 1):
        filepath = f"cases_agg/cases_agg_{year}.csv"

        # loading the csv file of the current year
        df_2 = pd.read_csv(filepath)
        print(f"loaded {filepath}")

        # concatinating the new dataframe with the old one
        df = pd.concat([df, df_2], axis=0) 
        print(f"concated {filepath}")
    
    # grouping by state code
    df = df[["state_code", "pending_cases", "solved_cases",
    "total_cases", "total_days"]].groupby(["state_code"]).agg(
    pending_cases=('pending_cases', 'sum'), solved_cases=('solved_cases', 'sum'),
    total_cases=('total_cases', 'sum'), total_days=('total_days', 'sum'))

    # calculating the new attributes
    df["mean_disposition_days"] = df["total_days"]/df["solved_cases"]
    df["case_pendency_rate"] = df["pending_cases"]/df["total_cases"]
    df["case_disposition_rate"] = df["solved_cases"]/df["total_cases"]

    # saving the merged and grouped df to a file
    df.to_csv(save_filepath)
    print(f"Saved the merged and grouped datafram to {save_filepath}")

def merge_with_judges(start_year, end_year):
    # merge the attribute file with the judges file

    # required filepaths
    cases_filepath = f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv"
    judge_filepath = f"temps/judges_count_{start_year}_{end_year}.csv"
    save_filepath = f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv" 

    # reading the required csv files
    cases_merge = pd.read_csv(cases_filepath)
    judge_count = pd.read_csv(judge_filepath)

    # merge the judge count with the attributes dataframe
    merged = pd.merge(cases_merge, judge_count, on=["state_code"])
    merged["cases_per_judge"] = merged["total_cases"]/merged["judges_count"]

    # saving the final dataframe
    merged.to_csv(save_filepath)
    print(f"saved the states attributes file combined with judge-count to {save_filepath}")

def data_map(column_name="mean_disposition_days"):
    # required filepath
    cases_filepath = f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv"
    state_key_filepath = "../processed/state_key.csv"
    save_filepath = f"./csv-files/states_{column_name}_{start_year}_{end_year}.csv"

    merged_df = pd.read_csv(cases_filepath)
    print(f"loaded {cases_filepath}")

    states = pd.read_csv(state_key_filepath)

    # merging the state_codes with state_names
    df = pd.merge(merged_df, states, how='left', on=["state_code"])

    # setting the sorting order
    ascend=True
    if column_name in ["case_disposition_rate"]:
        ascend=False

    # sorting the states
    df = df.sort_values(by=column_name, ascending=ascend)

    # saving the final datamap df
    df[["state_name", column_name]].to_csv(save_filepath, index=False)
    print(f"Saved the state-wise {column_name} datamap to {save_filepath}")


# process the data for each year separately
years = [year for year in range(start_year, end_year + 1)]

for year in years:
    process(year)

# merge the data for all the years
judges_per_state()
merge(start_year, end_year)
merge_with_judges(start_year, end_year)

# creating the datamap csv files
data_map(column_name)
