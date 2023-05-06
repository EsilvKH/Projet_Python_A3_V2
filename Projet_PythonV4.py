# -*- coding: utf-8 -*-
"""
Created on Sat May  6 14:13:07 2023

@author: user
"""



import pandas as pd
import numpy as np
import os

file_path_list = ["C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2018.txt",
                  "C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2019.txt",
                  "C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2020.txt",
                  "C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2021.txt",
                  "C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2022.txt"]

for i in range(len(file_path_list)):
    file_path=file_path_list[i]
    if os.access(file_path, os.R_OK):
        print('File has read permission')
    else:
        print('File does not have read permission')
    
    os.chmod(file_path, 0o400)

#data = 'D:\Esilv\Annee 3\Semestre 6\Python\Projet\Valeursfoncieres-2018.txt'
#<_io.TextIOWrapper name='D:\\Esilv\\Annee 3\\Semestre 6\\Python\\Projet\\Valeursfoncieres-2018.txt' mode='r' encoding='cp65001'>
#print(data)

dataframe2018 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2018.txt", sep="|")
#dataframe2019 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2019.txt", sep="|")
#dataframe2020 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2020.txt", sep="|")
#dataframe2021 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2021.txt", sep="|")
#dataframe2022 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2022.txt", sep="|")

#nom_colonnes=[]
#for col in dataframe2018.columns:
#    nom_colonnes.append(col)
#nom_colonnes

#Transcription rapide
#used_dataframe=dataframe2018

