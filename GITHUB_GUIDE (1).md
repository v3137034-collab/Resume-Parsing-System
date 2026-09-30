# How to Push This Project to GitHub

## One-time setup
1. Install Git: https://git-scm.com/downloads
2. Create a free account at https://github.com
3. Tell Git who you are:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Step 1: Create the repository on GitHub
1. Click **+ > New repository**.
2. Name: `resume-parsing-system`
3. Description: `Resume parser with ATS score checker built in Python`
4. Choose **Public**.
5. Do **NOT** tick "Add README", ".gitignore" or "license" (the project already has them).
6. Click **Create repository**.

## Step 2: Push from your computer
Open a terminal inside the project folder:
```bash
git init
git add .
git commit -m "Initial commit: resume parser with ATS score checker"
git branch -M main
git remote add origin https://github.com/<your-username>/resume-parsing-system.git
git push -u origin main
```
If asked to log in, use your GitHub username and a **Personal Access Token**
(GitHub > Settings > Developer settings > Personal access tokens) instead of a password.

## Step 3: Make it look professional
- Add **Topics** on the repo page: `python`, `resume-parser`, `ats`, `nlp`, `college-project`.
- Replace `<your-username>` in README.md and `<Your Name>` in LICENSE.
- Add a screenshot of the terminal output in a `docs/` folder and link it in the README.

## Suggested commit history (looks good in viva / portfolio)
```bash
git commit -m "Add file reader for TXT, PDF and DOCX"
git commit -m "Add resume information extraction"
git commit -m "Add ATS scoring module"
git commit -m "Add CLI, sample data and unit tests"
git commit -m "Add documentation"
```
Tip: commit small changes often, using messages that start with a verb
(Add / Fix / Update / Remove).

## Everyday workflow after the first push
```bash
git status
git add .
git commit -m "Describe your change"
git push
```

## Branching (optional, for teams)
```bash
git checkout -b feature/streamlit-ui
# ...make changes...
git push -u origin feature/streamlit-ui
# then open a Pull Request on GitHub
```

## Common problems
| Problem | Fix |
|---|---|
| `remote origin already exists` | `git remote set-url origin <url>` |
| `failed to push, updates were rejected` | `git pull origin main --rebase` then push again |
| Authentication failed | Use a Personal Access Token, not your password |
| Personal resume uploaded by mistake | Remove it, add to `.gitignore`, and change any exposed details |
