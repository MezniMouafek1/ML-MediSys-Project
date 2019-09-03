# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 12:01:45 2019

@author: Mezni Mouafek
"""

import pandas as pd


import pymysql
import pandas.io.sql as psql
# setup the database connection.  There's no need to setup cursors with pandas psql.s
db=pymysql.connect(host="localhost", user="root", passwd="root", db="medisys")#
query = "select * from Recommandations";

# execute the query and assign it to a pandas dataframe
df = psql.read_sql(query, con=db)

df['Temp']=df['Temp'].map({'H':1,'N':0,'L':-1})
X = df.iloc[:,[0,1]].values
y = df.iloc[:,-1].values
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


# Fitting Decision Tree Classification to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
tg=350
temp=1

resultat = classifier.predict([[tg,temp]])
resultat = resultat.astype('str')
a=pd.Series(resultat).to_json(orient='values')
from flask import Flask , jsonify
    # init app
app = Flask(__name__)

@app.route("/API22",methods=['GET'])
def Index():
    return jsonify({
   
          "Patient":{
                         "TG":tg,
                         "Temp":temp,
                         "resultat":a
                         
                       
                        
              },

               })

if __name__ == "__main__":
    app.run(port=5000,debug=False)

