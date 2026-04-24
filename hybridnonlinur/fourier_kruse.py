"""
Fourier-Kruse and Fractional Frequency Fourier-Kruse (FFKRUSE) unit root tests.

References
----------
- Kruse, R. (2011). Statistical Papers, 52(1), 71–85.
- Güriş, B. (2019). Comm. Stat. Simul. Comput., 48(10), 3056–3062.
- Biyikli, S.İ. & Hepsağ, A. (2025). Comm. Stat. Simul. Comput.
"""
import numpy as np
from .core import (TestResult, optimal_fourier_k, build_kruse_regressors, ols_tstat)
from .critical_values import FKRUSE_CV, FFKRUSE_CV, get_cv, BECKER_F_CV


def _kruse_tau(y_dep, X):
    """Compute Kruse τ = t²(δ₂⊥) + 1(δ̂₁<0)·t²(δ₁)."""
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    delta1_hat = beta[0]
    t_delta1 = t_stats[0]
    t_delta2 = t_stats[1]
    # Restricted: δ₂=0
    X_r = np.delete(X, 1, axis=1)
    beta_r, _, resid_r, _ = ols_tstat(y_dep, X_r)
    n = len(y_dep)
    k_full = X.shape[1]
    ssr_full = np.sum(resid ** 2)
    ssr_r = np.sum(resid_r ** 2)
    t_delta2_perp_sq = (ssr_r - ssr_full) / (ssr_full / (n - k_full))
    indicator = 1.0 if delta1_hat < 0 else 0.0
    tau = t_delta2_perp_sq + indicator * (t_delta1 ** 2)
    return tau, beta, t_stats


def fourier_kruse(y, model=1, kmax=5, pmax=12, ic='aic'):
    """
    Fourier-Kruse (Güriş, 2019) unit root test.

    Two-step: (1) Fourier detrend, (2) Kruse test on residuals.
    Allows non-zero threshold c ≠ 0.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    k_opt, v, f_stat = optimal_fourier_k(y, model, kmax)
    y_dep, X, p_opt = build_kruse_regressors(v, pmax, ic)
    tau, beta, t_stats = _kruse_tau(y_dep, X)

    cv = get_cv(FKRUSE_CV, model, k_opt, T)
    f_cv = BECKER_F_CV.get(model, {}).get(int(round(k_opt)), 4.0)

    return TestResult(
        test_name="Fourier-Kruse",
        statistic=tau, optimal_k=k_opt, optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(tau > cv["1%"]), reject_5=(tau > cv["5%"]),
        reject_10=(tau > cv["10%"]),
        f_stat=f_stat, f_cv_5=f_cv,
        reference="Güriş (2019)"
    )


def ffkruse(y, model=1, pmax=12, ic='aic', kfr_step=0.1, kfr_max=2.0):
    """
    Fractional Frequency Fourier-Kruse (Biyikli & Hepsağ, 2025).

    Same as Fourier-Kruse but searches over fractional frequency grid.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    k_opt, v, f_stat = optimal_fourier_k(y, model, fractional=True,
                                          kfr_step=kfr_step, kfr_max=kfr_max)
    y_dep, X, p_opt = build_kruse_regressors(v, pmax, ic)
    tau, beta, t_stats = _kruse_tau(y_dep, X)

    cv = get_cv(FFKRUSE_CV, model, k_opt)
    f_cv = BECKER_F_CV.get(model, {}).get(max(1, int(round(k_opt))), 4.0)

    return TestResult(
        test_name="FFKRUSE",
        statistic=tau, optimal_k=round(k_opt, 2), optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(tau > cv["1%"]), reject_5=(tau > cv["5%"]),
        reject_10=(tau > cv["10%"]),
        f_stat=f_stat, f_cv_5=f_cv,
        reference="Biyikli & Hepsağ (2025)"
    )
