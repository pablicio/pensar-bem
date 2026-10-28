require "rails_helper"

RSpec.describe Equipment do
  describe ".available" do
    it "inclui a máquina cujo único contrato foi cancelado" do
      pt121 = create(:equipment, patrimony: "PT-121")
      create(:contract, equipment: pt121, status: "cancelled")

      expect(Equipment.available).to include(pt121)
    end
  end
end
