# Deployment Guide for Python FastAPI Application on AWS EC2

This guide provides instructions on how to deploy a Python FastAPI application on an Amazon EC2 instance. 

## Prerequisites

- An AWS account
- Basic knowledge of AWS services
- Familiarity with SSH and terminal commands
- A local machine with Python and FastAPI application ready to be deployed

## Step 1: Set Up AWS EC2 Instance

1. **Log in to AWS Management Console**: Access your AWS account and go to the EC2 dashboard.

2. **Launch a New EC2 Instance**:
   - Click on "Launch Instance".
   - Choose an Amazon Machine Image (AMI), like Ubuntu Server.
   - Select an instance type (e.g., t2.micro for testing purposes).
   - Configure instance details as required.
   - Add storage if the default is not sufficient.
   - Add Tags for easier management (optional).
   - Configure the Security Group to set rules. Make sure to allow SSH (port 22) and HTTP (port 80) or other ports your app requires.
   - Review and launch the instance. 

3. **Create or Assign a Key Pair**: When prompted, create a new key pair or use an existing one. Download and securely store the key pair file (.pem), as you’ll need it to SSH into the instance.

## Step 2: Connect to Your EC2 Instance

1. **Locate Your Instance**: In the EC2 dashboard, select your instance and note down the public DNS/IP.

2. **SSH into the Instance**:
   - Open your terminal.
   - Navigate to the directory containing your .pem file.
   - Use the following command to connect:
     ```
     ssh -i "your-key-pair.pem" ubuntu@your-instance-public-dns
     ```
   - If prompted, confirm the connection.

## Step 3: Set Up the Environment

1. **Update and Upgrade**: Run `sudo apt update` and `sudo apt upgrade` to update the system packages.

2. **Install Python & Pip**:
   - Install Python3 and pip if not already installed:
     ```
     sudo apt install python3 python3-pip
     ```

3. **Install FastAPI and Uvicorn**:
   - Install FastAPI and Uvicorn using pip:
     ```
     pip3 install fastapi uvicorn
     ```

## Step 4: Deploy Your Application

1. **Transfer Your Application**: Use SCP or similar tools to upload your application files to the EC2 instance.

2. **Install Dependencies**:
   - Navigate to your project directory.
   - Install required dependencies (if you have a requirements.txt):
     ```
     pip3 install -r requirements.txt
     ```

3. **Run the Application**:
   - Start your FastAPI application using Uvicorn:
     ```
     uvicorn main:app --host 0.0.0.0 --port 80
     ```
   - Replace `main:app` with your file and application instance names.
