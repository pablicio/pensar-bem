class ContractsController < ApplicationController
  before_action :set_contract, only: [:show, :cancel]

  def show
  end

  def create
    @contract = Contract.new(contract_params)
    @contract.status = params[:reserve] ? "reserved" : "active"

    if @contract.save
      redirect_to @contract, notice: "Contrato criado."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def cancel
    @contract.update!(status: "cancelled")
    redirect_to @contract, notice: "Contrato cancelado."
  end

  private

  def set_contract
    @contract = Contract.find(params[:id])
  end

  def contract_params
    params.require(:contract).permit(
      :code, :customer_id, :equipment_id, :site, :responsible,
      :start_date, :end_date, :daily_rate_cents,
    )
  end
end
