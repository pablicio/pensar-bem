"""O plantão com a regra do simulado (capítulo 28)."""
from rio.plantao import Plantao

ESPERA = 6          # rodadas abaixo da cota antes do fim


class PlantaoComEspera(Plantao):
    """O alarme só desliga depois de ESPERA rodadas seguidas
    com o teto abaixo da cota."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abaixo = 0

    def hora(self, tele):
        ligado = self.alarme
        linha = super().hora(tele)
        if ligado and not linha["alarme"]:
            self.abaixo += 1
            if self.abaixo < ESPERA:      # ainda não: segura
                linha["alarme"], linha["nota"] = True, ""
                self.alarme = True
                return linha
        self.abaixo = 0
        return linha
