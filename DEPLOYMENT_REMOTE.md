# Pushing to Remote Repository

## 1. GitHub

### Setup steps:

1. Create a new repository on [github.com](https://github.com/new)
   - Repository name: `resume-optimizer-saas` (or preferred name)
   - Do NOT initialize with README, .gitignore, or license

2. From your local repo:

```powershell
cd C:\Projects\Saas
git remote add origin https://github.com/YOUR_USERNAME/resume-optimizer-saas.git
git branch -M main
git push -u origin main
```

If using SSH keys instead:

```powershell
git remote add origin git@github.com:YOUR_USERNAME/resume-optimizer-saas.git
git branch -M main
git push -u origin main
```

---

## 2. GitLab

### Setup steps:

1. Create a new project on [gitlab.com](https://gitlab.com/projects/new)
   - Project name: `resume-optimizer-saas`
   - Do NOT initialize with README or .gitignore

2. From your local repo:

```powershell
cd C:\Projects\Saas
git remote add origin https://gitlab.com/YOUR_USERNAME/resume-optimizer-saas.git
git branch -M main
git push -u origin main
```

---

## 3. Self-hosted (Gitea, Gitea Cloud)

1. Create new repository in your Gitea instance

2. From your local repo:

```powershell
cd C:\Projects\Saas
git remote add origin https://your-gitea-instance.com/YOUR_USERNAME/resume-optimizer-saas.git
git branch -M main
git push -u origin main
```

---

## Verify push success

```powershell
cd C:\Projects\Saas
git remote -v
git log --oneline
```

Should show your remote URL and the commit history.

