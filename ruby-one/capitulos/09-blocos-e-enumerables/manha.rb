# frozen_string_literal: true

contratos = [
  { code: "CT-2041", equipment: "PT-118", status: "active" },
  { code: "CT-2033", equipment: "PT-121", status: "cancelled" },
  { code: "CT-2050", equipment: "PT-140", status: "reserved" },
  { code: "CT-1987", equipment: "PT-133", status: nil },
]

contratos.each do |c|
  puts "#{c[:equipment]}: #{c[:status]}"
end
