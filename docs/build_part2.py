"""Part 2: Features, Install, Results tables"""

FEATURES = """
<section id="features" style="padding-top:5rem;">
<div class="container">
  <h2 class="section-title">✨ Key Features</h2>
  <p class="section-subtitle">State-of-the-art nonlinear unit root testing, faithfully translated from published papers and verified GAUSS source code.</p>
  <div class="card-grid">
    <div class="card">
      <div class="card-icon" style="background:#EEF2FF;color:#4F46E5;">📐</div>
      <h3>ESTAR &amp; AESTAR Nonlinearity</h3>
      <p>KSS, Kruse, and Sollis tests detect exponential smooth transition autoregressive dynamics with symmetric and asymmetric adjustment.</p>
    </div>
    <div class="card">
      <div class="card-icon" style="background:#F0FDF4;color:#059669;">〰️</div>
      <h3>Fourier Structural Breaks</h3>
      <p>Capture unknown smooth structural breaks using trigonometric functions — no need to specify break dates or number of breaks a priori.</p>
    </div>
    <div class="card">
      <div class="card-icon" style="background:#FEF3C7;color:#D97706;">📊</div>
      <h3>Quantile Regression</h3>
      <p>QR-KSS and QR-Fourier-KSS test for unit roots across the entire conditional distribution, robust to outliers and asymmetric shocks.</p>
    </div>
    <div class="card">
      <div class="card-icon" style="background:#FDF2F8;color:#DB2777;">🔬</div>
      <h3>Fractional Frequencies</h3>
      <p>FFKRUSE, FFSOLLIS, and KSS-FF extend integer Fourier to fractional frequencies, capturing gradual structural shifts more precisely.</p>
    </div>
    <div class="card">
      <div class="card-icon" style="background:#EFF6FF;color:#2563EB;">🌊</div>
      <h3>Wavelet Preprocessing</h3>
      <p>FWKSS applies Haar wavelet smoothing before Fourier-KSS testing, reducing noise while preserving long-run dynamics.</p>
    </div>
    <div class="card">
      <div class="card-icon" style="background:#F5F3FF;color:#7C3AED;">🎯</div>
      <h3>Bootstrap Critical Values</h3>
      <p>Sieve bootstrap generates data-specific critical values under H₀, providing exact finite-sample inference beyond asymptotic tables.</p>
    </div>
  </div>
</div>
</section>
"""

INSTALL = """
<section id="install">
<div class="container">
  <h2 class="section-title">📦 Installation</h2>
  <p class="section-subtitle">Get started in seconds with pip.</p>
  <div class="install-box">
    <span class="prompt">$</span> <span class="cmd">pip install hybridnonlinur</span>
  </div>
  <p style="color:var(--text2);font-size:0.92rem;margin-bottom:1rem;">Or install from source:</p>
  <div class="install-box">
    <span class="prompt">$</span> <span class="cmd">git clone https://github.com/merwanroudane/hybridnonlinur.git</span><br>
    <span class="prompt">$</span> <span class="cmd">cd hybridnonlinur</span><br>
    <span class="prompt">$</span> <span class="cmd">pip install -e .</span>
  </div>
  <h3 style="margin-top:2rem;font-size:1.1rem;font-weight:700;">Quick Start</h3>
  <div class="install-box" style="font-size:0.85rem;">
<span style="color:#7C3AED">import</span> <span style="color:#34D399">numpy</span> <span style="color:#7C3AED">as</span> np
<span style="color:#7C3AED">import</span> <span style="color:#34D399">hybridnonlinur</span> <span style="color:#7C3AED">as</span> hnl

<span style="color:#64748B"># Load your time series</span>
y = np.cumsum(np.random.randn(<span style="color:#F59E0B">200</span>))

<span style="color:#64748B"># Run individual test</span>
result = hnl.fourier_kss(y, model=<span style="color:#F59E0B">1</span>)
<span style="color:#7C3AED">print</span>(result.summary())

<span style="color:#64748B"># Run ALL 13 tests at once</span>
results = hnl.run_all(y, series_name=<span style="color:#34D399">"My Series"</span>)
  </div>
</div>
</section>
"""

TESTS_TABLE = """
<section id="tests-overview">
<div class="container">
  <h2 class="section-title">🧪 All 13 Implemented Tests</h2>
  <p class="section-subtitle">Each test is faithfully translated from the original papers and verified GAUSS source code.</p>
  <table class="results-table">
    <thead><tr><th>#</th><th>Test</th><th>Python Function</th><th>Type</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>KSS</td><td class="mono">kss()</td><td>ESTAR t-stat</td><td>Kapetanios, Shin &amp; Snell (2003)</td></tr>
      <tr><td>2</td><td>Fourier-KSS</td><td class="mono">fourier_kss()</td><td>ESTAR t-stat</td><td>Christopoulos &amp; León-Ledesma (2010)</td></tr>
      <tr><td>3</td><td>Fourier-ADF</td><td class="mono">fourier_adf()</td><td>Linear t-stat</td><td>Enders &amp; Lee (2012)</td></tr>
      <tr><td>4</td><td>Fourier-KSS Bootstrap</td><td class="mono">fourier_kss_bootstrap()</td><td>ESTAR + bootstrap</td><td>Christopoulos &amp; León-Ledesma (2010)</td></tr>
      <tr><td>5</td><td>Fourier-Kruse</td><td class="mono">fourier_kruse()</td><td>Kruse τ-stat</td><td>Güriş (2019)</td></tr>
      <tr><td>6</td><td>FFKRUSE</td><td class="mono">ffkruse()</td><td>Kruse τ-stat (FF)</td><td>Biyikli &amp; Hepsağ (2025)</td></tr>
      <tr><td>7</td><td>Fourier-Sollis</td><td class="mono">fourier_sollis()</td><td>AESTAR F-stat</td><td>Ranjbar et al. (2018)</td></tr>
      <tr><td>8</td><td>FFSOLLIS</td><td class="mono">ffsollis()</td><td>AESTAR F-stat (FF)</td><td>Biyikli &amp; Hepsağ (2025)</td></tr>
      <tr><td>9</td><td>Fourier-Sollis ZM</td><td class="mono">fourier_sollis_zeromean()</td><td>AESTAR F-stat</td><td>Hepkorucu &amp; Çınar (2021)</td></tr>
      <tr><td>10</td><td>QR-KSS</td><td class="mono">qr_kss()</td><td>Quantile t-stat</td><td>Li &amp; Park (2018)</td></tr>
      <tr><td>11</td><td>QR-Fourier-KSS</td><td class="mono">qr_fourier_kss()</td><td>Quantile + Fourier</td><td>Bahmani-Oskooee et al. (2020)</td></tr>
      <tr><td>12</td><td>KSS-FF</td><td class="mono">kss_ff()</td><td>ESTAR + Frac. Fourier</td><td>Omay, Corakci &amp; Hasdemir (2021)</td></tr>
      <tr><td>13</td><td>FWKSS</td><td class="mono">wavelet_kss()</td><td>Wavelet + Fourier</td><td>Haar Wavelet + Fourier-KSS</td></tr>
    </tbody>
  </table>
</div>
</section>
"""

with open('docs/_part2.html', 'w', encoding='utf-8') as f:
    f.write(FEATURES + INSTALL + TESTS_TABLE)
print("Part 2 written: docs/_part2.html")
