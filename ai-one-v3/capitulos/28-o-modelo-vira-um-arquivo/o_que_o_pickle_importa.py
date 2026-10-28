import pickle
from collections import Counter

from inspeciona import fora_do_esperado, importados
from risco.campeao import treinado

dados = pickle.dumps(treinado())     # o nosso modelo, em bytes
nomes = importados(dados)
print(f"{len(dados):,} bytes; {len(nomes)} nomes importados")
print(Counter(n.split(".")[0] for n in nomes))
fora = fora_do_esperado(nomes)
print("fora da lista esperada:", fora or "nenhum")
