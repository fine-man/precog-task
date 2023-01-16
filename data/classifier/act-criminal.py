import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

# getting the training data
X_train = unique_acts['act'].values.reshape(-1, 1)
y_train = unique_acts['criminal'].values

# getting the testing data
X_test = df['act'].values.reshape(-1, 1)
y_test = df['criminal'].values

clf = RandomForestClassifier(random_state=0)

# fitting the data
print("fitting the data to the classifier")
clf.fit(X_train, y_train)
print("fitted the classifier to the training data")

accuracy = []

n = len(X_test)

for i in range(0, n, chunksize):
    j = i + chunksize
    acc = 0
    if j >= n:
        acc = accuracy_score(clf.predict(X_test[i:]), y_test[i:])
    else:
        acc = accuracy_score(clf.predict(X_test[i:j]), y_test[i:j])

    print(i, j, acc)
    accuracy.append(acc)

print("found all the accuracy scores")

print(min(accuracy))
