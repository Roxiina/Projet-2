# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## Comment contribuer ?

### 1. Fork et Clone

1. Forkez le projet sur GitHub
2. Clonez votre fork localement :
```bash
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO
```

### 2. Créez une branche

Créez une branche pour votre fonctionnalité ou correction :
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

### 3. Développez

- Suivez les conventions de code du projet
- Écrivez des tests pour vos modifications
- Assurez-vous que tous les tests passent
- Utilisez Ruff pour le linting

### 4. Testez

```bash
# Tests de l'API
uv run --directory ./app_api pytest ../tests/ -v

# Linting
cd app_api
uv run ruff check .
```

### 5. Committez

Utilisez des messages de commit clairs :
```bash
git add .
git commit -m "feat: Ajout de la fonctionnalité X"
```

Types de commits recommandés :
- `feat:` : Nouvelle fonctionnalité
- `fix:` : Correction de bug
- `docs:` : Documentation
- `style:` : Formatage, points-virgules manquants, etc.
- `refactor:` : Refactoring du code
- `test:` : Ajout de tests
- `chore:` : Mise à jour des tâches de build, etc.

### 6. Pushez et créez une Pull Request

```bash
git push origin feature/ma-nouvelle-fonctionnalite
```

Puis créez une Pull Request sur GitHub.

## Standards de Code

### Python

- Python 3.11+
- Type hints autant que possible
- Docstrings pour les fonctions et classes
- Conformité avec Ruff

### Docker

- Images légères (alpine quand possible)
- Multi-stage builds si nécessaire
- `.dockerignore` à jour

### Tests

- Minimum 80% de couverture
- Tests unitaires et d'intégration
- Noms de tests descriptifs

## Structure des Pull Requests

Une bonne PR contient :

1. **Titre clair** : Résumé de la modification
2. **Description** : Explication détaillée
3. **Tests** : Preuve que ça fonctionne
4. **Documentation** : Mise à jour si nécessaire

## Questions ?

N'hésitez pas à ouvrir une issue pour discuter avant de commencer un gros changement.

## Code de Conduite

Veuillez lire notre [Code de Conduite](CODE_OF_CONDUCT.md) avant de contribuer.
