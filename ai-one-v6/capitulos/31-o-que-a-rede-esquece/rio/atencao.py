"""O extrator com atenção: o decoder olha de volta para a
mensagem inteira a cada caractere que escreve."""
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence
from torch.nn.utils.rnn import pad_packed_sequence

from rio.extrator import FIM, INICIO, Extrator


class ExtratorComAtencao(Extrator):
    def __init__(self, n_entrada, n_saida, dim=32, estado=128):
        super().__init__(n_entrada, n_saida, dim, estado)
        # o encoder lê nos dois sentidos, metade do estado cada
        self.encoder = nn.LSTM(dim, estado // 2,
                               batch_first=True,
                               bidirectional=True)
        self.compara = nn.Linear(estado, estado, bias=False)
        self.saida = nn.Linear(2 * estado, n_saida)

    def le(self, x, n):
        """Os estados do encoder em cada posição, e o final."""
        pacote = pack_padded_sequence(self.emb_e(x), n,
                                      batch_first=True,
                                      enforce_sorted=False)
        memoria, (h, c) = self.encoder(pacote)
        memoria, _ = pad_packed_sequence(
            memoria, batch_first=True, total_length=x.shape[1])
        # os dois sentidos juntos começam o decoder
        h = torch.cat([h[0], h[1]], dim=1)[None]
        c = torch.cat([c[0], c[1]], dim=1)[None]
        return memoria, (h, c)

    def olha(self, d, memoria, mascara):
        """Cada estado do decoder pondera as posições da
        mensagem pela semelhança com elas."""
        notas = self.compara(d) @ memoria.transpose(1, 2)
        notas = notas.masked_fill(~mascara[:, None, :], -1e9)
        pesos = torch.softmax(notas, dim=2)    # (lote, s, e)
        contexto = pesos @ memoria             # (lote, s, 128)
        junto = torch.cat([d, contexto], dim=2)
        return self.saida(junto), pesos

    def forward(self, x, n, y):
        memoria, estado = self.le(x, n)
        d, _ = self.decoder(self.emb_s(y[:, :-1]), estado)
        return self.olha(d, memoria, x != 0)[0]

    @torch.no_grad()
    def extrai(self, x, n, saida, maximo=60):
        self.eval()
        memoria, estado = self.le(x, n)
        mascara = x != 0
        atual = torch.full((len(x), 1), saida.numero[INICIO])
        gerado = []
        for _ in range(maximo):
            d, estado = self.decoder(self.emb_s(atual), estado)
            z, _ = self.olha(d, memoria, mascara)
            atual = z.argmax(2)
            gerado.append(atual)
        textos = []
        for seq in torch.cat(gerado, dim=1).tolist():
            texto = "".join(saida.tokens[i] for i in seq)
            textos.append(texto.split(FIM)[0])
        return textos
