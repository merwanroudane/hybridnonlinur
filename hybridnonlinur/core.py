"""
Core utilities for hybridnonlinur — Fourier generation, detrending, lag selection, result containers.

References
----------
- Becker, R., Enders, W., Lee, J. (2006). Journal of Time Series Analysis, 27(3), 381–409.
- Christopoulos, D.K. & León-Ledesma, M.A. (2010). JIMF, 29(6), 1076–1093.
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from tabulate import tabulate


# ──────────────────────────── Result Containers ────────────────────────────

@dataclass
class TestResult:
    """Base result container for all unit root tests."""
    test_name: str
    statistic: float
    optimal_k: float
    optimal_lag: int
    model: int
    cv_1: float
    cv_5: float
    cv_10: float
    reject_1: bool = False
    reject_5: bool = False
    reject_10: bool = False
    f_stat: Optional[float] = None
    f_cv_5: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    reference: str = ""

    def __post_init__(self):
        pass  # rejection flags set by each test

    def summary(self):
        """Pretty-print result table."""
        model_str = {1: "Intercept", 2: "Intercept + Trend"}.get(self.model, str(self.model))
        rows = [
            ["Test", self.test_name],
            ["Model", model_str],
            ["Test Statistic", f"{self.statistic:.4f}"],
            ["Optimal Frequency (k)", f"{self.optimal_k}"],
            ["Optimal Lag (p)", f"{self.optimal_lag}"],
            ["", ""],
            ["", "Critical Value | Reject H0"],
            ["1% level", f"{self.cv_1:.4f}  |  {'Yes *' if self.reject_1 else 'No'}"],
            ["5% level", f"{self.cv_5:.4f}  |  {'Yes *' if self.reject_5 else 'No'}"],
            ["10% level", f"{self.cv_10:.4f}  |  {'Yes *' if self.reject_10 else 'No'}"],
        ]
        if self.f_stat is not None:
            rows.append(["", ""])
            rows.append(["F-stat (Fourier)", f"{self.f_stat:.4f}"])
            if self.f_cv_5 is not None:
                rows.append(["F critical (5%)", f"{self.f_cv_5:.4f}"])
        if self.reference:
            rows.append(["", ""])
            rows.append(["Reference", self.reference])
        header = f"\n{'='*55}\n  {self.test_name} Unit Root Test\n{'='*55}"
        tbl = tabulate(rows, tablefmt="simple", colalign=("right", "left"))
        return header + "\n" + tbl + "\n" + "="*55


@dataclass
class QuantileTestResult:
    """Result container for quantile-based tests."""
    test_name: str
    tau_stats: Dict[float, float]
    qks_stat: float
    qcm_stat: float
    optimal_k: Optional[float]
    optimal_lag: int
    model: int
    cv_tau: Dict[float, Dict[str, float]]
    cv_qks: Dict[str, float]
    cv_qcm: Dict[str, float]
    extra: Dict[str, Any] = field(default_factory=dict)
    reference: str = ""

    def summary(self):
        header = f"\n{'='*65}\n  {self.test_name} Quantile Unit Root Test\n{'='*65}"
        rows = []
        for tau in sorted(self.tau_stats.keys()):
            cv = self.cv_tau.get(tau, {})
            rej = "Yes" if self.tau_stats[tau] < cv.get("5%", -np.inf) else "No"
            rows.append([f"t={tau:.1f}", f"{self.tau_stats[tau]:.4f}",
                         f"{cv.get('5%', 'N/A')}", rej])
        tbl1 = tabulate(rows, headers=["Quantile", "t_T(τ)", "CV 5%", "Reject"],
                        tablefmt="simple")
        rows2 = [
            ["QKS statistic", f"{self.qks_stat:.4f}"],
            ["QCM statistic", f"{self.qcm_stat:.4f}"],
        ]
        tbl2 = tabulate(rows2, tablefmt="simple")
        return header + "\n" + tbl1 + "\n\n" + tbl2 + "\n" + "="*65


# ──────────────────────────── Fourier Generation ────────────────────────────

def fourier_terms(T: int, k: float) -> np.ndarray:
    """
    Generate Fourier sine and cosine terms.

    Parameters
    ----------
    T : int
        Sample size.
    k : float
        Frequency (integer or fractional).

    Returns
    -------
    np.ndarray
        (T, 2) array with columns [sin(2πkt/T), cos(2πkt/T)].
    """
    t = np.arange(1, T + 1, dtype=np.float64)
    s = np.sin(2 * np.pi * k * t / T)
    c = np.cos(2 * np.pi * k * t / T)
    return np.column_stack([s, c])


# ──────────────────────────── OLS Detrending ────────────────────────────

def detrend_fourier(y: np.ndarray, model: int = 1, k: float = 1.0):
    """
    OLS detrend with Fourier components.

    Parameters
    ----------
    y : np.ndarray
        Time series (T,).
    model : int
        1 = intercept only, 2 = intercept + trend.
    k : float
        Fourier frequency.

    Returns
    -------
    residuals : np.ndarray
        Detrended residuals (T,).
    ssr : float
        Sum of squared residuals.
    coeffs : np.ndarray
        OLS coefficients.
    f_stat : float
        F-statistic for joint significance of Fourier terms.
    """
    T = len(y)
    t = np.arange(1, T + 1, dtype=np.float64)
    ft = fourier_terms(T, k)

    if model == 1:
        X = np.column_stack([np.ones(T), ft])
    elif model == 2:
        X = np.column_stack([np.ones(T), t, ft])
    else:
        raise ValueError(f"model must be 1 or 2, got {model}")

    # OLS
    coeffs, residuals_sum, _, _ = np.linalg.lstsq(X, y, rcond=None)
    residuals = y - X @ coeffs
    ssr = np.sum(residuals ** 2)

    # F-test for Fourier terms significance (H0: δ1 = δ2 = 0)
    if model == 1:
        X_r = np.ones((T, 1))
    else:
        X_r = np.column_stack([np.ones(T), t])

    coeffs_r = np.linalg.lstsq(X_r, y, rcond=None)[0]
    resid_r = y - X_r @ coeffs_r
    ssr_r = np.sum(resid_r ** 2)

    q = 2  # number of Fourier restrictions
    n_params = X.shape[1]
    f_stat = ((ssr_r - ssr) / q) / (ssr / (T - n_params))

    return residuals, ssr, coeffs, f_stat


def optimal_fourier_k(y: np.ndarray, model: int = 1, kmax: int = 5,
                      fractional: bool = False,
                      kfr_step: float = 0.1, kfr_max: float = None):
    """
    Find optimal Fourier frequency by minimizing SSR.

    Parameters
    ----------
    y : np.ndarray
        Time series.
    model : int
        1 or 2.
    kmax : int
        Maximum integer frequency (used when fractional=False).
    fractional : bool
        If True, search over fractional grid.
    kfr_step : float
        Step size for fractional grid.
    kfr_max : float
        Maximum fractional frequency (default T/2 for integer, 2.0 for fractional).

    Returns
    -------
    k_opt : float
        Optimal frequency.
    resid_opt : np.ndarray
        Residuals at optimal k.
    f_stat : float
        F-statistic at optimal k.
    """
    if fractional:
        if kfr_max is None:
            kfr_max = 2.0
        k_grid = np.arange(kfr_step, kfr_max + kfr_step / 2, kfr_step)
    else:
        k_grid = np.arange(1, kmax + 1, dtype=float)

    best_ssr = np.inf
    k_opt = k_grid[0]
    resid_opt = None
    f_opt = 0.0

    for k in k_grid:
        resid, ssr, _, f_stat = detrend_fourier(y, model, k)
        if ssr < best_ssr:
            best_ssr = ssr
            k_opt = k
            resid_opt = resid
            f_opt = f_stat

    return k_opt, resid_opt, f_opt


# ──────────────────────────── Lag Selection ────────────────────────────

def lag_select_aic(dy: np.ndarray, x_base: np.ndarray, pmax: int = 12):
    """
    Select optimal lag order using AIC.

    Parameters
    ----------
    dy : np.ndarray
        First differences Δy (dependent variable).
    x_base : np.ndarray
        Base regressors (e.g., y³_{t-1}).
    pmax : int
        Maximum lag order.

    Returns
    -------
    p_opt : int
        Optimal lag order.
    """
    T = len(dy)
    best_aic = np.inf
    p_opt = 0

    for p in range(0, pmax + 1):
        if p >= T - x_base.shape[0] - 2:
            break
        # Build lagged Δy
        if p == 0:
            y_dep = dy[pmax:]
            X = x_base[pmax:] if x_base.ndim == 2 else x_base[pmax:].reshape(-1, 1)
        else:
            y_dep = dy[pmax:]
            lags = np.column_stack([dy[pmax - j:-j] if j < len(dy) - pmax else dy[pmax - j:]
                                    for j in range(1, p + 1)])
            if x_base.ndim == 1:
                X = np.column_stack([x_base[pmax:].reshape(-1, 1), lags])
            else:
                X = np.column_stack([x_base[pmax:], lags])

        n = len(y_dep)
        if n <= X.shape[1] + 1:
            continue

        try:
            beta = np.linalg.lstsq(X, y_dep, rcond=None)[0]
            resid = y_dep - X @ beta
            sigma2 = np.sum(resid ** 2) / n
            if sigma2 <= 0:
                continue
            aic = np.log(sigma2) + 2 * X.shape[1] / n
            if aic < best_aic:
                best_aic = aic
                p_opt = p
        except np.linalg.LinAlgError:
            continue

    return p_opt


def lag_select_tsig(dy: np.ndarray, x_base: np.ndarray, pmax: int = 12,
                    sig: float = 0.10):
    """
    Select lag by general-to-specific t-significance on last lag.
    """
    T = len(dy)
    for p in range(pmax, -1, -1):
        if p == 0:
            return 0
        y_dep = dy[pmax:]
        lags = np.column_stack([dy[pmax - j:-j] if j < len(dy) - pmax else dy[pmax - j:]
                                for j in range(1, p + 1)])
        if x_base.ndim == 1:
            X = np.column_stack([x_base[pmax:].reshape(-1, 1), lags])
        else:
            X = np.column_stack([x_base[pmax:], lags])

        n = len(y_dep)
        if n <= X.shape[1] + 1:
            continue

        try:
            beta = np.linalg.lstsq(X, y_dep, rcond=None)[0]
            resid = y_dep - X @ beta
            sigma2 = np.sum(resid ** 2) / (n - X.shape[1])
            cov = sigma2 * np.linalg.inv(X.T @ X)
            se_last = np.sqrt(cov[-1, -1])
            t_last = beta[-1] / se_last
            if abs(t_last) > stats.t.ppf(1 - sig / 2, n - X.shape[1]):
                return p
        except (np.linalg.LinAlgError, FloatingPointError):
            continue
    return 0


# ──────────────────────────── OLS Regression Helper ────────────────────────────

def ols_tstat(y: np.ndarray, X: np.ndarray):
    """
    OLS regression returning coefficients, t-stats, residuals, sigma².

    Returns
    -------
    beta, t_stats, residuals, sigma2
    """
    n, k = X.shape
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    sigma2 = np.sum(resid ** 2) / (n - k)
    try:
        cov = sigma2 * np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        cov = sigma2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    se[se == 0] = 1e-15
    t_stats = beta / se
    return beta, t_stats, resid, sigma2


def build_kss_regressors(v: np.ndarray, pmax: int = 12, power: int = 3,
                         ic: str = 'aic'):
    """
    Build KSS-type regressors: y_dep = Δv_t, x_base = v^power_{t-1}.
    Selects optimal lags and returns trimmed arrays.

    Returns
    -------
    y_dep, X, p_opt
    """
    dv = np.diff(v)
    v_lag = v[:-1]
    v_power = v_lag ** power

    # Lag selection
    if ic == 'aic':
        p_opt = lag_select_aic(dv, v_power, pmax)
    else:
        p_opt = lag_select_tsig(dv, v_power, pmax)

    # Build final regressors
    T = len(dv)
    start = max(p_opt, 1)

    y_dep = dv[start:]
    x_base = v_power[start:].reshape(-1, 1)

    if p_opt > 0:
        lags = np.column_stack([dv[start - j: T - j] for j in range(1, p_opt + 1)])
        X = np.column_stack([x_base, lags])
    else:
        X = x_base

    return y_dep, X, p_opt


def build_kruse_regressors(v: np.ndarray, pmax: int = 12, ic: str = 'aic'):
    """
    Build Kruse-type regressors: Δv_t = δ₁v³_{t-1} + δ₂v²_{t-1} + lags.

    Returns
    -------
    y_dep, X, p_opt
    """
    dv = np.diff(v)
    v_lag = v[:-1]
    v3 = v_lag ** 3
    v2 = v_lag ** 2
    x_base = np.column_stack([v3, v2])

    if ic == 'aic':
        p_opt = lag_select_aic(dv, x_base, pmax)
    else:
        p_opt = lag_select_tsig(dv, x_base, pmax)

    T = len(dv)
    start = max(p_opt, 1)
    y_dep = dv[start:]
    xb = x_base[start:]

    if p_opt > 0:
        lags = np.column_stack([dv[start - j: T - j] for j in range(1, p_opt + 1)])
        X = np.column_stack([xb, lags])
    else:
        X = xb

    return y_dep, X, p_opt


def build_sollis_regressors(v: np.ndarray, pmax: int = 12, ic: str = 'aic'):
    """
    Build Sollis/AESTAR regressors: Δv_t = φ₁v³_{t-1} + φ₂v⁴_{t-1} + lags.

    Returns
    -------
    y_dep, X, p_opt
    """
    dv = np.diff(v)
    v_lag = v[:-1]
    v3 = v_lag ** 3
    v4 = v_lag ** 4
    x_base = np.column_stack([v3, v4])

    if ic == 'aic':
        p_opt = lag_select_aic(dv, x_base, pmax)
    else:
        p_opt = lag_select_tsig(dv, x_base, pmax)

    T = len(dv)
    start = max(p_opt, 1)
    y_dep = dv[start:]
    xb = x_base[start:]

    if p_opt > 0:
        lags = np.column_stack([dv[start - j: T - j] for j in range(1, p_opt + 1)])
        X = np.column_stack([xb, lags])
    else:
        X = xb

    return y_dep, X, p_opt
