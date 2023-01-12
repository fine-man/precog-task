# calculate the average time of decision per district for all cases 2010 - 2018

import pandas as pd
import datetime as dt

# take as input
start_year = 2010
end_year = 2018
disposed_after_end_year=0

def extract_disposition_days(year, cases):

    cases_df = cases.copy(deep=True)

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases_df = cases_df[(cases_df["date_of_decision"] < dt.datetime.now()) & 
    (cases_df["date_of_filing"] < cases_df["date_of_decision"])]

    # removing all the cases which are pending
    cases_df = cases_df[cases_df["date_of_decision"].notna()]

    # calculating disposition days
    cases_df["disposition_days"] = cases_df["date_of_decision"] - cases_df["date_of_filing"]
    cases_df["disposition_days"] = cases_df["disposition_days"].dt.days
    cases_df[["disposition_days"]].to_csv("data.csv", index=False)


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
    
    extract_disposition_days(year, cases)
    del cases

"""
for year in years:
    process(year)
"""

process(2018)
