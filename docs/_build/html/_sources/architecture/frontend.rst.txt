====================
Frontend (Streamlit)
====================

Architecture du frontend Streamlit.

Structure du Frontend
=====================

.. code-block:: text

   app_front/
   ├── pages/               # Pages Streamlit
   │   ├── 0_insert.py     # Page d'insertion de données
   │   └── 1_read.py       # Page de lecture de données
   ├── main.py              # Page d'accueil
   ├── Dockerfile
   └── pyproject.toml

Architecture Multi-Pages
=========================

Streamlit utilise une **architecture multi-pages** automatique :

* ``main.py`` → Page d'accueil (``/``)
* ``pages/0_insert.py`` → Page d'insertion
* ``pages/1_read.py`` → Page de lecture

Page d'Accueil (main.py)
=========================

.. code-block:: python

   import streamlit as st
   
   st.set_page_config(
       page_title="Projet 2 - Accueil",
       page_icon="🏠",
       layout="wide"
   )
   
   st.title("🏠 Bienvenue sur l'Application Projet 2")
   
   st.markdown("""
   Cette application permet de gérer des données via une API FastAPI.
   
   ### Fonctionnalités
   
   * 📝 **Insertion** : Ajouter de nouvelles données
   * 📊 **Lecture** : Visualiser les données existantes
   
   ### Navigation
   
   Utilisez le menu latéral pour naviguer entre les pages.
   """)

Page d'Insertion (pages/0_insert.py)
=====================================

Cette page permet d'ajouter des données via l'API.

.. code-block:: python

   import streamlit as st
   import requests
   import os
   
   API_URL = os.getenv("API_URL", "http://localhost:8000")
   
   st.set_page_config(
       page_title="Insertion de données",
       page_icon="📝"
   )
   
   st.title("📝 Insertion de Données")
   
   # Formulaire
   with st.form("insert_form"):
       name = st.text_input("Nom", placeholder="Alice")
       value = st.number_input("Valeur", min_value=0, value=0, step=1)
       description = st.text_area("Description (optionnel)", placeholder="Description...")
       
       submitted = st.form_submit_button("Ajouter")
       
       if submitted:
           if not name:
               st.error("Le nom est obligatoire")
           else:
               payload = {
                   "name": name,
                   "value": value,
                   "description": description if description else None
               }
               
               try:
                   response = requests.post(f"{API_URL}/data", json=payload)
                   
                   if response.status_code == 201:
                       st.success("✅ Donnée ajoutée avec succès !")
                       st.json(response.json())
                   else:
                       st.error(f"❌ Erreur : {response.status_code}")
                       st.json(response.json())
               
               except requests.exceptions.ConnectionError:
                   st.error("❌ Impossible de se connecter à l'API")

Page de Lecture (pages/1_read.py)
==================================

Cette page affiche les données sous forme de tableau.

.. code-block:: python

   import streamlit as st
   import requests
   import pandas as pd
   import os
   
   API_URL = os.getenv("API_URL", "http://localhost:8000")
   
   st.set_page_config(
       page_title="Lecture des données",
       page_icon="📊",
       layout="wide"
   )
   
   st.title("📊 Lecture des Données")
   
   # Bouton de rafraîchissement
   if st.button("🔄 Rafraîchir"):
       st.rerun()
   
   # Récupération des données
   try:
       response = requests.get(f"{API_URL}/data")
       
       if response.status_code == 200:
           data = response.json()
           
           if data:
               df = pd.DataFrame(data)
               
               st.dataframe(
                   df,
                   use_container_width=True,
                   hide_index=True
               )
               
               st.metric("Total", len(data))
           else:
               st.info("Aucune donnée disponible")
       else:
           st.error(f"Erreur : {response.status_code}")
   
   except requests.exceptions.ConnectionError:
       st.error("❌ Impossible de se connecter à l'API")

Communication avec l'API
=========================

Le frontend communique avec le backend via HTTP/REST :

.. code-block:: python

   import requests
   import os
   
   API_URL = os.getenv("API_URL", "http://api:8000")  # Dans Docker
   # API_URL = "http://localhost:8000"  # En local

Opérations API
--------------

**POST - Créer une donnée** :

.. code-block:: python

   payload = {"name": "Alice", "value": 42, "description": "Test"}
   response = requests.post(f"{API_URL}/data", json=payload)
   
   if response.status_code == 201:
       data = response.json()
       print(data)  # {"id": 1, "name": "Alice", ...}

**GET - Récupérer les données** :

.. code-block:: python

   response = requests.get(f"{API_URL}/data")
   
   if response.status_code == 200:
       data = response.json()
       # data est une liste de dictionnaires

Gestion des Erreurs
-------------------

.. code-block:: python

   try:
       response = requests.get(f"{API_URL}/data", timeout=5)
       response.raise_for_status()  # Lève une exception si 4xx/5xx
       data = response.json()
   
   except requests.exceptions.ConnectionError:
       st.error("Impossible de se connecter à l'API")
   
   except requests.exceptions.Timeout:
       st.error("La requête a expiré")
   
   except requests.exceptions.HTTPError as e:
       st.error(f"Erreur HTTP : {e}")

Customisation de l'Interface
=============================

Configuration de la Page
-------------------------

.. code-block:: python

   st.set_page_config(
       page_title="Mon Application",
       page_icon="🚀",
       layout="wide",           # ou "centered"
       initial_sidebar_state="expanded"  # ou "collapsed"
   )

Thème
-----

Créer un fichier ``.streamlit/config.toml`` :

.. code-block:: toml

   [theme]
   primaryColor = "#0066cc"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   font = "sans serif"

Widgets Streamlit
=================

Formulaires
-----------

.. code-block:: python

   with st.form("my_form"):
       name = st.text_input("Nom")
       age = st.number_input("Âge", min_value=0)
       submitted = st.form_submit_button("Soumettre")
       
       if submitted:
           st.success(f"Bonjour {name}, {age} ans")

Tableaux de Données
--------------------

.. code-block:: python

   import pandas as pd
   
   df = pd.DataFrame([...])
   
   # Tableau interactif
   st.dataframe(df, use_container_width=True)
   
   # Tableau statique
   st.table(df)

Métriques
---------

.. code-block:: python

   st.metric(label="Total", value=42, delta="+5")

Graphiques
----------

.. code-block:: python

   import pandas as pd
   
   df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
   
   st.line_chart(df)
   st.bar_chart(df)
   st.area_chart(df)

Messages
--------

.. code-block:: python

   st.success("✅ Succès !")
   st.error("❌ Erreur")
   st.warning("⚠️ Attention")
   st.info("ℹ️ Information")

État de Session
===============

Streamlit maintient un état entre les reruns :

.. code-block:: python

   if "counter" not in st.session_state:
       st.session_state.counter = 0
   
   if st.button("Incrémenter"):
       st.session_state.counter += 1
   
   st.write(f"Compteur : {st.session_state.counter}")

Deployment
==========

Variables d'Environnement
--------------------------

.. code-block:: bash

   # Dans .env
   API_URL=http://api:8000
   STREAMLIT_PORT=8501

Configuration Docker
--------------------

.. code-block:: dockerfile

   FROM python:3.11-slim
   
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   
   WORKDIR /app
   
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-dev
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["uv", "run", "streamlit", "run", "main.py", \
        "--server.port", "8501", \
        "--server.address", "0.0.0.0"]

Prochaines Sections
===================

* :doc:`database` : Schéma de la base de données
* :doc:`../testing/tests` : Tests du frontend