fr_departments = {
    "Auvergne-Rhône-Alpes": ["1", "3", "7", "15", "26", "38", "42", "43", "63", "69", "73", "74"],
    "Bourgogne-Franche-Comté": ["21", "25", "39", "58", "70", "71", "89", "90"],
    "Bretagne": ["22", "29", "35", "56"],
    "Centre-Val de Loire": ["18", "28", "36", "37", "41", "45"],
    "Corse": ["2A", "2B"],
    "Grand Est": ["8", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
    "Hauts-de-France": ["2", "59", "60", "62", "80"],
    "Île-de-France": ["75", "77", "78", "91", "92", "93", "94", "95"],
    "Normandie": ["14", "27", "50", "61", "76"],
    "Nouvelle-Aquitaine": ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"],
    "Occitanie": ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"],
    "Pays de la Loire": ["44", "49", "53", "72", "85"],
    "Provence-Alpes-Côte d'Azur": ["4", "5", "6", "13", "83", "84"]
}



#%% Nettoyage des colonnes inutiles
dataframe2018=dataframe2018.drop(
                    ["Identifiant de document",
                    "Reference document",
                    "1 Articles CGI",
                    "2 Articles CGI",
                    "3 Articles CGI",
                    "4 Articles CGI",
                    "5 Articles CGI",
                    "No disposition",
                    "Code commune",
                    "Prefixe de section",
                    "Section",
                    "No plan",
                    "No Volume",
                    "1er lot",
                    "2eme lot",
                    "3eme lot",
                    "4eme lot",
                    "5eme lot",
                    "Identifiant local"
                    ],axis=1)

#%%
list_colonnes_utiles=["Date mutation","Nature mutation","Valeur fonciere"]
indexes_to_drop=[]
for nom in list_colonnes_utiles: 
    indexes_to_drop += list(np.where(pd.isnull(dataframe2018[nom]))[0])
indexes_to_drop = list(set(indexes_to_drop))  # On supprime les doublons
dataframe2018 = dataframe2018.drop(indexes_to_drop)
dataframe2018 = dataframe2018.reset_index(drop=True)

del nom
del indexes_to_drop
del list_colonnes_utiles
#Methode verifiée

#%%  Rajout des valeurs principales


#Rajoute la région comme colonne des dataframes
print(fr_departments)
dataframe2018["Region"] = np.nan
for i in range(len(dataframe2018["Code departement"])):
    valeurdepartement = dataframe2018["Code departement"][i]
    for j in fr_departments:
        if(str(valeurdepartement) in fr_departments[j]):
            dataframe2018["Region"][i] = j
            break
print(dataframe2018["Region"])
del fr_departments
del i
del valeurdepartement
del j
#%% Séparez les lots uniques des lots multipes

dataframe2018_multi_lots = dataframe2018[dataframe2018['Nombre de lots'] >= 1]
dataframe2018_uni_lots = dataframe2018[dataframe2018['Nombre de lots'] == 0]
dataframe2018_multi_lots = dataframe2018_multi_lots.reset_index(drop=True)
dataframe2018_uni_lots = dataframe2018_uni_lots.reset_index(drop=True)

#%% Nettoyer les deux dataframes des valeurs non-renseignées
list_index_to_drop=[]
for i in range(len(dataframe2018_multi_lots)):
    if(pd.isnull(dataframe2018_multi_lots["Surface Carrez du 1er lot"][i])
       and pd.isnull(dataframe2018_multi_lots["Surface Carrez du 2eme lot"][i])
       and pd.isnull(dataframe2018_multi_lots["Surface Carrez du 3eme lot"][i])
       and pd.isnull(dataframe2018_multi_lots["Surface Carrez du 4eme lot"][i])
       and pd.isnull(dataframe2018_multi_lots["Surface Carrez du 5eme lot"][i])):
           list_index_to_drop.append(i)
dataframe2018_multi_lots = dataframe2018_multi_lots.drop(list_index_to_drop)

list_index_to_drop=[]
for i in range(len(dataframe2018_uni_lots)):
    if(pd.isnull(dataframe2018_uni_lots["Surface reelle bati"][i])
       and pd.isnull(dataframe2018_uni_lots["Surface terrain"][i])):
           list_index_to_drop.append(i)
dataframe2018_uni_lots = dataframe2018_uni_lots.drop(list_index_to_drop)

#Après nettoyage il faut reformater les dataframes
dataframe2018_multi_lots = dataframe2018_multi_lots.reset_index(drop=True)
dataframe2018_uni_lots = dataframe2018_uni_lots.reset_index(drop=True)

#%% Calcul des surfaces

#code unitaire bon à utilise en cas de détresse
#somme=0
#nombre_str = dataframe2018_multi_lots["Surface Carrez du 1er lot"][1]
#nombre_str=nombre_str.replace(",",".")
#somme + float(nombre_str)
#del somme

#surface_multi=[]
#list_colonne_multi=["Surface Carrez du 1er lot",
#              "Surface Carrez du 2eme lot",
#              "Surface Carrez du 3eme lot",
#              "Surface Carrez du 4eme lot",
#              "Surface Carrez du 5eme lot"]
#for i in range(len(dataframe2018_multi_lots)):
#    surface_totale=0
#    for colonne in list_colonne_multi:
#        nombre_str = dataframe2018_multi_lots[colonne][i]
#        if(isinstance(nombre_str,str)):
#            nombre_str=nombre_str.replace(",",".")
#        surface_totale += float(nombre_str)
#    surface_multi.append(surface_totale)
    
surface_multi=[]
list_colonne_multi=["Surface Carrez du 1er lot",
                    "Surface Carrez du 2eme lot",
                    "Surface Carrez du 3eme lot",
                    "Surface Carrez du 4eme lot",
                    "Surface Carrez du 5eme lot"]
for i in range(len(dataframe2018_multi_lots)):
    surface_totale=0
    for colonne in list_colonne_multi:
        nombre_str = dataframe2018_multi_lots[colonne][i]
        if(isinstance(nombre_str,str)):
            nombre_str=nombre_str.replace(",",".")
        if pd.isna(nombre_str):
            surface_totale += 0.0  # Ajouter une valeur nulle pour les valeurs manquantes
        else:
            surface_totale += float(nombre_str)
    surface_multi.append(surface_totale)


#Pas nécessaire de convertir pour surface reelle bati
#surface_uni=[]
#list_colonne_uni=["Surface reelle bati",
#                  "Surface terrain"]
#for i in range(len(dataframe2018_uni_lots)):
#    surface_totale=0
#    for colonne in list_colonne_uni:
#        nombre_str = dataframe2018_uni_lots[colonne][i]
#        surface_totale += float(nombre_str)
#    surface_uni.append(surface_totale)

surface_uni=[]
list_colonne_uni=["Surface reelle bati",
                  "Surface terrain"]
for i in range(len(dataframe2018_uni_lots)):
    surface_totale=0
    for colonne in list_colonne_uni:
        nombre_str = dataframe2018_uni_lots[colonne][i]
        if pd.isna(nombre_str):
            surface_totale += 0.0  # Ajouter une valeur nulle pour les valeurs manquantes
        else:
            surface_totale += float(nombre_str)
    surface_uni.append(surface_totale) 
   
#Rajout des colonnes aux dataframe
dataframe2018_multi_lots["Surface"]=surface_multi
dataframe2018_uni_lots["Surface"]=surface_uni
del nombre_str
del surface_multi
del surface_uni
del colonne
del i
del list_index_to_drop
#%% relier les 2 dataframes pour retrouver l'original
frames = [dataframe2018_multi_lots,dataframe2018_uni_lots]
dataframe2018=pd.concat(frames)
dataframe2018 = dataframe2018.reset_index(drop=True)
#%% Calcul du metre carre 

# valeur foncière est un str on fait la conversion
#dataframe2018["Valeur fonciere"]


for i in range(len(dataframe2018)):
    valeur=(dataframe2018.loc[i, "Valeur fonciere"])
    if(isinstance(valeur,str)):
        valeur=valeur.replace(",",".")
        dataframe2018.at[i,'Valeur fonciere']=valeur

dataframe2018["Valeur fonciere"]=dataframe2018["Valeur fonciere"].astype(float)

#Calcul du prix au metre carre
dataframe2018["Prix metre carre"]= dataframe2018["Valeur fonciere"] / dataframe2018["Surface"]


#%%        
