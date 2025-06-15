Fine-Tuning des modèles Phi-2 et Camembert
==========================================

Définition du Fine-Tuning
-------------------------

Le **fine-tuning** est une technique d'apprentissage supervisé qui consiste à adapter
un modèle pré-entraîné sur un large corpus généraliste à une tâche spécifique, en
poursuivant son entraînement sur un jeu de données ciblé et restreint.

Cette approche permet de bénéficier des connaissances acquises par le modèle tout
en le spécialisant pour améliorer ses performances sur la tâche souhaitée.

Fine-Tuning avec le modèle Phi-2
--------------------------------

**Phi-2** est un modèle de langage performant pour plusieurs tâches en français.
Le fine-tuning de Phi-2 ajuste ses poids à partir de notre corpus spécifique de
factures afin d'améliorer la classification comptable.

Fine-Tuning avec le modèle Camembert
------------------------------------

**Camembert** est un modèle de type BERT pré-entraîné exclusivement sur du texte français.
Sa formation optimisée pour le français lui permet une meilleure compréhension contextuelle,
ce qui est idéal pour la classification textuelle dans notre projet.

Causes du choix de Camembert dans notre projet
----------------------------------------------

- Spécificité linguistique : Camembert comprend mieux les subtilités du français que des modèles multilingues.
- Performances élevées en classification textuelle sur corpus francophones.
- Taille et efficacité adaptées aux ressources matérielles disponibles.

Exemples de code pour le fine-tuning
------------------------------------

Fine-Tuning avec Phi-2
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
    import datasets

    model_name = "bigscience/phi-2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=NUM_CLASSES)

    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding=True)

    train_dataset = datasets.load_dataset('csv', data_files='train.csv')['train']
    train_dataset = train_dataset.map(preprocess_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results_phi2",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()

Fine-Tuning avec Camembert
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from transformers import CamembertTokenizer, CamembertForSequenceClassification, Trainer, TrainingArguments
    import datasets

    model_name = "camembert-base"
    tokenizer = CamembertTokenizer.from_pretrained(model_name)
    model = CamembertForSequenceClassification.from_pretrained(model_name, num_labels=NUM_CLASSES)

    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding=True)

    train_dataset = datasets.load_dataset('csv', data_files='train.csv')['train']
    train_dataset = train_dataset.map(preprocess_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results_camembert",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()
