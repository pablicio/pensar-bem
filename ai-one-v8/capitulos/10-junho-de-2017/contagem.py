from torch import nn

# a tabela do artigo: modelo base
d, f, h, N, V = 512, 2048, 8, 6, 37000


def atencao(d):
    """W_Q, W_K, W_V e W_O, com os seus vieses."""
    return 4 * d * d + 4 * d


def ffn(d, f):
    """Duas camadas lineares, d -> f -> d."""
    return 2 * d * f + f + d


def norma(d):
    """Ganho e deslocamento da normalização de camada."""
    return 2 * d


cod = atencao(d) + ffn(d, f) + 2 * norma(d)
dec = 2 * atencao(d) + ffn(d, f) + 3 * norma(d)
emb = V * d                # um embedding só, entrada e saída
total = N * cod + N * dec + 2 * norma(d) + emb
print(f"uma camada do codificador:   {cod:12,}")
print(f"uma camada do decodificador: {dec:12,}")
print(f"6 + 6 camadas:               {N * (cod + dec):12,}")
print(f"embedding compartilhado:     {emb:12,}")
print(f"total pela fórmula:          {total:12,}")

modelo = nn.Transformer(d_model=d, nhead=h,
                        num_encoder_layers=N,
                        num_decoder_layers=N,
                        dim_feedforward=f, batch_first=True)
contados = sum(p.numel() for p in modelo.parameters()) + emb
print(f"total no PyTorch:            {contados:12,}")

# o custo do treino: cerca de 6 operações por parâmetro e token
tokens = 100_000 * 50_000     # passos × tokens por lote
print(f"6 N D = {6 * total * tokens:.1e} operações")
