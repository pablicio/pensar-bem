namespace :api do
  namespace :v1 do
    resources :contracts, only: [:index, :show]
  end
end
