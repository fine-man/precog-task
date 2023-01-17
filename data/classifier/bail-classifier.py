import pandas as pd
import datetime as dt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix

# filtering
# for each year, filter all the bail related cases
# combine the data of all these years

# transformations
# make a bail column to tell if bail was given
# remove all the unwanted columns

# making a training and testing data set
# make a train and test data set
# make a feature and label train and test data set

# train the model
# evaluate the model

cases_filename = "../cases/cases_2018.csv"
disp_filename = "../keys/disp_name_key.csv"

cases = pd.read_csv(cases_filename)
print(f"loaded file {cases_filename}")

cases["date_of_filing"] = pd.to_datetime(cases["date_of_filing"],
                                         infer_datetime_format=True,
                                         errors='coerce')

cases["date_of_decision"] = pd.to_datetime(cases["date_of_decision"],
                                         infer_datetime_format=True,
                                         errors='coerce')

cases = cases[['year', 'state_code', 'dist_code', 'court_no', 'type_name', 'purpose_name', 'disp_name', 'date_of_filing', 'date_of_decision']]

print(cases.columns)
## Cleaning the data

# remove all the invalid dates - done
# merge with disp_key.csv
# filter all the ones with bail in them
# make a 'bail' category

# transform the dates into year, month and day - easy to do
# transform the judge_position string into number matrix
# try to transform the mail female columns as well

# loading disp_key_name.csv
disp = pd.read_csv(disp_filename)
print(f"loaded file {disp_filename}")

# removing all the invalid entries (where date of decision is not a valid/real date)
# also removing all the date of decisions = ""
cases = cases[(cases["date_of_decision"] < dt.datetime.now()) & 
(cases["date_of_decision"] >= cases["date_of_filing"])]

cases = pd.merge(cases, disp, how='left', on=['year', 'disp_name'])

# filtering all cases where judgement is bail related
bail_strings = ['bail granted', 'bail order', 'bail refused', 'bail rejected']
cases = cases[cases['disp_name_s'].isin(bail_strings)]

# removing NaN values
cases = cases[cases['purpose_name'].notna()]

# setting the bail column
cases['bail'] = 0
cases.loc[cases['disp_name_s'] == "bail granted", ['bail']] = 1

# transforming the dates
cases['filing_year'] = cases['date_of_filing'].dt.year
cases['filing_month'] = cases['date_of_filing'].dt.month
cases['filing_day'] = cases['date_of_filing'].dt.day

cases['decision_year'] = cases['date_of_decision'].dt.year
cases['decision_month'] = cases['date_of_decision'].dt.month
cases['decision_day'] = cases['date_of_decision'].dt.day

cases.drop(['year', 'date_of_filing', 'date_of_decision', 'disp_name', 'disp_name_s', 'count'], axis=1, inplace=True)

# split the dataset into training and testing according to distribution
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(cases, cases["bail"]):
    strat_train_set = cases.iloc[train_index]
    strat_test_set = cases.iloc[test_index]

feature_columns = list(strat_train_set.columns)
feature_columns.remove('bail')

X_train = strat_train_set[feature_columns].to_numpy()
y_train = strat_train_set['bail'].to_numpy()

X_test = strat_test_set[feature_columns].to_numpy()
y_test = strat_test_set['bail'].to_numpy()

clf = RandomForestClassifier(random_state=0)
clf.fit(X_train, y_train)
acc = accuracy_score(clf.predict(X_test, y_test))

y_train_pred = cross_val_predict(clf, X_train, y_train, cv=3)
confusion_matrix(y_train, y_train_pred)
