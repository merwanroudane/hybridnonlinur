"""Quick test of all 13 tests in hybridnonlinur."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import hybridnonlinur as hnl

np.random.seed(42)
T = 200
y = np.cumsum(np.random.randn(T))

print(f"hybridnonlinur v{hnl.__version__}")
print(f"Author: {hnl.__author__}")
print(f"Series: T={T}, random walk")
print("=" * 60)

# Run all standard tests
results = hnl.run_all(y, series_name='Simulated RW', model=1, verbose=False)
print(f"\nrun_all completed: {len(results)} tests")
print("-" * 60)
for name, r in results.items():
    if hasattr(r, 'statistic'):
        stat = r.statistic
        rej = r.reject_5
        print(f"  {name:25s}  stat={stat:>10.4f}  reject@5%={'Yes' if rej else 'No'}")
    else:
        print(f"  {name:25s}  QKS={r.qks_stat:>10.4f}")

# Test the two bootstrap variants separately
print("\n--- Bootstrap tests (small nboot for speed) ---")
r_boot = hnl.fourier_kss_bootstrap(y, model=1, nboot=100)
print(f"  Fourier-KSS Bootstrap     stat={r_boot.statistic:>10.4f}  "
      f"cv5%={r_boot.cv_5:.4f}")

r_qrfkss = hnl.qr_fourier_kss(y, model=1, taus=np.array([0.25, 0.5, 0.75]),
                                 nboot=50)
print(f"  QR-Fourier-KSS            QKS={r_qrfkss.qks_stat:>10.4f}")

print("\n" + "=" * 60)
print("ALL 13 TESTS PASSED SUCCESSFULLY")
print("=" * 60)

# Generate comparison plot
import matplotlib
matplotlib.use('Agg')
fig, res = hnl.plot_all_tests(y, series_name='Random Walk', model=1)
if fig:
    fig.savefig('test_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\nComparison plot saved: test_comparison.png")
