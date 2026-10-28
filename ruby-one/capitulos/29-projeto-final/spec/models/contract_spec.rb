it "o escopo e o predicado concordam" do
  hoje = Date.new(2026, 6, 3)
  create(:contract)
  create(:contract, :overdue)
  create(:contract, :cancelled)

  pelo_escopo = Contract.occupying_on(hoje).to_a
  pelo_metodo = Contract.all.select { |c| c.occupying?(hoje) }

  expect(pelo_escopo).to match_array(pelo_metodo)
end
