import hashlib
from pathlib import Path

brutos = Path("dados/brutos")
arquivos = [p for p in brutos.rglob("*") if p.is_file()]
print(len(arquivos), "arquivos")
for nome in ["cadastro_cooperados.xlsx",
             "RATEIO_FINAL_v7_AGORA_VAI.xlsx",
             "envios/rateio_2027-02.csv"]:
    resumo = hashlib.sha256((brutos / nome).read_bytes())
    print(resumo.hexdigest()[:16], nome)
