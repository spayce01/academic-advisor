# Setup Guide: ticking every box

## ✅ 1. Install Git
* **Windows:** download from https://git-scm.com/download/win (or `winget install --id Git.Git -e`)
* **macOS:** `brew install git` (or `xcode-select --install`)
* **Linux:** `sudo apt install git`

Verify and configure:
```bash
git --version
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## ✅ 2. GitHub account + tooling
1. Create an account at https://github.com
2. Install the GitHub CLI: `winget install GitHub.cli` / `brew install gh` / `sudo apt install gh`
3. Log in: `gh auth login` (choose GitHub.com → HTTPS → browser login)
4. Verify: `gh auth status`

## ✅ 3. Create the repository and push
From inside the project folder (it already contains one local commit):
```bash
gh repo create academic-advisor --public --source=. --remote=origin --push
```
Manual alternative: create an empty repo on github.com, then
```bash
git remote add origin https://github.com/<your-username>/academic-advisor.git
git push -u origin main
```
Good habit: work on branches → open Pull Requests → CI must pass before merging.
```bash
git checkout -b feature/improve-advice
# edit, test
git add -A && git commit -m "feat: add advice for low credit load"
git push -u origin feature/improve-advice
gh pr create --fill
```

## ✅ 4. Python-optimised VS Code
1. Install VS Code: https://code.visualstudio.com and Python 3.11+ from https://python.org
2. Open the folder: `code .`. VS Code will offer the recommended extensions from `.vscode/extensions.json`
   (Python, Pylance, Jupyter, Ruff, GitLens, GitHub PRs). Click **Install All**.
3. Create the environment: `Ctrl+Shift+P` → *Python: Create Environment* → Venv → select `requirements-dev.txt`.
4. Pre-configured in `.vscode/settings.json`: Ruff format/lint on save, pytest integration (Testing panel 🧪),
   interpreter set to `.venv`. Press **F5** to launch the Flask app with the debugger (`launch.json`).

## ✅ 5. Build the model on Google Colab
1. Go to https://colab.research.google.com → *File ▸ Upload notebook* → `notebooks/train_model_colab.ipynb`
   (or *File ▸ Open notebook ▸ GitHub* and paste your repo URL).
2. *Runtime ▸ Run all*. The last cell downloads `advisor_model.pkl`.
3. Move the file to `models/advisor_model.pkl`, then:
```bash
pytest -v
git add models/advisor_model.pkl && git commit -m "model: retrain in Colab" && git push
```

## ✅ 6. Deploy the .pkl and test it on the web app
```bash
python -m flask --app "app.main:create_app" run
```
* Browser: http://127.0.0.1:5000, fill the form and click **Get advice**.
* Terminal: `curl -X POST localhost:5000/api/advise -H "Content-Type: application/json" -d '{...}'`
* Automated: `pytest -v` (10 tests: data, rules, model, validation, pages, API, error handling).

**Optional public hosting** (free tiers of Render / Railway / Hugging Face Spaces): connect the GitHub repo,
build command `pip install -r requirements.txt`, start command `gunicorn "app.main:create_app()"` (see `Procfile`).
