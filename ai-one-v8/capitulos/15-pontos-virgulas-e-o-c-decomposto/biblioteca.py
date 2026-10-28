import time

from tokenizers import (Regex, Tokenizer, decoders, models,
                        normalizers, pre_tokenizers, trainers)

from lupa.diario import atos
from lupa.extrator import limpa
from lupa.tokenizador import PEDACO, Tokenizador

corpus = atos()
treino = [a["texto"] for a in corpus if a["data"] < "2027"]
novos = [a["texto"] for a in corpus if a["data"] >= "2027"]
amostra = novos[:200]

tok = Tokenizer(models.BPE())
tok.normalizer = normalizers.Sequence([
    normalizers.NFC(), normalizers.Replace("-\n", "")])
tok.pre_tokenizer = pre_tokenizers.Sequence([
    pre_tokenizers.Split(Regex(PEDACO.pattern), "isolated"),
    pre_tokenizers.ByteLevel(add_prefix_space=False,
                             use_regex=False)])
tok.decoder = decoders.ByteLevel()
treinador = trainers.BpeTrainer(
    vocab_size=2000, special_tokens=["<|fim|>"],
    initial_alphabet=pre_tokenizers.ByteLevel.alphabet())

inicio = time.time()
tok.train_from_iterator(treino, treinador)
print(f"tokenizers: {time.time() - inicio:.2f} s,"
      f" {tok.get_vocab_size()} tokens")

nosso = Tokenizador()
nosso.treina(treino, 2000)
iguais = sum(len(tok.encode(t).ids) == len(nosso.codifica(t))
             for t in amostra)
print(f"atos com o mesmo número de tokens: {iguais}/200")
volta = all(tok.decode(tok.encode(t).ids) == limpa(t)
            for t in amostra)
print("ida e volta:", volta)
print(tok.encode(" Requalificação viária.").tokens)
