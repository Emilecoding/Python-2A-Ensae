
"""
Evidemment, une cuillère à café de farine ne pèse pas la même chose qu'une cuillère à café de sucre.
Mais nous choisissons ici de négliger ces différences car l'apport calorique d'un sachet, cuillère à café ou à soupe, n'est de toute façon 
pas conséquent. 

La plupart des autres aliments ont une quantité donné pour 100mL ou alors pour une unité de l'ingrédient (par exemple pour un avocat) 
directement dans la base, ce qui correspond souvent aux quantités des recettes. 
"""



liquides_en_ml = {
    "CUILLERE A CAFE" : 0.5,
    "CUILLERES A CAFE" : 0.5,
    "BONNE CUILLERE A CAFE" : 0.5,
    "C A C" : 0.5,
    "CUILLERE A SOUPE" : 14,
    "CUILERES A SOUPE" : 14,
    "BONNE CUILLERE A SOUPE" : 14, 
    "C A S" : 14,
    "L" : 1000,
    "DL" : 100,
    "CL" : 10,
    "ML" : 1,
    "PETITE CUILLERE" : 0.5, 
    "CUILLERE RASE" : 0.5,
    "TASSE" : 250,
    "BOL" : 250, 
    "VERRE" : 250,
    "LOUCHE" : 100,
    "LOUCHES" : 100,

}


solides_en_g = {
    "CUILLERE A CAFE" : 10,
    "CUILLERES A CAFE" : 10,
    "CUILERES A SOUPE" : 20,
    "CUILLERE A SOUPE" : 20,
    "ONCE" : 28.35,
    "SACHET" : 11,
    "PAQUET" : 11,
    "PINCEE" : 1,
    "GOUSSE" : 5,
    "NOISETTE" : 4,
    "SEL" : 1, 
    "POIVRE" : 1, 
    "LOUCHE" : 100,
    "LOUCHES" : 100,

}