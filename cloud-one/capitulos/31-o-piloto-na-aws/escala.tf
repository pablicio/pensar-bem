resource "aws_appautoscaling_policy" "api" {
  name               = "pedidos-por-tarefa"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.api.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  target_tracking_scaling_policy_configuration {
    target_value = 300
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = local.alb_target_label
    }
  }
}
