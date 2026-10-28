import unicodedata

exemplos = ["licitação", "Nº 001", "Art. 1º", "120 m²",
            "ﬁscal"]
print(f"{'texto':10}" + "".join(f"{f:>6}" for f in
                                ["NFC", "NFD", "NFKC"])
      + "  em NFKC")
for s in exemplos:
    formas = [unicodedata.normalize(f, s)
              for f in ["NFC", "NFD", "NFKC"]]
    tamanhos = "".join(f"{len(t):6}" for t in formas)
    print(f"{s:10}{tamanhos}  {formas[2]}")
