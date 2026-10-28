scope :occupying_on, ->(dia) {
  where(status: "active")
    .where("end_date >= :dia OR returned_at IS NULL", dia: dia)
}
