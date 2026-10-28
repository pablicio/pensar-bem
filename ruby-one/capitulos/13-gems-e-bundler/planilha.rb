# frozen_string_literal: true

require "roo"

planilha = Roo::Spreadsheet.open("patio_SEMANAL.xlsx")
aba = planilha.sheet(0)

aba.each(contrato: "Contrato", patrimonio: "Patrimônio") do |linha|
  puts "#{linha[:patrimonio]} -> #{linha[:contrato]}"
end
