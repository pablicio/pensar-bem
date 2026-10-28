import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from lupa.corpus import prepara
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()

# os 100 tokens antes de cada CNPJ de 2027 e os 18 do CNPJ
chave = tok.codifica(" CNPJ nº")
pos = [i for i in range(100, len(teste) - 20)
       if teste[i - 1:i + 1].tolist() == chave]
janelas = torch.stack([teste[i - 99:i + 19] for i in pos])
with torch.no_grad():
    logp = F.log_softmax(modelo(janelas[:, :-1]), -1)
# a probabilidade que o modelo deu a cada token verdadeiro
alvo = janelas[:, 1:]
p = logp.gather(-1, alvo[..., None])[..., 0].exp()[:, -18:]

media = p.mean(0)
digito = [i for i in range(18) if i not in (2, 6, 10, 15)]
print("dígito  token  P média do certo")
for n, i in enumerate(digito, start=1):
    print(f"{n:6}  {i:5}  {media[i].item():.3f}")

fig, eixo = plt.subplots(figsize=(6, 3))
eixo.bar(range(1, 15), media[digito])
eixo.axhline(0.1, ls="--", color="gray", label="acaso (1/10)")
eixo.set_xticks(range(1, 15))
eixo.set_xlabel("dígito do CNPJ")
eixo.set_ylabel("P(dígito certo)")
eixo.legend()
fig.tight_layout()
fig.savefig("digitos.png", dpi=300)
