FactoryBot.define do
  factory :contract do
    sequence(:code) { |n| format("CT-%04d", 5000 + n) }
    customer
    equipment
    site { "contagem" }
    responsible { "Rogério Tavares" }
    status { "active" }
    start_date { Date.new(2026, 5, 4) }
    end_date { Date.new(2026, 6, 30) }
    daily_rate_cents { 48_000 }

    trait :cancelled do
      status { "cancelled" }
      cancelled_at { Time.zone.local(2026, 5, 4, 9, 0) }
    end

    trait :overdue do
      start_date { Date.new(2026, 3, 2) }
      end_date { Date.new(2026, 4, 30) }
      returned_at { nil }
    end
  end
end
