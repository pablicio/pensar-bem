"""As mensagens do canal, montadas por partes.

A classe sai do sentido, não de palavras exclusivas: "presa
no telhado" é risco agora e informação se já passou; "a
barragem rompeu" é boato afirmado e informação perguntado."""
import re
import unicodedata

CLASSES = ["risco", "ajuda", "info", "boato"]
BAIRROS = ["Centro", "Barra", "Ponte de Ferro", "Vila Nova",
           "Testo Alto", "Encano", "Morro das Pedras",
           "Rio Morto", "Alto Feliz", "Volta Grande",
           "Jardim Hoffmann", "São Pedro"]
RUAS = ["rua Itoupava", "rua XV de Novembro",
        "rua dos Imigrantes", "rua das Palmeiras",
        "rua Bruno Klitzke", "rua Frederico Jensen",
        "rua São Paulo", "rua Amazonas", "rua Henrique Conrad",
        "rua Sete de Setembro", "rua da Ponte",
        "rua Otto Grützmacher", "estrada do Encano",
        "rua Marechal Deodoro", "rua das Missões"]
EXTENSO = ["", "uma", "duas", "três", "quatro", "cinco",
           "seis", "sete", "oito", "nove", "dez", "onze",
           "doze"]

# quem: (como se escreve, estar, estar no passado, conseguir)
EU = ("eu", "tô", "tava", "consigo")
NOS = ("nós", "estamos", "tava", "conseguimos")
OUTROS = [("minha mãe", "tá", "tava", "consegue"),
          ("minha vizinha", "tá", "tava", "consegue"),
          ("a família do lado", "tá", "tava", "consegue"),
          ("meu avô", "tá", "tava", "consegue"),
          ("o pessoal da casa da frente", "tá", "tava",
           "consegue")]

PERIGO = ["{estar} no telhado esperando o barco",
          "{estar} no segundo andar e a água não para de "
          "subir",
          "não {conseguir} sair de casa, a correnteza tá "
          "forte",
          "{estar} com a água no peito",
          "{estar} em cima do armário sem ter pra onde ir",
          "{estar} dentro do carro que a água arrastou"]
# o mesmo perigo, já passado: "tava no telhado ... mas já
# saímos"
SAIU = ["mas o barco já tirou", "mas os bombeiros já tiraram",
        "mas a água baixou", "mas agora já saímos"]
BEM = ["{estar} bem, sem perigo", "não {estar} em perigo",
       "{estar} na casa da minha irmã, longe da água"]
PRECISA = ["precisamos de água potável",
           "falta colchão e cobertor",
           "acabou o remédio de pressão",
           "a casa ficou cheia de lama",
           "o abrigo tá lotado, tem outro lugar?",
           "precisamos de comida pra {pessoas}"]
CONTA = ["a {rua} tá alagada, carro não passa",
         "já baixou a água na {rua}",
         "o rio vai subir mais hoje?",
         "a escola do {bairro} abre amanhã?",
         "qual o nível do rio agora na ponte?",
         "o ônibus pro {bairro} tá passando?"]
BOATO = ["a barragem de [Taió|Ituporanga] rompeu",
         "vão abrir todas as comportas da barragem",
         "o exército vai evacuar a cidade inteira",
         "vai faltar água por quinze dias",
         "a ponte de ferro rachou e vai cair"]
REPASSA = ["repassem", "compartilhem",
           "meu primo que trabalha lá falou", "saiam de casa",
           "urgente"]
CONTEXTO = ["choveu a noite toda", "a luz acabou faz uma hora",
            "o ribeirão atrás de casa encheu muito rápido",
            "liguei no 193 e ninguém atendeu"]


def escolhe(sorteio, lista):
    return lista[int(sorteio.integers(len(lista)))]


def conjuga(frase, quem):
    nome, estar, passado, conseguir = quem
    return frase.format(estar=estar, passado=passado,
                        conseguir=conseguir)


def oracao(sorteio, lista, quem):
    """Uma oração com o sujeito escrito ou só o verbo."""
    if lista == "passou":
        texto = escolhe(sorteio, PERIGO).format(
            estar=quem[2], conseguir="conseguia")
        texto += " " + escolhe(sorteio, SAIU)
    else:
        texto = conjuga(escolhe(sorteio, lista), quem)
    if quem in (EU, NOS) and sorteio.random() < 0.6:
        return texto
    return quem[0] + " " + texto


def pessoas_txt(sorteio, n):
    if n == 1:
        return "uma pessoa"
    return escolhe(sorteio, [f"{n} pessoas",
                             f"{EXTENSO[n]} pessoas",
                             f"somos {n}"])


