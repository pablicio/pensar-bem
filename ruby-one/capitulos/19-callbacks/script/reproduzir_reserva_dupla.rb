pt140 = Equipment.find_by!(patrimony: "PT-140")
serra = Customer.find_by!(name: "Construtora Serra Azul")

antes = Reservation.count

Contract.create!(
  code: "CT-9001", equipment: pt140, customer: serra,
  responsible: "Rogério", site: "betim", status: "active",
  start_date: Date.new(2026, 5, 4), end_date: Date.new(2026, 5, 29),
)

puts "reservas criadas: #{Reservation.count - antes}"
