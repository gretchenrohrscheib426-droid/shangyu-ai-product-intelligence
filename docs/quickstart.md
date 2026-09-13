# Quick start: two different scopes

## This portfolio (free, offline checks)
Use Python 3.11+ and Node 22+. No model, crawler or MySQL credentials are needed. In the extracted directory:

```sh
python -m unittest discover -s tests -v
python scripts/check_release.py
npm run build
npm run dev
```

Open `<preview-origin>`/docs/assets/demo/public-demo.html. This is a static aggregate case summary, not a new research run or a replica of the original workbench. `npm run build` builds this document; it is **not a Vue application build**. No npm dependencies are needed. PowerShell equivalents: scripts/doctor.ps1, start.ps1, stop.ps1, test.ps1, check_secrets.ps1. Use -Node for start.ps1; doctor.ps1 and test.ps1 accept -Python and -Node when PATH is not configured. The preview origin is your loopback host on port 8765.

## Full platform (not bundled)
Obtain the [upstream](https://github.com/JxKim/sentiment_analysis_platform) under suitable rights and inspect its instructions. The local audited deployment used the original Vue 3 app at5173, FastAPI at5000 and MySQL on a loopback-only mapped port. Its two Python environments, crawler, fonts, model dependencies and .env are not reproduced by the documentation compose example.

To test an already authorized private checkout, run its frontend's existing `npm run build`, keeping artifacts private. This release does not claim that copying .env.example and running Docker starts the full platform. API keys remain blank; configure only in private storage. Never run new collection or paid calls in CI.
