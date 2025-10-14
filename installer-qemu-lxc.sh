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
apt install -y lm-sensors python3 curl git ipmitool qemu qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager lxc lxd

# Read Information about the LXC Container
read -p "Please enter the name of the LXC container: "
read -p "Please enter the path where the LXC container should be created (default: /var/lib/lxc/): " 
if [ -z "$CONTAINER_PATH" ]; then
    CONTAINER_PATH="/var/lib/lxc/"
fi
read -p "Please enter the IP address for the LXC container: "
read -p "Please enter the netmask for the LXC container (default: 24): " 
if [ -z "$NETMASK" ]; then
    NETMASK="24"
fi
read -p "Please enter the gateway for the LXC container: "
read -p "Please enter the DNS server for the LXC container (default: 8.8.8.8): "
if [ -z "$DNS" ]; then
    DNS="8.8.8.8"
fi
read -p "Please enter the root password for the LXC container: "
read -p "Please enter the hostname for the LXC container: "

# Create the LXC container
lxc-create -n $CONTAINER_NAME -t download -- -d debian -r trixie -a amd64
lxc-config set $CONTAINER_NAME lxc.rootfs.path $CONTAINER_PATH/$CONTAINER_NAME/rootfs
lxc-config set $CONTAINER_NAME lxc.net.0.type veth
lxc-config set $CONTAINER_NAME lxc.net.0.link lxcbr0
lxc-config set $CONTAINER_NAME lxc.net.0.flags up
lxc-config set $CONTAINER_NAME lxc.net.0.ipv4.address $CONTAINER_IP/$NETMASK
lxc-config set $CONTAINER_NAME lxc.net.0.ipv4.gateway $GATEWAY
lxc-config set $CONTAINER_NAME lxc.net.0.ipv4.dns $DNS
lxc-config set $CONTAINER_NAME lxc.uts.name $CONTAINER_NAME
lxc-config set $CONTAINER_NAME lxc.uts.hostname $HOSTNAME
lxc-config set $CONTAINER_NAME lxc.rootfs.mount fstab
echo "$CONTAINER_IP/$NETMASK $HOSTNAME" >> /etc/hosts
echo "root:$ROOT_PASSWORD" | chpasswd
lxc-start -n $CONTAINER_NAME
lxc-attach -n $CONTAINER_NAME -- apt update && apt upgrade -y
lxc-attach -n $CONTAINER_NAME -- apt install -y sudo

# Install the autofan script in the LXC container
lxc-attach -n $CONTAINER_NAME -- bash -c "apt install -y lm-sensors python3 curl git ipmitool"
lxc-attach -n $CONTAINER_NAME -- bash -c "curl -o /root/installer-apt.sh https://raw.githubusercontent.com/Korbinian0/Luefter/main/installer-apt.sh"
lxc-attach -n $CONTAINER_NAME -- bash -c "bash installer-apt.sh"
echo "LXC container $CONTAINER_NAME created and autofan script installed."
echo "You can access the container using: lxc-attach -n $CONTAINER_NAME"
echo "Remember to configure the autofan.py script with your iLO and IPMI credentials."
echo "Reboot the container to apply all changes: lxc-stop -n $CONTAINER_NAME && lxc-start -n $CONTAINER_NAME"
echo "After reboot, you can check the status of the cron job with: lxc-attach -n $CONTAINER_NAME -- systemctl status cron"
echo "or check the log file at /var/log/syslog for entries related to autofan"
echo "Installation complete."