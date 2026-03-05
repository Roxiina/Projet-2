============
Contributing
============

Guide de contribution au projet.

Comment Contribuer
==================

1. Forker le projet
2. Créer une branche (``git checkout -b feature/AmazingFeature``)
3. Commiter les changements (``git commit -m 'feat: Add AmazingFeature'``)
4. Pusher vers la branche (``git push origin feature/AmazingFeature``)
5. Ouvrir une Pull Request

Standards de Code
=================

* Utiliser Ruff pour le linting
* Écrire des tests pour les nouvelles fonctionnalités
* Suivre les conventions PEP 8
* Documenter le code

Tests
=====

Lancer les tests avant de soumettre :

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ -v

Linting
=======

Vérifier la qualité du code :

.. code-block:: bash

   cd app_api
   uv run ruff check .
