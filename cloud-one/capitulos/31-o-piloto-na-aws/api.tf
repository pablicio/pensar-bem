resource "aws_ecs_task_definition" "api" {
  family                   = "arraia-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.execucao.arn
  task_role_arn            = aws_iam_role.api.arn
  container_definitions = jsonencode([{
    name         = "api"
    image        = local.imagem_api
    portMappings = [{ containerPort = 8080 }]
    secrets = [{
      name      = "DB_SENHA"
      valueFrom = local.segredo_db.secret_arn
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group  = aws_cloudwatch_log_group.api.name
        awslogs-region = "sa-east-1"
        awslogs-stream-prefix = "api"
      }
    }
  }])
}

locals {
  repo       = aws_ecr_repository.api.repository_url
  imagem_api = "${local.repo}:2027.03.1"
  segredo_db = aws_db_instance.arraia.master_user_secret[0]
}
