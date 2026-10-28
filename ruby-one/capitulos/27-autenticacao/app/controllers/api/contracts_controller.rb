module Api
  class ContractsController < BaseController
    before_action :require_write!, only: [:create, :update]
    # ...
  end
end
