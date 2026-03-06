# 🚀 Démarrage Rapide (2 minutes)

## Prérequis

✅ Docker Desktop installé et démarré  
✅ Git installé

## Installation Express

```bash
# 1. Cloner le projet
git clone https://github.com/Roxiina/Projet-2.git
cd Projet-2

# 2. Créer le fichier d'environnement
cp .env.example .env

# 3. Lancer l'application
docker-compose up -d

# 4. Attendre que les services soient prêts (1-2 min)
docker-compose ps
```

## ✅ Vérification

Une fois tous les conteneurs `healthy` :

- **Frontend** : http://localhost:8501
- **API** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs

## 🧪 Test Rapide

1. Ouvrez http://localhost:8501
2. Allez sur la page **"0_insert"**
3. Entrez :
   - Valeur : `42`
   - Description : `Test rapide`
4. Cliquez sur **"💾 Enregistrer"**
5. Allez sur la page **"1_read"**
6. Vérifiez que votre donnée apparaît ✅

## 🛑 Arrêt

```bash
docker-compose down
```

## 📚 Documentation Complète

- **README.md** : Architecture, CI/CD, structure du projet
- **docs/** : Documentation Sphinx détaillée
- **GitHub Pages** : https://roxiina.github.io/Projet-2/

## ⚠️ Problèmes ?

```bash
# Vérifier les logs
docker-compose logs -f

# Redémarrer proprement
docker-compose down
docker-compose up -d --build

# Supprimer les volumes et recommencer (⚠️ perte de données)
docker-compose down -v
docker-compose up -d
```

## 🎯 Pour aller plus loin

- Lire le [README.md](README.md) complet
- Consulter la [documentation](https://roxiina.github.io/Projet-2/)
- Voir le [cahier des charges](Projet_2_Orchestration.md)
