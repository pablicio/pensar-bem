situacao = "livre"
if c.status == "active"
  situacao = "ocupado"
end
if c.end_date >= hoje
  situacao = "ocupado"
end
