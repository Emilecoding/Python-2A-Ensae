import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re # for regular expressions 
from re import sub

## Fonctions d'affichage 

def transport_pie(dataframe, column, titre):
    """ 
    Fonction qui prend en entrée un dataframe, une colonne spécifiée et le titre correspondant 
    et qui renvoie la répartition correspondante 
    """
    mapping_labels = {1: 'Voiture/Véhicule motorisé ', 2: 'Transport public', 3: 'A pied', 4: 'Vélo/Trottinette'}
    dataframe[column] = dataframe[column].map(mapping_labels)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99', '#ff6666'])
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None

def pie_oui_non_eps(dataframe, column, titre):
    mapping_eps = {1: 'Oui', 2: 'Non, dispensé', 3: 'Non, pas de cours prévu', 4: 'Ne sait pas', 5: 'Refus'}
    dataframe[column] = dataframe[column].map(mapping_eps)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None

def pie_oui_non(dataframe, column, titre):
    mapping_labels = {1: 'Oui', 2: 'Non'}
    dataframe[column] = dataframe[column].map(mapping_labels)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None


## Fonctions de nettoyage des données 

nltk.download('stopwords')
nltk.download('punkt')

def cleaning(s):
    stop_words_spe = ['CRU','CRUE','ALIMENT','TOUT','TYPE','PREEMBALLE','PREEMBALLEE','PREEMBALLEES','MOYEN','CUIT',
                      'CUITE','PETIT DEJEUNER','ROTI','ROTIE','FOUR','AU FOUR','KG','CL','G','L','MG','MARTINIQUE',
                      'VITAMINES','MINERAUX'
                     ]
    stop_words_default = [s.upper() for s in stopwords.words('french')]
    stop_words = set(stop_words_default + stop_words_spe)
    s = unidecode(s)
    s = s.upper()
    s = sub("[^A-Z ]", " ", s)
    mots = word_tokenize(s)
    mots_filtres = [mot for mot in mots if mot not in stop_words]
    #from nltk.stem.snowball import FrenchStemmer
    #s = " ".join(FrenchStemmer().stem(s) for s in s.split())
    return ' '.join(mots_filtres)

## Fonctions de distance et de matching 


from itertools import product

def calcul_match(ingr_recette, ingr_ciqual):

    """ 
    returns the ingrédients in the Ciqual database that best match the ingredients 
    of the recipe we try to reproduce 
    
    """
    # Produit cartésien entre la recette et les produits Ciqual
    #produits_combines = list(product(ingr_recette, produits_ciqual))



import spacy

!python -m spacy download fr_core_news_sm     # Téléchargement du modèle de traitement du français

from scipy.spatial.distance import cosine

nlp = spacy.load('fr_core_news_sm')    #Modèle de traitement prédéfini, avec distance
vectors = np.array([nlp(aliment).vector for aliment in data_ciqual['Nom clean'] if nlp(aliment).vector.any()])     #Vectorisation des aliments de la base Ciqual par le modèle fr_core_news_sm#

def find_match(aliment_entre, dataframe, seuil=0.8):
    # Vectoriser le nouvel aliment
    vecteur_aliment_entre = nlp(aliment_entre).vector
    
    # Vérifier si vectors est vide
    if len(vectors) == 0:
        return "Aucun vecteur n'est disponible dans vectors"
    
    # Calculer la similarité cosinus avec tous les vecteurs d'aliments existants
    similarites = np.array([1 - cosine(vecteur_aliment_entre, vecteur) for vecteur in vectors])
    
    # Trouver la correspondance la plus proche
    index_correspondance = similarites.argmax()
    score_correspondance = similarites[index_correspondance]
    
    # Si le score est supérieur au seuil, retourner la correspondance
    if score_correspondance >= seuil:
        return dataframe['Nom clean'].iloc[index_correspondance]
    else:
        return "Aucune correspondance trouvée"



def calcul_calories(recette):                                     #Renvoie la valeur en kcal de la recette, cette dernière étant sous la forme : {'recette' : 'Titre recette' , 'Liste ingrédients' : [(ingrédient1, quantité1 en g);(ingrédient2, quantité2 en g) ...] , 'url':'url}#
    valeur = 0
    for ing in recette['Liste des ingrédients']:
        nom_ingredient = ing[0]
        nom_ingredient = nom_ingredient.upper()
        quantite = ing[1]  # La quantité doit être en g, la bdd ciqual rapporte les apports pour 100g

        # Utilisez le nom de l'ingrédient pour trouver la correspondance dans la base de données
        nom_ciqual = find_match(nom_ingredient, data_ciqual)

        # Vérifiez si la correspondance a été trouvée
        if nom_ciqual == "Aucune correspondance trouvée":
            continue
        else:
            # Filtrer le DataFrame pour l'ingrédient spécifié
            ligne_aliment = data_ciqual[data_ciqual['Nom clean'] == nom_ciqual]

            # Vérifiez si la correspondance a été trouvée dans la base de données
            if ligne_aliment.empty:
                continue

            energie_kcal_str = ligne_aliment['Energie kcal'].iloc[0].replace(',', '.')
            
            try:
                energie_kcal = float(energie_kcal_str)
            except ValueError:
                print(f"Erreur de conversion pour l'ingrédient {nom_ingredient}, Energie kcal : {energie_kcal_str}")
                continue

            # Calculez les calories pour l'ingrédient
            calorie_ingredient = energie_kcal * quantite / 100
            valeur += calorie_ingredient

    return valeur





