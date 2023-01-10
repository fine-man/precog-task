# calculate the average time of decision per year

import pandas as pd

def calculate_average_time(year):
    cases = pd.read_csv(f'../cases/cases_{year}.csv')
    print(f'cases_{year}.csv has been loaded')

    cases = cases[["ddl_case_id", "year", "state_code", "dist_code",
                   "date_of_filing", "date_of_decision"]]

    cases["date_of_filing"] = pd.to_datetime(cases["date_of_filing"],
                                             infer_datetime_format=True,
                                             errors='coerce')

    cases["date_of_decision"] = pd.to_datetime(cases["date_of_decision"],
                                             infer_datetime_format=True,
                                             errors='coerce')
    # cases = cases[cases["date_of_decision"].notna()]
    # print(cases.head())

    districts = pd.read_csv("../keys/cases_district_key.csv")
    districts = districts[["year", "state_code", "state_name", "dist_code", "district_name"]]
    districts.drop_duplicates(subset=["state_code", "dist_code"], keep='first')
    cases_districts = pd.merge(cases, districts, how="left", on=["state_code", "dist_code"])    

    decided_cases = cases_districts[cases_districts["date_of_decision"].notna()].copy(deep=True)

    decided_cases["decision_days"] = decided_cases["date_of_decision"] - decided_cases["date_of_filing"]

    average_days = decided_cases[["state_code", "state_name", "dist_code", "district_name"]].groupby(["state_code", "dist_code", "state_name", "district_name"]).mean()

    average_days["year"] = year
    average_days["decision_days"] = average_days["decision_days"]/pd.to_timedelta(1, unit='D')

    #states = pd.read_csv('../keys/cases_state_key.csv')
    #states = states.loc[states["year"] == year, ["year", "state_code", "state_name"]]

    #cases_states = pd.merge(cases, states, how="left", on=["state_code", "year"])

    del cases
    del states

    cases_states["decision_time"] = cases_states["date_of_decision"] - \
                                    cases_states["date_of_filing"]

    average_time_df = cases_states[["state_code", "state_name",  "decision_time"]].groupby(["state_code", "state_name"]).mean()
    average_time_df["average_days"] = average_time_df["decision_time"]/pd.to_timedelta(1, unit='D')
    average_time_df["year"] = year
    average_time_df = average_time_df[["year", "average_days"]]

    del cases_states
    
    average_time_df.to_csv("average_days_2018.csv")
    print(f'The average decision days per state for all {year} cases has been written to "average_days_{year}.csv')
    del average_time_df

years = [2010, 2011, 2012, 2013, 2014, 2015, 2017, 2018]

calculate_average_time(2018)
