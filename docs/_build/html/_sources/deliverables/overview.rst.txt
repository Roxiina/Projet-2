==================
Vue d'Ensemble
==================

Les trois livrables du Projet 2.

Livrable 1 : GitHub avec Badges
================================

Repository GitHub public avec :

* Code source complet
* README avec badges CI/CD
* Workflows GitHub Actions
* Documentation complète

**URL** : https://github.com/Roxiina/Projet-2

Livrable 2 : docker-compose.prod.yml
=====================================

Fichier Docker Compose pour la production utilisant des images DockerHub.

**Emplacement** : ``docker-compose.prod.yml``

Caractéristiques :

* Images depuis DockerHub (roxiina/projet-2-api:latest, roxiina/projet-2-front:latest)
* Configuration production-ready
* Health checks configurés

Livrable 3 : Gitleaks Actif
============================

Workflow de sécurité avec Gitleaks pour détecter les secrets.

**Emplacement** : ``.github/workflows/security.yml``

Fonctionnalités :

* Scan automatique sur push et PR
* Configuration dans ``.gitleaks.toml``
* Exécution dans le pipeline CI/CD
