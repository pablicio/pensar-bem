API_STATUS = {
  "active" => "ativo",
  "reserved" => "reservado",
  "cancelled" => "cancelado",
  "closed" => "encerrado",
}.freeze

def as_api
  {
    codigo: code,
    patrimonio: equipment.patrimony,
    canteiro: site,
    status: API_STATUS.fetch(status),
    chegada: started_at&.iso8601,
    fim: end_date.iso8601,
  }
end
