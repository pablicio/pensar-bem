def index
  # ... a validação do status, como antes
  contracts = @credential.customer.contracts
                         .includes(:equipment).where(status: status)
  render json: contracts.map(&:as_api)
end

def show
  contract = @credential.customer.contracts
                        .includes(:equipment)
                        .find_by!(code: params[:id])
  render json: contract.as_api
end
