def reservar(patrimonio, ocupados)
  if ocupados.key?(patrimonio)
    raise EquipamentoOcupado.new(
      patrimonio: patrimonio,
      contrato: ocupados[patrimonio],
    )
  end

  puts "#{patrimonio} reservado"
end

ocupados = { "PT-118" => "CT-2041" }

begin
  reservar("PT-118", ocupados)
rescue EquipamentoOcupado => e
  puts "Não dá: #{e.message}."
  puts "Ligue para o dono do #{e.contrato}."
end
