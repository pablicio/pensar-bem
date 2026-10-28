class Contract < ApplicationRecord
  has_many :reservations

  after_save :register_reservation, if: :became_active?

  private

  def became_active?
    saved_change_to_status? && status == "active"
  end

  def register_reservation
    reservations.find_or_create_by!(
      equipment: equipment,
      starts_on: start_date,
      ends_on: end_date,
    )
  end
end
