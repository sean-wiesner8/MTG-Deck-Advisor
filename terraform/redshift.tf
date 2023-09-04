resource "aws_db_instance" "mtg_redshift_db" {
  identifier             = "mtg-redshift-db"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "14.7"
  db_name                = "mtg_redshift_db"
  username               = "mtg_project_redshift"
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.rds_redshift.id]
  publicly_accessible    = true
  skip_final_snapshot    = true
}

resource "aws_security_group" "rds_redshift" {
  name = "mtg-rds-redshift"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
