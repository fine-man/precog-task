# calculate the average time of decision per district for all cases 2010 - 2018

import pandas as pd
import datetime as dt

# take as input
start_year = 2015
end_year = 2018
disposed_after_end_year=0

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

    cases_df["decision_days"] = cases_df["date_of_decision"] - cases_df["date_of_filing"]
    cases_df["decision_days"] = cases_df["decision_days"].dt.days

    final_df = cases_df[["year", "state_code", "dist_code", "pending",
    "solved", "total", "decision_days"]].groupby(["year", "state_code", "dist_code"]).agg(pending_cases=('pending', 'sum'),
    solved_cases=('solved', 'sum'), total_cases=('total', 'sum'), total_days=('decision_days', 'sum'))

    final_df["mean_decision_days"] = final_df["total_days"]/final_df["solved_cases"]

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
    
    df = df[["state_code", "dist_code", "pending_cases", "solved_cases",
    "total_cases", "total_days"]].groupby(["state_code", "dist_code"]).agg(
    pending_cases=('pending_cases', 'sum'), solved_cases=('solved_cases', 'sum'),
    total_cases=('total_cases', 'sum'), total_days=('total_days', 'sum'))

    df["mean_decision_days"] = df["total_days"]/df["solved_cases"]
    df[["mean_decision_days"]].to_csv(f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv")

def data_map(column_name="mean_decision_days"):
    mean_days_df = pd.read_csv(f"temps/merged{disposed_after_end_year}_{start_year}_{end_year}.csv")
    districts = pd.read_csv("../my-keys/district_key.csv")
    map_unique_id = pd.read_csv("../my-keys/district_unique_id.csv")

    df = pd.merge(mean_days_df, districts, how='left', on=["state_code", "dist_code"])
    data_map_df = pd.merge(df, map_unique_id, on=["district_name"])
    data_map_df[["Name", "Unique-ID", column_name]].to_csv(f"{column_name}_{start_year}_{end_year}.csv", index=False)
    #print(f"mean decision days data map {year} has been written to {column_name}_{start_year}_{end_year}.csv")

# process the data for each year separately
years = [year for year in range(start_year, end_year + 1)]


for year in years:
    process(year)

# merge the data for all the years
merge(start_year, end_year)

data_map()
