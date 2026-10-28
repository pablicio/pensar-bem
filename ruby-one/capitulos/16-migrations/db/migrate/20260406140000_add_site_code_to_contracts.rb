class AddSiteCodeToContracts < ActiveRecord::Migration[7.2]
  def change
    add_column :contracts, :site_code, :string,
               if_not_exists: true
  end
end
