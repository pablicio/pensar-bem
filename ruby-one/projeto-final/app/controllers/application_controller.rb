class ApplicationController < ActionController::Base
  before_action :require_login

  private

  def require_login
    @current_user = User.find_by(id: session[:user_id])
    redirect_to new_session_path unless @current_user
  end
end
