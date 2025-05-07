
### 3. **3_Pretraitement.rst**

#### Objectif :
Expliquer le processus de nettoyage et de structuration des données extraites.

```rst
# Prétraitement des Données

## Objectifs du Prétraitement
Le prétraitement des données est crucial pour améliorer la qualité des données extraites avant de les utiliser dans les étapes suivantes (extraction d'entités et association au compte comptable).

### Étapes du prétraitement
1. **Suppression des caractères non pertinents** : Les textes extraits par OCR peuvent contenir des caractères inutiles (par exemple, des symboles ou des espaces indésirables). Ces caractères doivent être supprimés.
2. **Correction des erreurs OCR** : L'OCR peut introduire des erreurs de reconnaissance, notamment des lettres mal interprétées. Nous utilisons des algorithmes de correction pour minimiser ces erreurs.
3. **Structuration des données** : Nous structurons les informations extraites sous forme de tableaux ou de dictionnaires pour faciliter l'analyse ultérieure. Par exemple, les informations sur la date de la facture et le montant sont extraites et stockées sous forme de champs.

### Exemple de code de prétraitement
```python
import re

# Suppression des caractères non pertinents
text_clean = re.sub(r'[^\w\s]', '', text)

# Correction d'erreurs OCR courantes (exemple simple)
text_clean = text_clean.replace('O', '0').replace('I', '1')

# Afficher le texte nettoyé
print(text_clean)
