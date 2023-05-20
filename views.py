from django.shortcuts import render
from django.template import loader
import os
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Create your views here.
from django.http import HttpResponse
from io import BytesIO
import base64
import datetime
# Create your views here.

'''








file_path_list = ["C:/Users/PC/mysite2/valeursfoncieres-2018.txt",
                  "C:/Users/PC/mysite2/valeursfoncieres-2019.txt",
                  "C:/Users/PC/mysite2/valeursfoncieres-2020.txt",
                  "C:/Users/PC/mysite2/valeursfoncieres-2021.txt",
                  "C:/Users/PC/mysite2/valeursfoncieres-2022.txt"]

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



dataframe2018 = pd.read_csv("C:/Users/PC/mysite2/valeursfoncieres-2018.txt", sep="|")
#dataframe2019 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2019.txt", sep="|")
#dataframe2020 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2020.txt", sep="|")
#dataframe2021 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2021.txt", sep="|")
#dataframe2022 = pd.read_csv("C:\Esilv\Annee 3\Semestre 6\Python\Valeursfoncieres-2021\Valeursfoncieres-2022.txt", sep="|")




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



# Nettoyage des colonnes inutiles
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
                    "Identifiant local",
                    "Code voie"
                    ],axis=1)

#
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

#  Rajout des valeurs principales


#Rajoute la région comme colonne des dataframes
#print(fr_departments)
dataframe2018["Region"] = np.nan
for i in range(len(dataframe2018["Code departement"])):
    valeurdepartement = dataframe2018["Code departement"][i]
    for j in fr_departments:
        if(str(valeurdepartement) in fr_departments[j]):
            dataframe2018["Region"][i] = j
            break
#print(dataframe2018["Region"])
del fr_departments
del i
del valeurdepartement
del j
# Séparez les lots uniques des lots multipes

dataframe2018_multi_lots = dataframe2018[dataframe2018['Nombre de lots'] >= 1]
dataframe2018_uni_lots = dataframe2018[dataframe2018['Nombre de lots'] == 0]
dataframe2018_multi_lots = dataframe2018_multi_lots.reset_index(drop=True)
dataframe2018_uni_lots = dataframe2018_uni_lots.reset_index(drop=True)

# Nettoyer les deux dataframes des valeurs non-renseignées
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

#Calcul des surfaces

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

# Inutilisée
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


#
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
# relier les 2 dataframes pour retrouver l'original
frames = [dataframe2018_multi_lots,dataframe2018_uni_lots]
dataframe2018=pd.concat(frames)
dataframe2018 = dataframe2018.reset_index(drop=True)
del frames
# Calcul du metre carre 

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

del dataframe2018_multi_lots
del dataframe2018_uni_lots
del list_colonne_multi
del list_colonne_uni
del surface_totale
del i
del valeur

dataframe2018.replace([np.inf, -np.inf], np.nan, inplace=True)
dataframe2018.dropna(subset=['Prix metre carre'], inplace=True)



# Conversions des données

dataframe2018['Date mutation'] = pd.to_datetime(dataframe2018['Date mutation'])



# Selection par dates

def filtre_dataframe_par_date(dataframe, date_debut, date_fin):
    mask = (dataframe["Date mutation"] >= date_debut) & (dataframe["Date mutation"] <= date_fin)
    dataframe_filtre = dataframe.loc[mask]
    return dataframe_filtre


# Selection de 2 parametres sous conditions

#Fonction Abandonnée
# Cette fonction sera très utile pour choisir les départements ou régions
#def filtre_dataframe(dataframe, colonne, value):
#    df_filtree = dataframe[dataframe[colonne] == value]
#    return df_filtree

#Cette fonction permet de sélectionner des lignes selon une liste de valeurs typiquement pour une comparaison entre départements
def multi_filtre_dataframe(dataframe, colonne, values):
    if isinstance(values, list):
        # Si la valeur est une liste, filtrer la DataFrame avec la méthode isin
        df_filtree = dataframe[dataframe[colonne].isin(values)]
    else:
        # Si la valeur est une valeur unique, filtrer la DataFrame avec l'opérateur ==
        df_filtree = dataframe[dataframe[colonne] == values]
    return df_filtree

# On veut déterminer le prix au metre carre moyen dans une region/departement

def prix_selon_param(dataframe, colonne, value, ascend):
    df_filtre = multi_filtre_dataframe(dataframe,colonne,value)
    if(ascend == True):
        df_filtre = df_filtre.sort_values(by=['Prix metre carre'],ascending=True)
    else:
        df_filtre = df_filtre.sort_values(by=['Prix metre carre'],ascending=False)
        
    #return df_filtre[['Prix metre carre','Commune','Code departement','Region','Type local','Nature culture', colonne]]
    return df_filtre

# tri d'une dataframe 

def tri_dataframe(dataframe, colonne, ascend=True):
    if(ascend == True):
        df_trie = dataframe.sort_values(by=colonne, ascending=True)
    else:
        df_trie = dataframe.sort_values(by=colonne, ascending=False)
    return df_trie

# Quel commune a le plus de vente ?

#Donne le nombre de mutation dans un département
#A retravailler
def popularite_par_zone(dataframe, colonne, IDzone):
    if isinstance(IDzone, list):
        mutations_par_zone = dataframe[colonne].isin(IDzone).sum()
    else:
        mutations_par_zone = (dataframe[colonne] == IDzone).sum()
    return mutations_par_zone


# Quelles Colonnes afficher ?

# Faire un menu avec des cases à sélectionner où l'utilisateur peut choisir quelles colonnes à enlever
def affichage_colonnes(dataframe, colonnes_a_virer):
    dataframe_retour = dataframe.drop(colonnes_a_virer,axis=1)
    return dataframe_retour

# Occurrences

def occurrences_data(dataframe,colonne,valeur):
    return dataframe[colonne].value_counts()[valeur]

# Execution (test)
#
#
#
#
#Pour laisser l'utilisateur s'amuser


# il faudra demander à l'utilisateur : 
    #quelle colonne il veut rechercher :
        #Région
        #Code département
        #Commune
    #Une liste de ce qu'il demande :
        #Ecrire donc la bonne type des :
            #Régions (fais une lecture des clées du dictionnaire qui s'affiche)
            #Departements (pas besoin ce sont que des chiffres)
            #Commune (pas de liste mais précise qu'elle doivent être en toutes majuscules)
df_demande = prix_selon_param(dataframe2018,"Region",["Bretagne"],True)
df_demande=tri_dataframe(df_demande,["Region","Code departement",'Prix metre carre'])

col_virer =['B/T/Q',            'Type de voie',            'Code voie',            'Voie',            'Code postal',            'Surface Carrez du 1er lot',            'Surface Carrez du 2eme lot',            'Surface Carrez du 3eme lot',            'Surface Carrez du 4eme lot',            'Surface Carrez du 5eme lot'] 
#df_demande2 = affichage_colonnes(df_demande, col_virer)

df_demande2 = prix_selon_param(dataframe2018,"Region",["Corse"],True)
df_demande3 = prix_selon_param(df_demande2,"Commune",["AJACCIO","BASTIA"],True)

# Application de prix_selon_param pour qqn qui recherche un appartement dans un département précis
df_demande2 = prix_selon_param(dataframe2018,"Type local",["Appartement","Maison"],True)
df_demande3= prix_selon_param(df_demande2,"Code departement",[75],True)
#La méthode est quasiment universelle donc, on la réutilsera selon les circonstances
#On pourrait 

compteur=popularite_par_zone(df_demande3,"Code departement",[75])

# Il faudra demander l'année, le mois et le jour (en chiffre)
x = datetime.datetime(2018, 3, 17)
y = datetime.datetime(2018, 5, 17)
df_par_date = filtre_dataframe_par_date(df_demande3, x, y)

del x
del y

df_demande['Prix metre carre'].mean()

# Prix moyen metre carré par région

def histo_dataframe(dataframe):
    prix_moyen_region = dataframe.groupby("Region")["Prix metre carre"].mean()
    plt.bar(prix_moyen_region.index, prix_moyen_region.values)
    plt.title("Prix moyen au mètre carré par région")
    plt.xlabel("Région")
    plt.ylabel("Prix moyen au mètre carré")
    plt.show()

#Execution 
#histo_dataframe(df_demande)

# Tranche de prix

#def tranches_de_prix_dataframe(dataframe,valeu_sup,valeur_inf):
        

# Nombre de ventes par région

def ventes_par_region(dataframe):
    ventes_par_region = dataframe['Region'].value_counts()
    fig, ax = plt.subplots()
    ventes_par_region.plot(kind='bar', ax=ax)
    ax.set_title('Nombre de ventes par région')
    ax.set_xlabel('Région')
    ax.set_ylabel('Nombre de ventes')
    plt.show()

#ventes_par_region(df_demande)

def ventes_par_Commune(dataframe):
    ventes_par_region = dataframe['Commune'].value_counts()
    fig, ax = plt.subplots()
    ventes_par_region.plot(kind='bar', ax=ax)
    ax.set_title('Nombre de ventes par Commune')
    ax.set_xlabel('Région')
    ax.set_ylabel('Nombre de ventes')
    plt.show()

ventes_par_Commune(df_demande2) #trier par communes

def ventes_par_region_camember(dataframe):
    ventes_par_region = dataframe['Region'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(ventes_par_region, labels=ventes_par_region.index, autopct='%1.1f%%')
    ax.set_title('Répartition des ventes par région')
    plt.show()
    
ventes_par_region_camember(df_demande)

def ventes_par_commune_camember(dataframe):
    ventes_par_region = dataframe['Commune'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(ventes_par_region, labels=ventes_par_region.index, autopct='%1.1f%%')
    ax.set_title('Répartition des ventes par Commune')
    plt.show()
    
ventes_par_commune_camember(df_demande3)

# Selon une période

#Réduire pour une région
def ventes_par_dates(dataframe):
    ventes_par_date = dataframe.groupby('Date mutation')['Valeur fonciere'].count()
    fig, ax = plt.subplots()
    ax.plot(ventes_par_date.index, ventes_par_date.values)
    ax.set_title('Nombre de ventes par date de mutation')
    ax.set_xlabel('Date de mutation')
    ax.set_ylabel('Nombre de ventes')
    plt.show()



# Types de ventes



def types_de_biens(dataframe):
    ventes_par_types = dataframe['Type local'].value_counts()
    fig, ax = plt.subplots()
    ventes_par_region.plot(kind='bar', ax=ax)
    ax.set_title('Nombre de ventes par types')
    ax.set_xlabel('Type local')
    ax.set_ylabel('Nombre de ventes')
    plt.show()
    

#types_de_biens(df_demande)
#

#def histo_vente(dataframe,colonne_recherche,valeur_cherchee):
    
    

# On veut déterminer le type de bien vendu

#A supprimer
def diagramme_prix_metre_carre_par_region(dataframe):
    prix_metre_carre_par_region = dataframe.groupby('Region')['Prix metre carre'].mean()
    plt.bar(prix_metre_carre_par_region.index, prix_metre_carre_par_region.values)
    plt.xticks(rotation=90)
    plt.xlabel('Region')
    plt.ylabel('Prix metre carre')
    plt.title('Prix metre carre par region')
    plt.show()

diagramme_prix_metre_carre_par_region()

#def diagramme_temporel_par_region(dataframe):
    
#df_demande.plot(kind='bar',
#        x='Type local',
#        color='green')

# Pense bête
def info_dataframe(dataframe):
    for col in dataframe.columns:
        print(col + ' : ' + str(dataframe[col].dtype))


#type(dataframe2018['Date mutation'][1])
#datetime_object.strftime(dataframe2018['Date mutation'][1])



#info_dataframe(dataframe2018)


nom_colonnes=[]
for col in dataframe2018.columns:
    nom_colonnes.append(col)
nom_colonnes
#nom_colonnes


#del col




#def index(request):

    
    #context = {'dep': dep}
    #return render(request, 'template1.html', context)
'''
from django.shortcuts import render
from localflavor.fr.forms import FRDepartmentsField
from django import forms
class MyForm(forms.Form):
    department = FRDepartmentsField()
class DepartementForm(forms.Form):
    departements = [
        ('01', 'Ain'),
        ('02', 'Aisne'),
        ('03', 'Allier'),
        # Ajoutez les autres départements ici
    ]
    departement = forms.ChoiceField(choices=departements, label='Département')

def ma_vue(request):
    form = DepartementForm()
    context = {'form': form}
    return render(request, 'mon_template.html', context)
