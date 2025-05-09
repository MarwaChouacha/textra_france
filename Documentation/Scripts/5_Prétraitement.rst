5_Prétraitement 
======================================
### 1. Prétraitement des Données

#### Objectif :
Expliquer le processus de nettoyage et de structuration des données extraites avant de les utiliser pour le finetuning avec le modèle Phi-2.

## Prétraitement des Données

### Objectifs du Prétraitement
Le prétraitement des données est une étape essentielle pour nettoyer et structurer les informations extraites par OCR avant de les passer à l'étape de finetuning du modèle Phi-2. L'objectif principal est de s'assurer que les données sont prêtes à être utilisées pour entraîner le modèle et obtenir des résultats fiables.

### Étapes du prétraitement
1. **Suppression des caractères non pertinents** : Les textes extraits par OCR peuvent contenir des caractères indésirables, comme des symboles ou des espaces superflus. Ces caractères doivent être éliminés pour éviter toute interférence dans le modèle.
2. **Correction des erreurs OCR** : Les erreurs courantes dans le texte OCR doivent être corrigées. Par exemple, les lettres mal interprétées comme des "I" pour des "1" ou des "O" pour des "0".
3. **Structuration des données** : Les informations doivent être organisées de manière structurée, comme des tableaux ou des dictionnaires, pour une meilleure interprétation par le modèle Phi-2.

### Exemple de code de prétraitement avec Phi-2

.. code-block:: python

    import re

    # Exemple de texte extrait par OCR
    text = "Facture #12345 Montant: 1500€ \nDate: 2021-05-20 \nNuméro de facture: 1234"

    # Suppression des caractères non pertinents
    text_clean = re.sub(r'[^\w\s]', '', text)

    # Correction des erreurs OCR courantes
    text_clean = text_clean.replace('O', '0').replace('I', '1')

    # Afficher le texte nettoyé
    print("Texte nettoyé : ", text_clean)



### 2. Finetuning du Modèle Phi-2

#### Objectif :
Adapter le modèle préentraîné Phi-2 à la tâche spécifique d'extraction d'informations pertinentes sur les factures (par exemple, dates, montants, numéros de facture) et d'association aux comptes comptables. Le modèle Phi-2 est basé sur des techniques d'apprentissage profond et peut être ajusté pour mieux s'adapter à des ensembles de données spécifiques.

## Objectifs du Finetuning
Le finetuning consiste à ajuster un modèle préexistant, comme Phi-2, afin qu'il soit capable de prédire des entités spécifiques à partir des factures. L'objectif est de rendre le modèle plus performant sur la tâche d'extraction des informations pertinentes comme :
- Les dates de factures
- Les montants
- Les numéros de facture

Le modèle sera ensuite utilisé pour associer ces informations aux comptes comptables.

### Étapes du Finetuning

1. **Chargement du modèle préentraîné** : Le modèle Phi-2 est déjà préentraîné sur une large base de données. Nous allons l'adapter à notre tâche en finetunant ses couches sur notre jeu de données spécifique.
2. **Préparation des données** : Avant d'entraîner le modèle, il faut préparer les données extraites de manière structurée et étiquetée (par exemple, factures avec des annotations pour les entités comme les montants et les dates).
3. **Entraînement** : Le modèle Phi-2 sera finetuné en utilisant notre jeu de données étiqueté. Ce processus implique de mettre à jour les poids du modèle afin qu'il apprenne à extraire correctement les informations des factures.
4. **Évaluation du modèle** : Une fois le modèle finetuné, il est essentiel de l'évaluer sur un jeu de données de test pour mesurer sa performance (précision, rappel, F-score).

### Exemple de code pour le Finetuning du Modèle Phi-2

.. code-block:: python

    from phi2 import Phi2Model, Phi2Tokenizer
    from transformers import Trainer, TrainingArguments
    import torch
    from torch.utils.data import Dataset

    # Charger le modèle Phi-2 préentraîné et son tokenizer
    tokenizer = Phi2Tokenizer.from_pretrained('phi2-base')
    model = Phi2Model.from_pretrained('phi2-base')

    # Préparer le jeu de données (exemple simple)
    class InvoiceDataset(Dataset):
        def __init__(self, texts, labels):
            self.texts = texts
            self.labels = labels
            self.tokenizer = tokenizer

        def __len__(self):
            return len(self.texts)

        def __getitem__(self, idx):
            text = self.texts[idx]
            labels = self.labels[idx]
            encoding = self.tokenizer(text, truncation=True, padding='max_length', max_length=512, return_tensors='pt')
            encoding['labels'] = torch.tensor(labels, dtype=torch.long)
            return encoding

    # Exemple de textes de factures et leurs labels (données fictives)
    texts = ["Facture #12345 Montant: 1500€ Date: 2021-05-20"]
    labels = [[0, 1, 2, 3, 4]]  # Labels fictifs, chaque chiffre représente une entité (ex: Date, Montant, etc.)

    # Créer le jeu de données
    train_dataset = InvoiceDataset(texts, labels)

    # Définir les paramètres d'entraînement
    training_args = TrainingArguments(
        output_dir='./results',  # Répertoire pour sauvegarder les résultats
        num_train_epochs=3,      # Nombre d'époques
        per_device_train_batch_size=8,  # Taille du batch
        evaluation_strategy="epoch",  # Évaluer chaque époque
        logging_dir='./logs',     # Répertoire pour les logs
        save_steps=500,
    )

    # Initialiser le Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    # Entraîner le modèle
    trainer.train()

    # Sauvegarder le modèle finetuné
    model.save_pretrained('./finetuned_phi2')
    tokenizer.save_pretrained('./finetuned_phi2')


### Conclusion

Le finetuning du modèle Phi-2 permet d'adapter un modèle préexistant aux spécificités de la tâche d'extraction des informations pertinentes des factures. Cela améliore la précision du modèle en l'entraînant sur des données spécifiques à la tâche, comme les dates, montants, et numéros de facture. Après l'entraînement, le modèle est évalué pour vérifier sa capacité à prédire correctement ces informations et à les associer aux comptes comptables.
