class BackfillContractStatus < ActiveRecord::Migration[7.2]
  def up
    execute <<~SQL
      UPDATE contracts SET status = 'closed'
      WHERE status IS NULL
        AND (returned_at IS NOT NULL OR end_date < CURRENT_DATE)
    SQL

    execute <<~SQL
      UPDATE contracts SET status = 'active'
      WHERE status IS NULL AND end_date >= CURRENT_DATE
    SQL
  end

  def down
    raise ActiveRecord::IrreversibleMigration
  end
end
