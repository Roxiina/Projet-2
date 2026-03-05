# Frontend Streamlit

Interface utilisateur développée avec Streamlit pour interagir avec l'API.

## 🚀 Démarrage

### Avec uv (recommandé)

```bash
# Installation des dépendances
uv sync

# Lancement
export API_URL=http://localhost:8000  # ou set API_URL=... sur Windows
uv run streamlit run main.py
```

### Avec pip

```bash
pip install -r requirements.txt
streamlit run main.py
```

L'application sera accessible sur http://localhost:8501

## 📱 Pages

### Page d'Accueil (main.py)
Présentation de l'application et instructions

### Page 0 - Insert (0_insert.py)
- Formulaire de saisie de données
- Validation des entrées
- Envoi vers l'API
- Confirmation visuelle

### Page 1 - Read (1_read.py)
- Affichage des données en tableau
- Vue en cartes
- Vue détaillée
- Statistiques
- Export CSV
- Pagination

## 🎨 Fonctionnalités

- ✅ Interface intuitive et moderne
- 📊 Visualisation des données en temps réel
- 🔄 Rafraîchissement manuel
- 📥 Export des données en CSV
- 📈 Statistiques en temps réel
- 🎯 Health check de l'API
- 🔍 Pagination des résultats

## 📁 Structure

```
app_front/
├── pages/
│   ├── 0_insert.py     # Page d'insertion
│   └── 1_read.py       # Page de lecture
├── .streamlit/
│   └── config.toml     # Configuration Streamlit
├── main.py             # Page d'accueil
├── Dockerfile
└── pyproject.toml
```

## 🔧 Configuration

Variables d'environnement :
```
API_URL=http://localhost:8000
```

Configuration Streamlit dans `.streamlit/config.toml`

## 🐳 Docker

```bash
# Build
docker build -t app-front .

# Run
docker run -p 8501:8501 -e API_URL=http://api:8000 app-front
```

## 🎯 Utilisation

1. **Insérer des données** :
   - Cliquez sur "Insert" dans la sidebar
   - Entrez une valeur numérique
   - Ajoutez une description (optionnel)
   - Cliquez sur "Enregistrer"

2. **Visualiser les données** :
   - Cliquez sur "Read" dans la sidebar
   - Choisissez le mode d'affichage
   - Utilisez les filtres et pagination
   - Téléchargez les données en CSV si besoin

## 🎨 Personnalisation

Modifiez `.streamlit/config.toml` pour personnaliser :
- Couleurs du thème
- Port du serveur
- Options de navigation
