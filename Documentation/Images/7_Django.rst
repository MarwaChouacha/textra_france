Introduction à Django et fichiers utilisés dans notre projet
===========================================================

Qu'est-ce que Django ?
----------------------

Django est un framework web open-source écrit en Python. Il permet de développer
rapidement des applications web robustes et sécurisées grâce à sa structure organisée.

Dans notre projet, Django nous a aidés à construire une application web qui permet
de charger des factures, d'extraire leur texte, de classifier les informations,
et de retourner les résultats à l'utilisateur.

Fichiers clés utilisés dans notre projet Django
-----------------------------------------------

Voici les fichiers principaux que nous avons utilisés, avec une explication simple de leur rôle :

1. **models.py**
   ~~~~~~~~~~~~~
   Ce fichier définit la structure des données que nous manipulons.
   Par exemple, il définit ce qu'est une "Facture" dans notre application, avec ses
   champs comme le texte extrait, la catégorie comptable, et le compte associé.

2. **views.py**
   ~~~~~~~~~~~~~
   C'est ici que se trouve la logique principale de notre application.
   Ce fichier contient les fonctions qui reçoivent les requêtes de l'utilisateur,
   exécutent les traitements (comme l'extraction du texte ou la classification),
   puis renvoient les réponses.

3. **urls.py**
   ~~~~~~~~~~~~
   Ce fichier relie les adresses web (URL) aux fonctions dans `views.py`.
   Par exemple, il définit qu'une requête vers `/extract/` doit appeler la fonction
   qui gère l'extraction et la classification.

4. **serializers.py**
   ~~~~~~~~~~~~~~~~~~~
   Il permet de transformer les objets Python (comme une facture) en format JSON
   pour que les données puissent être échangées via une API, et inversement.

5. **admin.py**
   ~~~~~~~~~~~~
   Ce fichier permet d'enregistrer les modèles (comme la facture) dans l'interface
   d'administration Django, facilitant ainsi la gestion des données via un panneau
   d'administration graphique.

Résumé du fonctionnement
------------------------

- L'utilisateur envoie une facture via l'interface web.
- La fonction dans `views.py` reçoit le fichier et utilise un module d'OCR pour extraire le texte.
- Le texte est ensuite analysé par nos modèles de classification pour déterminer les catégories comptables.
- Les résultats sont sauvegardés dans la base de données via les modèles définis dans `models.py`.
- Enfin, une réponse est renvoyée à l'utilisateur, souvent au format JSON, grâce aux serializers.

Cette architecture modulaire rend le code clair, maintenable, et facilite l’évolution
de l’application.

---

N'hésitez pas à me demander une version plus détaillée ou un schéma explicatif.
