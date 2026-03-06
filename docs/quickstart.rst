==================
Démarrage Rapide
==================

Ce guide vous permet de lancer l'application en **2 minutes** chrono ! ⏱️

Prérequis
=========

✅ Docker Desktop installé et démarré  
✅ Git installé

.. note::
   Python et uv ne sont **pas obligatoires** pour simplement lancer l'application.
   Ils sont nécessaires uniquement pour le développement local ou lancer les tests.

Installation Express
====================

.. code-block:: bash

   # 1. Cloner le projet
   git clone https://github.com/Roxiina/Projet-2.git
   cd Projet-2

   # 2. Créer le fichier d'environnement
   cp .env.example .env

   # 3. Lancer l'application
   docker-compose up -d

   # 4. Attendre que les services soient prêts (1-2 min)
   docker-compose ps

.. note::
   **Première exécution** : Le démarrage prend 1-2 minutes car Docker doit construire les images.
   Les démarrages suivants seront beaucoup plus rapides !

Vérification
============

Une fois tous les conteneurs avec le statut ``healthy`` :

* **Frontend Streamlit** : http://localhost:8501
* **API FastAPI** : http://localhost:8000
* **Documentation API** : http://localhost:8000/docs

Test Rapide
===========

Pour vérifier que tout fonctionne correctement :

1. Ouvrez http://localhost:8501 dans votre navigateur
2. Dans la barre latérale, cliquez sur **"0_insert"**
3. Entrez les valeurs suivantes :
   
   * **Valeur** : ``42``
   * **Description** : ``Test rapide``

4. Cliquez sur le bouton **"💾 Enregistrer"**
5. Vous devriez voir un message de confirmation ✅
6. Allez sur la page **"1_read"** dans la barre latérale
7. Vérifiez que votre donnée apparaît dans le tableau

.. tip::
   Testez la persistance : redémarrez les conteneurs avec ``docker-compose restart`` 
   et vérifiez que vos données sont toujours là !

Arrêt de l'Application
=======================

Pour arrêter tous les services :

.. code-block:: bash

   docker-compose down

.. warning::
   Pour supprimer aussi les volumes et les données (⚠️ perte de données) :
   
   .. code-block:: bash
   
      docker-compose down -v

Résolution de Problèmes
=======================

Si vous rencontrez des problèmes, voici quelques commandes utiles :

Vérifier les logs
-----------------

.. code-block:: bash

   # Logs de tous les services
   docker-compose logs -f
   
   # Logs d'un service spécifique
   docker-compose logs -f api

Redémarrer proprement
---------------------

.. code-block:: bash

   docker-compose down
   docker-compose up -d --build

Repartir de zéro
----------------

.. code-block:: bash

   # ⚠️ Attention : cela supprime les données !
   docker-compose down -v
   docker-compose up -d

Vérifier l'état des conteneurs
-------------------------------

.. code-block:: bash

   docker-compose ps

Installation pour le Développement
===================================

Si vous voulez développer localement sans Docker ou lancer les tests :

Installation de uv
------------------

**Windows (PowerShell)** :

.. code-block:: powershell

   irm https://astral.sh/uv/install.ps1 | iex

**Linux/macOS** :

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh

Lancer les tests
----------------

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ -v

Résultat attendu : **14 tests passed** ✅

Prochaines Étapes
=================

Maintenant que votre application est lancée, vous pouvez :

1. 🎨 **Explorer l'interface** Streamlit (insertion et lecture de données)
2. 📖 **Consulter la documentation API** interactive à http://localhost:8000/docs
3. 🧪 **Lancer les tests** unitaires (voir :doc:`testing/tests`)
4. 🏗️ **Comprendre l'architecture** microservices (voir :doc:`architecture/overview`)
5. 🚀 **Déployer en production** avec ``docker-compose.prod.yml`` (voir :doc:`deployment/production`)

Documentation Complète
======================

Pour une utilisation plus avancée, consultez :

* :doc:`installation` - Installation détaillée pour le développement
* :doc:`architecture/overview` - Comprendre l'architecture du projet
* :doc:`deployment/docker` - Déploiement et orchestration Docker
* :doc:`testing/tests` - Tests et qualité du code
* :doc:`guides/troubleshooting` - Guide de dépannage

Ressources Externes
===================

* `README.md <https://github.com/Roxiina/Projet-2>`_ - Vue d'ensemble du projet
* `GitHub Pages <https://roxiina.github.io/Projet-2/>`_ - Documentation en ligne complète
* `Cahier des charges <https://github.com/Roxiina/Projet-2/blob/main/Projet_2_Orchestration.md>`_ - Spécifications du projet

