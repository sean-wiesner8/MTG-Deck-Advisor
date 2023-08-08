resource "aws_budgets_budget" "monthly-budget" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "20"
  limit_unit        = "USD"
  time_period_start = "2023-08-05_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["sean.wiesner@gmail.com"]
  }
}
