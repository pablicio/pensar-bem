Rails.application.routes.draw do
  resources :contracts do
    member do
      patch :cancel
    end
  end
end
