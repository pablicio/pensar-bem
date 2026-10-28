import torch

_ = torch.manual_seed(0)
A, b = torch.randn(20, 5), torch.randn(20)
theta = torch.randn(5, requires_grad=True)
nosso = theta.detach().clone()
opt = torch.optim.AdamW([theta], lr=0.1, betas=(0.9, 0.95),
                        eps=1e-8, weight_decay=0.1)
lr, b1, b2, eps, lam = 0.1, 0.9, 0.95, 1e-8, 0.1
m, v = torch.zeros(5), torch.zeros(5)

for t in range(1, 6):
    perda = ((A @ theta - b) ** 2).mean()
    opt.zero_grad()
    perda.backward()
    opt.step()

    g = 2 * A.T @ (A @ nosso - b) / 20     # o mesmo gradiente
    m = b1 * m + (1 - b1) * g
    v = b2 * v + (1 - b2) * g ** 2
    m_hat = m / (1 - b1 ** t)              # sem viés
    v_hat = v / (1 - b2 ** t)
    nosso = nosso - lr * lam * nosso       # decaimento
    nosso = nosso - lr * m_hat / (v_hat.sqrt() + eps)
    dif = (nosso - theta.detach()).abs().max().item()
    print(f"passo {t}: perda {perda.item():.4f}"
          f"  |nosso - AdamW| = {dif:.1e}")
