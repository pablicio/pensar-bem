create_table "contracts", force: :cascade do |t|
  t.string "code", null: false
  t.bigint "customer_id", null: false
  t.bigint "equipment_id", null: false
  t.string "site"
  t.string "status"
  t.date "start_date"
  t.date "end_date"
  t.integer "daily_rate_cents"
  t.integer "delivery_fee_cents"
  t.string "responsible"
  t.text "notes"
  t.string "purchase_order"
  t.date "begin_date"
  t.integer "billing_day"
  t.bigint "created_by"
  t.string "legacy_id"
  t.datetime "started_at"
  t.datetime "returned_at"
  t.datetime "cancelled_at"
  t.string "cancel_reason"
  t.datetime "created_at", null: false
  t.datetime "updated_at", null: false
end
