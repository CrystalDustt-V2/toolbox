# Publishing to GitHub Wiki

GitHub Wikis are backed by a separate git repository (`<repo>.wiki.git`). This project keeps wiki sources in the `wiki/` folder so you can generate/update pages locally, then push them to the wiki repo.

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
