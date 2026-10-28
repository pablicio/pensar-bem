hoje = Date.new(2026, 3, 19)

a = Contrato.new(codigo: "CT-2041", patrimonio: "PT-118",
                 inicio: Date.new(2026, 3, 3),
                 fim: Date.new(2026, 6, 30), status: "active")
b = Contrato.new(codigo: "CT-2012", patrimonio: "PT-118",
                 inicio: Date.new(2026, 1, 5),
                 fim: Date.new(2026, 3, 2), status: "active")

puts a.ativo?(hoje)
puts b.ativo?(hoje)
