class Contract < ApplicationRecord
  has_many :reservations

  after_create :reserve_equipment
  after_save :register_reservation

  private

  def reserve_equipment
    reservations.create!(equipment: equipment,
                         starts_on: start_date, ends_on: end_date)
  end

  def register_reservation
    return unless status == "active"

    reservations.create!(equipment: equipment,
                         starts_on: start_date, ends_on: end_date)
  end
end
