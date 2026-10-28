class Reserva
  include Billable

  # ... attr_reader e initialize

  def valor_das_diarias
    super * 9 / 10
  end
end

puts Reserva.new(diaria: 21_000, dias: 4).total
