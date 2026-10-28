# frozen_string_literal: true

require "date"

CANTEIROS = {
  "Serra Azul - Contagem" => "contagem",
  "Serra Azul - Betim" => "betim",
}

def da_planilha(linha)
  {
    code: linha.fetch("Contrato").strip,
    equipment: linha.fetch("Patrimônio").strip.upcase,
    site: CANTEIROS.fetch(linha.fetch("Canteiro")),
    start_date: Date.strptime(linha.fetch("Saída"), "%d/%m/%Y"),
  }
end

def do_banco(registro)
  {
    code: registro.fetch(:code),
    equipment: registro.fetch(:equipment),
    site: registro.fetch(:site),
    start_date: registro.fetch(:start_date),
  }
end

planilha = {
  "Patrimônio" => "PT-118", "Contrato" => "CT-2041",
  "Canteiro" => "Serra Azul - Contagem", "Saída" => "03/03/2026",
}
banco = {
  code: "CT-2041", equipment: "PT-118", site: "contagem",
  start_date: Date.new(2026, 3, 3), responsible: "Helena",
}

puts da_planilha(planilha) == do_banco(banco)
