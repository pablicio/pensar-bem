def perform(contract_id)
  contract = Contract.find_by(id: contract_id)
  return if contract.nil? || contract.notified_customer_at

  SerraAzulClient.new.notify(contract)
  contract.update_column(:notified_customer_at, Time.current)
end
