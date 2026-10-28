import torch


def perda(w, x):
    return torch.tanh(w * x).sum() ** 2


for tipo in (torch.float32, torch.float64):
    torch.manual_seed(0)
    w = torch.randn(1000, dtype=tipo, requires_grad=True)
    x = torch.randn(1000, dtype=tipo)
    perda(w, x).backward()
    analitico = w.grad[0].item()
    with torch.no_grad():                   # sem montar grafo
        h = 1e-6
        mais, menos = w.clone(), w.clone()
        mais[0] += h
        menos[0] -= h
        dif = perda(mais, x) - perda(menos, x)
        num = (dif / (2 * h)).item()
    rel = abs(analitico - num) / abs(analitico)
    print(f"{str(tipo):13}: autograd {analitico:.6f},"
          f" numérica {num:.6f}, dif. rel. {rel:.0e}")
