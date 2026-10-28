describe "reserva" do
  it "cria uma reserva ao criar contrato ativo" do
    expect { create(:contract, status: "active") }
      .to change(Reservation, :count).by(1)
  end

  it "não cria reserva ao corrigir o responsável" do
    contrato = create(:contract, status: "active")

    expect { contrato.update!(responsible: "Juliana Prates") }
      .not_to change(Reservation, :count)
  end

  it "cria a reserva quando a reserva vira ativa" do
    contrato = create(:contract, status: "reserved")

    expect { contrato.update!(status: "active") }
      .to change(Reservation, :count).by(1)
  end
end
