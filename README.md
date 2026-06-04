<div align="center">

# 📊 DevPulse

**GitHub Portfolio Dashboard & Dynamic SVG Stats Badge Generator.**

[![Vercel Deploy](https://img.shields.io/badge/Vercel-Deploy-000000?logo=vercel&logoColor=white)](https://vercel.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

</div>

---

## ✨ Features

- **Dynamic SVG Generator**: Serves custom SVG metrics image cards at `/api/stats?username=yourname` loaded with real-time statistics (stars, forks, repositories, followers, and language percentages).
- **Beautiful Web Interface**: A glassmorphic dark-mode portfolio dashboard where users can query stats, configure themes, and preview badges.
- **Visual Design Themes**: Supports `dark` (GitHub default dark), `light` (GitHub default light), `cyber` (cyberpunk cyan), and `neon` (neon magenta) card layouts.
- **Embedded Caching**: Built-in 4-hour server HTTP caching (`Cache-Control`) to bypass GitHub API rate limit constraints.

---

## 🚀 One-Click Deploy to Vercel

You can deploy this widget platform to Vercel in one click. Vercel automatically deploys the static dashboard pages and maps the Python serverless API functions to `/api/stats`.

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/devpulse&env=GITHUB_TOKEN&envDescription=GITHUB_TOKEN+is+optional+but+recommended+to+prevent+GitHub+API+rate+limiting.+Get+from+Settings+->+Developer+Settings.&project-name=devpulse&repository-name=devpulse)

---

## 🛠️ Local Installation

```bash
git clone https://github.com/Lord1Egypt/devpulse.git
cd devpulse
pip install -r requirements.txt
```

### Running Serverless Local API
To test the serverless SVG generator locally, run a Flask dev server:
```bash
export GITHUB_TOKEN="your_optional_github_token_here"
python -m flask --app api/stats run --port 5000
```
Open your browser and navigate to:
`http://localhost:5000/api/stats?username=Lord1Egypt&theme=cyber`

---

## ⚙️ SVG Endpoint API Configuration

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | String | **Yes** | Your GitHub handle (e.g. `Lord1Egypt`). |
| `theme` | String | No | Color theme: `dark` (default), `light`, `cyber`, `neon`. |

---

<div align="center">

Made with ❤️ by [Lord1Egypt](https://github.com/Lord1Egypt)

⭐ Star this repo if you find it useful!

</div>
