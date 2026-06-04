import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# Basic SVG themes mapping
THEMES = {
    "dark": {
        "bg_start": "#0d1117",
        "bg_end": "#161b22",
        "border": "#30363d",
        "text_primary": "#58a6ff",
        "text_secondary": "#8b949e",
        "stat_val": "#f0f6fc",
        "icon": "#58a6ff"
    },
    "light": {
        "bg_start": "#ffffff",
        "bg_end": "#f6f8fa",
        "border": "#d0d7de",
        "text_primary": "#0969da",
        "text_secondary": "#57606a",
        "stat_val": "#24292f",
        "icon": "#0969da"
    },
    "cyber": {
        "bg_start": "#0b0c10",
        "bg_end": "#1f2833",
        "border": "#66fcf1",
        "text_primary": "#66fcf1",
        "text_secondary": "#c5c6c7",
        "stat_val": "#45f3ff",
        "icon": "#66fcf1"
    },
    "neon": {
        "bg_start": "#120136",
        "bg_end": "#03001e",
        "border": "#ff007f",
        "text_primary": "#00f0ff",
        "text_secondary": "#ea00d9",
        "stat_val": "#ffffff",
        "icon": "#00f0ff"
    }
}

def make_error_svg(message: str) -> str:
    """Return a clean fallback SVG in case of errors."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="150" viewBox="0 0 400 150">
        <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#b62324" stroke-width="1.5"/>
        <text x="50%" y="45%" dominant-baseline="middle" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="16" fill="#f85149" font-weight="bold">⚠️ DevPulse Service Error</text>
        <text x="50%" y="65%" dominant-baseline="middle" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="12" fill="#8b949e">{message}</text>
    </svg>"""

def generate_svg(username: str, profile: dict, repos: list, theme_name: str) -> str:
    theme = THEMES.get(theme_name, THEMES["dark"])
    
    # Calculate stats
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    total_repos = profile.get("public_repos", 0)
    followers = profile.get("followers", 0)
    
    # Language stats
    langs = {}
    for r in repos:
        lang = r.get("language")
        if lang:
            langs[lang] = langs.get(lang, 0) + 1
            
    sorted_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:3]
    total_lang_repos = sum(count for _, count in sorted_langs) if sorted_langs else 1
    
    # Build language progress indicators
    lang_elements = ""
    y_pos = 120
    colors = ["#f1e05a", "#3572A5", "#f34b7d", "#b07219", "#89e051"]
    
    for idx, (lang, count) in enumerate(sorted_langs):
        pct = int((count / total_lang_repos) * 100)
        color = colors[idx % len(colors)]
        lang_elements += f"""
        <text x="25" y="{y_pos}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="12" fill="{theme['text_secondary']}" font-weight="600">{lang}</text>
        <text x="120" y="{y_pos}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="12" fill="{theme['stat_val']}" font-weight="bold">{pct}%</text>
        <rect x="160" y="{y_pos - 9}" width="200" height="7" rx="3.5" fill="{theme['border']}"/>
        <rect x="160" y="{y_pos - 9}" width="{int(2 * pct)}" height="7" rx="3.5" fill="{color}"/>
        """
        y_pos += 22

    height = 200 if sorted_langs else 140
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="450" height="{height}" viewBox="0 0 450 {height}">
        <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{theme['bg_start']}"/>
                <stop offset="100%" stop-color="{theme['bg_end']}"/>
            </linearGradient>
        </defs>
        
        <!-- Background Panel -->
        <rect width="100%" height="100%" rx="12" fill="url(#bg)" stroke="{theme['border']}" stroke-width="1.5"/>
        
        <!-- Header -->
        <g transform="translate(25, 35)">
            <text x="0" y="0" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="18" fill="{theme['text_primary']}" font-weight="bold">{profile.get('name') or username}</text>
            <text x="0" y="18" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="12" fill="{theme['text_secondary']}">@{username} &middot; GitHub Pulse</text>
        </g>
        
        <!-- Metrics -->
        <g transform="translate(25, 75)">
            <!-- Repos -->
            <text x="0" y="0" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="10" fill="{theme['text_secondary']}" font-weight="bold" letter-spacing="1">REPOS</text>
            <text x="0" y="20" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="18" fill="{theme['stat_val']}" font-weight="bold">{total_repos}</text>
            
            <!-- Stars -->
            <text x="110" y="0" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="10" fill="{theme['text_secondary']}" font-weight="bold" letter-spacing="1">STARS</text>
            <text x="110" y="20" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="18" fill="{theme['stat_val']}" font-weight="bold">{total_stars}</text>
            
            <!-- Forks -->
            <text x="210" y="0" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="10" fill="{theme['text_secondary']}" font-weight="bold" letter-spacing="1">FORKS</text>
            <text x="210" y="20" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="18" fill="{theme['stat_val']}" font-weight="bold">{total_forks}</text>
            
            <!-- Followers -->
            <text x="310" y="0" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="10" fill="{theme['text_secondary']}" font-weight="bold" letter-spacing="1">FOLLOWERS</text>
            <text x="310" y="20" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="18" fill="{theme['stat_val']}" font-weight="bold">{followers}</text>
        </g>
        
        <!-- Divider -->
        {f'<line x1="25" y1="105" x2="425" y2="105" stroke="{theme["border"]}" stroke-dasharray="2 2" stroke-width="1"/>' if sorted_langs else ''}
        
        <!-- Languages section -->
        {lang_elements}
    </svg>"""
    return svg

@app.route("/api/stats")
def stats_api():
    username = request.args.get("username", "").strip()
    theme = request.args.get("theme", "dark").strip().lower()
    
    if not username:
        return Response(make_error_svg("Missing username query param (?username=yourname)"), mimetype="image/svg+xml")
        
    headers = {"User-Agent": "DevPulse-Widget"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        # Fetch profile
        p_res = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=10)
        if p_res.status_code == 403:
            return Response(make_error_svg("GitHub API rate limit hit. Deploy with GITHUB_TOKEN."), mimetype="image/svg+xml")
        elif p_res.status_code == 404:
            return Response(make_error_svg(f"User '{username}' not found."), mimetype="image/svg+xml")
        elif p_res.status_code != 200:
            return Response(make_error_svg(f"GitHub Error: {p_res.status_code}"), mimetype="image/svg+xml")
            
        profile = p_res.json()
        
        # Fetch repos
        r_res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers, timeout=10)
        repos = r_res.json() if r_res.status_code == 200 else []
        
        svg_content = generate_svg(username, profile, repos, theme)
        
        # Return SVG with 4-hour caching to optimize loading
        res = Response(svg_content, mimetype="image/svg+xml")
        res.headers["Cache-Control"] = "public, max-age=14400, s-maxage=14400"
        return res
        
    except Exception as e:
        return Response(make_error_svg(str(e)), mimetype="image/svg+xml")

# Required for Vercel
handler = app
