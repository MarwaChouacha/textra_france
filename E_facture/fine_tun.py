import pandas as pd
from transformers import CamembertTokenizer,CamembertForSequenceClassification
from transformers import TrainingArguments, Trainer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from datasets import Dataset # Need to import Dataset
import random

# Libellés comptables avec leurs comptes
# entries = [
# ('VENTE DE PRODUITS FINIS',701000),
# ('VENTE DE SERVICE',706000),
# ('VENTE DE SERVICE ANNEXE',708000),
# ('AUTRE GAIN DIVERS',758000),
# ('VENTE D UNE IMMOBILISATION',775000),
# ('VENTE DE MARCHANDISE',707000),
# ('GAIN DE CHANGE',756000),
# ('PRODUITS FINANCIERS',760000),
# ('APPORT D ASSOCIE',456000),
# ('DEPOT D ESPECES',512000),
# ('EMPRUNT',160000),
# ('SUBVENTIONS D INVESTISSEMENT',131000),
# ('AIDES ET SUBVENTIONS D EXPLOITATION',740000),
# ('INDEMNITE D ASSURANCE',790000),
# ('CAUTION RECUE',165000),
# ('CAUTION',165000),
# ('CAPITAL',101000),
# ('PRIMES D EMISSION',104000),
# ('DEBOURS POUR VOS CLIENTS',467000),
# ('PRODUIT EXCEPTIONNEL',770000),
# ('ACHAT DE PRODUITS FINIS',601000),
# ('ACHAT DE SERVICES',604000),
# ('FOURNITURES DE BUREAU',606400),
# ('ACHATS NON STOCKES DE MATIERES ET FOURNITURES',602000),
# ('TRANSPORT SUR ACHATS',624100),
# ('ASSURANCES',616000),
# ('FRAIS POSTAUX ET DE TELECOMMUNICATIONS',626000),
# ('LOCATION DE BIENS IMMOBILIERS',613200),
# ('LOCATION DE MATERIEL ET OUTILLAGE',613500),
# ('FRAIS DE MAINTENANCE ET REPARATIONS',615000),
# ('FRAIS DIVERS DE GESTION COURANTE',625000),
# ('SERVICES BANCAIRES ET ASSIMILES',627000),
# ('PUBLICITE PUBLICATIONS',623000),
# ('ETUDES ET RECHERCHES',622000),
# ('DOCUMENTATION GENERALE',618000),
# ('CHARGES SOCIALES',645000),
# ('IMPOTS TAXES ET VERSEMENTS ASSIMILES',635000),
# ('REMUNERATIONS DU PERSONNEL EXTERIEUR',621000),
# ('RETROCESSIONS SUR REMUNERATIONS',622000),
# ('CHARGES LOCATIVES ET DE COPROPRIETE',614000),
# ('PRIMES D ASSURANCE',616000),
# ('FRAIS DE RECEPTION',625100),
# ('INDEMNITES KILOMETRIQUES',625110),
# ('FRAIS DE FORMATION DU PERSONNEL',631300),
# ('INDEMNITES DE DEPART A LA RETRAITE',645800),
# ('FRAIS DE DEMENAGEMENT',625200),
# ('FRAIS DE MISSION',625300),
# ('FRAIS DE REPRESENTATION',625400),
# ('PERTE SUR CREANCES IRRECOUVRABLES',654000),
# ('DOTATIONS AUX AMORTISSEMENTS ET PROVISIONS',681000),
# ('CHARGES EXCEPTIONNELLES SUR OPERATIONS DE GESTION',671000),
# ('CHARGES EXCEPTIONNELLES SUR OPERATIONS EN CAPITAL',675000),
# ('SALAIRES NETS',641000),
# ('PRELEVEMENT A LA SOURCE',442100),
# ('COTISATIONS SOCIALES',645000),
# ('TITRES RESTAURANTS',647000),
# ('CHEQUES VACANCES',647000),
# ('AUTRES CHARGES SOCIALES',647000),
# ('PERSONNEL INTERIMAIRE',621000),
# ('RETROCESSION VERSEE',622000),
# ('IMMOBILISATION CORPORELLE',210000),
# ('IMMOBILISATION FINANCIERE',270000),
# ('TITRES DE PARTICIPATION',261000),
# ('AUTRE IMMO INCORPORELLE',203000),
# ('FONDS COMMERCIAL',207000),
# ('MATIERE PREMIERE ET FOURNITURES',601000),
# ('PRESTATION DE SERVICE',604000),
# ('SOUS TRAITANCE',604000),
# ('REMBOURSEMENT D ASSOCIE',455000),
# ('RETRAIT D ESPECES',531000),
# ('HONORAIRES DIVERS',622000),
# ('MATERIEL ET OUTILLAGE',215000),
# ('PERTE DE CHANGE',666000),
# ('FRAIS DIVERS',625000),
# ('MARCHANDISE POUR LA REVENTE',607000),
# ('TELECOM ET AFFRANCHISSEMENT',626000),
# ('FRAIS D ACTE ET DE CONTENTIEUX',622000),
# ('VIREMENT INTERNE',580000),
# ('DEBOURS POUR VOS CLIENTS',467000),
# ('PUBLICITE',623000),
# ('FRAIS DE DEPLACEMENT',625100),
# ('RECEPTION ET CONGRES',625200),
# ('RESTAURANT ET REPAS D AFFAIRES',625200),
# ('TVA payee',4451),
# ('Rembourssement TVA',44571),

