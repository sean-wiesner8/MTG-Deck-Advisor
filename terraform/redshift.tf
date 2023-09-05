resource "aws_redshift_cluster" "mtg_cluster" {
  cluster_identifier = "mtg-redshift-cluster"
  database_name      = "mtg_redshift_db"
  master_username    = "mtg_project_redshift"
  master_password    = var.db_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"

  skip_final_snapshot                 = true
  publicly_accessible                 = true
  automated_snapshot_retention_period = 0
  vpc_security_group_ids              = [aws_security_group.redshift.id]
}

resource "aws_security_group" "redshift" {
  name = "mtg-redshift"
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
