output "cluster_name" {
  description = "EKS cluster name."
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "EKS API server endpoint."
  value       = module.eks.cluster_endpoint
}

output "region" {
  description = "AWS region."
  value       = var.aws_region
}

output "configure_kubectl_command" {
  description = "Run this after terraform apply to connect kubectl to EKS."
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}

output "argocd_namespace" {
  description = "Namespace where Argo CD is installed."
  value       = helm_release.argocd.namespace
}

