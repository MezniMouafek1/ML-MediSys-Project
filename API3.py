# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
# Ici chargez les bibliothéques python

t"""
# Ici chargez le fichier contenant les données
# Ici chargez les bibliothéques python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Ici mettez la ou les commandes magiques jupyternote book

# Ici chargez le fichier contenant les données

dataset = pd.read_csv("Pima.te.csv")
dataset
for ind,row in dataset.iterrows():
    if row['glu']>=110:
        dataset.loc[ind,'statut']="Hyperglycémie"
    elif row['glu']>=75 and row['glu']<110:
         dataset.loc[ind,'statut']="Normal"
    else:
        dataset.loc[ind,'statut']="Hypoglécimie"
        
         
 
## Pourcentage des patients atteignent de l'hyperglécemie
pourcentageHyp=float((dataset ["statut"]=="Hyperglycémie").sum())/dataset.shape[0]
## Pourcentage des patients atteignent de l'hypoglécimie
percentHypo=float((dataset ["statut"]=="Hypoglécimie").sum())/dataset.shape[0]
## Pourcentage des patients atteignent de Normal
percentNormal=float((dataset ["statut"]=="Normal").sum())/dataset.shape[0]
## Pourcentage des patients Enfants (00 à 14 ans)
enfant=float((dataset['age']<=14).sum())/dataset.shape[0]
#Age
## Pourcentage des patients Adolescents (15 à 24 ans)
Adol=float(((dataset['age']>=15)&(dataset['age']<=24)).sum())/dataset.shape[0]
## Pourcentage des patients Adultes (25 à 64 ans)
Adulte=float(((dataset['age']>=25)&(dataset['age']<64)).sum())/dataset.shape[0]
## Pourcentage des patients Aînés (64 ans et plus)
Aine=float((dataset['age']>64).sum())/dataset.shape[0]
# Classement des ages par Statut
 ### patients Enfants
 ## Pourcentage des Hyperglycémies 
hyperEnfant=float(((dataset['age']<=14)&(dataset["statut"]=="Hyperglycémie")).sum())/dataset.shape[0]  
## Pourcentage des patients Normals
NormalEnfant=float(((dataset['age']<=14)&(dataset["statut"]=="Normal")).sum())/dataset.shape[0]  
## Pourcentage des patients Hypoglycémies 
HypoEnfant=float(((dataset['age']<=14)&(dataset["statut"]=="Hypoglycémie")).sum())/dataset.shape[0] 
 ### patients Adultes
 ### patients Adolescents
 ## Pourcentage des Hyperglycémies 
hyperAdo=float(((dataset['age']>=15)&(dataset['age']<=24)&(dataset["statut"]=="Hyperglycémie")).sum())/dataset.shape[0]  
## Pourcentage des patients Normals
NormalAdo=float(((dataset['age']>=15)&(dataset['age']<=24)&(dataset["statut"]=="Normal")).sum())/dataset.shape[0]  
## Pourcentage des patients Hypoglycémies 
HypoAdo=float(((dataset['age']>=15)&(dataset['age']<=24)&(dataset["statut"]=="Hypoglycémie")).sum())/dataset.shape[0] 
 ### patients Adultes
## Pourcentage des Hyperglycémies 
hyperAdult=float(((dataset['age']>=25)&(dataset['age']<64)&(dataset["statut"]=="Hyperglycémie")).sum())/dataset.shape[0]
## Pourcentage des Hypoglycémies 
HypoAdult=float(((dataset['age']>=25)&(dataset['age']<64)&(dataset["statut"]=="Hypoglycémie")).sum())/dataset.shape[0]
## Pourcentage des Hypoglycémies 
NormalAdult=float(((dataset['age']>=25)&(dataset['age']<64)&(dataset["statut"]=="Normal")).sum())/dataset.shape[0] 
 ## patients Aînés
## Pourcentage des Hyperglycémies 
hyperAine=float(((dataset['age']>=64)&(dataset["statut"]=="Hyperglycémie")).sum())/dataset.shape[0] 
## Pourcentage des patients Hypoglycémies 
hypoAine=float(((dataset['age']>=64)&(dataset["statut"]=="Hypoglycémie")).sum())/dataset.shape[0]  
## Pourcentage des patients Normals
NormalAine=float(((dataset['age']>=64)&(dataset["statut"]=="Normal")).sum())/dataset.shape[0]   
from flask import Flask , jsonify
a=2
# init app
app = Flask(__name__)

@app.route("/API3",methods=['GET'])
def Index():
    return jsonify({
   "Norme":{
     "hyper":pourcentageHyp,
     "hypo":percentHypo,
     "Normal":percentNormal
              },
  "causes": {
          "Age": [
                   {"Enfant": enfant,"NormeEnfant": [
                   {"hyper": hyperEnfant, "hypo":HypoEnfant ,"Normal":HypoEnfant},
                                                        ],
                   },
             
                   { "Adolescents":Adol ,"NormeAdolescents": [
                   {"hyper":hyperAdo , "hypo":HypoAdo,"Normal": NormalAdo },
                                                          ],
                   },
                   { "Adultes":Adulte ,"NormeAdulte": [
      {"hyper": hyperAdult, "hypo":HypoAdult,"Normal":NormalAdult },
                                               ],
                   },
                   { "Aînés":Aine ,"NormeAinés": [
      {"hyper": hyperAine, "hypo":hypoAine ,"Normal": NormalAine},
                                                          ],
                   }               
               
                ]
           }
          

               })

if __name__ == "__main__":
    app.run(port=9000,debug=False)
