# Precog Programming Task

## Build Instructions
First clone the repository
```
git clone https://github.com/fine-man/precog-task.git

cd precog-task
```
Now download the zip file from [here](https://www.dropbox.com/sh/hkcde3z2l1h9mq1/AAB2U1dYf6pR7qij1tQ5y11Fa/csv?dl=0&subfolder_nav_tracking=1)
and put the `csv.zip` file in `precog-task/data` directory
After that cd into the `precog-task/data` directory and run this

```
./build.sh
```

## Motivation behind the analysis
The underlying principle behind all three of my analyses is to identify 
ways to enhance court performance and efficiency. This involves identifying 
areas where efficiency is lacking and allocating resources accordingly. 

Another objective of the analysis is to use data to determine where stricter 
regulations are needed for certain crimes and where they are not. I used the 
example of women's domestic violence in my analysis, but the method can be 
applied to other crimes as well.

## Some terminology
These are some terms that I will be referencing throughout my analysis and
so I just kept it in the main README.

> Case Pendency Rate : The ratio of the number of pending cases and the total cases filed. Places with a lower case pendency rate will be considered to have a more efficient judiciary.

> Case Disposition Rate : Same as case pendency rate but this is the ratio of number of disposed (decided) cases and the total cases filed. Places with a higher case disposition rate will be considered to have a more efficient judiciary.

> Mean Disposition Days : The average number of days it took to dispose off a case. In other words, this is the mean difference between date of decision and date of filing. Places with a lower mean disposition days will be considered to have a more efficient judiciary.

> Cases Per Judge : This is the average number of cases assigned to each judge in a particular place. This is a measure of the workload on the judiciary and so places with lower cases per judge will be considered to have a more efficient judiciary.

## Different kinds of analysis
- A General Analysis : In this analysis, I look at the whole country at
once and try to find correlation between various things. The folder for
this analysis is `general-analysis` in `data` directory.

- A State Analysis : In this analysis, I look at the cases from a state
perspective and rank them based on various criteria and also find the state
with the most efficient judiciary according to the set of metrics
defined above. The folder for this analysis is `state-analysis` in `data`
directory.

- Delhi Analysis : In this analysis, I look at all the districts in Delhi
and plot the trends over the years for a set of attributes. The folder for
this analysis is `delhi-analysis` in `data` directory.

## Classification
I have done the following two classifications and both of them can be found
in `classifier` folder in the `data` directory.

- Classifying cases as `bail granted` or `bail rejected`
- Classifying cases as `acquited` or `convicted`
