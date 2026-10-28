import math

import torch

x = torch.linspace(-4, 4, 8001, dtype=torch.float64)
exata = x * 0.5 * (1 + torch.erf(x / math.sqrt(2)))   # x Φ(x)
c = math.sqrt(2 / math.pi)
aprox = 0.5 * x * (1 + torch.tanh(c * (x + 0.044715 * x**3)))
print(f"maior diferença exata x tanh: "
      f"{(exata - aprox).abs().max():.1e}")
print(f"mínimo da GELU: {exata.min():.4f}"
      f" em x = {x[exata.argmin()]:.3f}")
print("PyTorch = fórmula exata:",
      torch.allclose(torch.nn.functional.gelu(x), exata))
