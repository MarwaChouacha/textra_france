1_Introduction 
======================================

# Introduction

## Contexte du projet
L'extraction automatique de texte à partir des factures est devenue un élément fondamental dans la gestion comptable et administrative des entreprises modernes. En effet, avec l'augmentation des volumes de données traitées et la nécessité d'améliorer l'efficacité des processus, il devient essentiel de réduire l'intervention manuelle dans l'extraction d'informations à partir de documents tels que les factures. Ce projet vise à automatiser cette tâche en utilisant des techniques avancées de Reconnaissance Optique de Caractères (OCR) pour extraire les données pertinentes des factures françaises et les associer automatiquement aux comptes comptables appropriés.

## Objectifs du projet
Les objectifs principaux de ce projet sont les suivants :

**Extraire les données pertinentes des factures** : Cela inclut des informations telles que les montants, les dates, les numéros de facture, et les coordonnées des clients.

**Associer ces données à des comptes comptables appropriés** : À l'aide de règles métiers spécifiques et de modèles d'apprentissage, l'objectif est de garantir une association correcte des données extraites aux comptes comptables adéquats.

**Automatiser le processus** : L'automatisation permettra de réduire les erreurs humaines et d'améliorer l'efficacité et la productivité des équipes comptables, tout en assurant une meilleure traçabilité des données.

Le pipeline utilisée est:

.. figure:: /Documentation/Images/pipeline.jpg
    :width: 100%
    :align: center
    :alt: Alternative text for the image
    :name: Introduction

## Technologies utilisées
Pour atteindre ces objectifs, plusieurs technologies sont utilisées dans le cadre de ce projet :

**OCR (Reconnaissance Optique de Caractères)** : Des outils comme Tesseract ou d'autres modèles spécialisés sont employés pour extraire le texte à partir des images des factures.

**Modèles LLM** : Ces modèles permettent d'extraire des entités spécifiques telles que les dates, montants, et numéros de facture à partir du texte brut généré par l'OCR.

**Apprentissage supervisé** : Des modèles d'apprentissage supervisé sont utilisés pour effectuer l'association des données extraites aux comptes comptables, en s'appuyant sur des règles métiers et des données d'entraînement.

## Structure du projet
Le projet est organisé en plusieurs étapes clés pour garantir son efficacité et sa réussite :

**Extraction des données des factures via OCR** : L'outil OCR est utilisé pour convertir les images des factures en texte exploitable.

**Prétraitement et nettoyage des données** : Les données extraites sont nettoyées et préparées pour être traitées efficacement dans les étapes suivantes.

**Entraînement d'un modèle** : Un modèle NER est entraîné pour identifier et extraire les informations spécifiques, telles que les dates, montants et numéros de facture.

**Association des entités extraites aux comptes comptables** : Un modèle d'apprentissage supervisé est utilisé pour associer les entités extraites aux comptes comptables appropriés, selon des règles métiers prédéfinies.
