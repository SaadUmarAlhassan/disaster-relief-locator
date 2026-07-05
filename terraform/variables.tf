variable "aws_region" {
  description = "AWS region for deployment"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  default     = "disaster-relief"
}

variable "frontend_bucket_name" {
  description = "Globally unique name for the frontend S3 bucket"
  default     = "disaster-relief-frontend-bucket-saadumar10" # CHANGE THIS TO BE GLOBALLY UNIQUE
}
