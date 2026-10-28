status = "reserved"

rotulo =
  case status
  when "active" then "Em uso"
  when "reserved" then "Reservado"
  when "cancelled", "closed" then "Encerrado"
  else "Desconhecido"
  end

puts rotulo
