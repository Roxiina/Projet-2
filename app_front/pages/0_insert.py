"""Page pour insérer des données."""

import os

import requests
import streamlit as st

st.set_page_config(page_title="Insérer des Données", page_icon="🔢")

st.title("🔢 Insérer des Données")

# Récupérer l'URL de l'API depuis les variables d'environnement
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.markdown(f"""
Cette page permet d'ajouter de nouvelles données dans la base de données.

**API utilisée** : `{API_URL}`
""")

# Formulaire pour saisir les données
with st.form("insert_form"):
    st.subheader("Nouvelle Donnée")

    value = st.number_input(
        "Valeur numérique",
        min_value=-1000000.0,
        max_value=1000000.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Entrez une valeur numérique",
    )

    description = st.text_area(
        "Description (optionnelle)", max_chars=500, help="Ajoutez une description pour cette valeur"
    )

    submitted = st.form_submit_button("💾 Enregistrer", use_container_width=True)

    if submitted:
        # Préparer les données
        data = {"value": value, "description": description if description else None}

        # Envoyer à l'API
        try:
            with st.spinner("Envoi des données..."):
                response = requests.post(f"{API_URL}/data", json=data, timeout=5)

                if response.status_code == 201:
                    result = response.json()
                    st.success("✅ Données enregistrées avec succès !")

                    # Afficher les détails
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ID", result["id"])
                    with col2:
                        st.metric("Valeur", f"{result['value']:.2f}")
                    with col3:
                        st.info(f"📅 {result['created_at'][:10]}")

                    if result.get("description"):
                        st.info(f"📝 Description : {result['description']}")

                    # Message de confirmation
                    st.balloons()
                else:
                    st.error(f"❌ Erreur {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(f"❌ Impossible de se connecter à l'API ({API_URL})")
            st.info("💡 Assurez-vous que l'API est en cours d'exécution")
        except requests.exceptions.Timeout:
            st.error("⏱️ Délai d'attente dépassé")
        except Exception as e:
            st.error(f"❌ Erreur inattendue : {str(e)}")

# Section d'aide
with st.expander("ℹ️ Aide"):
    st.markdown("""
    ### Comment utiliser cette page ?
    
    1. **Valeur numérique** : Entrez le nombre que vous souhaitez enregistrer
    2. **Description** : Ajoutez une description (optionnel) pour comprendre la valeur
    3. **Enregistrer** : Cliquez sur le bouton pour sauvegarder
    
    ### Exemples de données :
    
    - Valeur : `42.5` | Description : "Température moyenne"
    - Valeur : `100.0` | Description : "Score du test"
    - Valeur : `-5.3` | Description : "Delta de variation"
    """)

# Vérifier la connexion à l'API
try:
    health_response = requests.get(f"{API_URL}/health", timeout=2)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API connectée")
    else:
        st.sidebar.warning("⚠️ API accessible mais problème")
except:
    st.sidebar.error("❌ API non accessible")
