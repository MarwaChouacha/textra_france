Limitations de la Démarche 1
-----------------------------

Bien que la démarche 1 repose sur des modèles avancés (Qwen2.5 et LLaMA3.1) et produise des résultats prometteurs, plusieurs limitations ont été identifiées au cours des expérimentations :

1. **Temps de réponse élevé**
- Le recours à **deux modèles de langage de grande taille (LLMs)** entraîne une latence importante lors du traitement d’une facture.
- Cette double invocation (extraction puis classification) rend l'approche peu adaptée à un déploiement temps réel ou à grande échelle.

2. **Incohérences dans la classification**
- Dans certains cas, notamment lorsque la facture est mal rédigée ou ambigüe, le modèle LLaMA3.1 **associe un compte comptable inapproprié**.
- L’absence de contexte explicite (libellé trop vague, client inconnu) réduit la fiabilité des prédictions.

3. **Dépendance forte au texte OCR**
- Toute erreur dans l’extraction initiale (Qwen2.5) impacte directement la classification finale, ce qui peut fausser totalement le résultat.
- Exemple : une mauvaise reconnaissance du montant ou du libellé peut conduire à un compte erroné.

4. **Manque d’adaptabilité**
- Le modèle LLaMA3.1 n’est pas facilement personnalisable sans fine-tuning, ce qui limite son adaptation à des règles métiers spécifiques d’une entreprise donnée.

---

Ces limitations ont motivé la conception d’une **deuxième démarche**, plus légère, modulaire et fine-tunable :  
➡️ **Classification automatique basée sur des modèles supervisés (TF-IDF + fine-tuning)**, présentée dans la section suivante.


Tests sur les factures françaises et canadiennes
================================================

Test 1 – Facture Française
--------------------------

**Contenu brut de la facture OCR** (extrait) :

::

    Facture n°: F2024-036
    Date: 12/03/2024
    Client: SARL Électro France
    Montant HT: 1250.00 €
    TVA: 250.00 €
    Total TTC: 1500.00 €
    Libellé: Achat de matériel informatique

**Entités extraites (via Qwen2.5)** :

.. code-block:: json

    {
        "numero_facture": "F2024-036",
        "date": "12/03/2024",
        "client": "SARL Électro France",
        "montant_ht": 1250.00,
        "tva": 250.00,
        "total_ttc": 1500.00,
        "libelle": "Achat de matériel informatique"
    }

**Compte prédit (via LLaMA3.1)** :

::

    2183 - Matériel de bureau et informatique

✅ *Prédiction correcte selon le Plan Comptable Français.*

---

Test 2 – Facture Canadienne
---------------------------

**Contenu brut de la facture OCR** (extrait) :

::

    Invoice No: CA-8791
    Date: 2024-04-10
    Customer: Construction MaxPro Inc.
    Subtotal: 3200.00 CAD
    GST: 160.00 CAD
    Total: 3360.00 CAD
    Description: Service de consultation en génie

**Entités extraites (via Qwen2.5)** :

.. code-block:: json

    {
        "numero_facture": "CA-8791",
        "date": "2024-04-10",
        "client": "Construction MaxPro Inc.",
        "montant_ht": 3200.00,
        "tva": 160.00,
        "total_ttc": 3360.00,
        "libelle": "Service de consultation en génie"
    }

**Compte prédit (via LLaMA3.1)** :

::

    6270 - Honoraires professionnels (Plan comptable canadien)

✅ *Classification cohérente selon le plan comptable canadien.*

---

Observations
------------

- Dans les deux cas, l’extraction a permis de retrouver les informations principales de la facture.
- La classification a fonctionné lorsque le libellé était explicite (ex. : “matériel informatique” ou “consultation”).
- En cas de libellé flou ou d’absence de structure (ex. : "Prestation diverse"), le modèle avait tendance à proposer un compte générique incorrect (d’où la nécessité de la Démarche 2).

