Démarche 1 : Extraction et classification comptable via LLMs
=============================================================

Objectif
--------

Cette première démarche vise à automatiser l’extraction d’informations à partir de factures,
puis à effectuer leur classification comptable selon le plan comptable français et canadien.
Le pipeline combine OCR, extraction par LLMs et classification supervisée.

Étapes de la démarche
---------------------

# 1_chargement_factures.py
import json

def charger_factures(fichier_json='factures.json'):
    with open(fichier_json, 'r', encoding='utf-8') as f:
        factures = json.load(f)
    return factures


# 2_pretraitement_images.py
import cv2

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    return img


# 3_extraction_qwen.py
def prompt_extraction_qwen(texte_facture):
    prompt = f"""
Texte extrait : {texte_facture}
Extrais les entités suivantes : Numéro de facture, Date, Client, Montant HT, TVA, Total TTC.
Réponse formatée en JSON :
"""
    return prompt


# 4_classification_llama.py
def prompt_classification_llama(client, montant, libelle):
    prompt = f"""
Voici les données extraites d'une facture :
- Client : {client}
- Montant HT : {montant}
- Libellé : {libelle}
Propose le compte comptable (PCG) associé à cette opération.
"""
    return prompt


# 5_evaluation.py
from sklearn.metrics import classification_report

def evaluer_classification(y_true, y_pred):
    report = classification_report(y_true, y_pred)
    print(report)


# app_demarche1.py (interface Streamlit)
import streamlit as st

# Fonctions à implémenter ailleurs
def ocr_extraction(uploaded_file):
    # Extraction OCR à implémenter (ex: Tesseract ou autre)
    return "texte extrait de la facture"

def extraction_llm_qwen(texte):
    # Appel au LLM Qwen2.5 avec prompt_extraction_qwen et parsing JSON réponse
    return {
    "Numéro facture": "F12345",
    "Date": "2025-05-23",
    "Client": "Entreprise XYZ",
    "Montant HT": 1000.0,
    "TVA": 200.0,
    "Total TTC": 1200.0,
    "Libellé": "Prestation de service"
    }

def classification_llm_llama(entites):
    # Appel au LLM LLaMA3.1 avec prompt_classification_llama et récupération compte
    return "606 - Achats fournisseurs"

uploaded_file = st.file_uploader("Importer une facture", type=["png", "jpg", "pdf"])
if uploaded_file:
    texte = ocr_extraction(uploaded_file)
    entites = extraction_llm_qwen(texte)
    compte = classification_llm_llama(entites)
    st.json({"Entités": entites, "Compte Comptable": compte})
