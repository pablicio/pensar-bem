class Contrato
  include Comparable

  attr_reader :fim

  def initialize(fim:)
    @fim = fim
  end

  def <=>(outro)
    fim <=> outro.fim
  end
end

a = Contrato.new(fim: Date.new(2026, 6, 30))
b = Contrato.new(fim: Date.new(2026, 4, 15))
puts a > b
