3_OCR
======================================

3.1 C'est quoi OCR ?
--------------------
OCR signifie Reconnaissance Optique de Caractères. C'est la technologie qui permet aux logiciels de reconnaître du texte dans des images ou des documents numérisés, 
et de le convertir en données modifiables et recherchables.

La reconnaissance optique de caractères (OCR) implique plusieurs étapes pour convertir des images de texte en texte éditable :

- **Prétraitement de l'image :** L'image est nettoyée pour améliorer la qualité et la lisibilité du texte. Cela peut inclure des opérations telles que la normalisation des couleurs, la suppression du bruit et l'amélioration du contraste.
- **Détection des régions d'intérêt :** Les zones de l'image contenant du texte sont identifiées à l'aide de techniques de détection d'objets ou de segmentation d'image.
- **Reconnaissance des caractères :** Les caractères individuels dans les régions d'intérêt sont identifiés à l'aide de modèles de reconnaissance de forme ou de réseaux de neurones convolutifs (CNN) pour reconnaître les formes des lettres et des chiffres.
- **Post-traitement :** Une fois les caractères reconnus, des techniques de traitement du langage naturel peuvent être utilisées pour améliorer la précision de la reconnaissance en tenant compte du contexte et de la grammaire.

3.3 OCR Benchmarking
---------------------

3.3.1 EasyOCR
~~~~~~~~~~~~~
EasyOCR est un logiciel de reconnaissance optique de caractères (OCR) open-source développé en Python. Il permet de convertir des images ou des fichiers PDF contenant du texte en texte
éditable et recherchable. EasyOCR est conçu pour être facile à utiliser et offre une bonne précision de reconnaissance pour plusieurs langues, y compris des langues asiatiques comme le
chinois, le japonais et le coréen. Il prend en charge plusieurs plates-formes, notamment Windows, macOS et Linux, et peut être intégré dans des applications grâce à une interface simple et des
fonctionnalités avancées telles que la détection de langage automatique, la segmentation de texte et la reconnaissance de mise en page.

3.3.2 Paddle_OCR
~~~~~~~~~~~~~~~~~~
PaddleOCR est un outil OCR (Reconnaissance Optique de Caractères) open-source développé par PaddlePaddle, un framework d'apprentissage profond développé par Baidu. PaddleOCR est conçu pour reconnaître
du texte à partir d'images et de documents en utilisant des techniques d'apprentissage profond. Il prend en charge différentes langues et fournit des modèles pré-entraînés pour différentes tâches
telles que la détection de texte de scène, la reconnaissance et le repérage de texte. PaddleOCR est reconnu pour sa précision, son efficacité et sa facilité d'utilisation, ce qui en fait un choix populaire
pour les développeurs et les chercheurs travaillant sur des projets liés à l'OCR. Il offre à la fois des outils en ligne de commande et des APIs Python pour une intégration dans diverses applications.

**Installation :**

.. code-block:: bash

    pip install "paddleocr>=2.0.1"  # Version recommandée 2.0.1+

**Les bibliothèques :**

.. code-block:: python

    import time
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt

**Fonction Plot Paddle :**

.. code-block:: python

    def Plot_Paddle(results, Image_path, Time, Threshold):
        image = cv2.imread(Image_path)

        # Annoter l'image avec le texte reconnu et la confiance
        for result in results:
            for box, text_info in result:
                text, confidence = text_info
                if confidence >= Threshold:
                    box = np.array(box, dtype=np.int32)
                    box = box.reshape((-1, 1, 2))
                    cv2.polylines(image, [box], isClosed=True, color=(0, 255, 0), thickness=2)
                    cv2.putText(image, f"{text} ", (box[0][0][0], box[0][0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    cv2.putText(image, f"{confidence:.2f} ", (box[0][0][0], box[0][0][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Afficher l'image annotée avec Matplotlib
        plt.figure(figsize=(16, 16))
        plt.imshow(image_rgb)
        plt.axis('off')
        plt.title(f"Paddle_OCR : {Time} secondes")
        plt.show()

.. code-block:: python

    def Run_Paddle(Image_path):
        ocr = PaddleOCR(use_angle_cls=True, lang='fr')  # Charger le modèle en mémoire
        start_time = time.time()
        results = ocr.ocr(Image_path, cls=True)
        end_time = time.time()
        Time = end_time - start_time
        return results, Time

.. code-block:: python

    results, Time = Run_Paddle('chemin/vers/votre/image.jpg')
    Plot_Paddle(results, 'chemin/vers/votre/image.jpg', round(Time), 0.9)

3.3.3 docTR
~~~~~~~~~~~~~~~~~~

À propos de docTR (Document Text Recognition) - une bibliothèque fluide, performante et accessible pour les tâches liées à l'OCR, alimentée par l'apprentissage profond.

**Installation :**

.. code-block:: bash

    !pip install python-doctr
    !pip install "python-doctr[tf]"
    !pip install "python-doctr[torch]"

.. code-block:: bash

    !pip install tf2onnx

.. code-block:: python

    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor
    import time

    model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
    model.det_predictor.model.postprocessor.bin_thresh = 0.5
    model.det_predictor.model.postprocessor.box_thresh = 0.2

.. code-block:: python

    img = DocumentFile.from_images('facile.jpg')
    start_time = time.time()
    result = model(img)
    end_time = time.time()
    Time = end_time - start_time
    output = result.export()
    print(Time)

.. code-block:: python

    result.show()
    for obj1 in output['pages'][0]["blocks"]:
        for obj2 in obj1["lines"]:
            for obj3 in obj2["words"]:
                print("{}: {}".format(obj3["geometry"], obj3["value"]))
    Text = result.render()
    print(Text)

3.4 Comparaison entre les outils d'OCR
-----------------------------------------
Nous avons traité deux images, une image simple (bien scannée et tout est clair) et l'autre image est un peu complexe (image prise par caméra de téléphone, défauts d'orientation, etc.).

**Pour EasyOCR :**

* Temps de traitement de l'image : 49 secondes
* Précision : ne détecte pas tous les champs du texte
* Autres remarques : incapable de lire les accents (é, è), les cédilles (ç), etc.

**Pour PaddleOCR :**

* Temps de traitement de l'image : 2 secondes
* Précision : détecte tous les champs du texte
* Autres remarques : incapable de lire certains accents (é, è) et cédilles (ç).

**Pour docTR :**

* Temps de traitement de l'image : 25 secondes
* Précision : détecte tous les champs du texte
* Autres remarques : incapable de lire les accents (é, è) et cédilles (ç).

3.5 Choix de l'outil à utiliser
----------------------------------
Après avoir testé plusieurs outils d'OCR (EasyOCR, PaddleOCR, Keras_OCR, Pytesseract, docTR), nous avons choisi **PaddleOCR** en raison de sa puissance, de sa précision, de son efficacité pour traiter des images complexes et de son temps d'exécution optimal.

.. raw:: html

    <a href="https://colab.research.google.com/github/MasrourTawfik/Textra/blob/main/Notebooks/OCR_Bench.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
