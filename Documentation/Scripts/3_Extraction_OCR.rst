# Extraction de Texte via OCR

## Qu'est-ce que l'OCR ?
La Reconnaissance Optique de Caractères (OCR) est une technologie qui permet de convertir du texte dans des images en données structurées. Dans notre projet, l'OCR est utilisé pour extraire le texte des factures scannées ou au format image.

## Outils utilisés
Nous utilisons **Tesseract OCR**, un moteur OCR open-source, pour extraire le texte des images de factures. Il est efficace et supporte plusieurs langues, dont le français.

### Processus d'extraction
1. **Prétraitement des images** : Les images de factures sont d'abord prétraitées (redimensionnement, binarisation, suppression de bruit) pour améliorer la qualité du texte extrait.
2. **Extraction du texte** : Tesseract est utilisé pour extraire le texte brut de chaque facture. Le texte extrait contient toutes les informations nécessaires à l'étape suivante.
3. **Validation du texte** : Après l'extraction, nous appliquons des règles simples pour vérifier si l'extraction du texte a bien fonctionné (par exemple, vérifier si certains champs clés sont présents dans le texte).

### Exemple de code pour l'extraction avec Tesseract
```python
import pytesseract
from PIL import Image

# Charger l'image
img = Image.open('facture.jpg')

# Extraire le texte
text = pytesseract.image_to_string(img)

# Afficher le texte extrait
print(text)
