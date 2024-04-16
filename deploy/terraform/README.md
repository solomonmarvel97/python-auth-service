### Steps to Deploy:

1. **Initialize Terraform**: Run `terraform init` in the directory of your `main.tf` file. This will initialize Terraform and download the necessary providers.

2. **Create an Execution Plan**: Run `terraform plan` to see what actions Terraform will perform.

3. **Apply the Configuration**: If you're satisfied with the plan, run `terraform apply` to create the resources. Confirm the action by typing `yes` when prompted.

4. **Access the EC2 Instance**: Once the process completes, Terraform will output the public IP of the EC2 instance. You can use this IP to access the instance via SSH.

### Additional Notes:

- **AWS Credentials**: Ensure your AWS credentials are configured. You can set them up using environment variables, shared credentials file, or IAM roles. Refer to the [Terraform AWS Provider documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication) for more details.

- **Security Group**: This basic setup doesn't include a custom security group. You might want to define one to control traffic to the instance. By default, AWS assigns the default security group to the instance.

- **Key Pair**: This example doesn't include a key pair for SSH access. You should modify the Terraform configuration to specify a key pair if you plan to SSH into the instance.

- **Amazon Linux 2 AMI**: The AMI ID `ami-0e34e7b9ca0ace12d` is for Amazon Linux 2 in the `us-west-2` region. AMI IDs vary between regions, so you'll need to replace this with the appropriate AMI ID for your region and desired OS.

### Clean Up:

When you no longer need the instance, you can destroy it with Terraform to avoid incurring unnecessary charges:

```bash
terraform destroy
```

This command will remove the resources that Terraform managed. Confirm the action by typing `yes` when prompted.