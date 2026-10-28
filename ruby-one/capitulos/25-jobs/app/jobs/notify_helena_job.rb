class NotifyHelenaJob < ApplicationJob
  queue_as :default
  retry_on Net::SMTPServerBusy, wait: :polynomially_longer,
                                attempts: 5

  def perform(contract_id)
    # ...
  end
end
