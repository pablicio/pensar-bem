class ApiCredential < ApplicationRecord
  belongs_to :customer
  has_secure_token :token

  SCOPES = %w[read write].freeze
  validates :scope, inclusion: { in: SCOPES }

  def can_write?
    scope == "write"
  end
end
