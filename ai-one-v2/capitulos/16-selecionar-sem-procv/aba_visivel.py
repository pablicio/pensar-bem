import pandas as pd

planilha = "dados/brutos/RATEIO_FINAL_v7_AGORA_VAI.xlsx"
visivel = pd.read_excel(planilha, sheet_name="Rateio")
print(visivel["kWh"].dtype)
print(visivel["kWh"].notna().sum(), "células com número")
