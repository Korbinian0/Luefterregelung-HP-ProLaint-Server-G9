## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
## This script installs the docker version of the autofan.py script and sets it up as a systemd service on a Debian-based system.
#################################################################################################################
#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Updating the system and installing the necessary packages
# Add Docker's official GPG key:
apt-get update & apt-get upgrade -y
apt-get install ca-certificates curl
apt-get install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update

# Install Docker Engine, containerd, and Docker Compose
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin git curl -y

# Download the files from the GitHub repository
git clone https://github.com/Korbinian0/Luefterregelung-HP-ProLaint-Server-G9.git
cd Luefterregelung-HP-ProLaint-Server-G9

# Move the reinstaller-update-deb.sh and autofan-test.py script to /root/autofan/ and make it executable
mkdir -p /root/autofan
cp reinstaller-update-deb-docker.sh /root/autofan/reinstaller-update-deb-docker.sh

# Move the docker Data to /root/autofan
mkdir -p /root/autofan/docker
cp Docker-Debian13 /root/autofan/

# Build and run the Docker container
cd /root/autofan/docker/Docker-Debian13
docker compose up -d --build

# Get the server's IP address (first non-local IP)
SERVER_IP=$(hostname -I | awk '{print $1}')

# Print SSH instruction with the detected IP
echo "Please start an SSH session to the container with:"
echo "ssh root@${SERVER_IP} -p 2222"
echo "Default password is 'root'. Please change it after first login."
echo "Start the installer-apt.sh script inside the container to configure the fan control."

# Clean up
cd /root
rm -r Luefterregelung-HP-ProLaint-Server-G9
