import pandas as pd

def visualize_data():
    mean_days_df = pd.read_csv(f"final.csv")
    districts = pd.read_csv("../my-keys/district_key.csv")
    map_unique_id = pd.read_csv("../my-keys/district_unique_id.csv")

    df = pd.merge(mean_days_df, districts, how='left', on=["state_code", "dist_code"])
    data_map_df = pd.merge(df, map_unique_id, on=["district_name"])
    data_map_df[["Name", "Unique-ID","mean_decision_days"]].to_csv(f"mean_decision_days.csv", index=False)
    #print(f"mean decision days data map {year} has been written to data-map/mean_map_{year}.csv"

visualize_data()
