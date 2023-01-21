import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedShuffleSplit

# setting all the parameters for acts_sections.csv
dtypes = {'act' : 'float64', 'criminal' : 'float64'}
chunksize = 10 ** 6
filename = "../acts_sections.csv"
usecols = ['act', 'criminal']

# reading the acts_sections.csv file
df = pd.read_csv(filename, usecols=usecols, dtype=dtypes)
print(f"{filename} loaded")

# removing all the NaN entries
df = df[(df['act'].notna()) & (df['criminal'].notna())]
df['act'] = df['act'].astype('int64')
df['criminal'] = df['criminal'].astype('int64')

unique_acts = df.drop_duplicates(subset=['act'], keep='first')

pipe = make_pipeline(StandardScaler(), LogisticRegression())

# data splitting
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in split.split(df, df['criminal']):
    strat_train_set = df.iloc[train_index]
    strat_test_set = df.iloc[test_index]

print("data splitted successfully")

X_train = strat_train_set['act'].values.reshape(-1, 1)
y_train = strat_train_set['criminal'].values

X_test = strat_test_set['act'].values.reshape(-1, 1)
y_test = strat_test_set['criminal'].values

print("fitting the training data")
pipe.fit(X_train, y_train)
print("data fitted successfully")

acc = accuracy_score(pipe.predict(X_test), y_test)
print(f"Accuracy = {acc}")
