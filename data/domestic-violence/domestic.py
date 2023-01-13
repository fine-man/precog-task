# filter all the cases of women domestic violence year and district wise

import pandas as pd
import datetime as dt

# take as input
start_year = 2010
end_year = 2018
disposed_after_end_year=0

def aggregate_cases(year, cases, max_year, disposed_after_end_year=0):
    # filter out all the invalid entries
    # make colums for pending, solved, total
    # filter in all the cases which are of women domestic violence
    # groupby [state_code, dist_code] and then aggregate
    # save to a file
    cases_df = cases.copy(deep=True)

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases_df = cases_df[((cases_df["date_of_decision"] < dt.datetime.now()) & 
    (cases_df["date_of_decision"] >= cases_df["date_of_filing"]))
    | (cases_df["date_of_decision"].isna())]

    # fixing the inconsistent data
    #temp = cases_df.loc[cases_df["date_of_decision"] < cases_df["date_of_filing"], "date_of_filing"]
    #cases_df.loc[cases_df["date_of_decision"] < cases_df["date_of_filing"], "date_of_decision"] = temp

    # condition to check if "date_of_decision" > max_year should be considered pending
    if not disposed_after_end_year:
        cases_df.loc[cases_df["date_of_decision"] > pd.to_datetime(f"{max_year}-12-31"), 
        "date_of_decision"] = pd.to_datetime("")

    # read all the cases of women domestic violence
    domestic_case_id = pd.read_csv("../processed/domestic_cases_id.csv")

    # filter in all the cases of domestic violence
    cases_df = pd.merge(domestic_case_id, cases_df, how='left', on=['ddl_case_id'])

    # aggregate attributes
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

# process the data for each year separately
years = [year for year in range(start_year, end_year + 1)]

for year in years:
    process(year)
