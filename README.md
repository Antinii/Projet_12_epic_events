
# EPIC EVENTS


## Description du projet

Epic Events, une entreprise de conseil et de gestion dans l'événementiel, qui répond aux besoins des start-up voulant organiser des « fêtes épiques » a décidé d'élaborer un système CRM (Customer
Relationship Management) qui aiderait à collecter et à traiter les données des clients et de leurs événements.

## Mise en place et exécution en local de l'application

1. Téléchargez le projet depuis Github en clonant le projet en utilisant la commande suivante:  
```
git clone https://github.com/Antinii/Projet_12_epic_events.git
```
2. Déplacez vous dans le répertoire du projet avec la commande:
```
cd Projet_12_epic_events
```
3. Créez un environnement virtuel Python en exécutant la commande suivante:
```
python -m venv env 
```
Puis, activez votre environnement virtuel avec la commande suivante:
```
source env/bin/activate pour Mac / Linux
env/Scripts/activate pour Windows
```
4. Installez les dépendances à l'aide de la commande:
```
pip install -r requirements.txt
```
5. Vous pouvez maintenant exécuter l'application à l'aide de la commande suivante :
```		
python main.py
```
6. Dans la base de donnée existante, 3 comptes ont été créés. Les noms d'utilisateurs sont les suivants :
```		
Antini (commercial)
```
```		
Julie (management)
```
```
Maxime (support)
```
Le mot de passe est le même pour tous les comptes :
```		
S3cret!
```

Afin de générer un nouveau rapport html flake8:
```		
flake8 --format=html --htmldir=rapport
```
Afin de lancer les tests à l'aide de pytest:
```
pytest tests
```
Afin de vérifier le coverage des tests:
```
pytest --cov
```
