import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

# Fonctions de distance et de matching 

def 


rapidfuzz.distance.Levenshtein.distance('sucre blanc','sucre roux', weights =(1,1,1))

generalisation of Levenshtein distance : string distance 

products_data["distance"] = products_data.apply(
        lambda x: distance(x.clean_name_prod, clean_product_name), axis=1
    )

produit cartésien codé en python ? 










from itertools import product

def calculer_meilleur_match(recette, produits_ciqual):
    # Produit cartésien entre la recette et les produits Ciqual
    produits_combines = list(product(recette, produits_ciqual))

    # Fonction de comparaison pour trouver le meilleur match
    def comparer_produits(produit):
        recette, produit_ciqual = produit
        # Ajoutez ici votre logique de comparaison entre la recette et le produit Ciqual
        # Par exemple, vous pourriez utiliser une mesure de similarité ou une autre métrique
        # Retournez la valeur de la métrique de similarité ou autre
        return len(set(recette) & set(produit_ciqual))

    # Trouver le meilleur match pour chaque produit de la recette
    meilleurs_matches = []
    for produit_recette in recette:
        # Triez les produits combinés en fonction de la comparaison
        produits_combines.sort(key=comparer_produits, reverse=True)
        # Le meilleur match est le premier élément trié
        meilleur_match = produits_combines[0][1]
        meilleurs_matches.append(meilleur_match)

    return meilleurs_matches

# Exemple d'utilisation
recette_exemple = ['tomate', 'poivre', 'oignon']
produits_ciqual_exemple = ['tomate', 'poivre', 'oignon', 'carotte', 'pomme']

meilleurs_matches = calculer_meilleur_match(recette_exemple, produits_ciqual_exemple)
print(meilleurs_matches)