import numpy as np

# L(N, D) = E + A / N^alfa + B / D^beta
AJUSTES = {
    "Hoffmann 2022": (1.69, 406.4, 410.7, 0.34, 0.28),
    "Besiroglu 2024": (1.8172, 482.01, 2085.43,
                       0.3478, 0.3658),
}


def perda(N, D, E, A, B, alfa, beta):
    return E + A / N ** alfa + B / D ** beta


def otimo(C, E, A, B, alfa, beta):
    """O N e o D que minimizam a perda com 6 N D = C."""
    G = (alfa * A / (beta * B)) ** (1 / (alfa + beta))
    N = G * (C / 6) ** (beta / (alfa + beta))
    return N, C / (6 * N)


C = 3.14e23                          # o cômputo do GPT-3
Ns = np.geomspace(1e9, 1e12, 100_000)
for nome, p in AJUSTES.items():
    N, D = otimo(C, *p)
    busca = Ns[np.argmin(perda(Ns, C / (6 * Ns), *p))]
    print(f"{nome}: N {N:.2e} (busca {busca:.2e})")
    print(f"  D {D:.2e}, D/N {D / N:.0f}")
    print(f"  perda do GPT-3 {perda(1.75e11, 3.0e11, *p):.3f},"
          f" no ótimo {perda(N, D, *p):.3f}")

# os diários do Brasil, pela densidade do corpus deste livro
por_municipio = 1_454_052 / 40          # tokens por ano
D_br = por_municipio * 5570 * 10      # 5.570 cidades, 10 anos
print(f"\ndiários do Brasil em 10 anos: {D_br:.1e} tokens")
print(f"  {D_br / 3.0e11:.2%} dos tokens do GPT-3")
print(f"N com 20 tokens por parâmetro: {D_br / 20:.1e}")
