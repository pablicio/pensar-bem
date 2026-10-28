validate :equipamento_livre_no_periodo

def equipamento_livre_no_periodo
  return if equipment_id.blank? || start_date.blank? ||
            end_date.blank?

  conflito = Contract
    .where(equipment_id: equipment_id)
    .where(status: %w[active reserved])
    .where.not(id: id)
    .where("start_date <= ? AND end_date >= ?", end_date, start_date)
    .first

  return unless conflito

  errors.add(:equipment,
             "já está no contrato #{conflito.code} nesse período")
end
