class EquipamentoOcupado < StandardError
  attr_reader :patrimonio, :contrato

  def initialize(patrimonio:, contrato:)
    @patrimonio = patrimonio
    @contrato = contrato
    super("#{patrimonio} já está no contrato #{contrato}")
  end
end
