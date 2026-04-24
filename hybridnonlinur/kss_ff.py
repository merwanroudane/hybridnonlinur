"""
KSS-FF (Fractional Fourier) and Wavelet-KSS (FWKSS) unit root tests.

References
----------
- Omay, T., Corakci, A. & Hasdemir, E. (2021). Mathematics, 9(20), 2534.
- Omay, T. (2015). Economics Letters, 134, 123-126.
- Aydin, M. (Sakarya University) — GAUSS fourier_wkss.src implementation.
"""
import numpy as np
from .core import (TestResult, build_kss_regressors, ols_tstat,
                   optimal_fourier_k, detrend_fourier)
from .critical_values import KSS_FF_CV, FKSS_CV, get_cv


def kss_ff(y, model=1, pmax=12, ic='aic', kfr_max=5.0, kfr_step=0.1):
    """
    KSS-FF: ESTAR unit root test with Fractional Fourier Function
    (Omay, Corakci & Hasdemir, 2021).

    The Fourier function restores Taylor expansion residuals lost during
    KSS linearization, rather than capturing structural breaks.

    Parameters
    ----------
    y : array_like - Time series.
    model : int - 1=intercept, 2=intercept+trend.
    pmax : int - Maximum lag order.
    ic : str - 'aic' or 'tsig'.
    kfr_max : float - Max fractional frequency.
    kfr_step : float - Fractional frequency step.

    Returns
    -------
    TestResult
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)

    # Two-step: fractional Fourier detrend, then KSS
    k_opt, v, f_stat = optimal_fourier_k(y, model, fractional=True,
                                          kfr_step=kfr_step, kfr_max=kfr_max)
    y_dep, X, p_opt = build_kss_regressors(v, pmax, power=3, ic=ic)
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    t_nl = t_stats[0]

    # Get critical values - find nearest kfr
    cv = get_cv(KSS_FF_CV, model, k_opt)

    return TestResult(
        test_name="KSS-FF",
        statistic=t_nl, optimal_k=round(k_opt, 2), optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(t_nl < cv["1%"]), reject_5=(t_nl < cv["5%"]),
        reject_10=(t_nl < cv["10%"]),
        f_stat=f_stat,
        reference="Omay, Corakci & Hasdemir (2021)"
    )


def _haar_wavelet_transform(y):
    """
    Simple Haar wavelet transform matching GAUSS __wavelet_transform exactly.

    GAUSS code:
        d1[n1] = (y[t2+1] - y[t2]) / sqrt(2)   (detail)
        yt[n1] = (y[t2+1] + y[t2]) / sqrt(2)   (approximation)
        t2 = t2 + 2

    Produces T/2 length approximation and detail coefficients.
    """
    T = len(y)
    T2 = T // 2
    d1 = np.zeros(T2)
    yt = np.zeros(T2)

    n1 = 0
    t2 = 0
    while t2 < T - 1 and n1 < T2:
        d1[n1] = (y[t2 + 1] - y[t2]) / np.sqrt(2)
        yt[n1] = (y[t2 + 1] + y[t2]) / np.sqrt(2)
        t2 += 2
        n1 += 1

    return d1, yt


def wavelet_kss(y, model=1, kmax=5, pmax=8, ic='aic', fmax=None):
    """
    Wavelet Fourier-KSS (FWKSS): Haar wavelet + Fourier-KSS.

    Matches GAUSS Fourier_WKSS procedure exactly:
    1. Apply simple Haar averaging: yt = (y[t] + y[t+1]) / sqrt(2)
    2. Run Fourier-KSS on the smoothed (halved) series

    Parameters
    ----------
    y : array_like - Time series.
    model : int - 1=intercept, 2=intercept+trend.
    kmax : int - Maximum Fourier frequency (fmax alias).
    pmax : int - Maximum lag order (default=8 matching GAUSS).
    ic : str - Information criterion: 'aic', 'bic', or 'tsig'.
    fmax : int - Alternative alias for kmax.

    Returns
    -------
    TestResult
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)

    if fmax is not None:
        kmax = fmax

    # Step 1: GAUSS-style simple Haar wavelet transform
    d1, yt = _haar_wavelet_transform(y)

    # Step 2: Run Fourier-KSS on the approximation coefficients
    k_opt, v, f_stat = optimal_fourier_k(yt, model, kmax)
    y_dep, X, p_opt = build_kss_regressors(v, pmax, power=3, ic=ic)
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    t_nl = t_stats[0]

    cv = get_cv(FKSS_CV, model, k_opt)

    return TestResult(
        test_name="FWKSS",
        statistic=t_nl, optimal_k=k_opt, optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(t_nl < cv["1%"]), reject_5=(t_nl < cv["5%"]),
        reject_10=(t_nl < cv["10%"]),
        f_stat=f_stat,
        extra={"original_T": T, "wavelet_T": len(yt), "wavelet": "Haar"},
        reference="Aydin (FWKSS, Haar wavelet + Fourier-KSS)"
    )
