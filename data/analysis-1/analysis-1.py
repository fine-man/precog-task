# calculate the average time of decision per year

import pandas as pd
import datetime as dt

def calculate_mean_days(year, cases):
    # remove all pending cases
    # calcualte the decision time for each case
    # calculate the mean decision time for each district by grouping over (state_code, dist_code)

    # filtering out all the cases which have been solved
    decided_cases = cases[cases["date_of_decision"].notna()].copy(deep=True)

    # removing all the invalid entries
    decided_cases = decided_cases[decided_cases["date_of_decision"] < pd.to_datetime("2023-01-01", infer_datetime_format=True)]

    decided_cases["decision_days"] = decided_cases["date_of_decision"] - decided_cases["date_of_filing"]

    mean_days_df = decided_cases[["year", "state_code", "dist_code", 
    "decision_days"]].groupby(["year", "state_code", "dist_code"]).mean()

    # converting datetime to just number of days
    mean_days_df["decision_days"] = mean_days_df["decision_days"]/pd.to_timedelta(1, unit='D')
    mean_days_df = mean_days_df.rename(columns={'decision_days':'mean_decision_days'})
    print(mean_days_df.head())
    
    mean_days_df.to_csv(f"mean-days/mean_days_{year}.csv")
    print(f"mean decision days per district ({year}) has been written to mean-days/mean_days_{year}.csv")

def aggregate_cases(year, cases):
    # filter out all the invalid entries
    # make colums for pending, solved, total
    # groupby [state_code, dist_code] and then aggregate
    # save to a file
    cases_df = cases.copy(deep=True)

    # removing all the invalid entries (where date_of_decision is not a valid/real date)
    cases_df = cases_df[(cases_df["date_of_decision"] < pd.to_datetime("2023-01-01"))
| (cases_df["date_of_decision"].isna())]

    temp = cases_df.loc[cases_df["date_of_decision"] < cases_df["date_of_filing"], "date_of_filing"]
    cases_df.loc[cases_df["date_of_decision"] < cases_df["date_of_filing"], "date_of_decision"] = temp
    cases_df["pending"] = cases_df["date_of_decision"].isna().apply(lambda x : 1 if x else 0)
    cases_df["solved"] = 1 - cases_df["pending"]
    cases_df["total"] = 1

    cases_df["decision_days"] = cases_df["date_of_decision"] - cases_df["date_of_filing"]
    cases_df["decision_days"] = cases_df["decision_days"].dt.days

    final_df = cases_df[["year", "state_code", "dist_code", "pending",
    "solved", "total", "decision_days"]].groupby(["year", "state_code", "dist_code"]).agg(pending_cases=('pending', 'sum'),
    solved_cases=('solved', 'sum'), total_cases=('total', 'sum'), total_days=('decision_days', 'sum'))

    final_df["mean_days"] = final_df["total_days"]/final_df["solved_cases"]

    final_df.to_csv(f"cases_agg/cases_agg_{year}.csv")

    #print(final_df.head())
    #print(cases_df[cases_df["date_of_decision"].isna()].head())


    """
    cases_courts = pd.merge(cases_df, courts, how="left", on=["year", "state_code", "dist_code", "court_no"]) 

    number_cases = cases_courts[["year", "state_code", "state_name", 
                                "dist_code", "district_name"]].groupby(["state_code", "dist_code"]).value_counts()
    number_cases.to_csv(f"total-cases/total_cases_{year}.csv")
    df = pd.read_csv(f"total-cases/total_cases_{year}.csv")
    df.columns.values[-1] = "total_cases"
    df.to_csv(f"total-cases/total_cases_{year}.csv", index=False)
    #number_cases.columns.values[-1] = "total_cases"
    print(f"total cases per district ({year}) has been writeen to total-cases/total_cases_{year}.csv")
    """

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
    
    #districts = pd.read_csv('../district_key.csv')

    #calculate_mean_days(year, cases)
    aggregate_cases(year, cases)
    #judges_per_district(year)
    #calculate_total_cases(year, cases, districts)

    #mean_days = pd.read_csv(f"mean-days/mean_days_{year}.csv")
    #judges = pd.read_csv(f"judges-count/judges_count_2018.csv")
    #total_cases = pd.read_csv(f"total-cases/total_cases_2018.csv")

    #merge_1 = pd.merge(means_days, judges, how='left', on=["year", "state_code", "dist_code"])
    #print(merge_1.head())

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

#judges_per_district(2018)
process(2018)
