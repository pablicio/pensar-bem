module Billable
  TAXA_DE_ENTREGA = 35_000

  def total
    valor_das_diarias + TAXA_DE_ENTREGA
  end

  def valor_das_diarias
    diaria * dias
  end
end
