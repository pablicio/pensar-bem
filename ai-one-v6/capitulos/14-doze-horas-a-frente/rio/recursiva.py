"""Prever várias horas com um modelo de uma hora só."""
import torch

ZERA = ("chuva", "sobe", "faltam")   # o que vira zero depois


def rola(modelo, x, escala, horas_frente):
    """Roda o modelo de uma hora `horas_frente` vezes, cada vez
    com uma linha nova na entrada, feita da previsão anterior.

    Para o futuro que não se conhece, a regra mais simples: não
    chove, as estações de cima ficam onde estão, nada falta."""
    colunas = list(escala.media.index)
    media = torch.tensor(escala.media.to_numpy(),
                         dtype=torch.float32)
    desvio = torch.tensor(escala.desvio.to_numpy(),
                          dtype=torch.float32)
    cidade = colunas.index("cidade")
    sobe = colunas.index("sobe_cidade")
    modelo.eval()
    with torch.no_grad():
        saida, estado = modelo.lstm(x)
        ultima = x[:, -1] * desvio + media     # em metros e mm
        variacao = torch.zeros(len(x))
        previstas = []
        for k in range(horas_frente):
            passo = modelo.saida(saida[:, -1])[:, 0] / 10
            variacao = variacao + passo
            previstas.append(variacao.clone())
            nova = ultima.clone()
            for j, nome in enumerate(colunas):
                if nome.startswith(ZERA):
                    nova[:, j] = 0.0
            nova[:, cidade] = ultima[:, cidade] + passo
            nova[:, sobe] = passo
            entrada = ((nova - media) / desvio)[:, None]
            saida, estado = modelo.lstm(entrada, estado)
            ultima = nova
    return torch.stack(previstas, dim=1).numpy()
