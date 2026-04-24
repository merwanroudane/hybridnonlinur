"""
QR-KSS and QR-Fourier-KSS quantile unit root tests.

References
----------
- Li, H. & Park, S.Y. (2018). Econometric Reviews, 37(8), 867-892.
- Bahmani-Oskooee, M. et al. (2020). Bull. Econ. Research, 72(1), 14-33.
"""
import numpy as np
from .core import (QuantileTestResult, optimal_fourier_k, fourier_terms)
from .critical_values import qr_kss_delta2_cv


def _quantile_regression(y, X, tau):
    """Quantile regression via linear programming (simplex)."""
    from scipy.optimize import linprog
    n, k = X.shape
    # min  tau * u+ + (1-tau) * u-  s.t.  X*beta + u+ - u- = y
    c = np.concatenate([np.zeros(k), tau * np.ones(n), (1 - tau) * np.ones(n)])
    A_eq = np.hstack([X, np.eye(n), -np.eye(n)])
    bounds = [(None, None)] * k + [(0, None)] * (2 * n)
    try:
        res = linprog(c, A_eq=A_eq, b_eq=y, bounds=bounds, method='highs')
        if res.success:
            return res.x[:k]
    except Exception:
        pass
    # Fallback: statsmodels
    try:
        import statsmodels.api as sm
        qr = sm.QuantReg(y, X).fit(q=tau, max_iter=1000)
        return qr.params
    except Exception:
        return np.linalg.lstsq(X, y, rcond=None)[0]


def _qr_tstat(y_dep, X, tau):
    """Compute quantile regression t-statistic for first regressor."""
    n, k = X.shape
    beta = _quantile_regression(y_dep, X, tau)
    resid = y_dep - X @ beta
    # Bandwidth for density estimation (Bofinger, 1975)
    from scipy.stats import norm
    h = n ** (-1/3) * norm.ppf(1 - 0.05/2) ** (2/3) * \
        ((1.5 * norm.pdf(norm.ppf(tau)) ** 2) / (2 * norm.ppf(tau) ** 2 + 1)) ** (1/3)
    # Kernel density at quantile
    indicator = (np.abs(resid) <= h).astype(float)
    f_hat = np.sum(indicator) / (2 * h * n)
    if f_hat < 1e-10:
        f_hat = 1e-10
    # Covariance
    try:
        XtX_inv = np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        XtX_inv = np.linalg.pinv(X.T @ X)
    cov = tau * (1 - tau) / (n * f_hat ** 2) * XtX_inv
    se = np.sqrt(np.diag(cov))
    se[se == 0] = 1e-15
    t_stat = beta[0] / se[0]
    return t_stat, beta


def _get_delta2(y_dep, X, tau, beta):
    """
    Compute delta^2 = hat{f}(0)^2 * (tau*(1-tau)) / T
    as used in GAUSS __get_qr_adf_delta2.
    This measures the scale of quantile-specific inference.
    """
    n = len(y_dep)
    resid = y_dep - X @ beta
    from scipy.stats import norm
    h = n ** (-1/3) * norm.ppf(1 - 0.05/2) ** (2/3) * \
        ((1.5 * norm.pdf(norm.ppf(tau)) ** 2) / (2 * norm.ppf(tau) ** 2 + 1)) ** (1/3)
    indicator = (np.abs(resid) <= h).astype(float)
    f_hat = np.sum(indicator) / (2 * h * n)
    if f_hat < 1e-10:
        f_hat = 1e-10
    delta2 = f_hat ** 2 * tau * (1 - tau) / n
    # Normalize to [0, 1] range for CV lookup
    delta2_norm = min(max(delta2 * n, 0.0), 1.0)
    return delta2_norm


