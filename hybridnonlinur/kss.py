"""
KSS, Fourier-KSS, Fourier-ADF, and Fourier-KSS Bootstrap unit root tests.

References
----------
- Kapetanios, G., Shin, Y. & Snell, A. (2003). J. Econometrics, 112(2), 359-379.
- Christopoulos, D.K. & Leon-Ledesma, M.A. (2010). JIMF, 29(6), 1076-1093.
- Enders, W. & Lee, J. (2012). J. Time Series Analysis, 33(5), 728-743.
"""
import numpy as np
from .core import (TestResult, detrend_fourier, optimal_fourier_k,
                   build_kss_regressors, ols_tstat)
from .critical_values import KSS_CV, FKSS_CV, get_cv, BECKER_F_CV


def kss(y, model=2, pmax=12, ic='aic'):
    """
    KSS (2003) nonlinear unit root test against ESTAR alternative.

    Parameters
    ----------
    y : array_like - Time series.
    model : int - 1=zero-mean, 2=demeaned, 3=detrended.
    pmax : int - Maximum lag order.
    ic : str - 'aic' or 'tsig'.

    Returns
    -------
    TestResult
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    if model == 1:
        v = y.copy()
    elif model == 2:
        v = y - np.mean(y)
    else:
        t = np.arange(1, T + 1)
        X = np.column_stack([np.ones(T), t])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        v = y - X @ b

    y_dep, X, p_opt = build_kss_regressors(v, pmax, power=3, ic=ic)
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    t_nl = t_stats[0]

    cv = get_cv(KSS_CV, model, 1, T)
    return TestResult(
        test_name="KSS",
        statistic=t_nl, optimal_k=0, optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(t_nl < cv["1%"]), reject_5=(t_nl < cv["5%"]),
        reject_10=(t_nl < cv["10%"]),
        reference="Kapetanios, Shin & Snell (2003)"
    )


def fourier_kss(y, model=1, kmax=5, pmax=12, ic='aic'):
    """
    Fourier-KSS (Christopoulos & Leon-Ledesma, 2010) unit root test.

    Two-step: (1) Fourier detrend, (2) KSS on residuals.
    Uses v^3_{t-1} as the transition regressor (ESTAR nonlinearity).
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    k_opt, v, f_stat = optimal_fourier_k(y, model, kmax)
    y_dep, X, p_opt = build_kss_regressors(v, pmax, power=3, ic=ic)
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    t_nl = t_stats[0]

    cv = get_cv(FKSS_CV, model, k_opt)
    f_cv = BECKER_F_CV.get(model, {}).get(int(round(k_opt)), 4.0)

    return TestResult(
        test_name="Fourier-KSS",
        statistic=t_nl, optimal_k=k_opt, optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(t_nl < cv["1%"]), reject_5=(t_nl < cv["5%"]),
        reject_10=(t_nl < cv["10%"]),
        f_stat=f_stat, f_cv_5=f_cv,
        reference="Christopoulos & Leon-Ledesma (2010)"
    )


