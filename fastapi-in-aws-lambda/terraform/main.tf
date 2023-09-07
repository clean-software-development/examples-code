terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67"
    }
  }
}

provider "aws" {
  region = var.REGION
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true  
}

variable "REGION" {
  description = "Region AWS"
  type        = string
  default     = "eu-west-3"
}

module "lambda_layer_poetry" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.0"

  create_layer        = true
  layer_name          = "fastapi-in-aws-lambda-layer"
  compatible_runtimes = ["python3.10"]

  source_path = [
    # "${path.module}/../project/fastapi_in_aws_lambda",
    {
      path           = "${path.module}/../project"
      poetry_install = true
    }
  ]
  hash_extra = "extra-hash-to-prevent-conflicts-with-module.package_dir"

  build_in_docker = true
  runtime         = "python3.10"
  docker_image    = "build-python3.10-poetry"
  docker_file     = "${path.module}/../project/docker/Dockerfile"
  artifacts_dir   = "${path.root}/builds/lambda_layer_poetry/"
}


module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.0"

  function_name = "fastapi-in-aws-lambda-function"
  description   = "FastAPI in AWS Lambda"
  handler       = "fastapi_in_aws_lambda.app.lambda_handler"
  runtime       = "python3.10"
  publish       = true
  create_lambda_function_url = true

#   source_path   = "${path.module}/../project/fastapi_in_aws_lambda"
  source_path = [
    {
      path             = "${path.module}../project"
      pip_requirements = false
      patterns = [
      "fastapi_in_aws_lambda",
      ]
    }
  ]
  hash_extra  = "extra-hash-to-prevent-conflicts-with-module.package_dir"
  artifacts_dir   = "${path.root}/builds/lambda_function/"

  build_in_docker = true
  docker_image    = "build-python3.10-poetry"
  docker_file     = "${path.module}/../project/docker/Dockerfile"

  layers = [
    module.lambda_layer_poetry.lambda_layer_arn,
  ]

  allowed_triggers = {
    AllowExecutionFromAPIGateway = {
      service    = "apigateway"
      source_arn = "${module.api_gateway.apigatewayv2_api_execution_arn}/*/*"
    }
  }

}

module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "~> 2.0"

  name          = "fastapi-in-aws-lambda-api"
  description   = "My awesome HTTP API Gateway"
  protocol_type = "HTTP"

  create_api_domain_name = false

  cors_configuration = {
    allow_headers = ["*"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  integrations = {
    "ANY /{proxy+}" = {
      lambda_arn             = module.lambda_function.lambda_function_arn
      payload_format_version = "2.0"
    }
  }

}

output "apigateway_url" {
  description = "Api Gateway URL"
  value       = module.api_gateway.apigatewayv2_api_api_endpoint
}

output "lambda_function_invoke_arn" {
  description = "The Invoke ARN of the Lambda Function"
  value       = module.lambda_function.lambda_function_invoke_arn
}

output "lambda_function_url" {
  description = "Lambda URL"
  value       = module.lambda_function.lambda_function_url
}

