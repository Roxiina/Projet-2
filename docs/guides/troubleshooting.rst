===============
Troubleshooting
===============

Guide de dépannage des problèmes courants.

Docker Desktop n'est pas démarré
=================================

**Erreur** : ``error during connect``

**Solution** : Démarrer Docker Desktop manuellement.

Port déjà utilisé
=================

**Erreur** : ``port is already allocated``

**Solution** :

.. code-block:: bash

   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   
   # Linux
   lsof -ti:8501 | xargs kill -9

Tests échouent
==============

**Solution** :

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ -v

Service unhealthy
=================

**Solution** : Vérifier les logs :

.. code-block:: bash

   docker-compose logs api
