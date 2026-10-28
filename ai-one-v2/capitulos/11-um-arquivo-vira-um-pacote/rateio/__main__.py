"""python -m rateio: o rateio de uma usina."""
import sys

from rateio import __version__
from rateio.cadastro import ler_cooperados

CADASTRO = "dados/brutos/cadastro_cooperados.xlsx"
AJUDA = """rateio {versao}, Coopersol Cerrado

uso: python -m rateio --usina NOME --geracao KWH
     python -m rateio --ajuda

  --usina NOME    a usina, como no cadastro
  --geracao KWH   a geração da usina no mês, em kWh"""


def valor_de(argumentos, opcao):
    """O que vem depois de uma opção na linha de comando."""
    return argumentos[argumentos.index(opcao) + 1]


def main(argumentos):
    if not argumentos or "--ajuda" in argumentos:
        print(AJUDA.format(versao=__version__))
        return 0
    usina = valor_de(argumentos, "--usina")
    geracao = float(valor_de(argumentos, "--geracao"))
    da_usina = [c for c in ler_cooperados(CADASTRO)
                if c.usina == usina and c.situacao == "Ativo"]
    total = sum(c.credito(geracao)[0] for c in da_usina)
    print(f"{usina}: {len(da_usina)} cooperados ativos")
    print(f"créditos: {total:.2f} kWh de {geracao:.3f}")
    print(f"sobra: {geracao - total:.3f} kWh")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
