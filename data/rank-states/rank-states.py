# rank all the states

import pandas as pd
import datetime as dt

# take as input
start_year = 2010
end_year = 2018
disposed_after_end_year=0

def judges_per_state(start_year=2010, end_year=2018):
    # read the judges_clean.csv file
    # filter all the active judges in {year}
    # merge this with district csv file
    # group by district and count number of entries

    # reading and setting up the judges dataframe
    judges = pd.read_csv("../judges_clean.csv")
    judges["start_date"] = pd.to_datetime(judges["start_date"],
                                          infer_datetime_format=True,
                                          errors='coerce')
    judges["end_date"] = pd.to_datetime(judges["end_date"],
                                        infer_datetime_format=True,
                                        errors='coerce')

    # filtering out all the judges who were active anywhere in the range[start_year, end_year]
    judges.loc[judges["end_date"].isna(), "end_date"] = dt.datetime.now()
    judges = judges[judges["start_date"] <= pd.to_datetime(f"{end_year}-12-31", infer_datetime_format=True)]
    judges = judges[judges["end_date"] >= pd.to_datetime(f"{start_year}-01-01", infer_datetime_format=True)]
    judges["active"] = 1

    # counting the number of judges per state
    judges = judges[["state_code", "active"]].groupby(["state_code"]).agg(judges_count=("active", "sum"))
    judges["judges_count"].to_csv(f"temps/judges_count_{start_year}_{end_year}.csv") 
    print(f"Number of judges per state ({start_year}-{end_year}) has been written to temps/judges_count_{start_year}_{end_year}.csv")

def aggregate_cases(year, cases, max_year, disposed_after_end_year=0):
    # filter out all the invalid entries
    # make colums for pending, solved, total
    # groupby [state_code, dist_code] and then aggregate
    # save to a file
    cases_df = cases.copy(deep=True)

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases_df = cases_df[(cases_df["date_of_decision"] < dt.datetime.now())
| (cases_df["date_of_decision"].isna())]

    # fixing the inconsistent data
    temp = cases_df.loc[cases_df["date_of_decision"] < cases_df["date_of_filing"], "date_of_filing"]
    cases_df.loc[cases_df["date_of_decision"] < cases_df["date_of_filing"], "date_of_decision"] = temp

    if not disposed_after_end_year:
        cases_df.loc[cases_df["date_of_decision"] > pd.to_datetime(f"{max_year}-12-31"), 
        "date_of_decision"] = pd.to_datetime("")

    cases_df["pending"] = cases_df["date_of_decision"].isna().apply(lambda x : 1 if x else 0)
    cases_df["solved"] = 1 - cases_df["pending"]
    cases_df["total"] = 1

    cases_df["disposition_days"] = cases_df["date_of_decision"] - cases_df["date_of_filing"]
    cases_df["disposition_days"] = cases_df["disposition_days"].dt.days

    final_df = cases_df[["year", "state_code", "pending",
    "solved", "total", "disposition_days"]].groupby(["year", "state_code"]).agg(pending_cases=('pending', 'sum'),
    solved_cases=('solved', 'sum'), total_cases=('total', 'sum'), total_days=('disposition_days', 'sum'))

    final_df["mean_disposition_days"] = final_df["total_days"]/final_df["solved_cases"]

    final_df.to_csv(f"cases_agg/cases_agg_{year}.csv")
    print(f"the aggregate of {year} cases has been written to cases_agg/cases_agg_{year}.csv")
    del cases_df
    del final_df


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
    
    aggregate_cases(year, cases, end_year)
    del cases

def merge(start_year, end_year):
    # start with each year
    # combine the dataframes
    df = pd.read_csv(f"cases_agg/cases_agg_{start_year}.csv")
    print(f"loaded cases_agg/cases_agg_{start_year}.csv")

    for year in range(start_year + 1, end_year + 1):
        df_2 = pd.read_csv(f"cases_agg/cases_agg_{year}.csv")
        print(f"loaded cases_agg/cases_agg_{year}.csv")
        df = pd.concat([df, df_2], axis=0) 
        print(f"concated cases_agg/cases_agg_{year}.csv")
    
    df = df[["state_code", "pending_cases", "solved_cases",
    "total_cases", "total_days"]].groupby(["state_code"]).agg(
    pending_cases=('pending_cases', 'sum'), solved_cases=('solved_cases', 'sum'),
    total_cases=('total_cases', 'sum'), total_days=('total_days', 'sum'))

    df["mean_disposition_days"] = df["total_days"]/df["solved_cases"]
    df["case_pendency_rate"] = df["pending_cases"]/df["total_cases"]
    df["case_disposition_rate"] = df["solved_cases"]/df["total_cases"]
    df.to_csv(f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv")

def merge_with_judges(start_year, end_year):
    cases_merge = pd.read_csv(f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv")
    judge_count = pd.read_csv(f"temps/judges_count_{start_year}_{end_year}.csv")

    merged = pd.merge(cases_merge, judge_count, on=["state_code"])
    merged["cases_per_judge"] = merged["total_cases"]/merged["judges_count"]
    merged.to_csv(f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv")

def data_map(column_name="mean_disposition_days"):
    merged_df = pd.read_csv(f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv")
    states = pd.read_csv("../my-keys/state_key.csv")

    df = pd.merge(merged_df, states, how='left', on=["state_code"])

    ascend=True
    if column_name in ["case_disposition_rate", "cases_per_judge"]:
        ascend=False

    df = df.sort_values(by=column_name, ascending=ascend)
    df[["state_name", column_name]].to_csv(f"states_{column_name}_{start_year}_{end_year}.csv", index=False)
    #data_map_df = pd.merge(df, map_unique_id, on=["district_name"])
    #data_map_df[["Name", "Unique-ID", column_name]].to_csv(f"states_{column_name}_{start_year}_{end_year}.csv", index=False)
    #print(f"mean decision days data map {year} has been written to {column_name}_{start_year}_{end_year}.csv")



# process the data for each year separately
years = [year for year in range(start_year, end_year + 1)]

"""
for year in years:
    process(year)
"""

# merge the data for all the years
#judges_per_state()
#merge(start_year, end_year)
#merge_with_judges(start_year, end_year)

data_map("cases_per_judge")

