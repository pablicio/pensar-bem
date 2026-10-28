after_commit :notify_helena, on: :create

private

def notify_helena
  NotifyHelenaJob.perform_later(id)
end
