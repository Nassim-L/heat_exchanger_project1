# heat_exchanger_project1
## Description
Ce logiciel est un outil de calcul performant conçu pour simplifier et accélérer les calculs liés à l'encrassement d'un réchauffeur-évaporateur KETTLE, c'est-à-dire en tenant compte de l'évaporation du fluide circulant dans la calandre.

## Fonctions
Le logiciel propose les fonctionnalités suivantes :

* Un calculateur simple qui permet le calcul direct de la résistance d'encrassement pour le cas considéré dans la présente étude.
* Un calculateur avancé qui permet de calculer la résistance d'encrassement pour plusieurs jours, avec une vitesse de calcul accrue. Cette fonction propose deux modes de fonctionnement distincts :
  
  * Un mode d'édition libre qui permet à l'utilisateur de spécifier les propriétés physiques et chimiques des deux fluides impliqués dans l'étude.
    
  * Un mode spécifiquement conçu pour certains fluides pour lesquels une étude a été menée et des corrélations spécifiques ont été développées. Dans ce mode, le logiciel utilise les corrélations disponibles pour obtenir les propriétés physiques et chimiques des fluides à partir des seules données de température et de débit. De plus, il applique la correction de la viscosité pour des résultats plus précis.
    
* Une fonction graphique qui permet de visualiser graphiquement les résultats de l'évolution de la résistance d'encrassement en fonction de temps. Cette fonction offre un contrôle total sur l'apparence du graphique, permettant de personnaliser divers aspects tels que le type d'échelle, la couleur du graphique, la taille des points, la résolution et le format de sortie.
  
## Technologies
Le logiciel a été développé en Python et utilise les technologies suivantes :

* PyQt6 pour l'interface utilisateur
* Pandas pour la manipulation des données
* Matplotlib pour les graphiques

## Vidéo d'installation et d'utilisation

https://youtu.be/LqUtyZQTeF0

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/LqUtyZQTeF0/0.jpg)](https://www.youtube.com/watch?v=LqUtyZQTeF0)



## Installation
Pour installer le logiciel, effectuez les opérations suivantes :

1- Téléchargez le code source du logiciel depuis GitHub.

2- Décompressez le fichier ZIP dans un répertoire de votre choix.

3- Ouvrez un terminal et naviguez jusqu'au répertoire contenant le code source du logiciel.

4- Créez un environnement virtuel en exécutant la commande suivante :
```
python -m venv venv
```

5- Activez l'environnement virtuel en exécutant la commande suivante :
```
venv\Scripts\activate.bat
```

6- Installez les dépendances en exécutant la commande suivante :
```
pip install -r requirements.txt
```

7- Lancez le logiciel en exécutant la commande suivante :
```
python heat_exchanger_beta.py
```

## Exécutable (Windows 64 bit)

https://drive.google.com/file/d/1MEx7GAh7sk2UjwfnhguyTRRGEPZDBQtM/view?usp=sharing

## Utilisation
Le logiciel est très simple à utiliser. Pour effectuer un calcul, procédez comme suit :

1- Ouvrez le logiciel.

2- Dans la fenêtre d'accueil, saisissez les valeurs des paramètres requis.

3- Cliquez sur le bouton "Calculer".

4- Les résultats du calcul seront affichés dans la fenêtre de sortie.
