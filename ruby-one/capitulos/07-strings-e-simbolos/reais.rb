# frozen_string_literal: true

def reais(centavos)
  inteiro = (centavos / 100).to_s
  com_ponto = inteiro.reverse.scan(/\d{1,3}/).join(".").reverse
  format("R$ %s,%02d", com_ponto, centavos % 100)
end

puts reais(181_980)
puts reais(360_000_000)
