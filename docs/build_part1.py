"""Part 1: Generate CSS + Header + Hero for docs/index.html"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #FAFBFE; --card: #FFFFFF; --text: #1E293B; --text2: #475569;
  --text3: #94A3B8; --border: #E2E8F0; --accent: #4F46E5;
  --accent2: #7C3AED; --green: #059669; --red: #DC2626;
  --blue: #2563EB; --orange: #D97706;
  --gradient: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #2563EB 100%);
  --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05);
  --radius: 12px;
}

* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); line-height:1.7; }

/* NAV */
.nav { position:fixed; top:0; left:0; right:0; z-index:100; background:rgba(255,255,255,0.85);
  backdrop-filter:blur(20px); border-bottom:1px solid var(--border); padding:0 2rem; }
.nav-inner { max-width:1200px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:64px; }
.nav-logo { font-weight:800; font-size:1.25rem; background:var(--gradient); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.nav-links { display:flex; gap:1.5rem; list-style:none; }
.nav-links a { color:var(--text2); text-decoration:none; font-size:0.9rem; font-weight:500; transition:color 0.2s; }
.nav-links a:hover { color:var(--accent); }

/* HERO */
.hero { padding:8rem 2rem 4rem; text-align:center; background:linear-gradient(180deg, #EEF2FF 0%, var(--bg) 100%); }
.hero h1 { font-size:3.2rem; font-weight:900; line-height:1.15; margin-bottom:1rem; }
.hero h1 span { background:var(--gradient); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero .subtitle { font-size:1.2rem; color:var(--text2); max-width:700px; margin:0 auto 2rem; font-weight:400; }
.hero-badges { display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap; margin-bottom:2rem; }
.badge { display:inline-flex; align-items:center; gap:0.4rem; padding:0.4rem 1rem; border-radius:99px;
  font-size:0.82rem; font-weight:600; border:1px solid var(--border); background:white; color:var(--text2); }
.badge.accent { background:var(--accent); color:white; border-color:var(--accent); }
.hero-btns { display:flex; gap:1rem; justify-content:center; flex-wrap:wrap; }
.btn { display:inline-flex; align-items:center; gap:0.5rem; padding:0.75rem 1.75rem; border-radius:99px;
  font-size:0.95rem; font-weight:600; text-decoration:none; transition:all 0.25s; }
.btn-primary { background:var(--accent); color:white; box-shadow:0 4px 14px rgba(79,70,229,0.35); }
.btn-primary:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(79,70,229,0.45); }
.btn-outline { background:white; color:var(--text); border:2px solid var(--border); }
.btn-outline:hover { border-color:var(--accent); color:var(--accent); }

/* SECTIONS */
.container { max-width:1200px; margin:0 auto; padding:0 2rem; }
section { padding:4rem 0; }
.section-title { font-size:2rem; font-weight:800; margin-bottom:0.5rem; }
.section-subtitle { color:var(--text2); font-size:1.05rem; margin-bottom:2.5rem; }

/* CARDS */
.card { background:var(--card); border:1px solid var(--border); border-radius:var(--radius);
  padding:2rem; box-shadow:var(--shadow); transition:all 0.3s; }
.card:hover { box-shadow:var(--shadow-lg); transform:translateY(-2px); }
.card-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:1.5rem; }
.card h3 { font-size:1.1rem; font-weight:700; margin-bottom:0.5rem; }
.card p { color:var(--text2); font-size:0.92rem; }
.card-icon { width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center;
  font-size:1.3rem; margin-bottom:1rem; }

/* INSTALL */
.install-box { background:#1E293B; border-radius:var(--radius); padding:1.5rem 2rem; color:#E2E8F0;
  font-family:'JetBrains Mono',monospace; font-size:0.95rem; position:relative; margin:1.5rem 0; }
.install-box .prompt { color:#7C3AED; }
.install-box .cmd { color:#34D399; }

/* TABLES */
.results-table { width:100%; border-collapse:separate; border-spacing:0; border-radius:var(--radius);
  overflow:hidden; box-shadow:var(--shadow); background:white; border:1px solid var(--border); }
.results-table th { background:linear-gradient(135deg, #4F46E5, #7C3AED); color:white; padding:0.85rem 1rem;
  font-size:0.82rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; text-align:left; }
.results-table td { padding:0.75rem 1rem; font-size:0.88rem; border-bottom:1px solid var(--border); }
.results-table tr:last-child td { border-bottom:none; }
.results-table tr:hover td { background:#F8FAFC; }
.results-table .reject-yes { color:var(--green); font-weight:700; }
.results-table .reject-no { color:var(--red); font-weight:700; }
td.mono { font-family:'JetBrains Mono',monospace; font-size:0.82rem; }

/* IMAGES */
.fig-container { margin:2rem 0; text-align:center; }
.fig-container img { max-width:100%; border-radius:var(--radius); box-shadow:var(--shadow-md);
  border:1px solid var(--border); }
.fig-caption { margin-top:0.75rem; font-size:0.85rem; color:var(--text3); font-style:italic; }

/* TEST DETAIL */
.test-detail { background:white; border:1px solid var(--border); border-radius:var(--radius);
  padding:1.5rem 2rem; margin:1.5rem 0; box-shadow:var(--shadow); }
.test-detail h4 { font-size:1rem; font-weight:700; margin-bottom:0.25rem; }
.test-detail .ref { font-size:0.82rem; color:var(--accent); margin-bottom:0.75rem; }
.test-detail pre { background:#F1F5F9; border-radius:8px; padding:1rem; font-family:'JetBrains Mono',monospace;
  font-size:0.8rem; overflow-x:auto; white-space:pre; line-height:1.6; color:var(--text); }

/* AUTHOR */
.author-card { display:flex; align-items:center; gap:2rem; background:white; border:1px solid var(--border);
  border-radius:var(--radius); padding:2rem; box-shadow:var(--shadow); }
.author-avatar { width:100px; height:100px; border-radius:50%; background:var(--gradient);
  display:flex; align-items:center; justify-content:center; font-size:2.5rem; color:white; flex-shrink:0; }
.author-info h3 { font-size:1.3rem; font-weight:700; }
.author-info p { color:var(--text2); font-size:0.92rem; }
.author-links { display:flex; gap:1rem; margin-top:0.75rem; flex-wrap:wrap; }
.author-links a { color:var(--accent); text-decoration:none; font-size:0.88rem; font-weight:500; }
.author-links a:hover { text-decoration:underline; }

/* FOOTER */
footer { background:#1E293B; color:#CBD5E1; padding:3rem 2rem; text-align:center; margin-top:4rem; }
footer a { color:#818CF8; text-decoration:none; }
footer a:hover { text-decoration:underline; }

/* REFERENCES */
.ref-list { columns:2; column-gap:2rem; }
.ref-list li { font-size:0.85rem; color:var(--text2); margin-bottom:0.5rem; break-inside:avoid; }

/* RESPONSIVE */
@media(max-width:768px) {
  .hero h1 { font-size:2rem; }
  .card-grid { grid-template-columns:1fr; }
  .author-card { flex-direction:column; text-align:center; }
  .ref-list { columns:1; }
  .nav-links { display:none; }
}
"""

HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>hybridnonlinur — Nonlinear Hybrid Unit Root Tests in Python</title>
<meta name="description" content="A comprehensive Python library implementing 13 nonlinear unit root tests for time series econometrics. Fourier-based, ESTAR, Quantile, Fractional Frequency testing.">
<style>
""" + CSS + """
</style>
</head>
<body>
"""

NAV = """
<nav class="nav">
<div class="nav-inner">
  <div class="nav-logo">hybridnonlinur</div>
  <ul class="nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#install">Install</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#visualizations">Visualizations</a></li>
    <li><a href="#tests">All Tests</a></li>
    <li><a href="#references">References</a></li>
    <li><a href="https://github.com/merwanroudane/hybridnonlinur" target="_blank">GitHub ↗</a></li>
  </ul>
</div>
</nav>
"""

HERO = """
<section class="hero">
<div class="container">
  <h1><span>hybridnonlinur</span></h1>
  <p class="subtitle">A comprehensive Python library implementing <strong>13 nonlinear unit root tests</strong> from the frontier of time series econometrics — Fourier-based structural breaks, ESTAR/AESTAR nonlinearity, quantile regression, fractional frequencies, and wavelet preprocessing.</p>
  <div class="hero-badges">
    <span class="badge accent">v1.0.0</span>
    <span class="badge">🐍 Python 3.9+</span>
    <span class="badge">📊 13 Tests</span>
    <span class="badge">📝 MIT License</span>
    <span class="badge">✅ Production Ready</span>
  </div>
  <div class="hero-btns">
    <a href="https://pypi.org/project/hybridnonlinur/" class="btn btn-primary" target="_blank">📦 Install from PyPI</a>
    <a href="https://github.com/merwanroudane/hybridnonlinur" class="btn btn-outline" target="_blank">⭐ View on GitHub</a>
  </div>
</div>
</section>
"""

with open('docs/_part1.html', 'w', encoding='utf-8') as f:
    f.write(HEADER + NAV + HERO)
print("Part 1 written: docs/_part1.html")
