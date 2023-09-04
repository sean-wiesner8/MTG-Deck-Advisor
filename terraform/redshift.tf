resource "aws_db_instance" "mtg_redshift_db" {
  identifier             = "mtg-redshift-db"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "14.7"
  db_name                = "mtg_redshift_db"
  username               = "mtg_project_redshift"
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = true
  skip_final_snapshot    = true
}
