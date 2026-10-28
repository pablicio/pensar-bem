import numpy as np

rng = np.random.default_rng(0)
N = 100_000
print("     d   média q·k   variância q·k   variância q·k/√d")
for d in [4, 16, 64, 256, 1024]:
    q = rng.normal(size=(N, d))
    k = rng.normal(size=(N, d))
    s = (q * k).sum(axis=1)          # N produtos escalares
    print(f"{d:6} {s.mean():11.3f} {s.var():15.1f}"
          f" {(s / np.sqrt(d)).var():18.3f}")
