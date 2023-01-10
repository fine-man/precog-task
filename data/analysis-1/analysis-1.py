# calculate the average time of decision per year

import pandas as pd

def calculate_mean_days(year, cases, districts):
    # remove all pending cases
    # merge things with court data
    # calcualte the decision time for each case
    # calculate the mean decision time for each court by grouping over courts

    decided_cases = cases[cases["date_of_decision"].notna()].copy(deep=True)

    # removing all the invalid entries
    decided_cases = decided_cases[decided_cases["date_of_decision"] < pd.to_datetime("2023-01-01", infer_datetime_format=True)]

    decided_cases["decision_days"] = decided_cases["date_of_decision"] - decided_cases["date_of_filing"]

    #max_days = cases_courts["decision_days"].max()
    #print(max_days)
    #print(cases_courts.loc[cases_courts["decision_days"] == max_days, ["state_name", "district_name", "date_of_filing", "date_of_decision"]])

    mean_days_df = decided_cases[["year", "state_code", "dist_code", 
    "decision_days"]].groupby(["year", "state_code", "dist_code"]).sum()

    # converting datetime to just number of days
    #mean_days_df["decision_days"] = mean_days_df["decision_days"]/pd.to_timedelta(1, unit='D')
    #mean_days_df = mean_days_df.rename(columns={'decision_days':'mean_decision_days'})
    print(mean_days_df.head())
    
    mean_days_df.to_csv(f"mean-days/mean_days_{year}.csv")
    print(f"mean decision days per district ({year}) has been written to mean-days/mean_days_{year}.csv")

def calculate_total_cases(year, cases, courts):
    cases_df = cases.copy(deep=True)

    # removing all the invalid entries
    cases_df = cases_df[cases_df["date_of_decision"] < pd.to_datetime("2023-01-01", infer_datetime_format=True)]

    cases_courts = pd.merge(cases_df, courts, how="left", on=["year", "state_code", "dist_code", "court_no"]) 

    number_cases = cases_courts[["year", "state_code", "state_name", 
                                "dist_code", "district_name"]].groupby(["state_code", "dist_code"]).value_counts()
    number_cases.to_csv(f"total-cases/total_cases_{year}.csv")
    df = pd.read_csv(f"total-cases/total_cases_{year}.csv")
    df.columns.values[-1] = "total_cases"
    df.to_csv(f"total-cases/total_cases_{year}.csv", index=False)
    #number_cases.columns.values[-1] = "total_cases"
    print(f"total cases per district ({year}) has been writeen to total-cases/total_cases_{year}.csv")

def judges_per_district(year):
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

    # filtering out all the judges who are active in the current year
    judges.loc[judges["end_date"].isna(), "end_date"] = pd.to_datetime("2023-01-01", infer_datetime_format=True)
    judges = judges[judges["start_date"] <= pd.to_datetime(f"{year}-12-31", infer_datetime_format=True)]
    judges = judges[judges["end_date"] >= pd.to_datetime(f"{year}-01-01", infer_datetime_format=True)]

    # preparing the districts dataframe
    districts = pd.read_csv("../keys/cases_district_key.csv") 
    districts = districts.drop_duplicates(subset=["state_code", "dist_code"], keep='first')

    # merging the judge df with districts df
    judges_dist = pd.merge(judges, districts, how='left', on=["state_code", "dist_code"])
    judges_dist["year"] = year

    number_judges = judges_dist[["year", "state_code",
                                "dist_code", "state_name",
                                "district_name"]].groupby(["state_code", "dist_code"]).value_counts()
    
    number_judges.to_csv(f"judges-count/judges_count_{year}.csv")
    df = pd.read_csv(f"judges-count/judges_count_{year}.csv")
    df.columns.values[-1] = "judges_count"
    df.to_csv(f"judges-count/judges_count_{year}.csv", index=False)

    print(f"Number of judges per district ({year}) has been written to judges-count/judges_count_{year}.csv")

def process(year):
    cases = pd.read_csv(f'../cases/small_cases_{year}.csv')
    print(f'cases_{year}.csv has been loaded')

    cases = cases[["ddl_case_id", "year", "state_code", "dist_code", "court_no",
                   "date_of_filing", "date_of_decision"]]

    cases["date_of_filing"] = pd.to_datetime(cases["date_of_filing"],
                                             infer_datetime_format=True,
                                             errors='coerce')

    cases["date_of_decision"] = pd.to_datetime(cases["date_of_decision"],
                                             infer_datetime_format=True,
                                             errors='coerce')
    
    districts = pd.read_csv('../district_key.csv')

    calculate_mean_days(year, cases, districts)
    judges_per_district(year)
    calculate_total_cases(year, cases, districts)

    mean_days = pd.read_csv(f"mean-days/mean_days_{year}.csv")
    #judges = pd.read_csv(f"judges-count/judges_count_2018.csv")
    #total_cases = pd.read_csv(f"total-cases/total_cases_2018.csv")

    #merge_1 = pd.merge(means_days, judges, how='left', on=["year", "state_code", "dist_code"])
    #print(merge_1.head())

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

#judges_per_district(2018)
process(2018)
