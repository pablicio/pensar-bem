situacao =
  if status == "active" && fim >= hoje
    "ocupado"
  else
    "livre"
  end

puts situacao