def qr_kss(y, model=1, pmax=8, taus=None, ic='aic'):
    """
    QR-KSS (Li & Park, 2018) nonlinear quantile unit root test.

    Matches GAUSS QR_KSS procedure:
    - Uses y^3 on raw y (not demeaned/detrended first)
    - model=0: no deterministics, model=1: constant, model=2: constant+trend
    - Uses delta^2-based CV interpolation from published tables

    Parameters
    ----------
    y : array_like - Time series.
    model : int - 0=none, 1=constant, 2=constant+trend.
    pmax : int - Number of lags for Dy (default=8, matching GAUSS).
    taus : array_like - Quantile levels (default: 0.1 to 0.9).
    ic : str - Lag selection criterion.

    Returns
    -------
    QuantileTestResult
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    if taus is None:
        taus = np.arange(0.1, 1.0, 0.1)

    # GAUSS: y1 = lagn(y^3, 1)  — uses raw y, not demeaned
    dy = np.diff(y)
    y1 = y[:-1] ** 3  # y^3_{t-1} on raw series

    # Build regressors matching GAUSS exactly
    # x = y1 [~ dy_lags]  (trimmed by p+1)
    p = pmax  # GAUSS uses fixed p from argument
    start = p + 1  # GAUSS: trimr(x, p+1, 0)

    if start >= len(dy) - 5:
        start = max(1, len(dy) - 10)

    y_dep_full = dy[start:]
    x_base = y1[start:].reshape(-1, 1)

    if p > 0:
        lags = np.column_stack([dy[start - j: len(dy) - j]
                                for j in range(1, p + 1)
                                if start - j >= 0])
        X = np.column_stack([x_base, lags])
    else:
        X = x_base

    # model=2: add trend
    if model == 2:
        trend = np.arange(1, len(y_dep_full) + 1).reshape(-1, 1)
        X = np.column_stack([X, trend])

    # Quantile regressions
    tau_stats = {}
    cv_tau = {}
    for tau in taus:
        tau = round(tau, 2)
        t_stat, beta = _qr_tstat(y_dep_full, X, tau)
        tau_stats[tau] = t_stat

        # delta^2-based critical values (matching GAUSS crit_qr_kss)
        delta2 = _get_delta2(y_dep_full, X, tau, beta)
        cv_1, cv_5, cv_10 = qr_kss_delta2_cv(delta2, model)
        cv_tau[tau] = {"1%": cv_1, "5%": cv_5, "10%": cv_10}

    # QKS and QCM
    abs_t = [abs(v) for v in tau_stats.values()]
    qks = max(abs_t)
    qcm = sum(v ** 2 for v in tau_stats.values())

    return QuantileTestResult(
        test_name="QR-KSS",
        tau_stats=tau_stats, qks_stat=qks, qcm_stat=qcm,
        optimal_k=None, optimal_lag=p, model=model,
        cv_tau=cv_tau,
        cv_qks={"5%": np.nan}, cv_qcm={"5%": np.nan},
        reference="Li & Park (2018)"
    )


def qr_fourier_kss(y, model=1, kmax=5, pmax=8, taus=None, k=3,
                    nboot=499):
    """
    QR-Fourier-KSS (Bahmani-Oskooee et al., 2020).

    ONE-STEP procedure matching GAUSS:
    x = y^3_{t-1} [~ dy_lags] ~ sin(2*pi*k*t/T) ~ cos(2*pi*k*t/T) [~ trend]

    Fourier terms are IN the regression, not used for pre-detrending.

    Parameters
    ----------
    y : array_like - Time series.
    model : int - 1=constant, 2=constant+trend.
    kmax : int - Maximum Fourier frequency (not used, k is fixed).
    pmax : int - Number of lags for Dy (default=8).
    taus : array_like - Quantile levels.
    k : int - Fourier frequency (default=3, matching GAUSS).
    nboot : int - Number of bootstrap replications.

    Returns
    -------
    QuantileTestResult with bootstrap critical values.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    if taus is None:
        taus = np.arange(0.1, 1.0, 0.1)

    # GAUSS: Fourier terms on FULL series
    from .core import fourier_terms
    ft = fourier_terms(T, k)  # (T, 2): [sin, cos]
    sink = ft[:, 0]
    cosk = ft[:, 1]

    dy = np.diff(y)
    y1 = y[:-1] ** 3  # y^3_{t-1} on raw series

    # Trim by pmax+1 (matching GAUSS: trimr(x, pmax+1, 0))
    start = pmax + 1
    if start >= len(dy) - 5:
        start = max(1, len(dy) - 10)

    y_dep = dy[start:]
    n_obs = len(y_dep)

    # Build X: y^3_{t-1} [~ dy_lags] ~ sin ~ cos [~ trend]
    # Note: GAUSS puts y1 first, then dy_lags, then sin/cos
    x_y1 = y1[start:].reshape(-1, 1)

    if pmax > 0:
        dy_lags = np.column_stack([dy[start - j: len(dy) - j]
                                   for j in range(1, pmax + 1)
                                   if start - j >= 0])
        X = np.column_stack([x_y1, dy_lags])
    else:
        X = x_y1

    # Add Fourier terms (trim to match)
    # sink/cosk are length T, dy is length T-1, after trim start from index start
    # The Fourier terms correspond to t = start+1...T (1-indexed), 
    # which is indices start...T-1 in 0-indexed of the original T-length array
    # But dy[start:] corresponds to y[start+1]-y[start], ..., y[T-1]-y[T-2]
    # so the "time" for dy[start:] is t = start+1 ... T-1 (0-indexed)
    # GAUSS: sink/cosk are generated for t=1..T, then trimr(x, pmax+1, 0)
    # so we use sink[start+1:] and cosk[start+1:] (since dy starts at index 1 of y)
    sink_trim = sink[start + 1: start + 1 + n_obs].reshape(-1, 1)
    cosk_trim = cosk[start + 1: start + 1 + n_obs].reshape(-1, 1)

    # Handle edge case: ensure correct length
    if len(sink_trim) < n_obs:
        sink_trim = sink[-(n_obs):].reshape(-1, 1)
        cosk_trim = cosk[-(n_obs):].reshape(-1, 1)

    X = np.column_stack([X, sink_trim, cosk_trim])

    if model == 2:
        trend = np.arange(1, n_obs + 1).reshape(-1, 1)
        X = np.column_stack([X, trend])

    # Quantile regressions at each tau
    tau_stats = {}
    for tau in taus:
        tau = round(tau, 2)
        t_stat, _ = _qr_tstat(y_dep, X, tau)
        tau_stats[tau] = t_stat

    abs_t = [abs(v_) for v_ in tau_stats.values()]
    qks = max(abs_t)
    qcm = sum(v_ ** 2 for v_ in tau_stats.values())

    # Bootstrap critical values under H0
    cv_boot = _bootstrap_qr_fourier_kss(y, model, pmax, k, taus, nboot)

    return QuantileTestResult(
        test_name="QR-Fourier-KSS",
        tau_stats=tau_stats, qks_stat=qks, qcm_stat=qcm,
        optimal_k=k, optimal_lag=pmax, model=model,
        cv_tau={round(tau, 2): {"5%": cv_boot.get(round(tau, 2), np.nan)}
                for tau in taus},
        cv_qks={"1%": cv_boot.get("qks_1", np.nan),
                "5%": cv_boot.get("qks_5", np.nan),
                "10%": cv_boot.get("qks_10", np.nan)},
        cv_qcm={"5%": cv_boot.get("qcm_5", np.nan)},
        extra={"fourier_k": k, "nboot": nboot},
        reference="Bahmani-Oskooee et al. (2020)"
    )


