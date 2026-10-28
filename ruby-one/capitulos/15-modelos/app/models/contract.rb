class Contract < ApplicationRecord
  belongs_to :customer
  belongs_to :equipment
  has_many :reservations

  def active?
    status == "active" && end_date >= Date.today
  end
end
