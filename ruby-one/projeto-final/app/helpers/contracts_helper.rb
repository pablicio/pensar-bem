module ContractsHelper
  def rotulo_de_ocupacao(contrato)
    if contrato.overdue?
      "Em uso, devolução atrasada"
    elsif contrato.occupying?
      "Em uso"
    else
      "Livre"
    end
  end
end
