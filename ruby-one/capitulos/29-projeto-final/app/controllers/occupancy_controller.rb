class OccupancyController < ApplicationController
  def index
    @customer = Customer.find(params[:customer_id])
    @contracts = @customer.contracts
                          .occupying_on(Date.current)
                          .eager_load(:equipment)
                          .order(:site, "equipment.patrimony")
  end
end
