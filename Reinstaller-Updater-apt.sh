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

# Prompt for access data and IPMI settings
read -p "Please enter iLO username: " USERNAME
read -sp "Please enter iLO password: " PASSWORD
echo
read -p "Please enter iLO IP address: " ILOIP
read -p "Please enter SSH options (leave blank for default): " SSHOPTS
echo
read -p "Please enter IPMI Username: " IPMIUSER
read -sp "Please enter IPMI Passwost: " IPMIPW
echo
read -p "Please set the IPMI Chipset name (default: '10-Chipset'): "
read -p "Please set the IPMI HD Max name (default: '10-HD Max'): "
read -p "Please set the IPMI HD Controller name (default: '10-HD Controller'): "
read -p "Please set the IPMI ILO Zone name (default: '10-ILO Zone'): "
read -p "Please set the IPMI Battery Zone name (default: '10-Battery Zone'): "
read -p "Please set the IPMI VRP1 name (default: '10-VRP1'): "
read -p "Please set the IPMI VRP2 name (default: '10-VRP2'): "
read -p "Please set the IPMI Storage Batt name (default: '10-Storage Batt'): "
echo

# Replace placeholders in autofan.py
sed -i "s/^USERNAME=.*/USERNAME=\"$USERNAME\"/" /usr/local/autofan/autofan.py
sed -i "s/^USERNAME=.*/USERNAME=\"$USERNAME\"/" /root//autofan/autofan-test.py
sed -i "s/^PASSWORD=.*/PASSWORD=\"$PASSWORD\"/" /usr/local/autofan/autofan.py
sed -i "s/^PASSWORD=.*/PASSWORD=\"$PASSWORD\"/" /root/autofan/autofan-test.py
sed -i "s/^ILOIP=.*/ILOIP=\"$ILOIP\"/" /usr/local/autofan/autofan.py
sed -i "s/^ILOIP=.*/ILOIP=\"$ILOIP\"/" /root//autofan/autofan-test.py
sed -i "s/^SSHOPTS=.*/SSHOPTS=\"$SSHOPTS\"/" /usr/local/autofan/autofan.py
sed -i "s/^SSHOPTS=.*/SSHOPTS=\"$SSHOPTS\"/" /root/autofan/autofan-test.py
sed -i "s/^IPMIUSER=.*/IPMIUSER=\"$IPMIUSER\"/" /usr/local/autofan/autofan.py
sed -i "s/^IPMIPW=.*/IPMIPW=\"$IPMIPW\"/" /usr/local/autofan/autofan.py
sed -i "s/^Chipset=.*/Chipset=\"${Chipset:-10-Chipset}\"/" /usr/local/autofan/autofan.py
sed -i "s/^HDMax=.*/HDMax=\"${HDMax:-10-HD Max}\"/" /usr/local/autofan/autofan.py
sed -i "s/^HDController=.*/HDController=\"${HDController:-10-HD Controller}\"/" /usr/local/autofan/autofan.py
sed -i "s/^ILOZone=.*/ILOZone=\"${ILOZone:-10-ILO Zone}\"/" /usr/local/autofan/autofan.py
sed -i "s/^Batteryzone=.*/Batteryzone=\"${Batteryzone:-10-Battery Zone}\"/" /usr/local/autofan/autofan.py
sed -i "s/^VRP1=.*/VRP1=\"${VRP1:-10-VRP1}\"/" /usr/local/autofan/autofan.py
sed -i "s/^VRP2=.*/VRP2=\"${VRP2:-10-VRP2}\"/" /usr/local/autofan/autofan.py
sed -i "s/^StorageBatt=.*/StorageBatt=\"${StorageBatt:-10-Storage Batt}\"/" /usr/local/autofan/autofan.py
sed -i "s/^HDCntlrZone=.*/HDCntlrZone=\"${HDCntlrZone:-10-HD Cntlr Zone}\"/" /usr/local/autofan/autofan.py


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