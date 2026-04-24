"""Part 3: Empirical results tables + visualizations + individual test outputs"""

RESULTS = """
<section id="results">
<div class="container">
  <h2 class="section-title">📈 Empirical Results — Real Financial Data</h2>
  <p class="section-subtitle">All 13 tests applied to EUR/USD, Gold, and Crude Oil WTI daily log-returns (Yahoo Finance).</p>

  <h3 style="font-size:1.2rem;font-weight:700;margin-bottom:1rem;">Table 1: Primary Series — EUR/USD Exchange Rate</h3>
  <table class="results-table">
    <thead><tr><th>Test</th><th>Statistic</th><th>k*</th><th>Lag</th><th>CV 1%</th><th>CV 5%</th><th>CV 10%</th><th>Reject H₀ (5%)</th></tr></thead>
    <tbody>
      <tr><td>KSS</td><td class="mono">-2.9962</td><td>0</td><td>0</td><td class="mono">-3.770</td><td class="mono">-3.090</td><td class="mono">-2.770</td><td class="reject-no">✗</td></tr>
      <tr><td>Fourier-KSS</td><td class="mono">-3.4528</td><td>1.0</td><td>0</td><td class="mono">-4.350</td><td class="mono">-3.550</td><td class="mono">-3.170</td><td class="reject-no">✗</td></tr>
      <tr><td>Fourier-ADF</td><td class="mono">-4.2818</td><td>1.0</td><td>0</td><td class="mono">-4.420</td><td class="mono">-3.810</td><td class="mono">-3.490</td><td class="reject-yes">✓</td></tr>
      <tr><td>Fourier-FKSS (Bootstrap)</td><td class="mono">-3.4528</td><td>1.0</td><td>0</td><td class="mono">-4.152</td><td class="mono">-3.541</td><td class="mono">-3.198</td><td class="reject-no">✗</td></tr>
      <tr><td>Fourier-Kruse</td><td class="mono">18.5061</td><td>1.0</td><td>0</td><td class="mono">18.820</td><td class="mono">14.800</td><td class="mono">12.520</td><td class="reject-yes">✓</td></tr>
      <tr><td>FFKRUSE</td><td class="mono">22.4471</td><td>1.1</td><td>0</td><td class="mono">19.560</td><td class="mono">14.860</td><td class="mono">12.700</td><td class="reject-yes">✓</td></tr>
      <tr><td>Fourier-Sollis</td><td class="mono">9.5171</td><td>1.0</td><td>0</td><td class="mono">9.780</td><td class="mono">7.472</td><td class="mono">6.395</td><td class="reject-yes">✓</td></tr>
      <tr><td>FFSOLLIS</td><td class="mono">10.7636</td><td>1.1</td><td>0</td><td class="mono">10.165</td><td class="mono">7.910</td><td class="mono">6.871</td><td class="reject-yes">✓</td></tr>
      <tr><td>Fourier-Sollis (Zero-Mean)</td><td class="mono">9.5171</td><td>1.0</td><td>0</td><td class="mono">9.767</td><td class="mono">7.472</td><td class="mono">6.391</td><td class="reject-yes">✓</td></tr>
      <tr><td>KSS-FF</td><td class="mono">-4.3171</td><td>1.1</td><td>0</td><td class="mono">-4.103</td><td class="mono">-3.522</td><td class="mono">-3.212</td><td class="reject-yes">✓</td></tr>
      <tr><td>FWKSS</td><td class="mono">-2.6440</td><td>1.0</td><td>0</td><td class="mono">-4.350</td><td class="mono">-3.550</td><td class="mono">-3.170</td><td class="reject-no">✗</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.82rem;color:var(--text3);margin-top:0.75rem;">Note: ✓ = reject H₀ (unit root) at 5%. KSS/Fourier-KSS/ADF use left-tail t-test; Kruse/Sollis use right-tail F/τ-test.</p>

  <div class="fig-container" style="margin-top:3rem;">
    <img src="img/cell_35.png" alt="Comparison Dashboard">
    <p class="fig-caption">Figure 1: Test Statistics Comparison Dashboard — All 11 standard tests on EUR/USD</p>
  </div>
  <div class="fig-container">
    <img src="img/cell_38.png" alt="Bar Chart">
    <p class="fig-caption">Figure 2: Test Statistics vs 5% Critical Values — Bar chart comparison</p>
  </div>
</div>
</section>
"""