def endereco(sorteio, campos, usados, com_numero=True):
    partes = [campos["rua"]]
    usados["rua"] = campos["rua"]
    if com_numero:
        partes[0] += f" {campos['numero']}"
        usados["numero"] = campos["numero"]
    if sorteio.random() < 0.85:
        partes.append(campos["bairro"])
        usados["bairro"] = campos["bairro"]
    return ", ".join(partes)


def mensagem(sorteio, classe, campos):
    """O texto de uma mensagem e os campos que ele contém."""
    usados = {}
    eu = EU if sorteio.random() < 0.5 else NOS
    outro = escolhe(sorteio, OUTROS)
    if classe == "risco":
        jeito = sorteio.random()
        if jeito < 0.35:
            nucleo = oracao(sorteio, PERIGO, eu)
        elif jeito < 0.7:
            nucleo = oracao(sorteio, PERIGO, outro)
        else:   # eu estou bem, mas o outro não
            nucleo = (oracao(sorteio, BEM, eu) + " mas "
                      + oracao(sorteio, PERIGO, outro))
        if sorteio.random() < 0.5:
            n = campos["pessoas"]
            nucleo += ", " + pessoas_txt(sorteio, n)
            usados["pessoas"] = n
        partes = [nucleo, endereco(sorteio, campos, usados)]
        if sorteio.random() < 0.5:
            grito = escolhe(sorteio, ["socorro", "urgente",
                                      "pelo amor de deus"])
            partes.insert(0, grito)
    elif classe == "ajuda":
        pedido = escolhe(sorteio, PRECISA)
        if "{pessoas}" in pedido:
            n = campos["pessoas"]
            usados["pessoas"] = n
            pedido = pedido.format(
                pessoas=pessoas_txt(sorteio, n))
        com_numero = sorteio.random() < 0.6
        onde = endereco(sorteio, campos, usados, com_numero)
        partes = [pedido, onde]
        if sorteio.random() < 0.4:
            lista = "passou" if sorteio.random() < 0.5 else BEM
            partes.insert(0, oracao(sorteio, lista, eu))
    elif classe == "info":
        jeito = sorteio.random()
        if jeito < 0.5:
            frase = escolhe(sorteio, CONTA)
            if "{rua}" in frase:
                usados["rua"] = campos["rua"]
            if "{bairro}" in frase:
                usados["bairro"] = campos["bairro"]
            partes = [frase.format(**campos)]
        elif jeito < 0.7:      # um perigo que já passou
            partes = [oracao(sorteio, "passou", outro),
                      oracao(sorteio, BEM, eu)]
        elif jeito < 0.85:     # o boato, perguntado ou negado
            boato = escolhe(sorteio, BOATO)
            partes = [escolhe(sorteio, [
                f"é verdade que {boato}?", f"{boato} mesmo?",
                f"não é verdade que {boato}, "
                "a defesa civil desmentiu"])]
        else:
            partes = [oracao(sorteio, BEM, eu),
                      "não precisa mandar ninguém"]
    else:
        partes = [escolhe(sorteio, BOATO)]
        if sorteio.random() < 0.3:
            partes[0] = ("estão pedindo socorro no "
                         f"{campos['bairro']} porque "
                         f"{partes[0]}")
        if sorteio.random() < 0.7:
            partes.append(escolhe(sorteio, REPASSA))
    texto = ", ".join(partes)
    texto = re.sub(r"\[([^\]]*)\]",
                   lambda m: escolhe(sorteio,
                                     m.group(1).split("|")),
                   texto)
    if sorteio.random() < 0.35:
        antes = [escolhe(sorteio, CONTEXTO)
                 for _ in range(int(sorteio.integers(1, 3)))]
        texto = ". ".join(dict.fromkeys(antes)) + ". " + texto
    return texto, usados


ABREVIA = {"você": "vc", "que": "q", "por favor": "pfv",
           "está": "tá", "aqui": "aki", "muito": "mto",
           "também": "tb", "porque": "pq", "estamos": "tamo"}


def sem_acento(texto):
    nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfd
                   if unicodedata.category(c) != "Mn")


def escreve_mal(sorteio, texto):
    """Do jeito que se digita no celular, com pressa."""
    if sorteio.random() < 0.5:
        for certo, curto in ABREVIA.items():
            texto = re.sub(rf"\b{certo}\b", curto, texto)
    if sorteio.random() < 0.7:
        texto = texto.lower()
    if sorteio.random() < 0.4:
        texto = sem_acento(texto)
    palavras = texto.split(" ")
    for i, p in enumerate(palavras):
        if (len(p) > 3 and p.isalpha()
                and sorteio.random() < 0.04):
            j = int(sorteio.integers(1, len(p) - 1))
            palavras[i] = p[:j] + p[j + 1] + p[j] + p[j + 2:]
    texto = " ".join(palavras)
    if sorteio.random() < 0.2:
        texto += "!" * int(sorteio.integers(1, 4))
    return texto
