output "instance_id" {
  description = "ID of the DBS instance"
  value       = aws_db_instance.c16-josh-museum-rds.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_db_instance.c16-josh-museum-rds.address
}
