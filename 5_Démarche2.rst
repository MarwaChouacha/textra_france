Démarche 2 : Extraction et Classification Comptable des Factures
================================================================

Cette démarche présente les étapes détaillées de l'extraction de texte à partir de factures
et la classification comptable associée grâce à des modèles de machine learning et deep learning,
intégrés dans une application web Django.

Étape 1 : Extraction du texte et association des étiquettes
------------------------------------------------------------

- Extraction OCR : Le texte est extrait à partir des images de factures grâce à une technologie
OCR (Optical Character Recognition) qui convertit l'image en texte brut.
- Association des étiquettes : Chaque élément de texte extrait est annoté par des étiquettes spécifiques
(labels) correspondant aux informations comptables à extraire (exemple : montant, date, fournisseur, compte comptable).

Étape 2 : Prédiction des catégories comptables à partir du texte de la facture
-------------------------------------------------------------------------------

Cette étape vise à classifier les textes extraits selon leurs catégories comptables, en utilisant plusieurs techniques :

2.1 Modèle de classification TF-IDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- On utilise la représentation TF-IDF (Term Frequency-Inverse Document Frequency) pour vectoriser les textes des factures.
- Un modèle de classification supervisée est entraîné pour prédire la catégorie comptable associée.

2.2 Fine-tuning avec le modèle Phi-2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Le modèle de langage **Phi-2** est fine-tuné pour améliorer la classification.
- Le fine-tuning adapte le modèle pré-entraîné aux spécificités des données comptables.

2.3 Fine-tuning avec le modèle Camembert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Camembert, un modèle de type BERT pour le français, est également fine-tuné pour la classification.
- Il permet une meilleure compréhension contextuelle du texte en français.

2.4 Résultats
~~~~~~~~~~~~~

- Après fine-tuning, les modèles sont évalués sur un jeu de test.
- Les résultats montrent une amélioration notable de la précision de classification.

Étape 3 : Intégration dans une application web Django
-----------------------------------------------------

3.1 Pipeline complet
~~~~~~~~~~~~~~~~~~~~

Le pipeline comprend les éléments suivants :

- Chargement de la facture (image ou PDF) via une interface utilisateur.
- Extraction OCR du texte.
- Prédiction comptable via les modèles fine-tunés (Phi-2, Camembert).
- Retour des résultats à l’utilisateur dans une interface web interactive.

3.2 Structure des fichiers clés
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------+----------------------------------------------------------------+
| Fichier           | Rôle                                                           |
+===================+================================================================+
| `models.py`       | Définit la structure des données (facture, texte, catégorie).  |
+-------------------+----------------------------------------------------------------+
| `views.py`        | Logique principale (upload, extraction, classification, API).  |
+-------------------+----------------------------------------------------------------+
| `urls.py`         | Routage des URL vers les fonctions dans `views.py`.            |
+-------------------+----------------------------------------------------------------+
| `serializers.py`  | Conversion des objets modèle en JSON pour l’API REST.          |
+-------------------+----------------------------------------------------------------+
| `admin.py`        | Enregistrement des modèles dans l’interface d’administration. |
+-------------------+----------------------------------------------------------------+

Exemples de codes clés
----------------------

models.py
^^^^^^^^^

.. code-block:: python

    from django.db import models

    class Facture(models.Model):
        texte_extrait = models.TextField()
        categorie = models.CharField(max_length=100)
        compte_comptable = models.CharField(max_length=50)

        def __str__(self):
        return f"Facture {self.id} - Catégorie: {self.categorie}"

views.py (extrait simplifié)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from django.shortcuts import render
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from .models import Facture
    from .serializers import FactureSerializer
    from ocr_module import extraire_texte
    from classification import predire_categorie

    @api_view(['POST'])
    def extract_and_classify(request):
        fichier = request.FILES['facture']
        texte = extraire_texte(fichier)
        categorie, compte = predire_categorie(texte)
        
        facture = Facture.objects.create(
        texte_extrait=texte,
        categorie=categorie,
        compte_comptable=compte
        )
        serializer = FactureSerializer(facture)
        return Response(serializer.data)

urls.py
^^^^^^^

.. code-block:: python

    from django.urls import path
    from . import views

    urlpatterns = [
        path('extract/', views.extract_and_classify, name='extract_and_classify'),
    ]

Conclusion
----------

Cette démarche permet une automatisation avancée de la gestion comptable des factures
grâce à l'association d'extraction OCR et de classification intelligente par modèles de langage
fine-tunés, intégrée dans une application web facile d’usage.
