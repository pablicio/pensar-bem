class SessionsController < ApplicationController
  skip_before_action :require_login, only: [:new, :create]

  def create
    user = User.find_by(email: params[:email])

    if user&.authenticate(params[:password])
      session[:user_id] = user.id
      redirect_to contracts_path
    else
      flash.now[:alerta] = "E-mail ou senha incorretos."
      render :new, status: :unprocessable_entity
    end
  end
end
