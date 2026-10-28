import unicodedata


def utf8(c):
    """Os bytes UTF-8 de um ponto de código, pela regra dos
    prefixos: 0xxxxxxx, 110xxxxx 10xxxxxx, 1110xxxx 10xxxxxx
    10xxxxxx, 11110xxx e três 10xxxxxx."""
    p = ord(c)
    if p < 0x80:
        return bytes([p])
    if p < 0x800:
        return bytes([0xC0 | p >> 6, 0x80 | p & 0x3F])
    if p < 0x10000:
        return bytes([0xE0 | p >> 12, 0x80 | p >> 6 & 0x3F,
                      0x80 | p & 0x3F])
    return bytes([0xF0 | p >> 18, 0x80 | p >> 12 & 0x3F,
                  0x80 | p >> 6 & 0x3F, 0x80 | p & 0x3F])


for c in ["a", "ç", "º", "€", "😀"]:
    b = utf8(c)
    bits = " ".join(f"{x:08b}" for x in b)
    ok = "ok" if b == c.encode("utf-8") else "ERRO"
    print(f"{c}  U+{ord(c):05X}  {bits:35} {ok}")

for forma in ["NFC", "NFD"]:
    s = unicodedata.normalize(forma, "licitação")
    print(forma, len(s), "pontos,",
          len(s.encode("utf-8")), "bytes:",
          " ".join(f"U+{ord(c):04X}" for c in s[6:]))
