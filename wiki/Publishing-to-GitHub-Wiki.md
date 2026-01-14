# Publishing to GitHub Wiki

GitHub Wikis are backed by a separate git repository (`<repo>.wiki.git`). This project keeps wiki sources in the `wiki/` folder so you can generate/update pages locally, then push them to the wiki repo.

## If You See 'Repository not found'

That usually means one of these is true:
- The wiki feature is disabled in the main repo settings.
- The wiki repo exists, but you don't have access (private repo / auth required).

Fix:
- Enable Wikis in the repository settings (GitHub UI).
- Create the first wiki page in the GitHub UI (this initializes the wiki git repo).
- Then clone/push again. For private repos, use an authenticated remote (PAT) or SSH.

## One-Time Setup

```bash
git clone https://github.com/CrystalDustt-V2/toolbox.wiki.git
```

## Publish / Update

```bash
python tools/generate_github_wiki.py --out wiki
cd toolbox.wiki
git rm -r --ignore-unmatch .
cp -r ../wiki/* .
git add -A
git commit -m "Update wiki"
git push
```

## Windows PowerShell Variant

```powershell
python tools/generate_github_wiki.py --out wiki
cd toolbox.wiki
git rm -r --ignore-unmatch .
Copy-Item -Recurse -Force ..\wiki\* .
git add -A
git commit -m "Update wiki"
git push
```
