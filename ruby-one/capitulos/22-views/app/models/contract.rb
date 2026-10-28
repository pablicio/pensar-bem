def occupying?(hoje = Date.current)
  return false unless status == "active"

  end_date >= hoje || returned_at.nil?
end

def overdue?(hoje = Date.current)
  occupying?(hoje) && end_date < hoje
end
