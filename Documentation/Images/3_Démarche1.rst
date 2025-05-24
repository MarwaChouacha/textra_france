Démarche 1 : Extraction et classification comptable via LLMs
=============================================================

Objectif
--------

Cette première démarche vise à automatiser l’extraction d’informations à partir de factures,
puis à effectuer leur classification comptable selon le plan comptable français et canadien.
Le pipeline combine OCR, extraction par LLMs et classification supervisée.

Étapes de la démarche
---------------------

1. Chargement des données
~~~~~~~~~~~~~~~~~~~~~~~~~

Les factures sont au format JSON contenant les chemins d’image et des métadonnées.

.. code-block:: python

    import json

    with open('factures.json', 'r', encoding='utf-8') as f:
        factures = json.load(f)

📍 **Notebook associé** : `1_chargement_factures.ipynb`

2. Prétraitement des images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Conversion des images en niveaux de gris et réduction du bruit.

.. code-block:: python

    import cv2

    def preprocess_image(image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        return img

📍 **Notebook associé** : `2_pretraitement_images.ipynb`

3. Extraction des entités avec Qwen2.5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le modèle Qwen2.5 est utilisé pour extraire les entités structurées du texte OCR.

.. code-block:: python

    prompt = f"""
    Texte extrait : {texte_facture}
    Extrais les entités suivantes : Numéro Facture, Date, Client, Montant HT, TVA, Total TTC.
    Réponse formatée en JSON :
    """

📍 **Notebook associé** : `3_extraction_qwen.ipynb`

4. Classification avec LLaMA3.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le modèle LLaMA3.1 propose le compte comptable adapté.

.. code-block:: python

    prompt = f"""
    Voici les données extraites d'une facture :
    - Client : {client}
    - Montant HT : {montant}
    - Libellé : {libelle}
    Propose le compte comptable (PCG) associé à cette opération.
    """

📍 **Notebook associé** : `4_classification_llama.ipynb`

5. Évaluation des résultats
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comparaison des résultats prédits avec des données validées manuellement.

.. code-block:: python

    from sklearn.metrics import classification_report

    print(classification_report(y_true, y_pred))

📍 **Notebook associé** : `5_evaluation.ipynb`

Référentiels utilisés
---------------------

- ✅ Plan Comptable Général (France)
- ✅ Plan Comptable Canadien (JSON)

Structure de l’interface utilisateur (Streamlit)
-------------------------------------------------

Une interface a été développée avec **Streamlit** pour tester le pipeline complet :

- Upload de facture
- Extraction OCR et Qwen2.5
- Classification LLaMA3.1
- Affichage des entités et du compte proposé

.. code-block:: python

    import streamlit as st

    uploaded_file = st.file_uploader("Importer une facture", type=["png", "jpg", "pdf"])
    if uploaded_file:
        texte = ocr_extraction(uploaded_file)
        entites = extraction_llm_qwen(texte)
        compte = classification_llm_llama(entites)
        st.json({"Entités": entites, "Compte Comptable": compte})

📍 **Fichier Streamlit associé** : `app_demarche1.py`

Fichiers Google Colab associés
------------------------------

.. list-table:: Liens vers les notebooks Google Colab
   :header-rows: 1

   * - Étape
     - Notebook Colab
   * - Chargement JSON
     - https://colab.research.google.com/drive/XXXXXXXXX
   * - Prétraitement des images
     - https://colab.research.google.com/drive/YYYYYYYYY
   * - Extraction Qwen2.5
     - https://colab.research.google.com/drive/ZZZZZZZZZ
   * - Classification LLaMA3.1
     - https://colab.research.google.com/drive/AAAAAAA
   * - Évaluation
     - https://colab.research.google.com/drive/BBBBBBB

*(Remplace les liens par les URL réels de tes notebooks Colab)*

