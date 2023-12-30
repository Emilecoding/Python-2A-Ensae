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
import re 
from unidecode import unidecode
from conversions_unites import liquides_en_ml, solides_en_g
import inflect
from fractions import Fraction

##############################################################################################################################################

## Fonctions d'affichage ##


def transport_pie(dataframe, column, titre):
    """ 
    Fonction qui prend en entrée un dataframe, une colonne relative aux moyens de transports et le titre correspondant.
    Elle renvoie en sortie le diagramme correspondant à la répartition.

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
    """
    Fonction qui prend en entrée un dataframe, une colonne dont les reponses possibles sont oui, non, quelques aures modalités, et un titre. 
    Elle renvoie la répartition correspondante en sortie. 
    
    """
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
    """
    Fonction qui prend en entrée un dataframe, une colonne dont les reponses possibles sont oui, non, et un titre. 
    Elle renvoie la répartition correspondante en sortie. 
    
    """
    mapping_labels = {1: 'Oui', 2: 'Non'}
    dataframe[column] = dataframe[column].map(mapping_labels)
    count_by_format = dataframe[column].value_counts()
    plt.figure(figsize=(4, 4))
    plt.pie(count_by_format, labels=count_by_format.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'{titre}')
    plt.legend(title = "Légende", loc='upper right', bbox_to_anchor=(1.2, 0.2)) 
    plt.show()
    return None

##############################################################################################################################################

## Fonctions de nettoyage des données ##

nltk.download('stopwords')
nltk.download('punkt')

def cleaning(s):
    """
    Cette fonction a pour but de nettoyer une chaîne de caractère d'aliment, en prenant en compte des stopwords et des expressions 
    régulières notamment. 
    
    Args : 
        s (str): chaîne de caractère à convertir (elle peut être en majuscules, minuscules, avec ou sans accents...)
    
    Returns :
        la chaîne de caractère "simplifiée" au maximum 

    """
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
    return ' '.join(mots_filtres)

##############################################################################################################################################

## Fonction de distance/matching  et conversions ## 

nlp = spacy.load('fr_core_news_sm')    #Modèle de traitement prédéfini, avec distance

def find_match(aliment_entre, dataframe, vec, seuil=0.8):
    """
    Cette fonction prend un aliment de la recette considérée en entrée (aliment_entre) ainsi qu'un dataframe 
    (contentant les ingrédients dont on connaît les caractéristiques ), un vecteur (vec) et un seuil. Elle cherche dans la vectorisation des aliments 
    de la base, l'aliment le plus proche de l'aliment de la recette en entrée. Si elle trouve une correspondance avec une distance supérieure au 
    seuil fixé (souvent 0.8 en pratique), elle apparie cet ingrédient à notre ingrédient d'entrée. Sinon, elle renvoie qu'il n'y a pas de 
    correspondance dans notre base. 

    Args : 
        aliment_entre (str) : aliment d'une recette, duquel on veut connaître les caractéristiques nutritionnelles grâce à la base de données 
        dataframe (dataframe): contient les informations nutritionnelles et les aliments de la grande distribution
        vec (vector) : vectorisation des aliments de la base de données grace à spacy et modèle de nlp 
        seuil (float) : seuil de correspondance des aliments 

    """
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
    

def string_to_float(value):
    """
    Transforme la valeur value en flottant, utile pour les ingrédients des recettes, qui sont des str et doivent parfois être convertis en fraction 

    """
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



def singulier(mot):
    """
    Met le mot au singulier 
    """
    p = inflect.engine()
    return p.singular_noun(mot)



##############################################################################################################################################

## Fonctions de conversion d'une recette et calcul des calories de celle-ci ##

def conversion_recette(recette):
    liste_ingredients = recette['Liste des ingrédients']           #Car recette est un dictionnaire de la forme {'recette' : """Titre""" , 'Liste des ingrédients' : ...}#
    """
    Cette fonction prend la liste des ingredients retournée par le scraper de marmiton pour une recette donnée, 
    et renvoie les ingrédients ainsi que leur conversion dans l'unité interprétable par notre base de données (qui prend à la fois des ingrédients à 
    l'unité : 1 oeuf, mais aussi des apports pour 100g ou 100ml)

    Args : 
        recette (Dict) : dictionnaire avec le titre de la recette, la liste des ingrédients, ainsi que le lien de la recette 

    Returns : 
        nv_res (Dict): avec comme clé l'ingrédient et comme valeur (quantité,unité de mesure) ou (quantité)
        fail (list) : liste contenant les ingrédients qui n'ont pas pu être matchés et interprétés par notre fonction
    
    """
    res = {} # dictionnaire resultat  
   
    # Pour les elements type : quantité DE ingrédient (ex : 1 pincée DE sel)
    pattern_1 = re.compile(r'(\d+)\s*(louches |cuillères à soupe|bonne cuillère à café|cuillère à café|cuillère à soupe|ml|l|kg|g|cl|cuillère|pincée|sachet)\s*de\s*([\w\s]+)')
   
    # Pour les elements type : quantité D' ingrédient (ex : 10 cl D'huile) 
    pattern_2 = re.compile(r'(\d+)\s*(louches|cuillères à soupe|bonne cuillère à café|cuillère à café|cuillère à soupe|ml|l|kg|g|cl|cuillère|pincée|sachet)\s*d\'\s*([\w\s]+)')
    
    # Pour les elements type : quantité ingrédient (ex : 4 oeufs)
    pattern_3 = re.compile(r'(\d+)\s*([\w\s]+)')  

    # Pour les elements type : quantite en fraction DE ingredient (ex : 0.5 l DE lait)
    pattern_4 = re.compile(r'^([\d.]+)\s*(ml|l|kg|g|cl|cuillère|pincée|sachet)\s*de\s*([\w\s]+)')

    # Pour les elements type : quantite en fraction D' ingredient (ex : 0.5 l D' eau)
    pattern_5 = re.compile(r'^([\d.]+)\s*(ml|l|kg|g|cl|cuillère|pincée|sachet)\s*d\'\s*([\w\s]+)')
    
    fail =[]

    for elt in liste_ingredients : 

        if '\n' in elt:
            qtte,nom = elt.split('\n')
            ingredient = qtte+" "+nom 

            # On essaie de trouver une correspondance avec chaque pattern précédemment défini 
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

            elif pattern_4.match(ingredient):
                match = pattern_4.match(ingredient)
                quantity = match.group(1)
                unit = match.group(2)
                ingredient_name = match.group(3)
                res[cleaning(ingredient_name)] = (string_to_float(quantity),unidecode(unit.upper()))

            elif pattern_5.match(ingredient):
                match = pattern_5.match(ingredient)
                quantity = match.group(1)
                unit = match.group(2)
                ingredient_name = match.group(3)
                res[cleaning(ingredient_name)] = (string_to_float(quantity),unidecode(unit.upper()))
        
            else: # si l'ingredient ne correspond à aucun des patterns précédents 
                fail.append(elt)

        else:   # pour les ingredients de type "sel", et on considère que si la quantité n'est pas renseignée c'est qu'il en faut très peu 
            res[cleaning(elt)] = (1,unidecode(elt.upper()))
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



def calcul_calories(recette,df,vec):
    """
    Cette fonction renvoie la valeur en kcal de la recette, cette dernière étant sous la forme : 
    {'recette' : 'Titre recette' ,
    'Liste ingrédients' : [(ingrédient1, quantité1 en g);(ingrédient2, quantité2 en g) ...] ,
    'url':'url}

    Args : 
        recette (Dict) : recette propre contenant les ingredients et leur quantité dans la bonne unité 
        df (dataframe) : la base de données des ingrédients ciqual 
        vec (vector) : la vectorisation des ingrédients 
    """
    calo = {}
    conv,fail = conversion_recette(recette) # renvoie un dictionnaire avec ingredient : qtte 
    nlp = spacy.load('fr_core_news_sm')
    if len(fail) !=0:
        # On affiche les elements de la recette qui n'ont pas pu être convertis 
        print("Les ingrédients suivants n'ont pas pu être convertis sont :\n ")
        print(*fail,sep=',')
    for (ingr,qtte) in conv.items(): 
        #ingr = singulier(ingr)
        match = find_match(ingr, df,vec, 0.7) # on set le seuil à 0.7 et on trouve l'ingredient correpondant
        if match == "Aucune correspondance trouvée":
            continue
        else:
            calo_ligne = df[df["Nom clean"]==match]
            if not calo_ligne.empty:
                calo [ingr] = calo_ligne['Energie kcal'].values[0]*qtte/100 # les calories sont données pour 100g de produit 
            else:   # si pas d'info sur l'ingredient 
                calo[ingr] = 0
    return calo,sum(calo.values())






