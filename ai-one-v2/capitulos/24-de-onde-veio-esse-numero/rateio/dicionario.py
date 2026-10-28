"""Dicionário de dados: o que se sabe de cada fonte bruta."""

FONTES = {
    "corumba": {
        "arquivo": "inversores/corumba/corumba_AAAA-MM.csv",
        "formato": "Latin-1; ';'; linha de título; '1.234,5'",
        "unidade": "Wh (kWh de 9 a 11/2/2027)",
        "horario": "Brasília, sem fuso",
        "colunas": ["Data", "Hora", "Inversor", "Energia"]},
    "cocalzinho": {
        "arquivo": "inversores/cocalzinho/AAAA-MM-DD.json",
        "formato": "JSON da API, um arquivo por dia",
        "unidade": "kWh",
        "horario": "Brasília até 11/2/2027; UTC ('Z') depois",
        "colunas": ["inversor", "inicio", "energia_kwh"]},
    "abadiania": {
        "arquivo": "inversores/abadiania/"
                   "abadiania_AAAA-MM.csv",
        "formato": "UTF-8 com BOM; ','; ponto decimal",
        "unidade": "kWh",
        "horario": "Brasília, sem fuso",
        "colunas": ["timestamp", "inverter", "energy_kwh"]},
    "cadastro": {
        "arquivo": "cadastro_cooperados.xlsx",
        "formato": "Excel; CPF como texto, com ou sem pontos",
        "unidade": "cota em %; consumo em kWh/mês",
        "horario": "-",
        "colunas": ["Código", "Nome", "CPF", "Tipo", "Usina",
                    "Cota (%)", "Consumo médio (kWh)",
                    "Situação", "Atualizado em"]},
}
