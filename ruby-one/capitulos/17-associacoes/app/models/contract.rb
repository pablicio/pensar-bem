class Contract < ApplicationRecord
  belongs_to :equipment

  scope :active, -> { where(status: "active") }
  scope :current, ->(hoje = Date.current) {
    active.where("end_date >= ?", hoje)
  }
end
