class Contrato
  def self.da_planilha(linha)
    new(
      codigo: linha.fetch("Contrato").strip,
      patrimonio: linha.fetch("Patrimônio").strip.upcase,
      inicio: Date.strptime(linha.fetch("Saída"), "%d/%m/%Y"),
      fim: Date.strptime(linha.fetch("Devolução"), "%d/%m/%Y"),
      status: "active",
    )
  end
end

c = Contrato.da_planilha(linha)
