# Projet Python ENSAE 2A

Projet réalisé dans le cadre du cours de Lino Galiana *Python pour la data science* année 2023-2024. 

Les contributeurs de ce projet sont : 
- Claire Bresson
- Emile Cassant
- Lila Mekki 

## Description du projet 

Ce projet a pour but d'aider les consommateurs à ne pas gaspiller ni acheter du superflu tout en maîtrisant leurs besoins nutritionnels. 

Pour cela, à l'aide d'une liste d'ingrédients dont ils disposent chez eux,l'idée est de leur proposer une liste de recettes réalisables (ainsi que leur apport nutritionnel). Une recette peut ensuite être choisies par l'utilisateur selon ses besoins caloriques ou son temps de préparation par exemple. 

## Organisation du répertoire 




## Structure du projet 

### Étape 1 : Récupération et nettoyage des données

Au cours de ce projet, nous avons utilisé des données de la base Ciqual, mise à disposition par l'ANSES, ainsi que des recettes en scrapant le site Marmiton. 

La base de données Ciqual est une base qui regroupe un grand nombre de produits alimentaires vendus dans la grande distribution. Son avantage pour notre projet est que la base donne accès pour chaque aliment à son apport énergétique, en protéines, glucides etc.

Afin d'avoir accès à des recettes, nous avons choisi de scraper Marmiton. Pour cela, nous avons utilisé le module Selenium à l'aide d'un browser chromedriver. Notre scraper prend en entrée une liste d'ingrédients et retourne quelques recettes compatibles avec ces ingrédients. 

### Étape 2 : Analyse descriptive et correspondance des ingrédients

Étant donné que notre but était de proposer des recettes selon les besoins nutritionnels des individus, nous nous sommes également penchés sur les habitudes de consommation des individus (base de données également mise à disposition par l'ANSES).

Nous avons pu effectuer une analyse descriptive de cette base afin d'extraire des données telles que l'apport énergétique quotidien, ou bien les préférences alimentaires (légumes, viande...) pour en tenir compte dans la proposition des repas. 

Nous avons dans un second temps mis au point des fonctions permettant de passer des ingrédients des recettes aux ingrédients de notre base de données, car les appellations différaient grandement entre les deux. 

### Étape 3 : Modélisation et résultats finaux 

À partir d'une liste de quelques ingrédients dont l'utilisateur dispose chez lui, lui sont proposées quelques recettes utilisant ces ingrédients. Les recettes sont classées par apport énergétique décroissant.  



