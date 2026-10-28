def index
  status = Contract::API_STATUS.key(params.fetch(:status, "ativo"))

  if status.nil?
    return render json: {
      erro: "status inválido",
      aceitos: Contract::API_STATUS.values,
    }, status: :unprocessable_entity
  end

  contracts = Contract.includes(:equipment).where(status: status)
  render json: contracts.map(&:as_api)
end
