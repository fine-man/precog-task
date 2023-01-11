import pandas as pd
import datetime as dt

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
    df[["mean_decision_days"]].to_csv("final.csv")

merge(2010, 2018)
