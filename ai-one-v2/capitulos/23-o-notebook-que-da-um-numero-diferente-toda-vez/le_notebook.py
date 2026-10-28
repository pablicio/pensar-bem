import json

with open("rateio.ipynb", encoding="utf-8") as f:
    notebook = json.load(f)

for n, celula in enumerate(notebook["cells"], start=1):
    fonte = "".join(celula["source"])
    primeira = fonte.splitlines()[0][:40]
    conta = celula["execution_count"]
    print(f"célula {n}  [{conta:>2}]  {primeira}")
    for saida in celula["outputs"]:
        print("          saída:", saida["text"].strip())
