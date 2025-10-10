## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
## This script installs the autofan.py script and sets it up as a systemd service on a Debian-based system.
######################################################################################################################
#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Updating the system and installing the necessary packages
apt update && apt upgrade -y
apt autoremove -y lm-sensors python3 curl git ipmitool

# Remove the files from the GitHub repository
rm -rf /root/autofan
rm -rf /usr/local/autofan

# Disable and remove the systemd service
if systemctl is-active --quiet autofan.service; then
    systemctl stop autofan.service
fi
if systemctl is-enabled --quiet autofan.service; then
    systemctl disable autofan.service
fi
rm -f /etc/systemd/system/autofan.service
systemctl daemon-reload
systemctl reset-failed autofan.service
systemctl status autofan.service
echo "Autofan service removed."
echo "Autofan uninstallation complete."

# Final message
echo "It is recommended to reboot the system to ensure all changes take effect."
echo "Reboot now? (y/n)"
read REBOOT_CHOICE
if [[ "$REBOOT_CHOICE" =~ ^[Yy]$ ]]; then
    reboot
else
    echo "Please remember to reboot the system later."
fi
