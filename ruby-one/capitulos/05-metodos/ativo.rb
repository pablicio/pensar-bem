def ativo?(status:, fim:, hoje: Date.today)
  status == "active" && fim >= hoje
end

puts ativo?(status: "active", fim: Date.new(2026, 6, 30))
puts ativo?(fim: Date.new(2026, 6, 30), status: "cancelled")
