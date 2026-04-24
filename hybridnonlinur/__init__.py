"""
hybridnonlinur — Nonlinear Hybrid Unit Root Tests
==================================================

A comprehensive Python library implementing 13 nonlinear unit root tests
from the econometrics literature, covering Fourier-based structural breaks,
ESTAR/AESTAR nonlinearity, quantile regression robustness, fractional
frequency extensions, and wavelet preprocessing.

Author: Dr. Merwan Roudane (merwanroudane920@gmail.com)
Repository: https://github.com/merwanroudane/hybridnonlinur

Tests Implemented
-----------------
1.  KSS              — Kapetanios, Shin & Snell (2003)
2.  Fourier-KSS      — Christopoulos & Leon-Ledesma (2010)
3.  Fourier-ADF      — Enders & Lee (2012)
4.  Fourier-KSS Boot — Christopoulos & Leon-Ledesma (2010) bootstrap
5.  Fourier-Kruse    — Guris (2019)
6.  FFKRUSE          — Biyikli & Hepsag (2025)
7.  Fourier-Sollis   — Ranjbar et al. (2018)
8.  FFSOLLIS         — Biyikli & Hepsag (2025)
9.  Fourier-Sollis-ZM — Hepkorucu & Cinar (2021)
10. QR-KSS           — Li & Park (2018)
11. QR-Fourier-KSS   — Bahmani-Oskooee et al. (2020)
12. KSS-FF           — Omay, Corakci & Hasdemir (2021)
13. FWKSS            — Haar Wavelet + Fourier-KSS
"""

__version__ = "1.0.0"
__author__ = "Dr. Merwan Roudane"
__email__ = "merwanroudane920@gmail.com"

# -- Core --
from .core import TestResult, QuantileTestResult

# -- Tests --
from .kss import kss, fourier_kss, fourier_adf, fourier_kss_bootstrap
from .fourier_kruse import fourier_kruse, ffkruse
from .fourier_sollis import fourier_sollis, ffsollis, fourier_sollis_zeromean
from .quantile import qr_kss, qr_fourier_kss
from .kss_ff import kss_ff, wavelet_kss

# -- Visualization --
from .visualize import (plot_series_with_fourier, plot_quantile_results,
                        plot_comparison_table, plot_all_tests)

# -- Convenience: run all tests --
def run_all(y, series_name="Series", model=1, pmax=12, verbose=True):
    """
    Run all unit root tests on a given series.

    Parameters
    ----------
    y : array_like - Time series.
    series_name : str - Name for display.
    model : int - 1=intercept, 2=intercept+trend.
    pmax : int - Maximum lag order.
    verbose : bool - Print summary tables.

    Returns
    -------
    dict of TestResult / QuantileTestResult
    """
    import numpy as np
    y = np.asarray(y, dtype=np.float64).ravel()
    results = {}

    tests = [
        ("KSS", lambda: kss(y, model=max(model, 2), pmax=pmax)),
        ("Fourier-KSS", lambda: fourier_kss(y, model=model, pmax=pmax)),
        ("Fourier-ADF", lambda: fourier_adf(y, model=model, pmax=pmax)),
        ("Fourier-Kruse", lambda: fourier_kruse(y, model=model, pmax=pmax)),
        ("FFKRUSE", lambda: ffkruse(y, model=model, pmax=pmax)),
        ("Fourier-Sollis", lambda: fourier_sollis(y, model=model, pmax=pmax)),
        ("FFSOLLIS", lambda: ffsollis(y, model=model, pmax=pmax)),
        ("Fourier-Sollis-ZM", lambda: fourier_sollis_zeromean(y, pmax=pmax)),
        ("QR-KSS", lambda: qr_kss(y, model=max(model, 1), pmax=min(pmax, 8))),
        ("KSS-FF", lambda: kss_ff(y, model=model, pmax=pmax)),
        ("FWKSS", lambda: wavelet_kss(y, model=model, pmax=min(pmax, 8))),
    ]

    for name, fn in tests:
        try:
            r = fn()
            results[name] = r
            if verbose:
                print(r.summary())
        except Exception as e:
            if verbose:
                print(f"  [!] {name}: {e}")

    return results


__all__ = [
    'kss', 'fourier_kss', 'fourier_adf', 'fourier_kss_bootstrap',
    'fourier_kruse', 'ffkruse',
    'fourier_sollis', 'ffsollis', 'fourier_sollis_zeromean',
    'qr_kss', 'qr_fourier_kss', 'kss_ff', 'wavelet_kss',
    'run_all',
    'plot_series_with_fourier', 'plot_quantile_results',
    'plot_comparison_table', 'plot_all_tests',
    'TestResult', 'QuantileTestResult',
]
