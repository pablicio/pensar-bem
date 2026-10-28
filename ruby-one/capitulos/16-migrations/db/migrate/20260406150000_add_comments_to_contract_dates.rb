class AddCommentsToContractDates < ActiveRecord::Migration[7.2]
  def change
    change_column_comment :contracts, :start_date,
      from: nil, to: "primeiro dia cobrado (faturamento)"
    change_column_comment :contracts, :begin_date,
      from: nil, to: "assinatura, início da vigência (jurídico)"
    change_column_comment :contracts, :started_at,
      from: nil, to: "saída do pátio (ocupação)"
  end
end
