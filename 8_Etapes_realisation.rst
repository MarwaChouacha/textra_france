7_Etapes_realisation
======================================
# Objectif projet : Extraction de texte à partir de factures et association avec le plan comptable (PCG)


Ce document a pour objectif de détailler les étapes du projet d'extraction de texte à partir des factures françaises et de l'association de ces données avec le plan comptable général (PCG) français. Le projet repose sur l'utilisation de techniques d'OCR (Reconnaissance Optique de Caractères) et de modèles d'apprentissage supervisé pour effectuer cette tâche de manière automatisée et efficace.


L'objectif principal est d'extraire des informations pertinentes à partir des factures françaises et de les associer automatiquement aux comptes comptables correspondants dans le cadre du PCG français.

### Étapes du projet

1. **Préparation des données**
    - Collecte des factures sous format image (PDF, JPEG, PNG, etc.).
    - Conversion des images en texte exploitable à l'aide d'un outil OCR (Tesseract, par exemple).
    - Vérification de la qualité de l'OCR pour minimiser les erreurs dans les données extraites.

2. **Extraction des données via OCR**
    - Le texte brut est extrait à partir des images des factures.
    - L'OCR identifie des éléments spécifiques tels que les montants, les dates, les numéros de facture, et les informations sur les clients.
    - Les erreurs d'extraction (comme les caractères mal reconnus) sont corrigées à cette étape pour garantir la précision des données.

3. **Prétraitement des données**
    - Nettoyage des données extraites pour éliminer les informations inutiles et garantir la structure des données (dates, montants, numéros de facture).
    - Normalisation des données, par exemple, en transformant les montants en une représentation uniforme.
    - Traitement des erreurs de format (dates mal formatées, montants avec des virgules, etc.).

4. **Identification des entités et extraction via NER**
    - Utilisation de modèles de reconnaissance d'entités nommées (NER) pour extraire des entités spécifiques comme les dates, les montants et les numéros de facture.
    - Les entités extraites sont ensuite organisées dans une structure de données (par exemple, un tableau ou une base de données).

5. **Association des données extraites au PCG français**
    - Utilisation du plan comptable général (PCG) français pour associer les données extraites aux comptes comptables appropriés.
    - Par exemple, les montants extraits sont associés aux comptes du type "606" pour les achats ou "4457" pour la TVA collectée.
    - Cette étape repose sur des règles métiers et des modèles d'apprentissage supervisé qui permettent d'identifier les comptes corrects en fonction des données extraites des factures.

6. **Vérification et validation des résultats**
    - Vérification de la correspondance entre les données extraites et les comptes comptables pour éviter toute erreur dans l'association.
    - Tests et validation du processus sur un échantillon de factures afin d'assurer la qualité de l'automatisation.

7. **Amélioration continue**
    - Ajustement du modèle d'apprentissage pour améliorer l'association des entités aux comptes comptables en fonction des erreurs identifiées.
    - Ajout de nouvelles règles métiers pour améliorer la précision de l'association et couvrir davantage de cas particuliers.

## Plan comptable français (PCG)
Le PCG français est la norme utilisée pour organiser les comptes d'une entreprise. Il est essentiel de bien comprendre la structure du PCG pour associer correctement les données extraites aux comptes appropriés.

Voici un extrait de la structure du PCG :

- **Classe 1** : Comptes de capitaux
- **Classe 2** : Comptes d'immobilisations
- **Classe 3** : Comptes de stocks
- **Classe 4** : Comptes de tiers (clients, fournisseurs, etc.)
- **Classe 5** : Comptes financiers
- **Classe 6** : Comptes de charges
- **Classe 7** : Comptes de produits

Chaque classe est subdivisée en sous-comptes qui permettent de classer les transactions de manière détaillée.

