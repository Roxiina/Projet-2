==================
Production
==================

Guide de déploiement en production.

Prérequis
=========

* Serveur Linux (Ubuntu 22.04 recommandé)
* Docker et Docker Compose installés
* Domaine avec DNS configuré
* Certificats SSL/TLS

Déploiement
===========

1. Cloner le projet :

.. code-block:: bash

   git clone https://github.com/Roxiina/Projet-2.git
   cd Projet-2

2. Configurer les variables d'environnement :

.. code-block:: bash

   cp .env.example .env
   nano .env

3. Lancer en production :

.. code-block:: bash

   docker-compose -f docker-compose.prod.yml up -d

Sécurité
========

* Utiliser des mots de passe forts
* Activer HTTPS avec Let's Encrypt
* Configurer un firewall
* Limiter l'accès SSH

Monitoring
==========

Surveiller les logs :

.. code-block:: bash

   docker-compose logs -f

Backup
======

Sauvegarder régulièrement la base de données :

.. code-block:: bash

   docker-compose exec db pg_dump -U projet2_user projet2_db > backup.sql
