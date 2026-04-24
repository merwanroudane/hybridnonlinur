"""
Fourier-Sollis (AESTAR) and Fractional Frequency FFSOLLIS unit root tests.

References
----------
- Sollis, R. (2009). Economic Modelling, 26(1), 118–125.
- Ranjbar, O. et al. (2018). Iranian Economic Review, 22(1), 51–62.
- Hepkorucu, A. & Çınar, M. (2021). KOCATEPEİİBFD, 23(2), 171–181.
- Biyikli, S.İ. & Hepsağ, A. (2025). Comm. Stat. Simul. Comput.
"""
import numpy as np
from scipy import stats as sp_stats
from .core import (TestResult, optimal_fourier_k, build_sollis_regressors, ols_tstat)
from .critical_values import FSOLLIS_CV, FFSOLLIS_CV, FSOLLIS_ZEROMEAN_CV, get_cv, BECKER_F_CV


def _sollis_ftest(y_dep, X):
    """Joint F-test for φ₁ = φ₂ = 0 (first two regressors)."""
    n, k_full = X.shape
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    ssr_full = np.sum(resid ** 2)
    # Restricted model: drop first two regressors (v³, v⁴)
    if k_full > 2:
        X_r = X[:, 2:]
        beta_r = np.linalg.lstsq(X_r, y_dep, rcond=None)[0]
        resid_r = y_dep - X_r @ beta_r
    else:
        resid_r = y_dep - np.mean(y_dep)
    ssr_r = np.sum(resid_r ** 2)
    q = 2
    f_stat = ((ssr_r - ssr_full) / q) / (ssr_full / (n - k_full))
    return f_stat, beta, t_stats


def fourier_sollis(y, model=1, kmax=5, pmax=12, ic='aic'):
    """
    Fourier-Sollis / Fourier-AESTAR (Ranjbar et al., 2018).

    Tests unit root against asymmetric ESTAR with Fourier structural breaks.
    Auxiliary: Δv_t = φ₁v³_{t-1} + φ₂v⁴_{t-1} + lags + η_t
    H₀: φ₁ = φ₂ = 0 (unit root) via F-test.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    k_opt, v, f_fourier = optimal_fourier_k(y, model, kmax)
    y_dep, X, p_opt = build_sollis_regressors(v, pmax, ic)
    f_stat, beta, t_stats = _sollis_ftest(y_dep, X)

    cv = get_cv(FSOLLIS_CV, model, k_opt, T)
    f_cv_becker = BECKER_F_CV.get(model, {}).get(int(round(k_opt)), 4.0)

    return TestResult(
        test_name="Fourier-Sollis",
        statistic=f_stat, optimal_k=k_opt, optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(f_stat > cv["1%"]), reject_5=(f_stat > cv["5%"]),
        reject_10=(f_stat > cv["10%"]),
        f_stat=f_fourier, f_cv_5=f_cv_becker,
        extra={"phi1": beta[0], "phi2": beta[1],
               "t_phi1": t_stats[0], "t_phi2": t_stats[1]},
        reference="Ranjbar et al. (2018)"
    )


def ffsollis(y, model=1, pmax=12, ic='aic', kfr_step=0.1, kfr_max=2.0):
    """
    Fractional Frequency Fourier-Sollis (Biyikli & Hepsağ, 2025).
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    k_opt, v, f_fourier = optimal_fourier_k(y, model, fractional=True,
                                             kfr_step=kfr_step, kfr_max=kfr_max)
    y_dep, X, p_opt = build_sollis_regressors(v, pmax, ic)
    f_stat, beta, t_stats = _sollis_ftest(y_dep, X)

    cv = get_cv(FFSOLLIS_CV, model, k_opt)

    return TestResult(
        test_name="FFSOLLIS",
        statistic=f_stat, optimal_k=round(k_opt, 2), optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(f_stat > cv["1%"]), reject_5=(f_stat > cv["5%"]),
        reject_10=(f_stat > cv["10%"]),
        f_stat=f_fourier,
        extra={"phi1": beta[0], "phi2": beta[1]},
        reference="Biyikli & Hepsağ (2025)"
    )


def fourier_sollis_zeromean(y, kmax=5, pmax=12, ic='aic'):
    """
    Fourier-Sollis zero-mean model (Hepkorucu & Çınar, 2021).
    For series where deterministic terms vanish after Fourier detrending.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    k_opt, v, f_fourier = optimal_fourier_k(y, model=1, kmax=kmax)
    y_dep, X, p_opt = build_sollis_regressors(v, pmax, ic)
    f_stat, beta, t_stats = _sollis_ftest(y_dep, X)

    k_int = int(round(k_opt))
    cv = FSOLLIS_ZEROMEAN_CV.get(k_int, FSOLLIS_ZEROMEAN_CV.get(1))

    return TestResult(
        test_name="Fourier-Sollis (Zero-Mean)",
        statistic=f_stat, optimal_k=k_opt, optimal_lag=p_opt, model=0,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(f_stat > cv["1%"]), reject_5=(f_stat > cv["5%"]),
        reject_10=(f_stat > cv["10%"]),
        f_stat=f_fourier,
        reference="Hepkorucu & Çınar (2021)"
    )