MULTI = """
<section id="multi-series">
<div class="container">
  <h2 class="section-title">🔄 Multi-Series Analysis</h2>
  <p class="section-subtitle">All 11 standard tests across EUR/USD, Gold, and Crude Oil WTI.</p>

  <table class="results-table">
    <thead><tr><th>Series</th><th>Test</th><th>Stat</th><th>k*</th><th>Lag</th><th>CV 5%</th><th>Result</th></tr></thead>
    <tbody>
      <tr><td>EUR/USD</td><td>KSS</td><td class="mono">-2.9962</td><td>0</td><td>0</td><td class="mono">-3.090</td><td class="reject-no">✗</td></tr>
      <tr><td>EUR/USD</td><td>F-KSS</td><td class="mono">-3.4528</td><td>1.0</td><td>0</td><td class="mono">-3.550</td><td class="reject-no">✗</td></tr>
      <tr><td>EUR/USD</td><td>F-ADF</td><td class="mono">-4.2818</td><td>1.0</td><td>0</td><td class="mono">-3.810</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>F-Kruse</td><td class="mono">18.5061</td><td>1.0</td><td>0</td><td class="mono">14.800</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>FFKRUSE</td><td class="mono">22.4471</td><td>1.1</td><td>0</td><td class="mono">14.860</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>F-Sollis</td><td class="mono">9.5171</td><td>1.0</td><td>0</td><td class="mono">7.472</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>FFSOLLIS</td><td class="mono">10.7636</td><td>1.1</td><td>0</td><td class="mono">7.910</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>F-Sol-ZM</td><td class="mono">9.5171</td><td>1.0</td><td>0</td><td class="mono">7.472</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>KSS-FF</td><td class="mono">-4.3171</td><td>1.1</td><td>0</td><td class="mono">-3.522</td><td class="reject-yes">✓</td></tr>
      <tr><td>EUR/USD</td><td>FWKSS</td><td class="mono">-2.6440</td><td>1.0</td><td>0</td><td class="mono">-3.550</td><td class="reject-no">✗</td></tr>
      <tr style="background:#F8FAFC;"><td colspan="7" style="padding:0.3rem;"></td></tr>
      <tr><td>Gold</td><td>KSS</td><td class="mono">-2.0616</td><td>0</td><td>0</td><td class="mono">-3.090</td><td class="reject-no">✗</td></tr>
      <tr><td>Gold</td><td>F-KSS</td><td class="mono">-3.9598</td><td>1.0</td><td>0</td><td class="mono">-3.550</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>F-ADF</td><td class="mono">-3.2751</td><td>1.0</td><td>0</td><td class="mono">-3.810</td><td class="reject-no">✗</td></tr>
      <tr><td>Gold</td><td>F-Kruse</td><td class="mono">20.3678</td><td>1.0</td><td>0</td><td class="mono">14.800</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>FFKRUSE</td><td class="mono">17.4392</td><td>0.9</td><td>0</td><td class="mono">14.860</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>F-Sollis</td><td class="mono">8.8477</td><td>1.0</td><td>0</td><td class="mono">7.472</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>FFSOLLIS</td><td class="mono">8.2378</td><td>0.9</td><td>0</td><td class="mono">7.910</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>F-Sol-ZM</td><td class="mono">8.8477</td><td>1.0</td><td>0</td><td class="mono">7.472</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>KSS-FF</td><td class="mono">-3.8767</td><td>0.9</td><td>0</td><td class="mono">-3.522</td><td class="reject-yes">✓</td></tr>
      <tr><td>Gold</td><td>FWKSS</td><td class="mono">-3.1232</td><td>1.0</td><td>0</td><td class="mono">-3.550</td><td class="reject-no">✗</td></tr>
      <tr style="background:#F8FAFC;"><td colspan="7" style="padding:0.3rem;"></td></tr>
      <tr><td>Crude Oil WTI</td><td>KSS</td><td class="mono">-2.7015</td><td>0</td><td>0</td><td class="mono">-3.090</td><td class="reject-no">✗</td></tr>
      <tr><td>Crude Oil WTI</td><td>F-KSS</td><td class="mono">-4.0031</td><td>1.0</td><td>0</td><td class="mono">-3.550</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>F-ADF</td><td class="mono">-4.3327</td><td>1.0</td><td>0</td><td class="mono">-3.810</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>F-Kruse</td><td class="mono">15.8427</td><td>1.0</td><td>0</td><td class="mono">14.800</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>FFKRUSE</td><td class="mono">16.1640</td><td>0.9</td><td>0</td><td class="mono">14.860</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>F-Sollis</td><td class="mono">7.8902</td><td>1.0</td><td>0</td><td class="mono">7.472</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>FFSOLLIS</td><td class="mono">7.8148</td><td>0.9</td><td>0</td><td class="mono">7.910</td><td class="reject-no">✗</td></tr>
      <tr><td>Crude Oil WTI</td><td>F-Sol-ZM</td><td class="mono">7.8902</td><td>1.0</td><td>0</td><td class="mono">7.472</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>KSS-FF</td><td class="mono">-3.9699</td><td>0.9</td><td>0</td><td class="mono">-3.522</td><td class="reject-yes">✓</td></tr>
      <tr><td>Crude Oil WTI</td><td>FWKSS</td><td class="mono">-3.7523</td><td>1.0</td><td>0</td><td class="mono">-3.550</td><td class="reject-yes">✓</td></tr>
    </tbody>
  </table>

  <div class="fig-container" style="margin-top:2rem;">
    <img src="img/cell_41.png" alt="Rejection Heatmap">
    <p class="fig-caption">Figure 3: Rejection Heatmap — All tests across all three financial series at 5% significance</p>
  </div>
</div>
</section>
"""

with open('docs/_part3.html', 'w', encoding='utf-8') as f:
    f.write(RESULTS + MULTI)
print("Part 3 written: docs/_part3.html")
