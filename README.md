# Deployment

Required components for project deployment

## Usage

Step 1: Clone this repository

Step 2: Create .env and .pem files in ```data``` folder (following examples in ```default```)

Step 3: Run ```docker compose up -d```.

Step 4: Verify all containers are properly running with ```docker ps```. Containers are set to restart on failure, so make sure none are recently restarted. If at least one is not functioning properly, then call ```docker compose down``` and start again from step 3.

## SSH Command for Github Action

A good starting point would be using `ssh -o StrictHostKeyChecking=no -i ~/ssh_key <username>@<hostname> "~/update.sh"`.
