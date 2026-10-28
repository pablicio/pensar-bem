class Reservation < ApplicationRecord
  include Billable

  def total
    daily_rate_cents * days
  end
end
