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

# Updateing the system bevore removing Packages
apt-get update & apt-get upgrade -y
apt-get autoremove ca-certificates curl
apt-get remove -m 0755 -d /etc/apt/keyrings
rm /etc/apt/keyrings/docker.asc
rm /etc/apt/sources.list.d/docker.list
apt-get update
apt-get autoremove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin git curl -y
apt-get autoremove -y

# Removing the docker data 
rm -r /var/lib/docker
rm -r /var/lib/containerd
echo "Docker and related components have been removed."

# Final messages
echo "The /var/lib/docker and /var/lib/containerd directories have been deleted."
echo "If you want to reinstall the fan control, please run the installer-apt-docker.sh script again."
echo "Reboot the system to complete the removal process."
echo "Reboot now? (y/n)"
read answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    reboot
else
    echo "Please remember to reboot the system later to complete the removal process."
fi
