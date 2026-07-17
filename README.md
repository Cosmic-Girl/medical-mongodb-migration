# Migration d'un jeu de données médical vers MongoDB

Projet réalisé dans le cadre de la formation **Data Engineer – OpenClassrooms**.
Ce projet consiste à migrer un jeu de données médical au format CSV vers une base MongoDB à l'aide d'un pipeline ETL développé en Python et conteneurisé avec Docker.


## 1. Présentation du projet

Le pipeline extrait les données d'un fichier CSV, les transforme en documents JSON structurés, puis les charge dans une collection MongoDB.
La solution est développée en Python et exécutée dans un environnement Docker afin de garantir une exécution reproductible et un déploiement simplifié.

## 2. Objectifs

- Migrer les données d'un fichier CSV vers MongoDB.
- Structurer les données sous forme de documents imbriqués.
- Industrialiser le processus de migration avec Docker.
- Mettre en place une configuration externalisée grâce aux variables d'environnement.
- Produire un code lisible, maintenable et documenté.


## 3. Architecture du pipeline


```mermaid
flowchart TD
    A[Jeu de données CSV<br/>55 500 hospitalisations]
    B[Service Python<br/>Script de migration]
    C[Extraction<br/>Lecture avec csv.DictReader]
    D[Transformation<br/>Nettoyage, typage et sous-documents]
    E[Chargement<br/>Insertion avec PyMongo]
    F[(Service MongoDB<br/>Collection hospitalizations)]
    G[MongoDB Compass<br/>Contrôle des données]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G

    subgraph DC[Docker Compose]
        B
        F
    end
```

Le script lit le fichier CSV, transforme chaque ligne en document MongoDB structuré, puis insère les documents dans la collection `hospitalizations`.


## 4. Structure du projet

```
.
├── data/
│   └── healthcare_dataset.csv
├── scripts/
│   └── migrate.py
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```


## 5. Technologies utilisées

### Langages
- Python 3.x : développement du script de migration et transformation des données.

### Base de données
- MongoDB : stockage des données sous forme de documents JSON.
- MongoDB Compass : visualisation et contrôle des données insérées.

### Conteneurisation
- Docker : création d'un environnement reproductible.
- Docker Compose : orchestration des services Python et MongoDB.

### Bibliothèques Python
- `pymongo` : connexion et interaction avec MongoDB.
- csv (bibliothèque standard Python) : lecture du fichier CSV.
- logging (bibliothèque standard Python) : journalisation.

### Outils de développement
- Git / GitHub : gestion du versionnage du code.
- VS Code : environnement de développement.


## 6. Installation

### Prérequis
Avant de lancer le projet, il est nécessaire d'avoir installé :
- Docker
- Docker Compose
- Git

### Cloner le repository
```bash
git clone https://github.com/Cosmic-Girl/medical-mongodb-migration.git
cd <repository>
```

### Variables d'environnement
Créer un fichier .env à la racine du projet
```env
MONGO_URI=mongodb://mongodb:27017/
DATABASE_NAME=medical_db
COLLECTION_NAME=hospitalizations
```

## 7. Lancement du projet

Le projet peut être lancé entièrement avec Docker Compose.

### Construction des images & démarrage des services

```bash
docker compose up --build
```

### Accès à MongoDB Compass

Pour visualiser les données, connectez-vous avec :

```text
mongodb://localhost:27018/
```

## 8. Structure des données

Le fichier CSV source contient des informations médicales sous forme tabulaire.
Afin d'exploiter les capacités documentaires de MongoDB, les données sont transformées en documents JSON.

Exemple de document stocké :

```json
{
  "_id": ObjectId("..."),
  "patient": {
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "bloodType": "A+"
  },
  "hospitalization": {
    "admissionDate": "2024-01-15",
    "dischargeDate": "2024-01-20",
    "roomNumber": 302,
    "admissionType": "Emergency"
  },
  "diagnosis": {
    "medicalCondition": "Diabetes",
    "testResults": "Positive"
  },
  "treatment": {
    "medication": "Metformin"
  },
  "doctor": {
    "name": "Dr. Smith"
  },
  "hospital": {
    "name": "General Hospital"
  },
  "billing": {
    "insuranceProvider": "Medicare",
    "billingAmount": 4500.75
  }
}
```

