4_Limitations
======================================

### 3. Prétraitement des Données

#### Objectif :
Expliquer le processus de nettoyage et de structuration des données extraites par OCR.

## Prétraitement des Données

### Objectifs du Prétraitement
Le prétraitement des données est crucial pour améliorer la qualité des données extraites avant de les utiliser dans les étapes suivantes (extraction d'entités et association au compte comptable). L'objectif est de nettoyer, structurer et corriger les erreurs avant d'analyser les informations de manière plus précise.

### Étapes du prétraitement
1. **Suppression des caractères non pertinents** : Les textes extraits par OCR peuvent contenir des caractères inutiles (par exemple, des symboles ou des espaces indésirables). Ces caractères doivent être supprimés pour garantir que seules les informations pertinentes soient utilisées.
2. **Correction des erreurs OCR** : L'OCR peut introduire des erreurs de reconnaissance, telles que des lettres mal interprétées ou des chiffres incorrects. Nous appliquons des algorithmes de correction pour minimiser ces erreurs.
3. **Structuration des données** : Une fois les données nettoyées, nous les structurons sous une forme appropriée (tableaux, dictionnaires, etc.) pour permettre une analyse efficace dans les étapes suivantes. Par exemple, les informations sur la date de la facture et le montant sont extraites et organisées sous forme de champs distincts.

### Exemple de code de prétraitement

Voici un exemple simple de code en Python pour le prétraitement des données extraites par OCR :

```python
import re

# Exemple de texte extrait par OCR
text = "Facture #12345 Montant: 1500€ \nDate: 2021-05-20 \n"

# Suppression des caractères non pertinents (par exemple, caractères spéciaux)
text_clean = re.sub(r'[^\w\s]', '', text)

# Correction d'erreurs OCR courantes (par exemple, remplacer 'O' par '0' et 'I' par '1')
text_clean = text_clean.replace('O', '0').replace('I', '1')

# Afficher le texte nettoyé
print(text_clean)

