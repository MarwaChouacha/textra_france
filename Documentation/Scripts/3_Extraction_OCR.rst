# Extraction de Texte via OCR

## Qu'est-ce que l'OCR ?
La Reconnaissance Optique de Caractères (OCR) est une technologie qui permet de convertir du texte dans des images en données structurées. Dans notre projet, l'OCR est utilisé pour extraire le texte des factures scannées ou au format image.

## Outils utilisés
Nous utilisons **Tesseract OCR**, un moteur OCR open-source, pour extraire le texte des images de factures. Ce moteur est largement utilisé en raison de son efficacité et de sa capacité à supporter plusieurs langues, y compris le français.

### Processus d'extraction
1. **Prétraitement des images** : Avant l'extraction proprement dite, les images de factures subissent un prétraitement pour améliorer la qualité du texte extrait. Ce traitement inclut :
   - **Redimensionnement** de l'image pour garantir qu'elle est d'une taille appropriée.
   - **Binarisation** pour transformer l'image en noir et blanc, ce qui améliore la précision de l'OCR.
   - **Suppression de bruit** pour éliminer les imperfections de l'image, comme les taches ou les distorsions, qui pourraient perturber l'extraction du texte.

2. **Extraction du texte** : L'outil **Tesseract** est utilisé pour extraire le texte brut de chaque facture. Il génère une chaîne de caractères contenant toutes les informations présentes sur la facture, y compris les montants, les dates, les numéros de facture, etc.

3. **Validation du texte** : Après l'extraction, nous appliquons des règles simples pour valider l'exactitude du texte extrait. Par exemple, nous vérifions si des champs clés tels que le montant, la date, ou le numéro de facture sont présents dans le texte. Cette étape permet d'assurer la qualité et la fiabilité des données extraites.

4. **Extraction des codes** : Une autre tâche importante est l'extraction des **codes de produit**, **codes de comptes comptables**, ou **numéros de référence** présents sur les factures. Ces codes permettent une identification plus précise et un rattachement direct aux comptes comptables ou aux produits spécifiques. Nous utilisons des expressions régulières et des modèles d'extraction spécifiques pour repérer ces codes dans le texte extrait.

### Exemple de code pour l'extraction avec Tesseract

```python
import pytesseract
from PIL import Image
import re

# Charger l'image
img = Image.open('facture.jpg')

# Extraire le texte avec Tesseract
text = pytesseract.image_to_string(img)

# Afficher le texte extrait
print(text)

# Exemple d'extraction de codes spécifiques, comme les numéros de facture et les montants
invoice_number = re.search(r'Facture\s*#(\d+)', text)
amount = re.search(r'(\d+,\d{2})\s*€', text)  # Montant en euros

if invoice_number:
    print("Numéro de facture trouvé :", invoice_number.group(1))

if amount:
    print("Montant trouvé :", amount.group(1))
