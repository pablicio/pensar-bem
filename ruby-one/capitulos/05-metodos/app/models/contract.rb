def active?
  status == "active" && end_date >= Date.today
end
