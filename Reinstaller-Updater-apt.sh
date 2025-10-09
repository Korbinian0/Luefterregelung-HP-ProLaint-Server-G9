## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
## This script installs the autofan.py script and sets it up as a systemd service on a Debian-based system.
#################################################################################################################
#!/bin/bash
# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi


# Updating the system 
apt update && apt upgrade -y

# Download the files from the GitHub repository
git clone https://github.com/Korbinian0/Luefterregelung-HP-ProLaint-Server-G9.git
cd Luefterregelung-HP-ProLaint-Server-G9

# Move the autofan.py script to /usr/local/autofan and make it executable
mkdir -p /usr/local/autofan
cp autofan.py /usr/local/autofan/autofan.py
chmod +x /usr/local/autofan/autofan.py

# Prompt for access data
read -p "Please enter iLO username: " USERNAME
read -sp "Please enter iLO password: " PASSWORD
echo
read -p "Please enter iLO IP address: " ILOIP
read -p "Please enter SSH options (leave blank for default): " SSHOPTS
echo
read -p "Please enter IPMI Username: " IPMIUSER
read -sp "Please enter IPMI Passwost: " IPMIPW
echo

# Replace placeholders in autofan.py
sed -i "s/^USERNAME=.*/USERNAME=\"$USERNAME\"/" /usr/local/autofan/autofan.py
sed -i "s/^USERNAME=.*/USERNAME=\"$USERNAME\"/" /root/autofan-test.py
sed -i "s/^PASSWORD=.*/PASSWORD=\"$PASSWORD\"/" /usr/local/autofan/autofan.py
sed -i "s/^PASSWORD=.*/PASSWORD=\"$PASSWORD\"/" /root/autofan-test.py
sed -i "s/^ILOIP=.*/ILOIP=\"$ILOIP\"/" /usr/local/autofan/autofan.py
sed -i "s/^ILOIP=.*/ILOIP=\"$ILOIP\"/" /root/autofan-test.py
sed -i "s/^SSHOPTS=.*/SSHOPTS=\"$SSHOPTS\"/" /usr/local/autofan/autofan.py
sed -i "s/^SSHOPTS=.*/SSHOPTS=\"$SSHOPTS\"/" /root/autofan-test.py
sed -i "s/^IPMIUSER=.*/IPMIUSER=\"$IPMIUSER\"/" /usr/local/autofan/autofan.py
sed -i "s/^IPMIUSER=.*/IPMIUSER=\"$IPMIUSER\"/" /root/autofan-test.py
sed -i "s/^IPMIPW=.*/IPMIPW=\"$IPMIPW\"/" /usr/local/autofan/autofan.py
sed -i "s/^IPMIPW=.*/IPMIPW=\"$IPMIPW\"/" /root/autofan-test.py

#IPMI Test
ipmitool -I lanplus -H "$ILOIP" -U "$IPMIUSER" -P "$IPMIPW" chassis status

# Create a systemd service file for the autofan script
cat <<EOL > /etc/systemd/system/autofan.service
[Unit]
Description=Autofan Service for HP ProLiant Server G9
After=network.target
Wants=network.target
StartLimitIntervalSec=0
StartLimitBurst=0
[Service]
Type=simple
Restart=always
RestartSec=5
User=root
ExecStart=/usr/bin/python3 /usr/local/autofan/autofan.py
[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to recognize the new service, enable it to start on boot, and start it immediately
systemctl daemon-reload
systemctl enable autofan.service
systemctl start autofan.service
systemctl status autofan.service

# Set permissions for the configuration file
chmod 600 /usr/local/autofan/*

# Clean up
cd ..
rm -rf Luefterregelung-HP-ProLaint-Server-G9

# Fan Testing 
echo "Starting fan test..."
python3 /root/autofan/autofan-test.py
echo "Fan test completed."

# Final message
echo "Installation complete. The autofan service is now running."
echo "You can check the service status with: systemctl status autofan.service"
echo "Log output can be viewed with: journalctl -u autofan.service -f"
echo "Configuration file is located at: /usr/local/autofan/"
# End of installer script