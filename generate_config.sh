cd terraform/
terraform output > ../tasks/configuration.env
cat $HOME/.aws/credentials >> ../tasks/configuration.env