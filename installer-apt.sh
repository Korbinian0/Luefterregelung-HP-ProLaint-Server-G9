## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
## This script installs the autofan.py script and sets it up as a systemd service on a Debian-based system.
###################
#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Updating the system and installing the necessary packages
apt update && apt upgrade -y
apt install -y lm-sensors python3 curl git

# Download the files from the GitHub repository
git clone https://github.com/Korbinian0/Luefterregelung-HP-ProLaint-Server-G9.git
cd L-fterregelung-HP-ProLaint-Server-G9

# Move the reinstaller-update-deb.sh and autofan-test.py script to /root/autofan/ and make it executable
mkdir -p /root/autofan
cp reinstaller-update-deb.sh /root/autofan/reinstaller-update-deb.sh
cp autofan-test.py /root/autofan/autofan-test.py
chmod +x /root/autofan/reinstaller-update-deb.sh
chmod +x /root/autofan/autofan-test.py

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

# Replace placeholders in autofan.py
sed -i "s/^USERNAME=.*/USERNAME=\"$USERNAME\"/" /usr/local/autofan/autofan.py
sed -i "s/^USERNAME=.*/USERNAME=\"$USERNAME\"/" /root/autofan-test.py
sed -i "s/^PASSWORD=.*/PASSWORD=\"$PASSWORD\"/" /usr/local/autofan/autofan.py
sed -i "s/^PASSWORD=.*/PASSWORD=\"$PASSWORD\"/" /root/autofan-test.py
sed -i "s/^ILOIP=.*/ILOIP=\"$ILOIP\"/" /usr/local/autofan/autofan.py
sed -i "s/^ILOIP=.*/ILOIP=\"$ILOIP\"/" /root/autofan-test.py
sed -i "s/^SSHOPTS=.*/SSHOPTS=\"$SSHOPTS\"/" /usr/local/autofan/autofan.py
sed -i "s/^SSHOPTS=.*/SSHOPTS=\"$SSHOPTS\"/" /root/autofan-test.py

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
rm -rf L-fterregelung-HP-ProLaint-Server-G9

# Testing Start
./root/autofan/autofan-test.py

# Final message
echo "Installation complete. The autofan service is now running."
echo "You can check the service status with: systemctl status autofan.service"
echo "Log output can be viewed with: journalctl -u autofan.service -f"
echo "Configuration file is located at: /usr/local/autofan/"
echo "To update the script in the future, run: /root/autofan/reinstaller-update-deb.sh"
echo "Please reboot the server to ensure all changes take effect."
echo "Test the script first with: python3 /root//autofan/autofan-test.py"
echo "The test sets all fans slowly in 1 second intervals up and then down again and then the normal script intervenes again and regulates the fans."
# End of installer script
