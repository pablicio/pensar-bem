require "rails_helper"

RSpec.describe "API de contratos" do
  let(:serra) { create(:customer) }
  let(:leitura) do
    create(:api_credential, customer: serra, scope: "read")
  end

  def auth(credencial)
    { "Authorization" => "Bearer #{credencial.token}" }
  end

  it "recusa gravação com credencial de leitura" do
    post "/api/contracts",
         params: { contract: attributes_for(:contract) },
         headers: auth(leitura)

    expect(response).to have_http_status(:forbidden)
    expect(Contract.count).to eq(0)
  end

  it "não mostra contrato de outro cliente" do
    alheio = create(:contract)

    get "/api/v1/contracts/#{alheio.code}", headers: auth(leitura)

    expect(response).to have_http_status(:not_found)
  end

  it "recusa pedido sem credencial" do
    get "/api/v1/contracts"

    expect(response).to have_http_status(:unauthorized)
  end
end
