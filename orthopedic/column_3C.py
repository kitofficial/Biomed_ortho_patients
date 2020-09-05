# -*- coding: utf-8 -*-
"""
Created on Mon May 18 00:02:31 2020

@author: Ankit
"""


# -*- coding: utf-8 -*-
"""
Created on Sat May  9 03:05:02 2020

@author: Ankit
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
# preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split



#models
from sklearn.linear_model import LogisticRegression,RidgeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier  
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.metrics import recall_score



#Downloading dataset
data=pd.read_csv("column_3C_weka.csv")
print(data)
top_data=data.head(3)
data.info()

# Categorical boolean mask
categorical_feature_mask = data.dtypes==object
# filter categorical columns using mask and turn it into a list
categorical_cols = data.columns[categorical_feature_mask].tolist()
# instantiate labelencoder object
le = LabelEncoder()
# apply le on categorical feature columns
data[categorical_cols] = data[categorical_cols].apply(lambda col: le.fit_transform(col))
data[categorical_cols].head(10)
print(data)

#I split data on 30% in the test dataset, the remaining 70% - in the training dataset
train, test, target, target_test = train_test_split(data[["pelvic_incidence","pelvic_tilt","lumbar_lordosis_angle","sacral_slope","pelvic_radius","degree_spondylolisthesis"]], data[["class"]], test_size=0.3, random_state=1)
train.info()
test.info()


##CONFUSION MATRIX FUNCTION
def confusionmatrix(y_test,y_predict,x='name of model'):
    cm=metrics.confusion_matrix(y_test,y_predict)
    recall=print(round(recall_score(y_test, y_predict, average='macro')*100,2))
    plt.figure(figsize=(10,7))
    sn.heatmap(cm,annot=True)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(x)
    return [ plt.show(),recall ]
    


## Logistic Regression

logreg = LogisticRegression()
logreg.fit(train, target)
acc_log = round(logreg.score(train, target) * 100, 2)
acc_test_log = round(logreg.score(test, target_test) * 100, 2)


# visualization using confusion matrix
confusionmatrix(target_test,logreg.predict(test),x='Logistic regression')





# Support Vector Machines
svc = SVC()
svc.fit(train, target)
acc_svc = round(svc.score(train, target) * 100, 2)

acc_test_svc = round(svc.score(test, target_test) * 100, 2)

# visualization using confusion matrix
confusionmatrix(target_test,svc.predict(test),x='support vector machine')



## Decision Tree Classifier
decision_tree = DecisionTreeClassifier()
decision_tree.fit(train, target)
acc_decision_tree = round(decision_tree.score(train, target) * 100, 2)

acc_test_decision_tree = round(decision_tree.score(test, target_test) * 100, 2)

# visualization using confusion matrix
confusionmatrix(target_test,decision_tree.predict(test),x='Decision Tree Classifier')


## Random Forest

acc_final_random_forest= []
acc_test_final_random_forest= []



for m in range(80,126):
    random_forest=RandomForestClassifier(n_estimators= m,random_state=1)
    random_forest.fit(train, target)
    acc_random_forest=round(random_forest.score(train,target) * 100, 2)
    acc_final_random_forest.append(acc_random_forest)
    acc_test_random_forest=round(random_forest.score(test, target_test) * 100, 2)
    acc_test_final_random_forest.append(acc_test_random_forest)


#here it is visible that max. accuracy of test data is at n = 80
plt.figure()        
l = range(80,126)
for j in range(len(l)):     
    plt.plot( l, acc_test_final_random_forest)
    plt.xlabel('Values of n_estimators')
    plt.ylabel('Accuracy of test data')
    plt.title('Variation of accuracy of prediction with different n_estimators values in random forest')

#visualization using confusion matrix for maximum accuracy as it comes at n=80
random_forest=RandomForestClassifier(n_estimators= 80,random_state=1)
random_forest.fit(train, target)
confusionmatrix(target_test,random_forest.predict(test),x='Random Forest')
   





## Ridge Classifier

ridge_classifier = RidgeClassifier()
ridge_classifier.fit(train, target)
acc_ridge_classifier = round(ridge_classifier.score(train, target) * 100, 2)
print(acc_ridge_classifier)

acc_test_ridge_classifier = round(ridge_classifier.score(test, target_test) * 100, 2)
print(acc_test_ridge_classifier)


# visualization using confusion matrix
confusionmatrix(target_test,ridge_classifier.predict(test),x='Ridge Classifier')



##KNN CLASSIFIER

acc_knn_classifier= np.empty((10, 1))


acc_test_knn_classifier= np.empty((10, 1))


for i in range(0,10):
      knn =KNeighborsClassifier(n_neighbors=i+1)
      knn.fit(train, target)
      acc_knn_classifier[i,:]=round(knn.score(train, target) * 100, 2)
      acc_test_knn_classifier[i,:]= round(knn.score(test, target_test) * 100, 2)
      
      
      
    
     
#here it is visible that max. accuracy of test data is with value of n=9   
plt.figure()        
l = range(1,11)
for j in range(len(l)):     
    plt.plot( l, acc_test_knn_classifier)
    plt.xlabel('Values of n_neighbors')
    plt.ylabel('Accuracy of test data')
    plt.title('Variation of accuracy of prediction with different n values in knn method')
    
    
#visualization using confusion matrix for maximum accuracy as it comes at n_neighbors=9
knn =KNeighborsClassifier(n_neighbors=9)
knn.fit(train, target)
confusionmatrix(target_test,knn.predict(test),x='KNN CLASSIFIER')
        
        
## K-mean CLASSIFIER

acc_k_mean_classifier= np.empty((10, 1))
acc_test_k_mean_classifier= np.empty((10, 1))

for p in range(0,10):
      k_mean =KMeans(n_clusters=p+1)
      k_mean.fit(train, target)
      acc_k_mean_classifier[p,:]=round(knn.score(train, target) * 100, 2)
      acc_test_k_mean_classifier[p,:]= round(knn.score(test, target_test) * 100, 2)
      
     
#here we can see the number of cluster are not able to affect the accuracy of test data   
plt.figure()       
m = range(1,11)
for k in range(len(m)):     
    plt.plot( m, acc_test_k_mean_classifier)
    plt.xlabel('Values of n_clusters')
    plt.ylabel('Accuracy of test data')
    plt.title('Variation of accuracy of prediction with different n values in k-mean')
    
#visualization using confusion matrix for maximum accuracy as it comes at n_neighbors=9
k_mean =KMeans(n_clusters=2)
k_mean.fit(train, target)
confusionmatrix(target_test,k_mean.predict(test),x='K-mean CLASSIFIER')  


##DETAILS
details_data=data.describe()
print(details_data)

##Models evaluation
models = pd.DataFrame({
    'Model': ['Logistic Regression', 'Support Vector Machines','Decision Tree Classifier', 'Random Forest','Ridge Classifier','KNN CLASSIFIER','K-mean CLASSIFIER'],
    
    'Score_train': [acc_log, acc_svc,acc_decision_tree, acc_final_random_forest[0],acc_ridge_classifier,acc_test_knn_classifier[8,:],acc_k_mean_classifier[1,:]],
    'Score_test': [acc_test_log, acc_test_svc,acc_test_decision_tree, acc_test_final_random_forest[0], acc_test_ridge_classifier,acc_test_knn_classifier[8,:],acc_test_k_mean_classifier[1,:]]})


models['Score_diff'] = abs(models['Score_train'] - models['Score_test'])
models.sort_values(by=['Score_diff'], ascending=True)
print(models)


## Final Plot
plt.figure()
xx = models['Model']
plt.tick_params(labelsize=14)
plt.plot(xx, models['Score_train'], label = 'Score_train')
plt.plot(xx, models['Score_test'], label = 'Score_test')
plt.legend()
plt.title('Score of 7 popular models for train and test datasets')
plt.xlabel('Models')
plt.ylabel('Score, %')
plt.xticks(xx, rotation='vertical')
plt.show()

