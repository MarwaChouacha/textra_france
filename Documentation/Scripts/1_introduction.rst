# Introduction

## Contexte du projet
L'extraction automatique de texte à partir des factures joue un rôle clé dans la gestion comptable et administrative. Notre projet vise à automatiser l'extraction des données à partir de factures françaises, à l'aide de techniques OCR (Reconnaissance Optique de Caractères), et à associer ces informations aux comptes comptables correspondants.

## Objectifs du projet
Les objectifs principaux du projet sont les suivants :
- **Extraire les données pertinentes des factures** : Montants, dates, numéros de facture, informations sur les clients, etc.
- **Associer ces données à des comptes comptables appropriés** : Utiliser des règles métiers et des modèles d'apprentissage pour effectuer cette association.
- **Automatiser le processus** pour éviter les erreurs humaines et améliorer l'efficacité des équipes comptables.

## Technologies utilisées
Le projet utilise plusieurs technologies, notamment :
- **OCR** (par exemple, Tesseract ou un autre modèle d'extraction de texte)
- **Modèles NER** pour l'extraction d'entités (par exemple, dates, montants, numéros de facture)
- **Apprentissage supervisé** pour l'association des données aux comptes comptables.

## Structure du projet
Le projet est structuré de manière à inclure les étapes suivantes :
1. Extraction des données des factures via OCR.
2. Prétraitement et nettoyage des données.
3. Entraînement d'un modèle pour l'extraction d'entités (NER).
4. Association des entités extraites aux comptes comptables.
