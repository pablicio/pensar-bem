class RequireContractStatus < ActiveRecord::Migration[7.2]
  def change
    change_column_default :contracts, :status,
                          from: nil, to: "active"
    change_column_null :contracts, :status, false
  end
end
