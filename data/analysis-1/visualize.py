import pandas as pd

def mean_days_to_data_map(year):
    mean_days_df = pd.read_csv(f"mean-days/mean_days_{year}.csv")
    districts = pd.read_csv("../my-keys/district_key.csv")
    map_unique_id = pd.read_csv("../my-keys/district_unique_id.csv")

    df = pd.merge(mean_days_df, districts, how='left', on=["state_code", "dist_code"])
    data_map_df = pd.merge(df, map_unique_id, on=["district_name"])
    data_map_df[["Name", "Unique-ID","mean_decision_days"]].to_csv(f"data-map/mean_map_{year}.csv", index=False)
    print(f"mean decision days data map {year} has been written to data-map/mean_map_{year}.csv")
