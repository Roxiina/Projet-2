# Configuration GitHub Secrets

Pour que le workflow CD fonctionne correctement, vous devez configurer les secrets suivants dans votre repository GitHub.

## 📝 Comment ajouter des secrets

1. Allez dans votre repository GitHub
2. Cliquez sur **Settings** (Paramètres)
3. Dans le menu latéral, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**
5. Ajoutez chaque secret listé ci-dessous

## 🔑 Secrets requis

### DOCKERHUB_USERNAME
- **Description** : Votre nom d'utilisateur DockerHub
- **Exemple** : `monusername`
- **Comment l'obtenir** : C'est votre nom d'utilisateur Docker Hub (https://hub.docker.com/)

### DOCKERHUB_TOKEN
- **Description** : Token d'accès DockerHub (pas votre mot de passe!)
- **Comment l'obtenir** :
  1. Connectez-vous sur https://hub.docker.com/
  2. Allez dans **Account Settings** → **Security**
  3. Cliquez sur **New Access Token**
  4. Donnez un nom au token (ex: "GitHub Actions")
  5. Sélectionnez les permissions : **Read, Write, Delete**
  6. Copiez le token généré (vous ne pourrez plus le voir après)

### GITLEAKS_LICENSE (Optionnel)
- **Description** : Licence Gitleaks (optionnel, version gratuite disponible)
- **Comment l'obtenir** : Pas nécessaire pour la version gratuite de Gitleaks

## ✅ Vérification

Une fois les secrets ajoutés, vous devriez voir dans Settings → Secrets and variables → Actions :

```
✅ DOCKERHUB_USERNAME
✅ DOCKERHUB_TOKEN
```

## 🚀 Test

Pour tester que tout fonctionne :

1. Faites un commit sur la branche `main`
2. Vérifiez que le workflow CI passe au vert
3. Le workflow CD devrait se déclencher automatiquement
4. Vérifiez sur DockerHub que les images ont été publiées

## 🔒 Sécurité

⚠️ **Important** :
- Ne partagez JAMAIS vos tokens
- Ne commitez JAMAIS vos secrets dans le code
- Utilisez toujours des tokens, pas vos mots de passe
- Réveillez les tokens si vous pensez qu'ils ont été compromis

## 🛠️ Utilisation dans les workflows

Les secrets sont utilisés dans `.github/workflows/cd.yml` :

```yaml
- name: Login vers DockerHub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

Et dans `docker-compose.prod.yml` via variables d'environnement :

```yaml
image: ${DOCKERHUB_USERNAME}/app-api:latest
```

## 📚 Ressources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [DockerHub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [Docker Login Action](https://github.com/docker/login-action)