# ]

# # Génération aléatoire de 100 lignes
# data = [random.choice(entries) for _ in range(100)]
# df = pd.DataFrame(data, columns=["libelle", "compte_comptable"])

# Sauvegarde en CSV
# create csv file hadi une seule fois
# df.to_csv('dataset_comptable.csv', index=False)


# read .csv file
df = pd.read_csv("dataset_comptable.csv")
df.head()
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# 4. Extraire les labels uniques et créer mappings
# Use the correct column name 'compte_comptable' instead of 'label'
labels = sorted(train_df['compte_comptable'].unique().tolist())
label2id = {label: idx for idx, label in enumerate(labels)}
id2label = {idx: label for label, idx in label2id.items()}

print(id2label)
# 5. Convertir les labels en ids
# Use the correct column name 'compte_comptable' instead of 'label'
train_df["label_id"] = train_df["compte_comptable"].map(label2id)
val_df["label_id"] = val_df["compte_comptable"].map(label2id)
 
 
 
# Rename 'libelle' to 'text' and 'label_id' to 'label' for Hugging Face Dataset compatibility
train_dataset = Dataset.from_pandas(train_df[["libelle", "label_id"]].rename(columns={"libelle": "text", "label_id": "label"}))
val_dataset = Dataset.from_pandas(val_df[["libelle", "label_id"]].rename(columns={"libelle": "text", "label_id": "label"}))
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")

# Vérification des colonnes
df = df[["libelle", "compte_comptable"]].dropna()
df = df.rename(columns={"libelle": "text", "compte_comptable": "label"})

tokenizer = CamembertTokenizer.from_pretrained("camembert-base")

def tokenize_function(example):
    return tokenizer(example["text"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

model = CamembertForSequenceClassification.from_pretrained(
    "camembert-base",
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)
trainer.train()

trainer.save_model("modele_comptable")  # dossier de sauvegarde

# Sauvegarde du tokenizer (important pour le futur usage)
tokenizer.save_pretrained("modele_comptable")





# # {0: 4451, 1: 104000, 2: 131000, 3: 165000, 4: 203000, 5: 207000, 6: 261000, 7: 270000, 8: 442100, 9: 455000, 10: 467000, 11: 531000, 12: 601000, 13: 602000, 14: 604000, 15: 606400, 16: 607000, 17: 613200, 18: 621000, 19: 622000, 20: 623000, 21: 624100, 22: 625000, 23: 625110, 24: 625200, 25: 625400, 26: 626000, 27: 631300, 28: 641000, 29: 645000, 30: 647000, 31: 654000, 32: 666000, 33: 671000, 34: 681000, 35: 701000, 36: 707000, 37: 756000, 38: 760000, 39: 770000, 40: 790000}


# code de test  ila bghiti tester hna khass commenter l code dyal preparation au dessus 7it hadak ghir kan9ado bih lmodel une mour totu 

import torch
from transformers import CamembertTokenizer, CamembertForSequenceClassification
#  oui db lmodel dialna m sauvegarder fhal dakchi li kna derna lphi2 yak don db ana min nbghi ntester f inerface manhtajch n 3awd nheyd comment llcode li lfo9 nn hada ghir ill bghiti t9adi model akhor olla tzidi f data ah ok amma lmodel dyal linterface olla ldef dyal l interface hiya had 
#hna kan3ayto lmodel dyalna f ay wa9t bghin andiro test
model_path = "modele_comptable"
tokenizer = CamembertTokenizer.from_pretrained(model_path)
model = CamembertForSequenceClassification.from_pretrained(model_path)
# Your test sentence
text = "PRODUITS FINANCIERS"

# Example: recreate your label mapping
id2label = {0: 4451, 1: 44571, 2: 104000, 3: 131000, 4: 160000, 5: 165000, 6: 207000, 7: 215000, 8: 261000, 9: 455000, 10: 456000, 11: 467000, 12: 512000, 13: 601000, 14: 604000, 15: 606400, 16: 607000, 17: 613500, 18: 616000, 19: 621000, 20: 622000, 21: 623000, 22: 625000, 23: 625200, 24: 625400, 25: 627000, 26: 631300, 27: 635000, 28: 645000, 29: 645800, 30: 671000, 31: 681000, 32: 701000, 33: 707000, 34: 708000, 35: 756000, 36: 760000, 37: 770000, 38: 775000, 39: 790000}

# Tokenize the input
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# Disable gradient calculation
with torch.no_grad():
    outputs = model(**inputs)

# Get prediction
logits = outputs.logits
predicted_class_id = torch.argmax(logits, dim=1).item()

# Map back to account number
predicted_account = id2label[predicted_class_id]
print(f"Texte : {text}")
print(f"Compte comptable prédit : {predicted_account}")

