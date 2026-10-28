module Api
  class BaseController < ActionController::API
    include ActionController::HttpAuthentication::Token::
              ControllerMethods

    before_action :authenticate!

    private

    def authenticate!
      @credential = authenticate_with_http_token do |token, _|
        ApiCredential.find_by(token: token)
      end

      head :unauthorized unless @credential
    end

    def require_write!
      head :forbidden unless @credential.can_write?
    end
  end
end
