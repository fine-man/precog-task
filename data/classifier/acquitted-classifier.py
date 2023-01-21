import pandas as pd
import datetime as dt
import pickle
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
from sklearn.metrics import classification_report

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

# reading the display file
disp_filename = "../keys/disp_name_key.csv"
disp_df = pd.read_csv(disp_filename)
print(f"loaded file {disp_filename}")

disp_df.drop('count', axis=1, inplace=True)

# strings related to bail judgement
disp_strings = ['acquitted', 'convicted']

# filtering all the judgements related to bail
disp_df = disp_df[disp_df['disp_name_s'].isin(disp_strings)]

disp_cases_list = []

# function for data cleaning
def transform(cases_df):
    # remove unwanted columns
    # change the type of date columns
    # remove all invalid date columns

    # make 3 new columns for each date column
    # make a bail column
    # turn judges into onehotencoding
    # remove all na values
    
    cases = cases_df.copy(deep=True)
    # change the type of all date columns
    date_columns = ['date_of_filing', 'date_first_list', 'date_last_list', 
    'date_next_list', 'date_of_decision']

    for column_name in date_columns:
        cases[column_name] = pd.to_datetime(cases[column_name], errors='coerce')

    # make sure the dates are in ascending order
    print(cases.shape)
    for i in range(1, len(date_columns)):
        column_name = date_columns[i]
        prev_name = date_columns[i-1]
        print(column_name, prev_name, end=' ')
        cases = cases[(cases[column_name] < dt.datetime.now()) &
                      (cases[column_name] >= cases[prev_name])]
        print(cases.shape)

    # drop all the NaN values
    cases.dropna(subset=cases.columns.values, inplace=True)
    
    # dropping all useless columns
    cases.drop(['ddl_case_id', 'cino', 'female_defendant',
                       'female_petitioner', 'female_adv_def',
                       'female_adv_pet'], axis=1, inplace=True)

    
    # adding the acquitted column
    cases['acquitted'] = 0
    cases.loc[cases['disp_name_s'].isin(disp_strings[0:1]), 'acquitted'] = 1
    
    column_dict = {'date_of_filing' : 'filing', 'date_first_list' : 'first', 
                   'date_last_list' : 'last', 'date_next_list' : 'next',
                   'date_of_decision' : 'decision'}

    # transforming all the datetime columns
    for column_name, name in column_dict.items():
        cases[f"{name}_year"] = cases[column_name].dt.year
        cases[f"{name}_month"] = cases[column_name].dt.month
        cases[f"{name}_day"] = cases[column_name].dt.day

    # removing unwanted columns
    cases.drop(['judge_position', 'disp_name_s'] + date_columns, axis=1, inplace=True)
    return cases

def filter_cases(year, disp=disp_df):
    cases = pd.read_csv(f'../cases/cases_{year}.csv')
    print(f'cases_{year}.csv has been loaded')

    cases = pd.merge(cases, disp, on=['year', 'disp_name'])
    return cases

years = [year for year in range(2018, 2019)]

for year in years:
    disp_cases_list.append(filter_cases(year))

# all the cases where judgement is related to bail
disp_cases_df = pd.concat(disp_cases_list)
print("filtered all the acquitted cases from all the years")

cases = transform(disp_cases_df)
print("cleaned and transformed the data successfully")

# split the dataset into training and testing according to distribution
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(cases, cases["acquitted"]):
    strat_train_set = cases.iloc[train_index]
    strat_test_set = cases.iloc[test_index]

print("dataset splitted")

feature_columns = list(strat_train_set.columns)
feature_columns.remove('acquitted')

X_train = strat_train_set[feature_columns].to_numpy()
y_train = strat_train_set['acquitted'].to_numpy()

X_test = strat_test_set[feature_columns].to_numpy()
y_test = strat_test_set['acquitted'].to_numpy()

print("training the model...")
clf = RandomForestClassifier(random_state=0)
clf.fit(X_train, y_train)
print("model trained")

with open('acquitted.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("trained model has been saved to acquitted.pkl")

acc = accuracy_score(clf.predict(X_test), y_test)
print(f"Accuracy of model = {acc}")

y_train_pred = cross_val_predict(clf, X_train, y_train, cv=3)

print("Confusition Matrix: ")
print(confusion_matrix(y_train, y_train_pred))

print("Classification Report")
print(classification_report(y_train, y_train_pred))
