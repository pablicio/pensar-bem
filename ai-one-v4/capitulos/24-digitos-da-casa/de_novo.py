import torch

from leitora.calibra import erro_de_calibracao, temperatura
from leitora.carrega import leitora
from leitora.dados import CaixasDoCartao
from leitora.decide import REVISAO, limiar

valid = CaixasDoCartao("validacao")
cartoes = list(dict.fromkeys(o[0] for o in valid.origem))
ajuste = torch.tensor([o[0] in cartoes[:30]
                       for o in valid.origem])
confere = ~ajuste
alvo = valid.rotulos[confere]
escritas = 738_000 * len(valid) / (60 * 30)

for nome in ["mnist", "casa"]:
    modelo = leitora(f"modelos/leitora_{nome}.pt")
    with torch.no_grad():
        z = modelo(valid.imagens)
    t = temperatura(z[ajuste], valid.rotulos[ajuste])
    p = (z[confere] / t).softmax(dim=1)
    confianca, leu = p.max(dim=1)
    certo = leu == alvo
    le = confianca >= limiar(160)
    revisao = (~le).float().mean() * escritas * REVISAO
    erros = (1 - confianca[le]).sum() / len(le) * escritas
    print(f"leitora_{nome}: temperatura {t:.3f},"
          f" ECE {erro_de_calibracao(p, alvo):.2%}")
    uns = certo[alvo == 1].float().mean()
    revisa = 1 - le.float().mean()
    print(f"  uns lidos certo: {uns:.1%}")
    print(f"  revisa {revisa:.1%}: R$ {revisao:,.0f},"
          f" {erros:.0f} erros esperados")
