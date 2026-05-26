variable "aws_region" {
  description = "AWS region where EKS will be created."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name used for AWS resource names."
  type        = string
  default     = "resume-ai"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "dev"
}

variable "cluster_version" {
  description = "EKS Kubernetes version."
  type        = string
  default     = "1.33"
}

variable "node_instance_types" {
  description = "EC2 instance types for worker nodes."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_min_size" {
  type    = number
  default = 1
}

variable "node_desired_size" {
  type    = number
  default = 2
}

variable "node_max_size" {
  type    = number
  default = 3
}

variable "argocd_chart_version" {
  description = "Argo CD Helm chart version."
  type        = string
  default     = "8.5.8"
}

variable "tags" {
  description = "Common tags."
  type        = map(string)
  default = {
    Project = "resume-ai"
    Owner   = "portfolio"
  }
}

