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
.. image:: Images/pip4.png
   :width: 400
   :alt: Pipeline 4

**Contenu brut de la facture OCR** (extrait) :

::

    Facture n°: FR-001
    Date: 29/01/2019
    Client: Cendrillon Ayot
    Montant HT: 145.00 €
    TVA: 29.00 €
    Total TTC: 174.00 €
    Libellé: Grand brun escargot pour manger et Petit mariniere uniforme en bleuet Facile a jouer accordeon

**Entités extraites (via Qwen2.5)** :

.. code-block:: json

    {
        "numero_facture": "FR-001",
        "date": " 29/01/2019",
        "client": "Cendrillon Ayot",
        "montant_ht": 145.00 €,
        "tva": 29.00 €,
        "total_ttc": 174.00 €,
        "libelle": "Grand brun escargot pour manger et Petit mariniere uniforme en bleuet Facile a jouer accordeon
"
    }

**Compte prédit (via LLaMA3.1)** :

::

    2183 - Matériel de bureau et informatique

✅ *Prédiction correcte selon le Plan Comptable Français.*

---

Test 2 – Facture Canadienne
---------------------------
.. image:: Images/pip5.png
   :width: 400
   :alt: Pipeline 5

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

