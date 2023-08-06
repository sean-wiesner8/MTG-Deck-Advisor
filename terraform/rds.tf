resource "aws_db_instance" "rds_instance" {
  allocated_storage = 20
  identifier        = "rds-terraform"
  instance_class    = "db.t3.micro"
  engine            = "postgres"
  engine_version    = "14.7"

  db_name  = "mtgAppDB"
  username = "mtgdbadmin"
  password = var.rds_password


  publicly_accessible    = true
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]

}

resource "aws_security_group" "rds_security_group" {
  name = "rds_security_group"
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
