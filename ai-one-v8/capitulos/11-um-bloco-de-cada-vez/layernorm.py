import torch

torch.manual_seed(0)
x = torch.randn(4, 8, dtype=torch.float64, requires_grad=True)
g = torch.randn(8, dtype=torch.float64)       # ganho
b = torch.randn(8, dtype=torch.float64)       # deslocamento
eps = 1e-5

# a ida, à mão
mu = x.mean(dim=-1, keepdim=True)
var = x.var(dim=-1, unbiased=False, keepdim=True)
sigma = torch.sqrt(var + eps)
xh = (x - mu) / sigma                         # x normalizado
y = g * xh + b
ref = torch.nn.functional.layer_norm(x, (8,), g, b, eps)
print(f"ida:   {(y - ref).abs().max():.1e}")

# a volta, à mão
dy = torch.randn(4, 8, dtype=torch.float64)
dxh = dy * g
dx = (dxh - dxh.mean(-1, keepdim=True)
      - xh * (dxh * xh).mean(-1, keepdim=True)) / sigma
(y * dy).sum().backward()
print(f"volta: {(dx - x.grad).abs().max():.1e}")

# a saída não muda se a entrada for esticada e deslocada
with torch.no_grad():
    z = torch.nn.functional.layer_norm(3 * x + 7, (8,), g, b,
                                       eps)
print(f"LN(3x + 7) - LN(x): {(z - ref).abs().max():.1e}")
