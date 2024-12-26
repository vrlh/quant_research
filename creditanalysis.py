#random fores notes
# good to have sqrt(number of feature) per tree for each set of bootstrapped data

# fico score is credit-worthiness for assessing credit risk

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np

df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

df = df.drop('customer_id', axis=1)

print(df.head(10))

# df['Debt to Income'] = df['total_debt_outstanding'] / df['income']
# df['Utilization'] = df['loan_amt_outstanding'] / df['credit_lines_outstanding']

X = df.drop('default', axis=1)
y = df['default']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators = 100, random_state = 42)

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")


def pred(id, credit, loan, debt, income, years, fico):
    new_data = [[credit, loan, debt, income, years, fico]]
    return rf_model.predict_proba(new_data)

print(pred(4616950, 4, 5396.366774, 7009.017521, 85529.84591, 1, 610))

def calc_mse(boundaries):
    totMse = 0
    for i in range(len(boundaries)-1):
        lowVal = boundaries[i]
        highVal = boundaries[i+1]

        #calculating mean:
        counts = df[(df['fico_score'] >= lowVal) & (df['fico_score'] < highVal)]['default'].value_counts()
        total = counts[0] + counts[1]
        average = counts[1]/total

        #calculate MSE
        totMse += (counts[0]*(0 - average)**2 + counts[1]*(1-average)**2)/total
    return totMse

        
    

def selectBuckets(num_buckets):
    boundary = np.linspace(min(df['fico_score']), max(df['fico_score']), num_buckets+1)
    eps = 10

    for _ in range(10000):
        curr_mse = calc_mse(boundary)

        for i in range(1, len(boundary) - 1):
            left_boundary = list(boundary[:i]) + [boundary[i] - eps] + list(boundary[i+1:])
            right_boundary = list(boundary[:i]) + [boundary[i] + eps] + list(boundary[i+1:])

            left_mse = calc_mse(left_boundary)
            right_mse = calc_mse(right_boundary)

            if left_mse < curr_mse:
                boundary[i] -= eps
                curr_mse = left_mse
            elif right_mse < curr_mse:
                boundary[i] += eps
                curr_mse = right_mse

    return boundary




#WoE - Weight of Evidence is the predictive power of a FICO score range
# WoE = ln(% of non-events / % of events)
# non-events represnts good credit outcomes (0)
# evenets represent bad credit (1)

def WoE(bottomVal, topVal): 
    counts = df[(df['fico_score'] >= bottomVal) & (df['fico_score'] < topVal)]['default'].value_counts()
    total = counts[0] + counts[1]
    return (counts[0]/total)


finBoundary = selectBuckets(5)

for i in range(len(finBoundary) - 1):
    lowVal = finBoundary[i]
    highVal = finBoundary[i+1]
    print(f"Bucket from {lowVal} to {highVal} has {WoE(lowVal, highVal)} WoE")





    
    