## 9. Résultats obtenus

À l'exécution du pipeline :
- lecture des 55 500 lignes du fichier CSV ;
- transformation des lignes en documents MongoDB ;
- insertion de 55 500 documents ;
- journalisation des principales étapes.

La migration s'exécute intégralement dans un environnement Docker reproductible et les données sont immédiatement consultables via MongoDB Compass.
Les données sont ensuite consultables directement depuis MongoDB Compass.

### Aperçu dans MongoDB Compass

![MongoDB Compass](docs/images/Capture_MongoDB_Compass.png)


## 10. Choix techniques

### MongoDB

MongoDB a été choisi car son modèle documentaire est adapté aux données semi-structurées.
Contrairement à une base relationnelle nécessitant plusieurs tables et des jointures, MongoDB permet de stocker les informations liées à un patient dans un document unique.
Le modèle documentaire permet de conserver les informations fortement liées dans un même document, ce qui réduit le besoin de jointures et facilite certaines requêtes.

Avantages :
- flexibilité du schéma
- gestion native des documents JSON
- facilité d'évolution de la structure des données
- bonne adaptation aux volumes importants de données

### Transformation des données avant insertion

La transformation est réalisée avant l'insertion afin de :
- nettoyer les données issues du CSV ;
- convertir les types de données ;
- organiser les informations sous forme de documents imbriqués ;
- garantir une structure homogène dans MongoDB.

### Utilisation de Docker

Docker permet de reproduire facilement l'environnement du projet.

Avantages :
- absence de configuration manuelle de MongoDB ;
- déploiement simplifié ;
- isolation des dépendances ;
- meilleure portabilité du projet.

### Gestion des paramètres avec des variables d'environnement

Les informations de connexion MongoDB sont externalisées afin de :
- éviter de stocker des informations sensibles dans le code ;
- faciliter le changement d'environnement (développement, test, production) ;
- respecter les bonnes pratiques d'industrialisation.

### Logging

Le module `logging` de Python est utilisé afin de :

- suivre l'exécution du pipeline ;
- distinguer les niveaux de gravité (`INFO`, `WARNING`, `ERROR`) ;
- horodater les événements ;
- faciliter le débogage en cas d'échec.

## 11. Améliorations possibles

Plusieurs évolutions pourraient être envisagées :

### Qualité des données
- Ajouter davantage de contrôles de validation avant insertion.
- Mettre en place un système de logs plus complet.
- Identifier et gérer automatiquement les doublons.

### Industrialisation
- Ajouter des tests unitaires avec `pytest`.
- Mettre en place une intégration continue avec GitHub Actions.
- Ajouter une gestion des erreurs et des reprises après échec.

### Performance
- Mettre en place des insertions par lots (`bulk_insert`).
- Ajouter des index MongoDB sur les champs fréquemment utilisés.
- Optimiser le traitement pour des fichiers CSV volumineux.

### Architecture
- Séparer davantage les responsabilités :
  - extraction des données ;
  - transformation ;
  - chargement dans MongoDB (architecture ETL).
- Ajouter un orchestrateur comme Airflow pour automatiser les pipelines.

## Conclusion

Ce projet illustre la mise en œuvre d'un pipeline ETL automatisé permettant de migrer un jeu de données CSV vers une base MongoDB.

Il met en œuvre plusieurs bonnes pratiques de Data Engineering, notamment la conteneurisation avec Docker, l'utilisation de variables d'environnement, la transformation des données avant chargement et la journalisation des traitements.

Ce projet met également en évidence l'importance de la qualité du code, de la reproductibilité des environnements et de l'automatisation des traitements dans une démarche de Data Engineering.





## Compétences mises en œuvre

Au cours de ce projet, les compétences suivantes ont été mobilisées :

- Python
- MongoDB
- Docker
- Docker Compose
- Git et GitHub
- Transformation de données (ETL)
- Variables d'environnement
- Logging
- Documentation technique