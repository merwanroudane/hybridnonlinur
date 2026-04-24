# hybridnonlinur

**Nonlinear Hybrid Unit Root Tests** — A comprehensive Python library for advanced econometric unit root testing.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

`hybridnonlinur` implements **13 nonlinear unit root tests** from the frontier of time series econometrics. Each test is faithfully translated from published papers and verified GAUSS source code.

## Implemented Tests

| # | Test | Python Function | Reference |
|---|------|----------------|-----------|
| 1 | KSS | `kss()` | Kapetanios, Shin & Snell (2003) |
| 2 | Fourier-KSS | `fourier_kss()` | Christopoulos & Leon-Ledesma (2010) |
| 3 | Fourier-ADF | `fourier_adf()` | Enders & Lee (2012) |
| 4 | Fourier-KSS Bootstrap | `fourier_kss_bootstrap()` | Christopoulos & Leon-Ledesma (2010) |
| 5 | Fourier-Kruse | `fourier_kruse()` | Guris (2019) |
| 6 | FFKRUSE | `ffkruse()` | Biyikli & Hepsag (2025) |
| 7 | Fourier-Sollis | `fourier_sollis()` | Ranjbar et al. (2018) |
| 8 | FFSOLLIS | `ffsollis()` | Biyikli & Hepsag (2025) |
| 9 | Fourier-Sollis (Zero-Mean) | `fourier_sollis_zeromean()` | Hepkorucu & Cinar (2021) |
| 10 | QR-KSS | `qr_kss()` | Li & Park (2018) |
| 11 | QR-Fourier-KSS | `qr_fourier_kss()` | Bahmani-Oskooee et al. (2020) |
| 12 | KSS-FF | `kss_ff()` | Omay, Corakci & Hasdemir (2021) |
| 13 | FWKSS | `wavelet_kss()` | Haar Wavelet + Fourier-KSS |

## Installation

```bash
pip install hybridnonlinur
```

Or from source:
```bash
git clone https://github.com/merwanroudane/hybridnonlinur.git
cd hybridnonlinur
pip install -e .
```

## Quick Start

```python
import numpy as np
import hybridnonlinur as hnl

# Load your time series
y = np.cumsum(np.random.randn(200))

# Run individual tests
result = hnl.fourier_kss(y, model=1)
print(result.summary())

# Run ALL 13 tests at once
results = hnl.run_all(y, series_name="My Series", model=1)

# Quantile unit root test
qr_result = hnl.qr_kss(y, model=1, taus=np.arange(0.1, 1.0, 0.1))
print(qr_result.summary())

# Bootstrap critical values
boot_result = hnl.fourier_kss_bootstrap(y, model=1, nboot=1000)
print(boot_result.summary())
```

## Visualization

```python
# Publication-quality comparison table
fig = hnl.plot_comparison_table(list(results.values()))
fig.savefig('comparison.png', dpi=300)

# Quantile profile plot
fig = hnl.plot_quantile_results(qr_result)
fig.savefig('quantile_profile.png', dpi=300)

# Series with Fourier fit
fig = hnl.plot_series_with_fourier(y, model=1, k=1)
fig.savefig('fourier_fit.png', dpi=300)
```

## Model Specifications

- `model=0`: No deterministic components (QR-KSS only)
- `model=1`: Intercept only
- `model=2`: Intercept + trend

## Test Categories

### ESTAR Tests (t-statistic, reject if stat < CV)
KSS, Fourier-KSS, Fourier-ADF, KSS-FF, FWKSS

### Kruse Tests (tau-statistic, reject if stat > CV)
Fourier-Kruse, FFKRUSE

### AESTAR/Sollis Tests (F-statistic, reject if stat > CV)
Fourier-Sollis, FFSOLLIS, Fourier-Sollis (Zero-Mean)

### Quantile Tests (t-statistic per quantile)
QR-KSS, QR-Fourier-KSS

## Dependencies

- NumPy, SciPy, Matplotlib, tabulate

## Author

**Dr. Merwan Roudane**  
Email: merwanroudane920@gmail.com  
GitHub: https://github.com/merwanroudane/hybridnonlinur

## License

MIT License — see [LICENSE](LICENSE) for details.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{roudane2026hybridnonlinur,
  author = {Roudane, Merwan},
  title = {hybridnonlinur: Nonlinear Hybrid Unit Root Tests in Python},
  year = {2026},
  url = {https://github.com/merwanroudane/hybridnonlinur}
}
```