Pour plus de détails sur le PCG, vous pouvez consulter la documentation officielle disponible ici : [PCG Français - Documentation](https://textra-franceee.readthedocs.io/en/latest/index.html#).

## Conclusion
Ce projet d'extraction automatique de texte à partir des factures françaises et d'association avec le plan comptable français vise à automatiser et à simplifier la gestion comptable en réduisant l'intervention manuelle. Il repose sur des technologies avancées d'OCR et d'apprentissage supervisé pour garantir une efficacité maximale et une traçabilité des données améliorée.

.. code:: python
    import cv2
    import pytesseract
    import re
    import spacy
    import pandas as pd
    from PIL import Image
    import torch
    from transformers import Phi2Tokenizer, Phi2ForTokenClassification, Trainer, TrainingArguments

# 1. Préparation des données
# Description : Cette étape consiste à charger une image de facture, la convertir en texte avec OCR et vérifier la qualité du texte extrait.
# Charger une image de facture
    img = cv2.imread('facture_image.png')

# Appliquer l'OCR sur l'image
    text = pytesseract.image_to_string(img)

# Afficher le texte extrait
    print("Texte extrait de l'image :")
    print(text)

# 2. Extraction des données via OCR
# Description : Extraction des informations spécifiques à partir du texte extrait via l'OCR. Cela inclut la date, les montants et les numéros de facture.
# Exemple de texte extrait avec OCR
extracted_text = """
Facture n° 12345
Date : 15/05/2025
Montant : 150.00 EUR
"""

# Extraction de la date
.. code:: python
date_pattern = r"\d{2}/\d{2}/\d{4}"
dates = re.findall(date_pattern, extracted_text)
print("Dates extraites:", dates)
---
# Extraction des montants
.. code:: python
amount_pattern = r"\d+\.\d{2}"
amounts = re.findall(amount_pattern, extracted_text)
print("Montants extraits:", amounts)
---
# 3. Prétraitement des données
# Description : Nettoyage et structuration des données extraites pour s'assurer que toutes les informations sont prêtes à être utilisées dans les étapes suivantes.
# Données extraites après OCR
.. code:: python 
    data = {
        "Facture": [12345],
        "Date": ["15/05/2025"],
        "Montant": [150.00]
    }
---
# Création d'un DataFrame
.. code:: python
    df = pd.DataFrame(data)
---
# Nettoyage des données (par exemple, convertir la colonne "Date" en format datetime)
.. code:: python
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
---
# Affichage du DataFrame nettoyé
.. code:: python
    print("\nDonnées prétraitées :")
    print(df)
---
# 4. Identification des entités et extraction via NER
# Description : Extraction d'entités comme la date, les montants et les numéros de facture via un modèle de reconnaissance d'entités nommées (NER) de SpaCy.
.. code:: python
    # Charger le modèle de NER
    nlp = spacy.load("fr_core_news_sm")
---
# Texte extrait de la facture
.. code:: python
    text = "Facture n° 12345, Date : 15/05/2025, Montant : 150.00 EUR"
---
# Appliquer le modèle NER pour extraire les entités
.. code:: python
    doc = nlp(text)
---
# Extraire les entités
.. code:: python
    print("\nEntités extraites via NER :")
    for ent in doc.ents:
        print(ent.text, ent.label_)
---
# 5. Fine-tuning du modèle Phi-2 pour l'extraction des données spécifiques
# Description : Fine-tuning du modèle Phi-2 pour l'extraction des entités spécifiques comme les dates, montants et numéros de facture à partir des factures.

# Charger le tokenizer et le modèle Phi-2
.. code:: python
    tokenizer = Phi2Tokenizer.from_pretrained("phi-2")
    model = Phi2ForTokenClassification.from_pretrained("phi-2")
---
# Exemple d'annotation des données (facture, date, montant)
# Vous devez avoir des données annotées pour faire le fine-tuning
.. code:: python
    train_dataset = [
        {"text": "Facture n° 12345, Date : 15/05/2025, Montant : 150.00 EUR", "labels": [1, 0, 2]}  # labels sont des indices pour les entités
    ]

# Tokenisation des données
def tokenize_data(example):
    return tokenizer(example['text'], padding=True, truncation=True)

train_dataset = [tokenize_data(data) for data in train_dataset]

# Définir les arguments d'entraînement
training_args = TrainingArguments(
    output_dir='./results',          # sortie du modèle fine-tuné
    num_train_epochs=3,              # nombre d'époques
    per_device_train_batch_size=4,   # taille du batch
    logging_dir='./logs',            # répertoire pour les logs
)

# Création du Trainer
trainer = Trainer(
    model=model,                         # modèle à fine-tuner
    args=training_args,                  # arguments d'entraînement
    train_dataset=train_dataset          # jeu de données d'entraînement
)

# Lancer le fine-tuning
trainer.train()

# Sauvegarder le modèle fine-tuné
model.save_pretrained("./fine_tuned_phi2_model")

# 6. Association des données extraites au PCG français
# Description : Après l'extraction et le fine-tuning, les données extraites sont associées aux comptes comptables définis dans le PCG.
# Exemple de correspondance entre un type de facture et un compte comptable
def associer_compte(montant):
    if montant < 1000:
        return "606 - Achats"
    elif montant < 10000:
        return "4457 - TVA collectée"
    else:
        return "4456 - TVA à décaisser"

# Application de l'association des comptes
df['Compte comptable'] = df['Montant'].apply(associer_compte)

# Affichage des résultats
print("\nDonnées associées aux comptes comptables :")
print(df)

# 7. Vérification et validation des résultats
# Description : Cette étape permet de vérifier que les entités extraites et les comptes associés sont corrects et cohérents.
# Exemple de fonction pour valider les données
def verifier_association(df):
    for index, row in df.iterrows():
        if row['Compte comptable'] == "606 - Achats" and row['Montant'] > 1000:
        print(f"Erreur dans l'association de la facture {row['Facture']}")
        else:
        print(f"Facture {row['Facture']} validée.")

# Vérification des données extraites
verifier_association(df)

# 8. Amélioration continue
# Description : Améliorer l'association des données en fonction des erreurs identifiées et des nouvelles règles métier ajoutées.
# Exemple d'ajustement des règles métiers pour améliorer l'association
def ajuster_regles(df):
    df['Compte comptable'] = df['Montant'].apply(lambda x: "607 - Achats de services" if x > 5000 else "606 - Achats")
    return df

# Application des règles améliorées
df = ajuster_regles(df)

# Affichage des résultats
print("\nAprès ajustement des règles métiers :")
print(df)
---






