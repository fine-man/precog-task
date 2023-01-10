# calculate the average time of decision per district for all cases 2010 - 2018

import pandas as pd
import datetime as dt

def aggregate_cases(year, max_year, cases):
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
    
    aggregate_cases(year, 2018, cases)
    del cases

years = [year for year in range(2010, 2019)]

for year in years:
    process(year)
