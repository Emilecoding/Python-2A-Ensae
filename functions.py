import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re # for regular expressions 
from re import sub
from unidecode import unidecode
import spacy
from scipy.spatial.distance import cosine

## Fonctions d'affichage 

def transport_pie(dataframe, column, titre):
    """ 
    Fonction qui prend en entrée un dataframe, une colonne spécifiée et le titre correspondant 
    et qui renvoie la répartition correspondante 
    """
    mapping_labels = {1: 'Voiture/Véhicule motorisé ', 2: 'Transport public', 3: 'A pied', 4: 'Vélo/Trottinette'}
    dataframe[column] = dataframe[column].map(mapping_labels)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(4, 4))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99', '#ff6666'])
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None

def pie_oui_non_eps(dataframe, column, titre):
    mapping_eps = {1: 'Oui', 2: 'Non, dispensé', 3: 'Non, pas de cours prévu', 4: 'Ne sait pas', 5: 'Refus'}
    dataframe[column] = dataframe[column].map(mapping_eps)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(4, 4))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None

def pie_oui_non(dataframe, column, titre):
    mapping_labels = {1: 'Oui', 2: 'Non'}
    dataframe[column] = dataframe[column].map(mapping_labels)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(4, 4))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None


## Fonctions de nettoyage des données 

nltk.download('stopwords')
nltk.download('punkt')

def cleaning(s):
    from unidecode import unidecode 
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


#!python -m spacy download fr_core_news_sm     # Téléchargement du modèle de traitement du français

nlp = spacy.load('fr_core_news_sm')    #Modèle de traitement prédéfini, avec distance


def find_match(aliment_entre, dataframe, vec, seuil=0.8):
    # Vectoriser le nouvel aliment
    vecteur_aliment_entre = nlp(aliment_entre).vector

    # Vérifier si vec est vide
    if len(vec) == 0:
        return "Aucun vecteur n'est disponible dans vectors"
    
    # Calculer la similarité cosinus avec tous les vecteurs d'aliments existants
    similarites = np.array([1 - cosine(vecteur_aliment_entre, vecteur) for vecteur in vec])
    
    # Trouver la correspondance la plus proche
    index_correspondance = similarites.argmax()
    score_correspondance = similarites[index_correspondance]
    
    # Si le score est supérieur au seuil, retourner la correspondance
    if score_correspondance >= seuil:
        return dataframe['Nom clean'].iloc[index_correspondance]
    else:
        return "Aucune correspondance trouvée"




def calcul_calories(recette,vec):                                     #Renvoie la valeur en kcal de la recette, cette dernière étant sous la forme : {'recette' : 'Titre recette' , 'Liste ingrédients' : [(ingrédient1, quantité1 en g);(ingrédient2, quantité2 en g) ...] , 'url':'url}#
    valeur = 0
    for ing in recette['Liste des ingrédients']:
        nom_ingredient = ing[0]
        nom_ingredient = nom_ingredient.upper()
        quantite = ing[1]  # La quantité doit être en g, la bdd ciqual rapporte les apports pour 100g

        # Utilisez le nom de l'ingrédient pour trouver la correspondance dans la base de données
        nom_ciqual = find_match(nom_ingredient, data_ciqual,vec)

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

  
## Conversion des strings 
    
from fractions import Fraction

def string_to_float(value):
    try:
        # Conversion directe
        result = float(value)
    except ValueError:
        try:
            # Conversion si fraction 
            result = float(Fraction(value))
        except ValueError:
            # Si les deux essais echouent, on a une erreur 
            raise ValueError(f"Impossible de convertir '{value}' en float")

    return result



import re 
from unidecode import unidecode
from conversions_unites import liquides_en_ml, solides_en_g

