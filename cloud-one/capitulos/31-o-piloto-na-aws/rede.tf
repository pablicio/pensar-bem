module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "arraia"
  cidr = "10.20.0.0/16"
  azs  = ["sa-east-1a", "sa-east-1b"]

  public_subnets   = ["10.20.0.0/20", "10.20.16.0/20"]
  private_subnets  = ["10.20.64.0/20", "10.20.80.0/20"]
  database_subnets = ["10.20.128.0/20", "10.20.144.0/20"]

  enable_nat_gateway = true
  single_nat_gateway = true
}
