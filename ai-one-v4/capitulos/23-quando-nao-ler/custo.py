import torch

from leitora.carrega import leitora
from leitora.dados import CaixasDoCartao
from leitora.decide import REVISAO, decide, limiar

valid = CaixasDoCartao("validacao")
with torch.no_grad():
    logitos = leitora()(valid.imagens)
cartoes = list(dict.fromkeys(o[0] for o in valid.origem))
confere = torch.tensor([o[0] in cartoes[30:]
                        for o in valid.origem])
logitos = logitos[confere]

# do conferido para o inverno: 738 mil caixas, nem todas
# escritas
escritas = 738_000 * len(valid) / (60 * 30)
print(f"caixas escritas no inverno: {escritas:,.0f}")
print(f"revisar tudo: R$ {738_000 * REVISAO:,.0f}\n")

print(f"{'erro custa':>10} {'limiar':>7} {'revisa':>7}"
      f" {'revisão':>10} {'erros':>6} {'total':>10}")
for custo_erro in [16, 160, 1600]:
    lim = limiar(custo_erro)
    _, confianca, le = decide(logitos, lim)
    revisao = (~le).float().mean() * escritas * REVISAO
    erros = (1 - confianca[le]).sum() / len(le) * escritas
    total = revisao + erros * custo_erro
    revisa = 1 - le.float().mean()
    print(f"R$ {custo_erro:7,} {lim:7.4f} {revisa:7.1%} R$"
          f" {revisao:7,.0f} {erros:6,.0f} R$ {total:7,.0f}")
