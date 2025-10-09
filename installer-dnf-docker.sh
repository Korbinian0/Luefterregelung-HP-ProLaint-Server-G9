## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
## This script installs the docker version of the autofan.py script and sets it up as a systemd service on a Fedora/CentOS/RHEL-based system.
#################################################################################################################
#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Update system and install required packages
dnf -y update
dnf -y install dnf-plugins-core curl git

# Add Docker repository
dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo

# Update the package database
dnf -y update

# Install Docker Engine and Compose
dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Enable and start Docker service
systemctl enable --now docker

# Download the files from the GitHub repository
git clone https://github.com/Korbinian0/Luefterregelung-HP-ProLaint-Server-G9.git
cd Luefterregelung-HP-ProLaint-Server-G9

# Move the reinstaller-update-deb-docker.sh script to /root/autofan/
mkdir -p /root/autofan
cp reinstaller-update-deb-docker.sh /root/autofan/reinstaller-update-deb-docker.sh

# Move the docker-compose.yaml and Dockerfile to /root/autofan/docker
mkdir -p /root/autofan/docker
cp Dockerfile /root/autofan/docker/Dockerfile
cp docker-compose.yaml /root/autofan/docker/docker-compose.yaml

# Build and run the Docker container
cd /root/autofan/docker
docker compose up -d --build

# Get the server's IP address (first non-local IP)
SERVER_IP=$(hostname -I | awk '{print $1}')

# Print SSH instruction with the detected IP
echo "Please start an SSH session to the container with:"
echo "ssh root@${SERVER_IP} -p 2222"
echo "Default password is 'root'. Please change it after first login."
echo "Start the installer-dnf.sh script inside the container to configure the fan control."

# Clean up
cd ../../..
rm -rf Luefterregelung-HP-ProLaint-Server-G9