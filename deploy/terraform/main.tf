provider "aws" {
  region = "us-west-2" # Change to your preferred AWS region
}

resource "aws_instance" "example" {
  ami           = "ami-0e34e7b9ca0ace12d" # Amazon Linux 2 AMI ID in us-west-2, change as needed
  instance_type = "t2.micro" # Change to your preferred instance type

  tags = {
    Name = "auth-serivce-instance"
  }
}
