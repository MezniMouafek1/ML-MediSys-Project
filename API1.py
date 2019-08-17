# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 10:58:24 2019

@author: Mezni Mouafek
"""

# Ici chargez les bibliothéques python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt# Ici chargez les bibliothéques python

# Ici mettez la ou les commandes magiques jupyternote book
# Ici chargez le fichier contenant les données
import pymysql
import pandas.io.sql as psql
# setup the database connection.  There's no need to setup cursors with pandas psql.s
db=pymysql.connect(host="localhost", user="root", passwd="root", db="medisys")# create the query
query1 = "select * from positions";
query2= "select * from temperature";
query3= "select * from tauxglucose";
# execute the query and assign it to a pandas dataframe
dataset1 = psql.read_sql(query1, con=db)
dataset1
#extract hour from timedelta
dataset1['heure']=dataset1['heure']/ np.timedelta64(1, 'h')
dataset2=psql.read_sql(query2, con=db)
dataset2
#extract hour from timedelta
dataset2['heure']=dataset2['heure']/ np.timedelta64(1, 'h')
dataset3 = psql.read_sql(query3, con=db)
#extract hour from timedelta
dataset3['heure']=dataset3['heure']/ np.timedelta64(1, 'h')
## ajouter champ temperature  à propos la date et l'heure
for ind,row in dataset1.iterrows():
    for ind1,row1 in dataset2.iterrows():
        if (row['date']==row1['date'] and abs(row['heure']-row1['heure'])<=4):
            dataset1.loc[ind,'temperature']=row1["temp"]  
    
## ajouter champ satut en fonction de la temperature
for ind,row in dataset1.iterrows():
    if row['temperature']<16:
        dataset1.loc[ind,'statutTemp']="L"
    elif row['temperature']>=16 and row['temperature']<=35:
         dataset1.loc[ind,'statutTemp']="N"
    else:
        dataset1.loc[ind,'statutTemp']="H"
    
## ajouter champ taux de glécimie à propos la date et l'heure
for ind,row in dataset3.iterrows():
    for ind2,row2 in dataset1.iterrows():
        if (row['id']==row2['id'] and row['date']==row2['date'] and abs(row1['heure']-row2['heure'])<=4 ):
            dataset1.loc[ind,'tauxglécimie']=row["tauxglucosemgdl"]
data=dataset1.drop(['id','date','heure','latitude','longitude','statutTemp'],axis=1)
data.columns = ['position','temperature','tauxglucose']

for ind,row in dataset1.iterrows():
    if row['tauxglécimie']>=110:
        dataset1.loc[ind,'statutglecimie']="Hyperglycémie"
    elif row['tauxglécimie']>75 and row['tauxglécimie']<110:
         dataset1.loc[ind,'statutglecimie']="Normal"
    else:
        dataset1.loc[ind,'statutglecimie']="Hypoglécimie"
##effacer les valeurs na
dataset1.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)       
## Pourcentage des patients atteignent de l'hyperglécemie
pourcentageHyp=float((dataset1 ["statutglecimie"]=="Hyperglycémie").sum())/dataset1.shape[0]
pourcentageHyp
## Pourcentage des patients atteignent de l'hypoglécimie
percentHypo=float((dataset1 ["statutglecimie"]=="Hypoglécimie").sum())/dataset1.shape[0]
percentHypo
## Pourcentage des patients atteignent de Normal
percentNormal=float((dataset1 ["statutglecimie"]=="Normal").sum())/dataset1.shape[0] 
percentNormal   
##classement des statutglecimie par temperature
## hyper & Low temperature
HyperLtemp=float(((dataset1["statutTemp"]=="L")&(dataset1 ["statutglecimie"]=="Hyperglycémie")).sum())/dataset1.shape[0]
## hypo & Hight temperature
HyperHtemp=float(((dataset1["statutTemp"]=="H")&(dataset1 ["statutglecimie"]=="Hyperglycémie")).sum())/dataset1.shape[0]
## hypo & Normal temperature
HyperNtemp=float(((dataset1["statutTemp"]=="N")&(dataset1 ["statutglecimie"]=="Hyperglycémie")).sum())/dataset1.shape[0]

## hypo & Low temperature
HypoLtemp=float(((dataset1["statutTemp"]=="L")&(dataset1 ["statutglecimie"]=="Hypoglycémie")).sum())/dataset1.shape[0]
## hypo & Hight temperature
HypoHtemp=float(((dataset1["statutTemp"]=="H")&(dataset1 ["statutglecimie"]=="Hypoglycémie")).sum())/dataset1.shape[0]
## hypo & Normal temperature
HypoNtemp=float(((dataset1["statutTemp"]=="N")&(dataset1 ["statutglecimie"]=="Hypoglycémie")).sum())/dataset1.shape[0]

## Normal & Low temperature
NormalLtemp=float(((dataset1["statutTemp"]=="L")&(dataset1 ["statutglecimie"]=="Normal")).sum())/dataset1.shape[0]
## Normal & Hight temperature
NormalHtemp=float(((dataset1["statutTemp"]=="H")&(dataset1 ["statutglecimie"]=="Normal")).sum())/dataset1.shape[0]
## Normal & Normal temperature
NormalNtemp=float(((dataset1["statutTemp"]=="N")&(dataset1["statutglecimie"]=="Normal")).sum())/dataset1.shape[0]

##classement des statutglecimie par Position
## hyper & Home positions
HyperHome=float(((dataset1["nom"]=="Home")&(dataset1 ["statutglecimie"]=="Hyperglycémie")).sum())/dataset1.shape[0]
## hyper & Work Position
HyperWork=float(((dataset1["nom"]=="Work")&(dataset1 ["statutglecimie"]=="Hyperglycémie")).sum())/dataset1.shape[0]
## hypo & Home positions
HypoHome=float(((dataset1["nom"]=="Home")&(dataset1 ["statutglecimie"]=="Hypoglycémie")).sum())/dataset1.shape[0]
## hypo & work positions
HypoWork=float(((dataset1["nom"]=="Work")&(dataset1 ["statutglecimie"]=="Hypoglycémie")).sum())/dataset1.shape[0]
## Normal & Home positions
NormalHome=float(((dataset1["nom"]=="Home")&(dataset1 ["statutglecimie"]=="Normal")).sum())/dataset1.shape[0]
## Normal & work positions
NormalWork=float(((dataset1["nom"]=="Work")&(dataset1 ["statutglecimie"]=="Normal")).sum())/dataset1.shape[0]

from flask import Flask , jsonify

# init app
app = Flask(__name__)

@app.route("/API1",methods=['GET'])
def Index():
    return jsonify({
   "Norme":{
     "hyper":pourcentageHyp,
     "hypo":percentHypo,
     "Normal":percentNormal
              },
  "causes": {
          "Hyper":
                     {
                         "temperature":
                                     {"High": HyperHtemp, "Normal":HyperNtemp ,"Low":HyperLtemp},
                                                        
                         "Position": {"Home": HyperHome, "Work":HyperWork}
                 
          },
        "Hypo":
            { 
            
                         "temperature":
                                     {"High": NormalHtemp, "Normal":NormalNtemp ,"Low":NormalLtemp},
                                                        
                         "Position": {"Home": HypoHome, "Work":HypoWork
                 
          },
                      
                      },
                "Normal":
            { 
            
                         "temperature":
                                     {"High": HypoHtemp, "Normal":NormalNtemp ,"Low":NormalLtemp},
                                                        
                         "Position": {"Home": NormalHome, "Work":NormalWork}
                 
          }}
                      
                      
             

               
              })

if __name__ == "__main__":
    app.run(port=8000,debug=True)