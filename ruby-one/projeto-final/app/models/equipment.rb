class Equipment < ApplicationRecord
  has_many :contracts

  def self.available(hoje = Date.current)
    ocupados = Contract.current(hoje).select(:equipment_id)
    where.not(id: ocupados)
  end

  def available?(hoje = Date.current)
    contracts.current(hoje).none?
  end
end