def conversion_recette(recette):
    liste_ingredients = recette['Liste des ingrédients']           #Car recette est un dictionnaire de la forme {'recette' : """Titre""" , 'Liste des ingrédients' : ...}#
    """
    Cette fonction prend la liste des ingredients retournée par le scraper de marmiton pour une recette donnée, et renvoie les ingrédients ainsi que leur conversion 

    Args : 
        liste_ingredients (list of str) : liste d'ingredients issus de la page marmiton de la recette 

    Returns : 
        Dict : avec comme clé l'ingrédient et comme valeur (quantité,unité de mesure) ou (quantité)
    
    """
    res = {} # dictionnaire resultat  
   
    # Pour les elements type : quantité DE ingrédient (ex : 1 pincée DE sel)
    pattern_1 = re.compile(r'(\d+)\s*(bonne cuillère à café|cuillère à café|cuillère à soupe|ml|l|kg|g|cl|cuillère|pincée|sachet)\s*de\s*([\w\s]+)')
   
    # Pour les elements type : quantité D' ingrédient (ex : 10 cl D'huile) 
    pattern_2 = re.compile(r'(\d+)\s*(bonne cuillère à café|cuillère à café|cuillère à soupe|ml|l|kg|g|cl|cuillère|pincée|sachet)\s*d\'\s*([\w\s]+)')
    
    # Pour les elements type : quantité ingrédient (ex : 4 oeufs)
    pattern_3 = re.compile(r'(\d+)\s*([\w\s]+)')  
    fail =[]

    for elt in liste_ingredients : 

        qtte,nom = elt.split('\n')
        ingredient = qtte+" "+nom 

        if pattern_1.match(ingredient):
            match = pattern_1.match(ingredient)
            quantity = match.group(1)
            unit = match.group(2)
            ingredient_name = match.group(3)
            res[cleaning(ingredient_name)] = (string_to_float(quantity),unidecode(unit.upper()))
        
        elif pattern_2.match(ingredient):
            match = pattern_2.match(ingredient)
            quantity = match.group(1)
            unit = match.group(2)
            ingredient_name = match.group(3)
            res[cleaning(ingredient_name)] = (string_to_float(quantity),unidecode(unit.upper()))
        
        elif pattern_3.match(ingredient):
            match = pattern_3.match(ingredient)
            quantity = match.group(1)
            ingredient_name = match.group(2)
            res[cleaning(ingredient_name)] = (string_to_float(quantity),"UNITE") # Pour les elements comme "1 oeuf"
        
        else: # si l'ingredient ne correspond à aucun des patterns précédents 
            fail.append(elt)
    nv_res = {}
    for ingr,(qtte,unite) in res.items():
        if unite == "UNITE":
            nv_res[ingr] = qtte
        else :
            if unite in liquides_en_ml:
                nv_res[ingr] = liquides_en_ml[unite]*qtte
            elif unite in solides_en_g:
                nv_res[ingr] = solides_en_g[unite]*qtte
            else: #cas où l'ingrédient est déjà en g ou dans la bonne unité
                nv_res[ingr] = qtte 
    return (nv_res,fail)


from pattern.text.fr import singularize

    def singulier(mot):
        return singularize(mot)



    def calcul_calories(recette,df):
    """

    Args : recette, dataframe data_ciqual

    Returns : 
    
    
    """
    calo = {}
    conv,fail = conversion_recette(recette) # renvoie un dictionnaire avec ingredient : qtte 
    nlp = spacy.load('fr_core_news_sm')
    if len(fail) !=0:
        # On affiche les elements de la recette qui n'ont pas pu être convertis 
        print("Les ingrédients suivants n'ont pas pu être convertis sont :\n ")
        print(*fail,sep=',')
    for (ingr,qtte) in conv.items(): 
        ingr = singulier(ingr)
        match = find_match(ingr, df,vectors, 0.7) # on set le seuil à 0.7 et on trouve l'ingredient correpondant
        calo_ligne = df[df["Nom clean"]==match]
        if not calo_ligne.empty:
            calo [ingr] = calo_ligne['Energie kcal'].values[0]*qtte/100 # les calories sont données pour 100g de produit 
        else:   # si pas d'info sur l'ingredient 
            calo[ingr] = 0
    return calo,sum(calo.values())






