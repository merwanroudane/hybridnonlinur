"""
Publication-quality visualization for hybridnonlinur test results.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

# ── Global Style ──
COLORS = {
    'primary': '#2563EB', 'secondary': '#7C3AED', 'accent': '#059669',
    'danger': '#DC2626', 'warning': '#D97706', 'surface': '#0F172A',
    'text': '#F8FAFC', 'grid': '#334155', 'bg': '#1E293B',
    'card': '#1E293B', 'gradient1': '#3B82F6', 'gradient2': '#8B5CF6',
}
PALETTE = ['#3B82F6', '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B',
           '#EF4444', '#EC4899', '#6366F1', '#14B8A6']


def _setup_style():
    rcParams.update({
        'figure.facecolor': COLORS['surface'], 'axes.facecolor': COLORS['bg'],
        'axes.edgecolor': COLORS['grid'], 'axes.labelcolor': COLORS['text'],
        'text.color': COLORS['text'], 'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'], 'grid.color': COLORS['grid'],
        'grid.alpha': 0.3, 'font.family': 'sans-serif',
        'font.size': 11, 'axes.titlesize': 14, 'axes.labelsize': 12,
    })


def plot_series_with_fourier(y, model=1, k=1, title="Series with Fourier Fit"):
    """Plot original series with Fourier deterministic components."""
    _setup_style()
    from .core import fourier_terms, detrend_fourier
    T = len(y)
    t = np.arange(1, T + 1)
    resid, ssr, coeffs, f_stat = detrend_fourier(y, model, k)
    ft = fourier_terms(T, k)

    if model == 1:
        X = np.column_stack([np.ones(T), ft])
    else:
        X = np.column_stack([np.ones(T), t, ft])
    fitted = X @ coeffs

    fig, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [2, 1]})
    # Top: series + fit
    axes[0].plot(t, y, color=COLORS['primary'], alpha=0.7, lw=1, label='Original')
    axes[0].plot(t, fitted, color=COLORS['accent'], lw=2, label=f'Fourier fit (k={k})')
    axes[0].set_title(title, fontsize=16, fontweight='bold')
    axes[0].legend(facecolor=COLORS['card'], edgecolor=COLORS['grid'])
    axes[0].grid(True, alpha=0.2)
    # Bottom: residuals
    axes[1].fill_between(t, resid, 0, alpha=0.4, color=COLORS['secondary'])
    axes[1].plot(t, resid, color=COLORS['secondary'], lw=0.8)
    axes[1].axhline(0, color=COLORS['text'], alpha=0.3, lw=0.5)
    axes[1].set_title('Detrended Residuals', fontsize=13)
    axes[1].set_xlabel('Time')
    axes[1].grid(True, alpha=0.2)
    plt.tight_layout()
    return fig


def plot_quantile_results(qr_result, title=None):
    """Plot quantile regression unit root test results across quantiles."""
    _setup_style()
    taus = sorted(qr_result.tau_stats.keys())
    stats = [qr_result.tau_stats[t] for t in taus]
    cvs = [qr_result.cv_tau.get(t, {}).get("5%", np.nan) for t in taus]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(taus, stats, width=0.06, color=COLORS['primary'], alpha=0.8,
           label='t_T(τ)', edgecolor=COLORS['gradient1'], linewidth=0.5)
    ax.plot(taus, cvs, 'o--', color=COLORS['danger'], lw=2, markersize=8,
            label='5% Critical Value')
    ax.axhline(0, color=COLORS['text'], alpha=0.3, lw=0.5)
    ax.set_xlabel('Quantile (τ)', fontsize=13)
    ax.set_ylabel('Test Statistic', fontsize=13)
    ax.set_title(title or f'{qr_result.test_name} — Quantile Profile',
                 fontsize=16, fontweight='bold')
    ax.legend(facecolor=COLORS['card'], edgecolor=COLORS['grid'])
    ax.grid(True, alpha=0.2)
    # Highlight rejections
    for i, tau in enumerate(taus):
        cv = cvs[i] if not np.isnan(cvs[i]) else -99
        if stats[i] < cv:
            ax.annotate('✓', (tau, stats[i]), ha='center', va='bottom',
                        fontsize=14, color=COLORS['accent'], fontweight='bold')
    plt.tight_layout()
    return fig


def plot_comparison_table(results, title="Unit Root Test Comparison"):
    """
    Create a visual comparison table of multiple test results.

    Parameters
    ----------
    results : list of TestResult
    """
    _setup_style()
    n = len(results)
    fig, ax = plt.subplots(figsize=(16, max(4, 1.2 * n + 2)))
    ax.axis('off')

    headers = ['Test', 'Statistic', 'k*', 'Lag', 'CV 1%', 'CV 5%', 'CV 10%',
               'Reject 5%']
    rows = []
    for r in results:
        stat_fmt = f"{r.statistic:.4f}"
        rej = '✓ Yes' if r.reject_5 else '✗ No'
        rows.append([r.test_name, stat_fmt, f"{r.optimal_k}", f"{r.optimal_lag}",
                     f"{r.cv_1:.3f}", f"{r.cv_5:.3f}", f"{r.cv_10:.3f}", rej])

    table = ax.table(cellText=rows, colLabels=headers, loc='center',
                     cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    # Style
    for i in range(len(headers)):
        table[0, i].set_facecolor(COLORS['primary'])
        table[0, i].set_text_props(color='white', fontweight='bold')
    for i in range(1, n + 1):
        for j in range(len(headers)):
            table[i, j].set_facecolor(COLORS['card'])
            table[i, j].set_text_props(color=COLORS['text'])
        # Color rejection column
        if results[i-1].reject_5:
            table[i, 7].set_text_props(color=COLORS['accent'], fontweight='bold')
        else:
            table[i, 7].set_text_props(color=COLORS['danger'])

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20,
                 color=COLORS['text'])
    plt.tight_layout()
    return fig


def plot_all_tests(y, series_name="Series", model=1, pmax=12):
    """
    Run ALL tests on a series and produce a comprehensive visual dashboard.
    """
    from . import (kss, fourier_kss, fourier_kruse, ffkruse,
                   fourier_sollis, ffsollis, kss_ff, wavelet_kss)

    results = []
    for fn, name in [(kss, 'kss'), (fourier_kss, 'fourier_kss'),
                     (fourier_kruse, 'fourier_kruse')]:
        try:
            if name == 'kss':
                r = fn(y, model=max(model, 2), pmax=pmax)
            else:
                r = fn(y, model=model, pmax=pmax)
            results.append(r)
        except Exception:
            pass

    for fn in [ffkruse, fourier_sollis, ffsollis, kss_ff, wavelet_kss]:
        try:
            r = fn(y, model=model, pmax=pmax)
            results.append(r)
        except Exception:
            pass

    if results:
        fig = plot_comparison_table(results, title=f"Nonlinear Unit Root Tests — {series_name}")
        return fig, results
    return None, []
