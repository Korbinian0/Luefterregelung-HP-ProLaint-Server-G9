## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
## This script Remove the docker version of the autofan.py script and sets it up as a systemd service on a Fedora system.
#################################################################################################################
#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Update system and uninstall Docker packages
dnf -y update
dnf -y remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
dnf -y remove dnf-plugins-core curl git
dnf -y autoremove
dnf -y clean all

# Remove Docker files and directories
rm -rf /etc/docker
rm -rf /var/run/docker.sock
rm -rf /usr/lib/systemd/system/docker.service
rm -rf /usr/lib/systemd/system/docker.socket
rm -rf /usr/bin/docker
rm -rf /usr/bin/docker-compose
rm -rf /usr/bin/dockerd
rm -rf /usr/bin/docker-init
rm -rf /usr/bin/docker-proxy
rm -rf /usr/bin/docker-scan
rm -rf /usr/bin/docker-buildx
rm -rf /usr/bin/containerd
rm -rf /usr/bin/containerd-shim
rm -rf /usr/bin/containerd-shim-runc-v2
rm -rf /usr/bin/runc
rm -rf /var/lib/docker
rm -rf /var/lib/containerd

# Final message
echo "Docker and related files have been removed from the system."
echo "If you want to reinstall the fan control, please run the installer-dnf-docker.sh script again."
echo "Thank you for using the fan control for HP ProLiant Server G9!"
echo "Creator: Korbinian Musch, October 2025, Au in der Hallertau"
echo "It is recommended to reboot the system to ensure all changes take effect."
echo "Reboot now? (y/n)"
read REBOOT_CHOICE
if [[ "$REBOOT_CHOICE" =~ ^[Yy]$ ]]; then
    reboot
else
    echo "Please remember to reboot the system later."
fi