def fourier_adf(y, model=1, kmax=5, pmax=12, ic='aic'):
    """
    Fourier-ADF (FADF) linear unit root test with Fourier terms.

    Two-step: (1) Fourier detrend, (2) ADF on residuals.
    Uses v_{t-1} (linear, power=1) instead of v^3_{t-1}.

    References
    ----------
    Enders, W. & Lee, J. (2012). J. Time Series Analysis, 33(5), 728-743.
    Christopoulos, D.K. & Leon-Ledesma, M.A. (2010). JIMF, 29(6), 1076-1093.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    k_opt, v, f_stat = optimal_fourier_k(y, model, kmax)
    # ADF: use power=1 (v_{t-1} instead of v^3_{t-1})
    y_dep, X, p_opt = build_kss_regressors(v, pmax, power=1, ic=ic)
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X)
    t_adf = t_stats[0]

    # FADF uses different critical values than FKSS
    # These are closer to standard ADF CVs for Fourier models
    FADF_CV = {
        1: {1: {"1%": -4.42, "5%": -3.81, "10%": -3.49},
            2: {"1%": -3.97, "5%": -3.39, "10%": -3.10},
            3: {"1%": -3.77, "5%": -3.23, "10%": -2.96},
            4: {"1%": -3.64, "5%": -3.12, "10%": -2.86},
            5: {"1%": -3.58, "5%": -3.07, "10%": -2.81}},
        2: {1: {"1%": -4.95, "5%": -4.35, "10%": -4.05},
            2: {"1%": -4.51, "5%": -3.93, "10%": -3.65},
            3: {"1%": -4.33, "5%": -3.78, "10%": -3.51},
            4: {"1%": -4.20, "5%": -3.68, "10%": -3.42},
            5: {"1%": -4.13, "5%": -3.62, "10%": -3.37}},
    }
    k_int = int(round(k_opt))
    k_int = max(1, min(k_int, 5))
    cv = FADF_CV.get(model, FADF_CV[1]).get(k_int, FADF_CV[1][1])
    f_cv = BECKER_F_CV.get(model, {}).get(k_int, 4.0)

    return TestResult(
        test_name="Fourier-ADF",
        statistic=t_adf, optimal_k=k_opt, optimal_lag=p_opt, model=model,
        cv_1=cv["1%"], cv_5=cv["5%"], cv_10=cv["10%"],
        reject_1=(t_adf < cv["1%"]), reject_5=(t_adf < cv["5%"]),
        reject_10=(t_adf < cv["10%"]),
        f_stat=f_stat, f_cv_5=f_cv,
        reference="Enders & Lee (2012)"
    )


def fourier_kss_bootstrap(y, model=1, kmax=5, pmax=12, ic='aic',
                           test='FKSS', nboot=1000):
    """
    Bootstrap Fourier-KSS/FADF (Christopoulos & Leon-Ledesma, 2010).

    Generates bootstrap critical values under H0 (unit root).
    Matches GAUSS `Fourier_KSS_bootstrap()` procedure exactly.

    Parameters
    ----------
    y : array_like - Time series.
    model : int - 1=intercept, 2=intercept+trend.
    kmax : int - Max Fourier frequency.
    pmax : int - Max lag order.
    test : str - 'FKSS' or 'FADF'.
    nboot : int - Number of bootstrap replications.

    Returns
    -------
    TestResult with bootstrap critical values.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    T = len(y)
    power = 3 if test == 'FKSS' else 1

    # Step 1: Get optimal k and residuals
    k_opt, v, f_stat = optimal_fourier_k(y, model, kmax)

    # Step 2: Compute test statistic
    y_dep, X_reg, p_opt = build_kss_regressors(v, pmax, power=power, ic=ic)
    beta, t_stats, resid, sigma2 = ols_tstat(y_dep, X_reg)
    t_stat_orig = t_stats[0]

    # Step 3: Bootstrap under H0
    # Fit null model: Dy_t = sum(rho_j * Dy_{t-j}) + e_t  (no y^3 term)
    dv = np.diff(v)
    if p_opt > 0:
        X_null = np.column_stack([dv[p_opt - j: len(dv) - j]
                                  for j in range(1, p_opt + 1)])
        dy_null = dv[p_opt:]
        b_null = np.linalg.lstsq(X_null, dy_null, rcond=None)[0]
        yd = dy_null - X_null @ b_null
    else:
        yd = dv
        b_null = np.array([])

    # AR(1) on residuals for sieve bootstrap
    yd1 = yd[:-1]
    yd0 = yd[1:]
    fi = np.sum(yd1 * yd0) / np.sum(yd1 ** 2) if np.sum(yd1 ** 2) > 0 else 0
    mu = yd0 - fi * yd1
    mu = mu - np.mean(mu)  # Center residuals

    tt = len(mu)
    test_boot = np.zeros(nboot)

    for rep in range(nboot):
        # Resample centered residuals
        idx = np.random.randint(0, tt, tt)
        mustar = mu[idx]

        # Generate unit root process
        ydstar = np.zeros(tt)
        ydstar[0] = mustar[0]
        for s in range(1, tt):
            ydstar[s] = ydstar[s - 1] + mustar[s]

        # Run test on bootstrap sample
        try:
            k_b, v_b, _ = optimal_fourier_k(ydstar, model, kmax)
            y_b, X_b, _ = build_kss_regressors(v_b, pmax, power=power, ic=ic)
            _, t_b, _, _ = ols_tstat(y_b, X_b)
            test_boot[rep] = t_b[0]
        except Exception:
            test_boot[rep] = 0

    # Bootstrap critical values
    test_boot_sorted = np.sort(test_boot)
    cv_1 = test_boot_sorted[int(0.01 * nboot)]
    cv_5 = test_boot_sorted[int(0.05 * nboot)]
    cv_10 = test_boot_sorted[int(0.10 * nboot)]

    return TestResult(
        test_name=f"Fourier-{test} (Bootstrap)",
        statistic=t_stat_orig, optimal_k=k_opt, optimal_lag=p_opt, model=model,
        cv_1=cv_1, cv_5=cv_5, cv_10=cv_10,
        reject_1=(t_stat_orig < cv_1), reject_5=(t_stat_orig < cv_5),
        reject_10=(t_stat_orig < cv_10),
        f_stat=f_stat,
        extra={"nboot": nboot, "test_type": test},
        reference="Christopoulos & Leon-Ledesma (2010)"
    )
