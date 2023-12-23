terraform {
  backend "s3" {
    bucket = "terraform-kiran"
    key    = "ssmview.tfstate"
    region = "eu-west-2"
  }

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.0"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "github" {}
provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}
variable "aws_region" {
  type    = string
  default = "eu-west-2"
}
