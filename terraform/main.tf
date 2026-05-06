terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ECR Repository for Docker images
resource "aws_ecr_repository" "job_matching" {
  name = "job-matching-mlops"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "job-matching-cluster"
}

# RDS for metadata
resource "aws_db_instance" "metadata" {
  identifier = "job-matching-db"
  engine = "postgres"
  engine_version = "14"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  db_name = "jobmatching"
  username = var.db_username
  password = var.db_password
  
  skip_final_snapshot = true
  
  tags = {
    Environment = "production"
    Project = "job-matching-mlops"
  }
}

# S3 for artifacts
resource "aws_s3_bucket" "artifacts" {
  bucket = "job-matching-artifacts-${random_id.bucket_suffix.hex}"
  
  tags = {
    Environment = "production"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# IAM Roles
resource "aws_iam_role" "ecs_task_role" {
  name = "job-matching-ecs-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Outputs
output "ecr_repository_url" {
  value = aws_ecr_repository.job_matching.repository_url
}

output "rds_endpoint" {
  value = aws_db_instance.metadata.endpoint
}

output "s3_bucket_name" {
  value = aws_s3_bucket.artifacts.id
}