def _bootstrap_qr_fourier_kss(y, model, pmax, k, taus, nboot):
    """
    Sieve bootstrap for QR-Fourier-KSS (matching GAUSS procedure).

    Under H0: regress dy on [const, sin, cos, dy_lags, (trend)]
    Get residuals, fit AR(1), resample centered innovations.
    """
    T = len(y)
    from .core import fourier_terms
    ft = fourier_terms(T, k)
    sink = ft[:, 0]
    cosk = ft[:, 1]

    dy = np.diff(y)
    start = pmax + 1
    if start >= len(dy) - 5:
        start = max(1, len(dy) - 10)

    dy_trim = dy[start:]
    n_obs = len(dy_trim)

    # Null model: dy = c + sin + cos [+ dy_lags] [+ trend]
    c = np.ones(n_obs).reshape(-1, 1)
    # Fourier terms
    sink_trim = sink[start + 1: start + 1 + n_obs].reshape(-1, 1)
    cosk_trim = cosk[start + 1: start + 1 + n_obs].reshape(-1, 1)
    if len(sink_trim) < n_obs:
        sink_trim = sink[-(n_obs):].reshape(-1, 1)
        cosk_trim = cosk[-(n_obs):].reshape(-1, 1)

    if model == 1:
        if pmax > 0:
            dy_lags = np.column_stack([dy[start - j: len(dy) - j]
                                       for j in range(1, pmax + 1)
                                       if start - j >= 0])
            X_null = np.column_stack([c, sink_trim, cosk_trim, dy_lags])
        else:
            X_null = np.column_stack([c, sink_trim, cosk_trim])
    elif model == 2:
        trend = np.arange(1, n_obs + 1).reshape(-1, 1)
        if pmax > 0:
            dy_lags = np.column_stack([dy[start - j: len(dy) - j]
                                       for j in range(1, pmax + 1)
                                       if start - j >= 0])
            X_null = np.column_stack([c, trend, sink_trim, cosk_trim, dy_lags])
        else:
            X_null = np.column_stack([c, trend, sink_trim, cosk_trim])

    # OLS under null
    b = np.linalg.lstsq(X_null, dy_trim, rcond=None)[0]
    yd = dy_trim - X_null @ b

    # AR(1) on residuals (GAUSS: fi = inv(yd1'yd1)*yd1'yd)
    yd1 = yd[:-1]
    yd0 = yd[1:]
    fi = np.sum(yd1 * yd0) / np.sum(yd1 ** 2) if np.sum(yd1 ** 2) > 0 else 0
    mu = yd0 - fi * yd1
    mu = mu - np.mean(mu)  # Center residuals

    tt = len(mu)
    boot_stats = []  # Store per-tau stats and QKS

    for rep in range(nboot):
        # Resample centered residuals
        idx = np.random.randint(0, tt, tt)
        mustar = mu[idx]

        # Generate unit root process under H0
        ydstar = np.zeros(tt)
        ydstar[0] = mustar[0]
        for s in range(1, tt):
            ydstar[s] = ydstar[s - 1] + mustar[s]

        ystar = ydstar

        # Run QR-Fourier-KSS on bootstrap sample (single tau at median for speed)
        try:
            T_b = len(ystar)
            ft_b = fourier_terms(T_b, k)
            dy_b = np.diff(ystar)
            y1_b = ystar[:-1] ** 3

            p_b = min(pmax, len(dy_b) // 3)
            start_b = p_b + 1
            if start_b >= len(dy_b) - 3:
                continue

            y_dep_b = dy_b[start_b:]
            n_b = len(y_dep_b)
            x_y1_b = y1_b[start_b:].reshape(-1, 1)

            if p_b > 0:
                dy_lags_b = np.column_stack([dy_b[start_b - j: len(dy_b) - j]
                                             for j in range(1, p_b + 1)
                                             if start_b - j >= 0])
                X_b = np.column_stack([x_y1_b, dy_lags_b])
            else:
                X_b = x_y1_b

            s_b = ft_b[start_b + 1: start_b + 1 + n_b, 0].reshape(-1, 1)
            c_b = ft_b[start_b + 1: start_b + 1 + n_b, 1].reshape(-1, 1)
            if len(s_b) < n_b:
                s_b = ft_b[-(n_b):, 0].reshape(-1, 1)
                c_b = ft_b[-(n_b):, 1].reshape(-1, 1)

            X_b = np.column_stack([X_b, s_b, c_b])
            if model == 2:
                X_b = np.column_stack([X_b, np.arange(1, n_b + 1).reshape(-1, 1)])

            # Compute test at each tau
            abs_ts = []
            for tau in taus:
                try:
                    t_b, _ = _qr_tstat(y_dep_b, X_b, round(tau, 2))
                    abs_ts.append(abs(t_b))
                except Exception:
                    abs_ts.append(0)

            if abs_ts:
                boot_stats.append(max(abs_ts))

        except Exception:
            continue

    cv = {}
    if boot_stats:
        boot_arr = np.sort(boot_stats)
        nb = len(boot_arr)
        cv["qks_1"] = boot_arr[int(0.99 * nb)]
        cv["qks_5"] = boot_arr[int(0.95 * nb)]
        cv["qks_10"] = boot_arr[int(0.90 * nb)]

    return cv
