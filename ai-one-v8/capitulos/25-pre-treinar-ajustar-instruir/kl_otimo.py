import torch

# cinco respostas possíveis, um modelo de referência e notas
_ = torch.manual_seed(0)
ref = torch.softmax(torch.randn(5), 0)
r = torch.tensor([1.0, 0.0, 2.0, -1.0, 0.5])
beta = 0.5

# a solução fechada: pi* proporcional a ref * exp(r / beta)
fechada = ref * torch.exp(r / beta)
fechada = fechada / fechada.sum()

# subir o objetivo E_pi[r] - beta KL(pi || ref) por gradiente
z = torch.zeros(5, requires_grad=True)
opt = torch.optim.Adam([z], lr=0.05)
for _ in range(3000):
    pi = torch.softmax(z, 0)
    kl = (pi * (pi / ref).log()).sum()
    objetivo = (pi * r).sum() - beta * kl
    opt.zero_grad()
    (-objetivo).backward()
    opt.step()
pi = torch.softmax(z, 0).detach()
print("fechada:  ", [round(x, 4) for x in fechada.tolist()])
print("gradiente:", [round(x, 4) for x in pi.tolist()])

# a nota que o DPO lê da política: beta log(pi / ref)
implicita = beta * (pi / ref).log()
print("r - nota implícita:",
      [round(x, 4) for x in (r - implicita).tolist()])
