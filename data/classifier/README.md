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
These are the results that we got for the bail classifier:
```
Accuracy of model = 0.9999719069558377

Confusition Matrix: 
[[51953     0]
 [    0 90427]]

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00     51953
           1       1.00      1.00      1.00     90427

    accuracy                           1.00    142380
   macro avg       1.00      1.00      1.00    142380
weighted avg       1.00      1.00      1.00    142380

```

## Acquitted/Convicted Classifier

### Run Instructions

```
python acquitted-classifier.py`
```

### Results
These are the results that we got for this classifier:

```
Accuracy of model = 1.0

Confusition Matrix: 
[[300109      0]
 [     0 160182]]

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00    300109
           1       1.00      1.00      1.00    160182

    accuracy                           1.00    460291
   macro avg       1.00      1.00      1.00    460291
weighted avg       1.00      1.00      1.00    460291


```
