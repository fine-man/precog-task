# Classifier

The feature space for both the classifiers are the meta-data of the case like
`state_code, dist_code, court_no, date_of_filing, date_first_list,
date_next_list, date_last_list, date_of_decision`

## Bail Classifier

### Run Instructions

```
python bail-classifier.py
```

### Results
I first trained the classifier using a Random Forrest Classifier and got
the following results.

```
Accuracy of model = 0.6957300352565896

Confusion Matrix: 
[[25687 26527]
 [18541 72195]]

Classification Report: 
              precision    recall  f1-score   support

           0       0.58      0.49      0.53     52214
           1       0.73      0.80      0.76     90736

    accuracy                           0.68    142950
   macro avg       0.66      0.64      0.65    142950
weighted avg       0.68      0.68      0.68    142950
```
After that I tried training the classifier using a Gaussian Naive Bayes
model but still didn't got good results.

## Acquitted/Convicted Classifier

### Run Instructions

```
python acquitted-classifier.py`
```

### Results
The model that I used for this is a Random Forrest Classifier and I got
the following result

```
Accuracy of model = 0.9404291189071285

Confusion Matrix: 
[[281393  18716]
 [ 10310 149872]]

Classification Report: 
              precision    recall  f1-score   support

           0       0.96      0.94      0.95    300109
           1       0.89      0.94      0.91    160182

    accuracy                           0.94    460291
   macro avg       0.93      0.94      0.93    460291
weighted avg       0.94      0.94      0.94    460291
```
